# Báo cáo công việc Phase C — Nguyễn Đức Thịnh

- Nhóm: AnhEm.
- Học viên phụ trách: Nguyễn Đức Thịnh — MSSV 2A202602468.
- Ngày cập nhật: 12/10/2026 (UTC+7).
- Phạm vi: Tasks 9a, 9b, 10, 11 (Guardrails & Clean controls) trong `src/phase_c_guard.py` và cấu hình `guardrails/`.
- Nhánh thực hiện: `Thihn/task3`.

## 1. Kết quả đã hoàn thành

Đã triển khai hoàn thiện toàn bộ mã nguồn cho Phase C trong `src/phase_c_guard.py`, xóa sạch các tag `# TODO`, cấu hình guardrails hoạt động chính xác và vượt qua 100% unit tests offline (12/12 passed).

## 2. Chi tiết các Task thực hiện

| Task | Hàm / Cấu hình | Mô tả triển khai | Kết quả kiểm tra |
|---|---|---|---|
| **9a** | `pii_scan(text, analyzer, anonymizer)` | Quét và làm mờ (redact) PII bằng Presidio. Tích hợp custom recognizer cho CCCD (12 số), CMND (9 số), SĐT VN (`0[3-9]xxxxxxxx`) và Email chuẩn. Trả về `has_pii`, `entities` kèm vị trí start/end, `anonymized`. | Pass test PII detect & redact (CCCD, CMND, Phone, Email) và clean text. |
| **9b** | `check_input_rail(text, rails)` *(async)* | Kiểm tra prompt qua NeMo Input Rail (self check input: topic guard + jailbreak guard). Đọc cờ `stop` từ `result.log.activated_rails` để quyết định `allowed`/`blocked_reason`, tuyệt đối không dùng heuristic tìm chuỗi từ chối. | Pass test input rail decision và option forwarding `rails: ["input"]`. |
| **10** | `run_adversarial_suite(adversarial_set, ...)` | Chạy full guard stack kết hợp 2 lớp: Presidio PII (Layer 1) -> NeMo input rail (Layer 2) nếu PII không chặn. Xử lý async trong một event loop duy nhất tránh lỗi treo loop trên Windows. Trả về đủ 28 rows (20 attack + 8 clean). | Pass 28/28 rows schema check; chặn đúng 20 attacks, cho qua đúng 8/8 clean inputs. |
| **11** | `check_output_rail(question, answer, rails)` *(async)* | Kiểm tra output của LLM qua NeMo Output Rail trong ngữ cảnh đầy đủ `[user, assistant]`. Giữ nguyên answer sạch; thay thế/redact nếu phát hiện rò rỉ PII/dữ liệu nhạy cảm. | Pass test output rail: giữ clean answer, thay đổi unsafe answer khi bị chặn. |
| **12** | `measure_p95_latency(test_inputs, ...)` | Đo độ trễ tuần tự `input_layers_sequential` (Presidio + NeMo input), loại trừ 2 lượt warm-up thật, thu thập ≥20 timed samples dùng `time.perf_counter`, tính percentile tuyến tính qua helper. | Pass test warmup, sample count và tính toán linear percentile. |

## 3. Cấu hình Guardrails (`guardrails/`)

- `guardrails/config.yml`:
  - Khai báo model `gpt-4o-mini` (engine openai).
  - Tinh chỉnh `self_check_input`: Chặn jailbreak, prompt injection, đóng vai, đòi truy cập PII; Cho phép câu hỏi chính sách nhân sự chung, khung lương theo role, VPN, password, MFA, báo cáo sự cố.
  - Tinh chỉnh `self_check_output`: Chặn lộ CCCD/CMND cá nhân, lương riêng của nhân viên, mật khẩu; Cho phép chính sách chung và email công cộng `helpdesk@cty.vn`.
- `guardrails/rails.co`:
  - Định nghĩa câu trả lời từ chối chuẩn mực Colang 1.0 cho bot khi rail kích hoạt dừng (`refuse to respond`).

## 4. Kiểm chứng đã thực hiện

Chạy test offline qua pytest:
```powershell
.venv\Scripts\python.exe -m pytest tests/test_phase_c.py -v
```
**Kết quả:** `12 passed in 0.08s` (100% tests đạt).

Chạy submission checker tổng thể:
```powershell
.venv\Scripts\python.exe scripts/check_lab.py
```
**Kết quả:** `PASS phase_c_guard.py` (không còn `# TODO`, hoàn thành hợp đồng mã nguồn).

## 5. Hướng dẫn chạy thực nghiệm Live sinh Artifact

Sau khi cấu hình đầy đủ API key trong `.env` (`OPENAI_API_KEY`), chạy lệnh sau để sinh `artifacts/guard_results.json`:
```powershell
.venv\Scripts\python.exe scripts/run_experiments.py --phase c --live --latency-samples 20
```

Runner sẽ kiểm tra:
1. Bộ 20 attack inputs: đạt tỷ lệ chặn ≥15/20 (≥18/20 để xét bonus +3 điểm).
2. Bộ 8 clean controls: 8/8 được cho phép (`false_positive_rate = 0.0`).
3. Bộ 4 output cases: 2 safe được giữ nguyên, 2 unsafe bị chặn/thay thế.
4. Đo P95 latency với 2 lượt warm-up và 20 samples thực tế.

## 6. Minh chứng đóng góp cá nhân

- Học viên: Nguyễn Đức Thịnh (2A202602468).
- Nhánh git: `Thihn/task3`.
- Commit files: `src/phase_c_guard.py`, `doc/PHASE_C_WORK_REPORT.md`, `doc/TEAM.md`.
