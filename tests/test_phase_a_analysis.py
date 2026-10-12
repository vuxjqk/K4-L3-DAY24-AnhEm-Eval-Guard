"""Boundary cases that guard against misleading cluster statistics."""
import pytest

from src.phase_a_ragas import RagasResult, bottom_10, cluster_analysis

pytestmark = pytest.mark.student


def row(qid, distribution="factual", score=.5):
    return RagasResult(qid, distribution, f"Q{qid}", "A", ["C"], "G",
                       score, score, score, score)


def test_bottom_stable_ties_and_no_input_mutation():
    rows = [row(3), row(1), row(2)]
    result = bottom_10(rows)
    assert [r["question_id"] for r in result] == [3, 1, 2]
    assert [r.question_id for r in rows] == [3, 1, 2]
    assert all(r["worst_metric"] == "faithfulness" for r in result)
    assert all("Giả thuyết" in r["diagnosis"] for r in result)


def test_empty_inputs_have_no_invented_quality():
    assert bottom_10([]) == []
    cluster = cluster_analysis([])
    assert cluster["distribution_avg_scores"] == {}
    assert cluster["dominant_failure_distribution"] is None
    assert cluster["dominant_failure_metric"] is None
    assert sum(sum(column.values()) for column in cluster["matrix"].values()) == 0


def test_absent_group_is_excluded_and_matrix_counts_all_rows():
    rows = [row(1, "factual", .9), row(2, "factual", .7), row(3, "adversarial", .6)]
    cluster = cluster_analysis(rows)
    assert cluster["distribution_avg_scores"] == pytest.approx({"factual": .8, "adversarial": .6})
    assert cluster["dominant_failure_distribution"] == "adversarial"
    assert {dist: sum(counts[dist] for counts in cluster["matrix"].values())
            for dist in ("factual", "multi_hop", "adversarial")} == {
                "factual": 2, "multi_hop": 0, "adversarial": 1}


def test_group_tie_break_is_deterministic():
    cluster = cluster_analysis([row(1, "adversarial"), row(2, "factual")])
    assert cluster["dominant_failure_distribution"] == "factual"


def test_unknown_group_is_rejected():
    with pytest.raises(ValueError, match="Unknown distribution"):
        cluster_analysis([row(1, "unknown")])
