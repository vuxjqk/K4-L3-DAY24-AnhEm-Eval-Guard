"""Report export checks use synthetic measurements only inside pytest temp dirs."""
import pytest

from scripts.write_phase_a_report import main
from src.experiment_support import metadata, write_json
from src.phase_a_ragas import (RagasResult, load_test_set_50q, build_phase_a_report,
                               bottom_10, cluster_analysis)
from src.report_contracts import validate_markdown

pytestmark = pytest.mark.student


@pytest.fixture
def report_root(tmp_path):
    questions = load_test_set_50q()
    answers = [{**q, "answer": "TEST answer", "contexts": ["TEST context"],
                "generation_mode": "llm", "generation_model": "test-generation"} for q in questions]
    ap = tmp_path / "artifacts/answers_50q.json"
    qp = tmp_path / "fixtures/test_set_50q.json"
    write_json(ap, answers)
    write_json(qp, questions)
    results = [RagasResult(a["id"], a["distribution"], a["question"], a["answer"],
                           a["contexts"], a["ground_truth"], .5, .6, .7, .8) for a in answers]
    bottom = bottom_10(results)
    bottom[0]["diagnosis"] = "Specific diagnosis preserved from Task 3"
    report = build_phase_a_report(results, cluster_analysis(results), bottom)
    report["metadata"] = metadata([ap, qp], models={"generation": ["test-generation"],
        "evaluator": ["test-evaluator"], "judge": [], "guard": []})
    write_json(tmp_path / "artifacts/ragas_50q.json", report)
    return tmp_path, answers


def test_report_preserves_diagnosis_and_evidence(report_root):
    root, _ = report_root
    assert main(["--root", str(root)]) == 0
    content = validate_markdown(root / "doc/reports/failure_clusters.md")
    assert "Specific diagnosis preserved from Task 3" in content
    assert "TEST answer" in content and "TEST context" in content
    assert "test-evaluator" in content and "test-generation" in content
    assert content.count("### Câu ") == 10
    assert "cần bổ sung nhận xét" in content


def test_stale_evidence_is_rejected_before_overwriting_report(report_root):
    root, answers = report_root
    target = root / "doc/reports/failure_clusters.md"
    target.parent.mkdir(parents=True)
    target.write_text("Existing human analysis", encoding="utf-8")
    answers[0]["answer"] = "changed answer after evaluation"
    write_json(root / "artifacts/answers_50q.json", answers)
    with pytest.raises(ValueError, match="Stale experiment source"):
        main(["--root", str(root)])
    assert target.read_text(encoding="utf-8") == "Existing human analysis"
