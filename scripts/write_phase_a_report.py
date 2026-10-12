"""Render saved, validated Phase A evidence into the lab report; no API calls."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import ROOT_DIR
from src.experiment_support import read_json
from src.report_contracts import validate_answers, validate_metadata, validate_phase_a


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def render_report(report, answers):
    """Include raw evidence so the learner can verify each suggested diagnosis."""
    validate_phase_a(report, answers)
    meta = report["metadata"]
    distributions = ("factual", "multi_hop", "adversarial")
    metrics = ("faithfulness", "answer_relevancy", "context_precision", "context_recall")
    by_id = {row["question_id"]: row for row in report["per_question"]}
    modes = {mode: sum(a["generation_mode"] == mode for a in answers)
             for mode in ("llm", "extractive_fallback")}
    lines = ["# Phân tích lỗi Phase A", "", "Nhóm: AnhEm",
             "Người phụ trách: Trần Võ Hoàng Nguyên — 2A202602551.", "",
             "Nguồn: artifacts/ragas_50q.json và artifacts/answers_50q.json.",
             f"Run timestamp: {meta['created_at']}.",
             f"Generation models: {', '.join(meta['models']['generation']) or 'không có (fallback)' }.",
             f"Evaluator models: {', '.join(meta['models']['evaluator'])}.",
             f"Generation modes: LLM {modes['llm']}/50; extractive fallback {modes['extractive_fallback']}/50.",
             "", "Bảng và trích xuất bằng chứng được tạo offline từ JSON đã validate. "
             "Diagnosis theo metric là giả thuyết; cần đọc các trường hợp bên dưới để xác nhận nguyên nhân.",
             "", "## Điểm theo distribution", "",
             "| Metric | factual (20) | multi_hop (20) | adversarial (10) |",
             "|---|---|---|---|"]
    for metric in (*metrics, "avg_score"):
        values = " | ".join(f"{report['per_distribution'][dist][metric]:.6f}" for dist in distributions)
        lines.append(f"| {metric} | {values} |")
    lines += ["", "## Bottom 10", "",
              "| Rank | ID | Question | Distribution | Avg score | Worst metric | Diagnosis | Suggested fix |",
              "|---|---|---|---|---|---|---|---|"]
    for row in report["bottom_10"]:
        values = [row[key] for key in ("rank", "question_id", "question", "distribution", "avg_score",
                                      "worst_metric", "diagnosis", "suggested_fix")]
        lines.append("| " + " | ".join(cell(value) for value in values) + " |")
    lines += ["", "## Bằng chứng cho từng câu yếu", ""]
    for bottom in report["bottom_10"]:
        row = by_id[bottom["question_id"]]
        lines += [f"### Câu {row['question_id']}: {row['question']}", "",
                  f"Answer thực tế: {row['answer']}", "", f"Reference: {row['ground_truth']}", "",
                  "Contexts đã truy xuất:", ""]
        lines += [f"- Context {i}: {text}" for i, text in enumerate(row["contexts"], 1)] or ["Không có contexts."]
        lines += ["", f"Giả thuyết cần kiểm chứng: {bottom['diagnosis']}",
                  f"Cải tiến đề xuất: {bottom['suggested_fix']}", ""]
    cluster = report["failure_clusters"]
    lines += ["## Matrix và nhóm yếu nhất", "",
              "| Worst metric | factual | multi_hop | adversarial |", "|---|---|---|---|"]
    for metric in metrics:
        values = " | ".join(str(cluster["matrix"][metric][dist]) for dist in distributions)
        lines.append(f"| {metric} | {values} |")
    lines += ["", cluster["insight"], "", "## Bẫy adversarial, cách cải tiến và giới hạn", ""]
    factual = report["per_distribution"]["factual"]["avg_score"]
    adversarial = report["per_distribution"]["adversarial"]["avg_score"]
    lines.append(f"Adversarial mean={adversarial:.6f}; factual mean={factual:.6f}; "
                 f"điều kiện số liệu adversarial < factual: {'đạt' if adversarial < factual else 'chưa đạt'}.")
    lines += ["", "Bẫy có sẵn trong corpus gồm phép năm v2023/v2024, mật khẩu v1/v2, "
              "phủ định quyền lợi thử việc và việc cấm VPN cá nhân. Cần đối chiếu các contexts "
              "đã lấy và answer để phân biệt retrieval sai phiên bản với generation bỏ qua điều kiện. "
              "Chênh lệch mean không tự chứng minh pipeline nhận ra version conflict và chưa đủ kết luận bonus.",
              "", "Nếu context thiếu thông tin, thử chunking/hybrid search/top-k; nếu context nhiễu, "
              "thử reranking/metadata phiên bản; nếu context đúng mà answer sai, siết prompt và yêu cầu "
              "trích dẫn. Chỉ chọn cải tiến sau khi đọc bằng chứng, chạy lại trên cùng 50 câu, "
              "so sánh bốn metric và kiểm tra không làm giảm chất lượng nhóm khác.",
              "", "Giới hạn: 50 câu, điểm phụ thuộc evaluator/model và generation fallback; "
              "worst_metric không phải kết luận nhân quả. Trước khi nộp, học viên cần bổ sung nhận xét "
              "nguyên nhân cụ thể cho các câu đại diện và kiểm chứng các đề xuất. "
              "AI hỗ trợ mã và tổng hợp số liệu; không tạo số đo hoặc thay answer bằng ground truth.", ""]
    # The starter checker treats a trailing question mark as a measurement
    # placeholder; HTML entities preserve real question punctuation in Markdown.
    return "\n".join(lines).replace("?", "&#63;")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(ROOT_DIR))
    args = parser.parse_args(argv)
    root = args.root.resolve()
    answers_path = root / "artifacts/answers_50q.json"
    questions_path = root / "fixtures/test_set_50q.json"
    answers = read_json(answers_path)
    validate_answers(answers, read_json(questions_path))
    report = read_json(root / "artifacts/ragas_50q.json")
    validate_metadata(report, [answers_path, questions_path])
    content = render_report(report, answers)
    target = root / "doc/reports/failure_clusters.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"Saved {target}; review individual causes before submitting.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
