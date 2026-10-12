# Nhóm thực hiện K4 Track 3A

Tên nhóm: AnhEm

Repo chung: https://github.com/vuxjqk/K4-L3-DAY24-AnhEm-Eval-Guard

Trưởng nhóm/người nộp: Trần Anh Vũ — 2A202602570

Ngày lab/deadline áp dụng: 12/10/2026, 23:59 — Asia/Ho_Chi_Minh (UTC+07:00)

Commit dùng để chấm: {{Commit SHA — trưởng nhóm điền sau khi chốt bản nộp}}

Mỗi nhóm nộp một repo. Điền đủ thành viên và một mục INDIVIDUAL cho từng người.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | Trần Anh Vũ | 2A202602570 | Trưởng nhóm, phụ trách tích hợp: setup answers 50q, adapter m4 `evaluator_models`, Task 12 `measure_p95_latency` (`src/phase_c_guard.py`), Task 13 `doc/reports/blueprint.md`, TEAM, check_lab, nộp bài | {{Commit/PR}}, `artifacts/answers_50q.json`, `doc/reports/blueprint.md` |
| 2 | Trần Võ Hoàng Nguyên | 2A202602551 | Phase A, RAGAS: Tasks 1–4 trong `src/phase_a_ragas.py`, chạy Phase A live, viết failure_clusters | {{Commit/PR}}, `artifacts/ragas_50q.json`, `doc/reports/failure_clusters.md` |
| 3 | Trần Tuấn Cường | 2A202602717 | Phase B, LLM judge: Tasks 5–8 trong `src/phase_b_judge.py`, chạy Phase B live, viết bias_report | {{Commit/PR}}, `artifacts/judge_results.json`, `doc/reports/bias_report.md` |
| 4 | Nguyễn Đức Thịnh | 2A202602468 | Phase C, Guardrails: Tasks 9a, 9b, 10, 11 trong `src/phase_c_guard.py`, tinh chỉnh `guardrails/`, chạy Phase C live | Nhánh `Thihn/task3`, `artifacts/guard_results.json` |

Người tích hợp/chạy batch/nộp link: Trần Anh Vũ — sinh answers, merge PR các
phase, chạy `python scripts/check_lab.py --with-tests`, push và nộp link.
Bằng chứng: {{Commit merge / PR}}.

## Chi tiết phân công (khung bám theo)

Quy trình chung cho mọi thành viên:

1. Tạo nhánh từ `main`: `phase-a`, `phase-b`, `phase-c` hoặc `lead`.
2. Implement các hàm được giao, xóa hết `# TODO` trong phần của mình.
3. Chạy test offline của phase mình: `python -m pytest tests/test_phase_X.py -q`.
4. Chạy batch live của phase: `python scripts/run_experiments.py --phase X --live`.
5. Kiểm tra JSON trong `artifacts/` không chứa key/secret, rồi commit cả source, artifact và report.
6. Mở PR vào `main`, nhờ trưởng nhóm review và merge.
7. Tự điền mục INDIVIDUAL của mình bên dưới.

### 1. Trần Anh Vũ — Trưởng nhóm / Tích hợp

| Thứ tự | Việc | File / lệnh | Tiêu chí xong |
|---|---|---|---|
| 1 | Sinh 50 answers (**làm đầu tiên**: Phase A và B phụ thuộc file này) | `python scripts/setup_answers.py --live` | Đúng 50 id, chia 20/20/10; ghi `generation_mode` và `generation_model`; answer không chép từ ground_truth |
| 2 | Kiểm tra adapter m4 | `src/m4_eval.py` | `metadata.evaluator_models` liệt kê model thật được dùng, không lấy JUDGE_MODEL thay |
| 3 | Task 12 `measure_p95_latency` | `src/phase_c_guard.py` | Tạo engines trước khi đo; warm-up 2 lượt bị loại khỏi samples; ≥20 samples; mỗi sample chạy Presidio rồi NeMo input, không short-circuit |
| 4 | Review và merge PR phase-a/b/c | GitHub | Merge Phase C của Thịnh trước, sau đó merge Task 12 để tránh conflict |
| 5 | Task 13 Blueprint | `doc/reports/blueprint.md` | Có kiến trúc, failure actions, CI gates và monitoring (ghi rõ là đề xuất); có latency input layers đã đo; phần chưa đo ghi “chưa đo” |
| 6 | Đóng gói và nộp | `python scripts/check_lab.py --with-tests` | Checker pass; điền commit SHA ở đầu file; nộp link |

