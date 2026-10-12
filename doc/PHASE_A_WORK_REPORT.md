# Báo cáo công việc Phase A — Trần Võ Hoàng Nguyên

- Nhóm AnhEm; MSSV 2A202602551; ngày cập nhật 12/10/2026 (UTC+7).
- Nhánh codex/phase-a-hoang-nguyen; PR mã ban đầu #1 đã merge vào main.
- Phạm vi Tasks 1–4 (30 điểm bắt buộc) và bằng chứng/report Phase A.

## Công việc hoàn thành

| Task | Implementation và kiểm chứng |
|---|---|
| 1 | group_by_distribution: đúng 20/20/10, giữ nội dung/thứ tự, từ chối distribution không hợp lệ |
| 2 | run_ragas_50q: evaluate m4 trên 50 answers thật; giữ nguồn và evaluator models; từ chối NaN, thiếu rows, sai nguồn/thứ tự, metrics ngoài [0,1] |
| 3 | bottom_10: stable sort, đúng 10 rows, đủ rank/id/question/distribution/worst_metric/diagnosis/fix; exporter giữ nguyên |
| 4 | cluster_analysis: matrix mọi câu, nhóm yếu theo mean thấp nhất, bỏ nhóm rỗng và có insight |

Đã sửa metadata evaluator và biến endpoint còn thiếu trong m4/config; sửa CLI
để Phase A dùng key Gemini phù hợp evaluator, không yêu cầu OpenAI riêng.
Đã pin runtime Phase A riêng sau khi môi trường global LangChain 1.x và bản
PyTorch mới gây lỗi import/DLL. Không thay environment chung của máy.

## Thực nghiệm và bằng chứng

- Answers thật của nhóm đã có trên main: 50 câu, 20/20/10, generation_mode llm,
  generation model gpt-4o-mini-2024-07-18; giữ nguyên inputs và corpus cũ/mới.
- Chạy bốn metric RAGAS thật, 200 phép đo; evaluator ag/gemini-3.8-flash và
  embedding local BAAI/bge-m3. Timestamp UTC 2026-10-12T09:52:54.986101+00:00.
- Đã lưu artifacts/ragas_50q.json hợp lệ và hoàn thiện
  doc/reports/failure_clusters.md từ JSON cùng đối chiếu nội dung.
- doc/PHASE_A_SOURCE_REVIEW.md chứa ghi chú đối chiếu thêm các case, không
  tự gán điểm hoặc thay danh sách bottom 10.

| Distribution | Avg score |
|---|---|
| factual | 0.918184 |
| multi_hop | 0.709813 |
| adversarial | 0.743413 |

Multi_hop yếu nhất; context_recall là metric thấp nhất ở 17/50 câu.
Bottom 10: 33, 39, 44, 25, 48, 9, 32, 50, 37, 22.
Adversarial < factual, kèm phân tích bẫy trong report, đáp ứng điều kiện xét
bonus Phase A +4; điểm cuối do coach xác nhận.

## Phân tích nổi bật

- Câu 21/22/25/33/39: retrieval thiếu ý hoặc hàng bảng, và có nhiễu giữa quy trình.
- Câu 9/32/44/48/50: context có thông tin nhưng generation trả không tìm thấy.
- Câu 37: generation thêm sự kiện không được câu hỏi hỗ trợ, khái quát nhãn dữ liệu.
- Câu 41 ngoài bottom 10: chọn 12 ngày v2023 dù context có v2024 là 15 ngày;
  faithfulness=1 không đồng nghĩa đúng phiên bản hiện hành.
- Câu 24/29 ngoài bottom 10: phí tạm ứng sai vì thiếu công thức pro-rata và
  generation suy ra cả tháng. Cải tiến đã đề xuất, chưa chạy lại sau cải tiến.

## Kiểm tra đã chạy

```powershell
.\.venv-phase-a\Scripts\python.exe -m pytest tests/test_phase_a.py tests/test_phase_a_adapter.py tests/test_phase_a_analysis.py tests/test_phase_a_report.py tests/test_phase_a_cli.py tests/test_report_contracts.py tests/test_support.py -q
```

**96 passed, không bỏ test.** Tests dùng mocks/synthetic data trong thư mục tạm;
JSON nộp bài là lượt live riêng. Đã validate counts, ids, sources, metrics,
metadata, hashes và báo cáo Markdown offline. Không chạy batch live lặp lại
chỉ để kiểm chứng artifact đã lưu.

## Bàn giao và AI hỗ trợ

Bàn giao mã, runtime manifest, tests, ragas_50q.json, failure_clusters.md,
source review và phần INDIVIDUAL của Nguyên. TEAM lấy phân công từ commit
35905ab của nhóm; giữ phần các thành viên khác cho chính họ hoàn thiện.

Codex hỗ trợ mã/tests/chạy và phân tích. Claude được giao ban đầu nhưng người
 dùng đã dừng trước khi có file bàn giao. Không có số đo tự điền, không dùng
 ground_truth làm answer, không sửa fixtures hoặc xóa policy cũ.
Nguyên cần đọc, giải thích và kiểm chứng theo chính sách AI của lớp.

Đây là hoàn thiện Phase A, không tuyên bố Phase B/C, blueprint hoặc toàn bài
nộp đã hoàn thành. Không commit API key, .env, virtualenv hay cache model.
