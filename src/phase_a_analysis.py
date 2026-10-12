"""Tasks 3–4: summarize measured RAGAS rows without changing the evidence."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.phase_a_ragas import RagasResult

DISTRIBUTIONS = ("factual", "multi_hop", "adversarial")


def bottom_10(results: list[RagasResult]) -> list[dict]:
    """Return up to ten weakest rows; metric-based diagnoses need source review."""
    from src.phase_a_ragas import DIAGNOSTIC_TREE

    rows = []
    for rank, result in enumerate(sorted(results, key=lambda row: row.avg_score)[:10], 1):
        diagnosis, fix = DIAGNOSTIC_TREE[result.worst_metric]
        rows.append({
            "rank": rank, "question_id": result.question_id,
            "distribution": result.distribution, "question": result.question,
            "avg_score": result.avg_score, "worst_metric": result.worst_metric,
            "diagnosis": f"Giả thuyết theo metric: {diagnosis}. Cần đối chiếu answer, contexts và reference.",
            "suggested_fix": f"{fix}; chạy lại evaluation để kiểm chứng.",
        })
    return rows


def cluster_analysis(results: list[RagasResult]) -> dict:
    """Count each row once; identify the weakest group by its measured mean."""
    from src.phase_a_ragas import DIAGNOSTIC_TREE

    matrix = {metric: {dist: 0 for dist in DISTRIBUTIONS} for metric in DIAGNOSTIC_TREE}
    totals = {dist: 0.0 for dist in DISTRIBUTIONS}
    counts = {dist: 0 for dist in DISTRIBUTIONS}
    for result in results:
        if result.distribution not in counts:
            raise ValueError(f"Unknown distribution: {result.distribution!r}")
        matrix[result.worst_metric][result.distribution] += 1
        totals[result.distribution] += result.avg_score
        counts[result.distribution] += 1
    means = {dist: totals[dist] / counts[dist] for dist in DISTRIBUTIONS if counts[dist]}
    weakest = min(means, key=means.get) if means else None
    most_frequent = max(matrix, key=lambda metric: sum(matrix[metric].values())) if results else None
    if weakest is None:
        insight = "Chưa có dữ liệu đánh giá; chưa thể xác định nhóm yếu hoặc metric thấp nhất chủ đạo."
    else:
        frequency = sum(matrix[most_frequent].values())
        insight = (
            f"Nhóm {weakest} có avg_score trung bình thấp nhất ({means[weakest]:.4f}). "
            f"{most_frequent} là metric thấp nhất ở {frequency}/{len(results)} câu. "
            "Matrix thống kê mọi câu, không khẳng định tất cả đều là failures; "
            "tổng cột chỉ là số câu. Cần đọc answer/contexts/reference để xác định nguyên nhân. "
            f"Hướng kiểm chứng: {DIAGNOSTIC_TREE[most_frequent][1]}."
        )
    return {
        "matrix": matrix, "distribution_avg_scores": means,
        "dominant_failure_distribution": weakest,
        "dominant_failure_metric": most_frequent, "insight": insight,
    }