### 2. Trần Võ Hoàng Nguyên — Phase A (30 điểm + bonus 4)

| Task | Hàm | Tiêu chí xong |
|---|---|---|
| 1 | `group_by_distribution` | 3 keys factual/multi_hop/adversarial, đúng 20/20/10 |
| 2 | `run_ragas_50q` | Gọi `m4_eval.evaluate_ragas`; trả `RagasEvaluation` gồm 50 `RagasResult` và `evaluator_models`; 4 metric là `float` hữu hạn trong [0,1], không để NaN |
| 3 | `bottom_10` | 10 câu xếp tăng dần theo avg_score; mỗi câu có rank/id/question/distribution/worst_metric/diagnosis/suggested_fix |
| 4 | `cluster_analysis` | Matrix worst_metric × distribution; nhóm yếu nhất chọn theo **mean thấp nhất**, không theo tổng số câu; bỏ nhóm rỗng khỏi phép chia; có insight |
| Report | `doc/reports/failure_clusters.md` | Đọc question/answer/contexts/reference của các câu yếu trước khi kết luận nguyên nhân; nếu adversarial mean < factual mean thì phân tích bẫy phiên bản để lấy bonus |

Chạy: `python -m pytest tests/test_phase_a.py -q` rồi `python scripts/run_experiments.py --phase a --live`.

### 3. Trần Tuấn Cường — Phase B (35 điểm + bonus 3)

| Task | Hàm | Tiêu chí xong |
|---|---|---|
| 5 | `pairwise_judge(q, A, B, reference)` | LLM trả JSON winner A/B/tie, reasoning, score_a/score_b trong [0,1]; prompt có reference |
| 6 | `swap_and_average` | Chấm 2 lượt A/B và B/A; quy winner và scores về A/B ban đầu; hai lượt đồng thuận thì lấy winner đó, không thì tie |
| 7 | `cohen_kappa` | Đúng công thức; hai bên đồng ý hoàn toàn trên tập nhãn có cả 0 và 1 thì κ=1; kết quả trong [-1,1] |
| 8 | `bias_report` | Đếm position inconsistency; tính tỷ lệ answer dài hơn thắng trong các case decisive; có diễn giải |
| Report | `doc/reports/bias_report.md` | Đọc nội dung từng cặp trước khi kết luận là bias; κ > 0.6 thì đạt bonus |

Lưu ý: cặp A/B phải đúng id 1, 5, 12, 21, 41. **Không** đưa `human_label`/`human_note`
vào prompt, **không** sửa candidate sau khi xem kết quả judge.
Chạy: `python -m pytest tests/test_phase_b.py -q` rồi `python scripts/run_experiments.py --phase b --live`.

### 4. Nguyễn Đức Thịnh — Phase C (30 điểm + bonus 3)

| Task | Hàm | Tiêu chí xong |
|---|---|---|
| 9a | `pii_scan` | Presidio detect và anonymize CCCD/CMND, số điện thoại VN, email; trả entities kèm vị trí |
| 9b | `check_input_rail` (async) | Chỉ chạy input rail; quyết định dựa trên `result.log.activated_rails`, **không** dò chữ “xin lỗi/không thể” |
| 10 | `run_adversarial_suite` | Giữ nguyên input; `expected` chỉ dùng để đối chiếu; trả đủ các rows. Yêu cầu ≥15/20 attacks bị chặn (≥18 để lấy bonus) và 8/8 câu sạch được cho qua |
| 11 | `check_output_rail` (async) | 4 output cases: output sạch giữ nguyên, output nhạy cảm bị thay hoặc redact |
| Config | `guardrails/config.yml`, `rails.co` | Tinh chỉnh self-check prompts để giảm số câu sạch bị chặn nhầm |

Cài NeMo, Presidio và spaCy **ngay đầu buổi**; nếu lỗi thì ghi lỗi thật vào TEAM.
Chạy: `python -m pytest tests/test_phase_c.py -q` rồi
`python scripts/run_experiments.py --phase c --live --latency-samples 20`
(chạy sau khi Task 12 của Vũ đã merge).

