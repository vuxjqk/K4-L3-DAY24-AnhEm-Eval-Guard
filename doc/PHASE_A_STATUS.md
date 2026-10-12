# Bàn giao Phase A — Trần Võ Hoàng Nguyên (2A202602551)

## Trạng thái

Người dùng đã dừng Claude Code và giao Codex làm toàn bộ Tasks 1–4.
Mã và kiểm tra offline đã hoàn thành. Chưa hoàn thành bằng chứng live và báo cáo
phân tích kết quả để nộp: chưa có artifacts/answers_50q.json; OPENAI_API_KEY và
GEMINI_API_KEY hiện chưa được cấu hình. Không có số đo RAGAS thật trong repo.
Không tạo mock artifact hay thay answer bằng ground_truth.

## Phần đã làm

| Task | Implementation | Kiểm tra chính |
|---|---|---|
| 1 | group_by_distribution trong src/phase_a_ragas.py | Đúng nhóm, giữ thứ tự/nội dung, từ chối distribution không hợp lệ |
| 2 | run_ragas_50q trong src/phase_a_ragas.py | Đủ 50 rows, 20/20/10, model metadata từ m4; từ chối NaN, thiếu rows, sai nguồn/thứ tự và metric ngoài [0,1] |
| 3 | bottom_10 trong src/phase_a_analysis.py, public wrapper trong phase_a_ragas | Stable sort, tối đa 10, đầy đủ rank/id/diagnosis/fix; không mutate input |
| 4 | cluster_analysis trong src/phase_a_analysis.py, public wrapper trong phase_a_ragas | Matrix mọi câu, weakest theo mean thấp nhất, bỏ nhóm rỗng, tie-break ổn định, insight có giới hạn |

Sửa tương thích tối thiểu: config có GEMINI_OPENAI_BASE_URL mà m4 đang import;
m4 trả metadata.evaluator_models từ LLM và embedding được cấu hình thực tế.
Nếu evaluator lỗi thì báo lỗi; không trả điểm 0 hay rows rỗng như kết quả hợp lệ.
Chưa kiểm chứng endpoint, model availability hoặc evaluator trên API thật.

Thêm scripts/write_phase_a_report.py để tạo bảng, bottom 10, matrix và trích
answer/contexts/reference từ report đã validate, không gọi API. Script từ chối
nguồn stale trước khi ghi file. Report sinh ra vẫn cần học viên đọc bằng chứng
và bổ sung nhận xét nguyên nhân cụ thể trước khi nộp; metric đơn lẻ chưa chứng
minh nguyên nhân. Lệnh này sẽ ghi lại doc/reports/failure_clusters.md, nên chạy
trước khi chỉnh tay nội dung phân tích để không mất phần nhận xét đã bổ sung.

## Kiểm tra thực tế

Python trên máy: 3.11.9.

```powershell
python -m pytest tests/test_phase_a.py tests/test_phase_a_adapter.py tests/test_phase_a_analysis.py tests/test_phase_a_report.py tests/test_report_contracts.py tests/test_support.py -k "not phase_c_runner_executes" -q
```

Kết quả: **92 passed, 1 deselected**. Bao gồm toàn bộ Phase A tests, các edge
cases mới, kiểm tra report export và regressions schema/support.
Các dữ liệu synthetic chỉ dùng bên trong tests và thư mục pytest tạm, không
ghi mock results vào artifacts của bài nộp.

Một support test Phase C bị loại khỏi lần chạy này: test_phase_c_runner_executes_one_input_batch_and_four_outputs.
Lần chạy riêng bị treo ở Windows socketpair/accept khi asyncio tạo event loop
trong môi trường thực thi hiện tại; đã dừng tiến trình. Không sửa test để né lỗi.
Đây là kiểm tra ngoài Phase A; không tuyên bố toàn bộ tests lab đã pass.

## Bước cần thiết để có bài nộp Phase A hoàn chỉnh

1. Nhận answers_50q.json thật từ Trần Anh Vũ, đúng 50 ids và 20/20/10;
   hoặc trưởng nhóm chạy python scripts/setup_answers.py --live sau khi pipeline sẵn sàng.
2. Cấu hình key trong .env trên máy, không gửi key trong chat hoặc commit.
   CLI starter yêu cầu OPENAI_API_KEY; m4 hiện dùng GEMINI_API_KEY/GOOGLE_API_KEY
   và GEMINI_MODEL để evaluation. Xác nhận model/endpoint hoạt động trước batch.
3. Chạy từ gốc repo:

```powershell
python scripts/run_experiments.py --phase a --live
python scripts/write_phase_a_report.py
```

4. Đọc bằng chứng bottom 10 trong failure_clusters.md, bổ sung phân tích các
   câu đại diện: retrieval/generation/version/negation; đề xuất sửa và cách kiểm chứng.
5. Đối chiếu adversarial mean với factual mean, phân tích bẫy để xét bonus +4
   nếu điều kiện thật đạt. Không sửa dữ liệu hoặc làm điểm thấp đi để lấy bonus.
6. Cập nhật INDIVIDUAL và bằng chứng commit/PR thật, kiểm tra secrets; bàn giao
   source, ragas_50q.json và report cho trưởng nhóm. B/C và blueprint vẫn do
   người được phân công trong TEAM phụ trách.
7. Trưởng nhóm chạy python scripts/check_lab.py --with-tests trên bản tích hợp.
   Checker toàn lab sẽ còn fail nếu B/C, reports hoặc TEAM chưa hoàn thiện.

## AI hỗ trợ và giới hạn

Codex viết mã, tests và công cụ tổng hợp báo cáo; Claude đã được giao nhưng
bị người dùng dừng trước khi có file bàn giao. Không khai Claude đã implement.
Nguyên cần đọc, giải thích và tự kiểm chứng mã trước khi nộp theo chính sách lớp.
Các thay đổi hiện chỉ ở working tree, chưa commit/push; không phải bằng chứng
đã chạy API và chưa đủ để tuyên bố đạt trọn 30 điểm.
