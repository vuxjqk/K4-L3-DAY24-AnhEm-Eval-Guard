# Báo cáo công việc Phase A — Trần Võ Hoàng Nguyên

- Nhóm: AnhEm.
- Học viên phụ trách: Trần Võ Hoàng Nguyên — MSSV 2A202602551.
- Ngày cập nhật: 12/10/2026 (UTC+7).
- Phạm vi: Tasks 1–4, đánh giá RAG bằng RAGAS (30 điểm bắt buộc).
- Nhánh bàn giao: codex/phase-a-hoang-nguyen.

## Kết quả đã hoàn thành

Đã hoàn thiện mã cho bốn tasks, tích hợp evaluator m4 và kiểm tra offline.
Đã chuẩn bị công cụ xuất báo cáo từ bằng chứng thực nghiệm đã validate.
Chưa chạy RAGAS trên API thật: repo chưa có answers_50q.json và các key cần thiết
chưa được cấu hình. Báo cáo này mô tả công việc triển khai; không thay thế
doc/reports/failure_clusters.md và artifacts/ragas_50q.json trong bài nộp.

## Công việc theo task

| Task | Công việc đã làm | Kết quả |
|---|---|---|
| 1 — group_by_distribution | Nhóm factual/multi_hop/adversarial, giữ nguyên nội dung và thứ tự, báo lỗi distribution không hợp lệ | Implement trong src/phase_a_ragas.py |
| 2 — run_ragas_50q | Gọi m4, chuyển object hoặc mapping metrics thành RagasResult, giữ ids/answer/contexts/reference và evaluator_models | Đủ 50 rows và 20/20/10; từ chối metrics không hữu hạn, sai nguồn hoặc thiếu metadata |
| 3 — bottom_10 | Stable sort theo avg_score, lấy tối đa 10 rows, đầy đủ rank/id/question/distribution/worst_metric/diagnosis/fix | Implement trong src/phase_a_analysis.py, giữ public API của lab |
| 4 — cluster_analysis | Matrix worst_metric × distribution của mọi câu, tính mean theo nhóm, bỏ nhóm rỗng, chọn mean thấp nhất | Có insight, xử lý empty/ties và không dùng số lượng câu thay chất lượng |

Diagnosis tự động là giả thuyết theo metric, chưa chứng minh nguyên nhân. Khi có
answers thật, cần đối chiếu answer, contexts và reference để xác nhận lỗi retrieval,
generation, phiên bản hoặc phủ định.

## Sửa tích hợp và công cụ hỗ trợ

- src/m4_eval.py: thêm metadata.evaluator_models từ LLM Gemini và embedding local
  được cấu hình trong evaluator. Khi evaluation lỗi, báo lỗi thay vì trả rows rỗng
  hoặc các điểm 0 như một kết quả hợp lệ; kiểm tra các input lists cùng độ dài.
- config.py: bổ sung GEMINI_OPENAI_BASE_URL mà m4 đang import nhưng trước đó thiếu.
- .env.example: ghi các biến cấu hình evaluator; không chứa API key thật.
- scripts/write_phase_a_report.py: đọc answers/report đã lưu, validate schema,
  nguồn và hashes trước khi viết failure_clusters.md; giữ diagnosis/fix Task 3,
  bảng điểm, bottom 10, matrix và answer/contexts/reference từng câu yếu.
- CLAUDE_PHASE_A.md: lưu lịch sử phân công, đã ghi rõ Claude bị dừng và Codex
  nhận toàn bộ Tasks 1–4.
- doc/PHASE_A_STATUS.md: lưu trạng thái, dependencies và các bước chạy tiếp.
- doc/TEAM.md: bản phân công được người dùng yêu cầu lấy từ nhánh docs,
  commit nguồn 35905ab. Nội dung này do nhóm cung cấp, không phải Codex tự đặt
  thành viên/phân công; các mục minh chứng cá nhân còn cần cập nhật sau thực nghiệm.

## Kiểm chứng đã thực hiện

Python thực tế trên máy: 3.11.9. Đã chạy:

```powershell
python -m pytest tests/test_phase_a.py tests/test_phase_a_adapter.py tests/test_phase_a_analysis.py tests/test_phase_a_report.py tests/test_report_contracts.py tests/test_support.py -k "not phase_c_runner_executes" -q
```

**Kết quả: 92 passed, 1 deselected.** Bao gồm toàn bộ Phase A tests, kiểm tra
schema/source contracts, bảo toàn nguồn, NaN/invalid metrics, missing rows/models,
sorting, matrix, nhóm rỗng, tie-break và report export.
Tests dùng mocks hoặc synthetic data trong thư mục tạm, không dùng chúng làm
artifacts nộp bài.

Một support test Phase C bị loại vì lần chạy riêng treo ở Windows socketpair/accept
khi asyncio tạo event loop trong môi trường thực thi này. Không sửa hoặc nới test;
không tuyên bố full suite toàn lab đã pass.

Đã chạy python scripts/check_lab.py: Phase A không còn TODO và năm module RAG
tồn tại. Checker toàn lab còn 10 failed checks do TEAM/reports còn mẫu,
Phase B/C còn TODO và thiếu bốn JSON kết quả. Số checks này không phải điểm rubric.

## Phần còn lại trước khi nộp

1. Trưởng nhóm Trần Anh Vũ cung cấp artifacts/answers_50q.json thật hoặc chạy
   setup_answers.py --live sau khi môi trường/pipeline đã sẵn sàng.
2. Cấu hình OPENAI_API_KEY cho CLI starter và GEMINI_API_KEY hoặc GOOGLE_API_KEY
   cho evaluator m4 trong .env; xác nhận model/endpoint khả dụng. Không gửi key
   trong chat, report hoặc commit.
3. Chạy thực nghiệm và xuất bản tổng hợp:

```powershell
python scripts/run_experiments.py --phase a --live
python scripts/write_phase_a_report.py
```

4. Bổ sung nhận xét nguyên nhân cụ thể cho các câu đại diện trong failure_clusters.md,
   dựa trên kết quả thực tế; kiểm chứng hướng sửa. Script xuất báo cáo ghi lại file,
   vì vậy chạy trước bước viết nhận xét thủ công.
5. Xét bonus +4 chỉ khi adversarial mean < factual mean và có phân tích bẫy.
   Không làm điểm xấu đi hoặc sửa corpus/fixtures để lấy bonus.
6. Nguyên cập nhật INDIVIDUAL, đọc và giải thích mã; trưởng nhóm tích hợp A/B/C,
   chạy checker/tests và chốt commit nộp.

## AI hỗ trợ và giới hạn bàn giao

Codex hỗ trợ triển khai mã, tests, tài liệu và công cụ xuất báo cáo. Claude Code
được giao ban đầu nhưng người dùng đã dừng trước khi có file bàn giao; không
khai Claude đã hoàn thành Tasks 3–4. Học viên chịu trách nhiệm đọc, giải thích
và kiểm chứng theo chính sách AI của lớp.

Nhánh/PR bàn giao mã và bằng chứng offline; không phải bằng chứng thực nghiệm
live và chưa đủ để xác nhận đạt trọn 30 điểm hoặc bonus.