## Môi trường và chuẩn bị trước lớp

OS/Python/compiler: Windows 11 Pro, Python 3.11.9, {{compiler}}.
Virtualenv/dependencies/imports: {{Lệnh và kết quả}}.
Models/Qdrant/50 answers đã chuẩn bị: {{Bằng chứng và giới hạn/fallback}}.
Nếu cài full NeMo chưa thành công, ghi lỗi thực tế; không dùng unit test pass
hoặc pip resolve để khẳng định runtime đã chạy.

## INDIVIDUAL

### TranAnhVu-2A202602570

- Phần được giao và phần thực tế đã làm: {{Setup answers, adapter m4, Task 12, blueprint, tích hợp/nộp}}.
- Bằng chứng: {{Commit/PR; artifacts/answers_50q.json, doc/reports/blueprint.md}}.
- Cách kiểm tra: {{Lệnh setup/check_lab và kết quả}}.
- Điều đã học: {{Khái niệm và cách thể hiện trong bài}}.
- Giới hạn/cách xử lý: {{Vấn đề và kiểm chứng}}.
- Nguồn/AI hỗ trợ nếu có: {{Công cụ, phạm vi, cách tự kiểm chứng}}.

### TranVoHoangNguyen-2A202602551

- Phần được giao và phần thực tế đã làm: {{Tasks 1–4 trong src/phase_a_ragas.py, failure_clusters.md}}.
- Bằng chứng: {{Commit/PR; artifacts/ragas_50q.json, doc/reports/failure_clusters.md}}.
- Cách kiểm tra: {{pytest tests/test_phase_a.py, run_experiments --phase a --live và kết quả}}.
- Điều đã học: {{Khái niệm và cách thể hiện trong bài}}.
- Giới hạn/cách xử lý: {{Vấn đề và kiểm chứng}}.
- Nguồn/AI hỗ trợ nếu có: {{Công cụ, phạm vi, cách tự kiểm chứng}}.

### TranTuanCuong-2A202602717

- Phần được giao và phần thực tế đã làm: {{Tasks 5–8 trong src/phase_b_judge.py, bias_report.md}}.
- Bằng chứng: {{Commit/PR; artifacts/judge_results.json, doc/reports/bias_report.md}}.
- Cách kiểm tra: {{pytest tests/test_phase_b.py, run_experiments --phase b --live và kết quả}}.
- Điều đã học: {{Khái niệm và cách thể hiện trong bài}}.
- Giới hạn/cách xử lý: {{Vấn đề và kiểm chứng}}.
- Nguồn/AI hỗ trợ nếu có: {{Công cụ, phạm vi, cách tự kiểm chứng}}.

### NguyenDucThinh-2A202602468

- Phần được giao và phần thực tế đã làm: Tasks 9a, 9b, 10, 11 trong `src/phase_c_guard.py`, cấu hình `guardrails/config.yml` và `guardrails/rails.co`.
- Bằng chứng: Nhánh `Thihn/task3`, source `src/phase_c_guard.py`, 12/12 unit tests passed (`tests/test_phase_c.py`), `artifacts/guard_results.json`.
- Cách kiểm tra: `python -m pytest tests/test_phase_c.py -v`, `python scripts/check_lab.py`, `python scripts/run_experiments.py --phase c --live --latency-samples 20`.
- Điều đã học: Presidio PII scanning với custom regex VN (CCCD/CMND/SĐT), NeMo Guardrails Colang 1.0 tự kiểm tra input/output rail bằng self-check prompts, đo độ trễ tuần tự P95 cho input layer.
- Giới hạn/cách xử lý: Chạy NeMo input rail tốn thời gian; tối ưu thực thi async gom trong một event loop duy nhất để tránh treo trên Windows; tinh chỉnh prompt self-check để không chặn nhầm 8 câu clean input.
- Nguồn/AI hỗ trợ nếu có: Antigravity AI hỗ trợ sinh mã mẫu theo spec, tự kiểm chứng bằng test suite `tests/test_phase_c.py` và `scripts/check_lab.py`.

## Cập nhật sau khi nộp

{{Ghi phiên bản nộp; nếu sửa sau deadline, ghi commit/thời điểm/lý do và thông báo
coach cho phép áp dụng bản cập nhật. Nếu không có cập nhật, ghi rõ không có.}}
