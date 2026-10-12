from __future__ import annotations

"""Phase A: RAGAS Production Evaluation — 50q, 3 distributions, cluster analysis."""

import json
import math
from collections.abc import Mapping
import os
import sys
from dataclasses import asdict, dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TEST_SET_PATH, ANSWERS_PATH, ARTIFACTS_DIR
from src.experiment_support import write_json

Distribution = str  # "factual" | "multi_hop" | "adversarial"

DIAGNOSTIC_TREE = {
    "faithfulness":      ("LLM hallucinating", "Tighten system prompt, lower temperature"),
    "context_recall":    ("Missing relevant chunks", "Improve chunking or add BM25"),
    "context_precision": ("Too many irrelevant chunks", "Add reranking or metadata filter"),
    "answer_relevancy":  ("Answer doesn't match question", "Improve prompt template"),
}


@dataclass
class RagasResult:
    question_id: int
    distribution: Distribution
    question: str
    answer: str
    contexts: list[str]
    ground_truth: str
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float

    @property
    def avg_score(self) -> float:
        return (self.faithfulness + self.answer_relevancy +
                self.context_precision + self.context_recall) / 4

    @property
    def worst_metric(self) -> str:
        scores = {
            "faithfulness":      self.faithfulness,
            "answer_relevancy":  self.answer_relevancy,
            "context_precision": self.context_precision,
            "context_recall":    self.context_recall,
        }
        return min(scores, key=scores.get)


# ─── Đã implement sẵn ────────────────────────────────────────────────────────

@dataclass
class RagasEvaluation:
    """Task 2 output: measured rows plus model identifiers reported by m4."""
    results: list[RagasResult]
    evaluator_models: list[str]

def load_test_set_50q(path: str = TEST_SET_PATH) -> list[dict]:
    """Load 50q test set với 3 distributions."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_answers(path: str = ANSWERS_PATH) -> list[dict]:
    """Load pre-generated answers từ setup_answers.py."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"answers_50q.json không tìm thấy tại {path}\n"
            "→ Chạy trước: python scripts/setup_answers.py --live"
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_phase_a_report(results: list[RagasResult], clusters: dict, bottom: list[dict]) -> dict:
    """Provided exporter: preserve the student-produced Task 3 rows verbatim."""
    per_dist: dict[str, dict] = {}
    for dist in ["factual", "multi_hop", "adversarial"]:
        subset = [r for r in results if r.distribution == dist]
        if subset:
            per_dist[dist] = {
                "count": len(subset),
                "faithfulness":      sum(r.faithfulness for r in subset) / len(subset),
                "answer_relevancy":  sum(r.answer_relevancy for r in subset) / len(subset),
                "context_precision": sum(r.context_precision for r in subset) / len(subset),
                "context_recall":    sum(r.context_recall for r in subset) / len(subset),
                "avg_score":         sum(r.avg_score for r in subset) / len(subset),
            }

    report = {
        "total_questions": len(results),
        "per_question": [asdict(r) for r in results],
        "per_distribution": per_dist,
        "failure_clusters": clusters,
        "bottom_10": bottom,
    }
    return report


def save_phase_a_report(results: list[RagasResult], clusters: dict, bottom: list[dict],
                        path: str = os.path.join(ARTIFACTS_DIR, "ragas_50q.json")) -> None:
    write_json(path, build_phase_a_report(results, clusters, bottom))



# ─── Tasks 1-4: Sinh viên implement ──────────────────────────────────────────

def group_by_distribution(test_set: list[dict]) -> dict[str, list[dict]]:
    """Task 1: Group source rows without changing their content or order."""
    groups = {"factual": [], "multi_hop": [], "adversarial": []}
    for item in test_set:
        distribution = item.get("distribution")
        if distribution not in groups:
            raise ValueError(f"Unknown distribution: {distribution!r}")
        groups[distribution].append(item)
    return groups


def run_ragas_50q(answers: list[dict]) -> RagasEvaluation:
    """Task 2: Evaluate 50 source answers and preserve m4 model provenance.

    Reject incomplete/non-finite measurements instead of generating scores or
    silently truncating rows. The runner validates source ids against fixtures.
    """
    if len(answers) != 50:
        raise ValueError("Phase A requires exactly 50 answers.")
    groups = group_by_distribution(answers)
    if [len(groups[dist]) for dist in ("factual", "multi_hop", "adversarial")] != [20, 20, 10]:
        raise ValueError("Phase A distributions must contain 20/20/10 answers.")
    ids = [row["id"] for row in answers]
    if any(type(qid) is not int or qid < 1 for qid in ids) or len(set(ids)) != 50:
        raise ValueError("Answer ids must be distinct positive integers.")

    from src.m4_eval import evaluate_ragas

    raw = evaluate_ragas(
        [a["question"] for a in answers],
        [a["answer"] for a in answers],
        [a["contexts"] for a in answers],
        [a["ground_truth"] for a in answers],
    )
    if not isinstance(raw, Mapping):
        raise ValueError("m4 must return a mapping with per_question and metadata.")
    per_question = raw.get("per_question")
    if not isinstance(per_question, list) or len(per_question) != len(answers):
        raise ValueError("m4 must return one measured row per answer (50 rows).")
    metadata = raw.get("metadata")
    models = metadata.get("evaluator_models") if isinstance(metadata, Mapping) else None
    if (not isinstance(models, list) or not models
            or any(not isinstance(model, str) or not model.strip()
                   or model != model.strip() for model in models)):
        raise ValueError("m4 metadata must declare actual evaluator_models.")

    results = []
    metric_names = ("faithfulness", "answer_relevancy", "context_precision", "context_recall")
    for answer, measured in zip(answers, per_question):
        scores = {}
        for metric in metric_names:
            value = measured.get(metric) if isinstance(measured, Mapping) else getattr(measured, metric, None)
            if value is None or isinstance(value, (bool, str, bytes)):
                raise ValueError(f"Answer {answer['id']}: invalid {metric} measurement.")
            try:
                score = float(value)
            except (TypeError, ValueError, OverflowError) as error:
                raise ValueError(f"Answer {answer['id']}: invalid {metric} measurement.") from error
            if not math.isfinite(score) or not 0 <= score <= 1:
                raise ValueError(f"Answer {answer['id']}: {metric} must be finite in [0, 1].")
            scores[metric] = score
        # When m4 includes row identities, catch reordered evaluation output.
        for field in ("question", "answer", "ground_truth", "contexts"):
            measured_value = measured.get(field) if isinstance(measured, Mapping) else getattr(measured, field, None)
            if measured_value is not None and measured_value != answer[field]:
                raise ValueError(f"Answer {answer['id']}: m4 {field} order/source mismatch.")
        results.append(RagasResult(
            question_id=answer["id"], distribution=answer["distribution"],
            question=answer["question"], answer=answer["answer"],
            contexts=list(answer["contexts"]), ground_truth=answer["ground_truth"],
            **scores,
        ))
    return RagasEvaluation(results=results, evaluator_models=list(models))


def bottom_10(results: list[RagasResult]) -> list[dict]:
    """Task 3: Return the ten lowest-scoring measured rows and suggested fixes."""
    from src.phase_a_analysis import bottom_10 as analyze_bottom
    return analyze_bottom(results)


def cluster_analysis(results: list[RagasResult]) -> dict:
    """Task 4: Count worst metrics and choose the weakest group by mean quality."""
    from src.phase_a_analysis import cluster_analysis as analyze_clusters
    return analyze_clusters(results)


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from scripts.run_experiments import main
    raise SystemExit(main(["--phase", "a", *sys.argv[1:]]))
