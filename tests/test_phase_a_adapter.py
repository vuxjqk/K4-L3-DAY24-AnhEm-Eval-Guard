"""Offline checks for incomplete measurements and evaluator provenance."""
from types import SimpleNamespace
from unittest.mock import Mock
import sys

import pytest

from src.phase_a_ragas import group_by_distribution, load_test_set_50q, run_ragas_50q

pytestmark = pytest.mark.student
METRICS = {"faithfulness": .8, "answer_relevancy": .7,
           "context_precision": .6, "context_recall": .5}


@pytest.fixture
def measurement(monkeypatch):
    answers = [{**q, "answer": f"Generated {q['id']}", "contexts": [f"Context {q['id']}"]}
               for q in load_test_set_50q()]
    raw = {"per_question": [dict(METRICS) for _ in answers],
           "metadata": {"evaluator_models": ["actual-evaluator", "actual-embedding"]}}
    evaluator = Mock(return_value=raw)
    monkeypatch.setitem(sys.modules, "src.m4_eval", SimpleNamespace(evaluate_ragas=evaluator))
    return answers, raw, evaluator


def test_mapping_metrics_keep_sources_and_model_roles(measurement):
    answers, raw, evaluator = measurement
    result = run_ragas_50q(answers)
    assert result.evaluator_models == raw["metadata"]["evaluator_models"]
    assert [r.answer for r in result.results] == [a["answer"] for a in answers]
    assert [r.contexts for r in result.results] == [a["contexts"] for a in answers]
    assert [r.ground_truth for r in result.results] == [a["ground_truth"] for a in answers]
    assert all(type(r.faithfulness) is float for r in result.results)
    assert result.results[0].contexts is not answers[0]["contexts"]
    assert evaluator.call_args.args == (
        [a["question"] for a in answers], [a["answer"] for a in answers],
        [a["contexts"] for a in answers], [a["ground_truth"] for a in answers])


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -.1, 1.1, True, "0.8", None])
def test_invalid_metric_rejected_instead_of_replaced(measurement, value):
    answers, raw, _ = measurement
    raw["per_question"][0]["faithfulness"] = value
    with pytest.raises(ValueError, match="faithfulness"):
        run_ragas_50q(answers)


def test_missing_rows_never_silently_truncate(measurement):
    answers, raw, _ = measurement
    raw["per_question"].pop()
    with pytest.raises(ValueError, match="50 rows"):
        run_ragas_50q(answers)


@pytest.mark.parametrize("models", [None, [], [""], [" evaluator "], "judge-model"])
def test_missing_evaluator_metadata_has_no_judge_fallback(measurement, models):
    answers, raw, _ = measurement
    raw["metadata"]["evaluator_models"] = models
    with pytest.raises(ValueError, match="evaluator_models"):
        run_ragas_50q(answers)


def test_reordered_measured_rows_rejected(measurement):
    answers, raw, _ = measurement
    raw["per_question"][0]["question"] = answers[1]["question"]
    with pytest.raises(ValueError, match="order/source mismatch"):
        run_ragas_50q(answers)


def test_incomplete_answers_rejected_before_api(measurement):
    answers, _, evaluator = measurement
    with pytest.raises(ValueError, match="exactly 50"):
        run_ragas_50q(answers[:-1])
    evaluator.assert_not_called()


def test_wrong_group_counts_rejected_before_api(measurement):
    answers, _, evaluator = measurement
    answers[0]["distribution"] = "adversarial"
    with pytest.raises(ValueError, match="20/20/10"):
        run_ragas_50q(answers)
    evaluator.assert_not_called()


def test_mismatched_contexts_rejected(measurement):
    answers, raw, _ = measurement
    raw["per_question"][0]["contexts"] = ["unrelated evidence"]
    with pytest.raises(ValueError, match="contexts order/source mismatch"):
        run_ragas_50q(answers)


def test_group_preserves_order_and_rejects_unknown_distribution():
    rows = [{"id": 2, "distribution": "factual"}, {"id": 1, "distribution": "factual"}]
    assert group_by_distribution(rows)["factual"] == rows
    with pytest.raises(ValueError, match="Unknown distribution"):
        group_by_distribution([{"distribution": "typo"}])


def test_real_m4_adapter_records_configured_models_without_network(monkeypatch):
    from src import m4_eval
    rows = [{"question": "Q", "answer": "A", "contexts": ["C"],
             "ground_truth": "G", **METRICS}]
    frame = SimpleNamespace(iterrows=lambda: enumerate(rows))
    evaluate = Mock(return_value=SimpleNamespace(to_pandas=lambda: frame))
    metrics = {name: SimpleNamespace() for name in METRICS}
    monkeypatch.setitem(sys.modules, "ragas", SimpleNamespace(evaluate=evaluate))
    monkeypatch.setitem(sys.modules, "ragas.metrics", SimpleNamespace(**metrics))
    monkeypatch.setitem(sys.modules, "ragas.run_config", SimpleNamespace(RunConfig=lambda **kw: kw))
    monkeypatch.setitem(sys.modules, "datasets", SimpleNamespace(
        Dataset=SimpleNamespace(from_dict=lambda value: value)))
    monkeypatch.setattr(m4_eval, "_get_ragas_models", lambda: ("llm-instance", "embedding-instance"))
    monkeypatch.setattr(m4_eval, "GEMINI_MODEL", "configured-evaluator")
    monkeypatch.setattr(m4_eval, "EMBEDDING_MODEL", "configured-embedding")
    raw = m4_eval.evaluate_ragas(["Q"], ["A"], [["C"]], ["G"])
    assert raw["metadata"]["evaluator_models"] == ["configured-evaluator", "configured-embedding"]
    assert evaluate.call_args.kwargs["llm"] == "llm-instance"
    assert evaluate.call_args.kwargs["embeddings"] == "embedding-instance"
    evaluate.side_effect = RuntimeError("evaluation service failed")
    with pytest.raises(RuntimeError, match="no valid results"):
        m4_eval.evaluate_ragas(["Q"], ["A"], [["C"]], ["G"])
