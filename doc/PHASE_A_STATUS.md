# Bàn giao Phase A — Trần Võ Hoàng Nguyên (2A202602551)

## Trạng thái hiện tại

**Tasks 1–4, thực nghiệm thật và báo cáo phân tích đã hoàn thành.**
Đã kéo main tới commit 4404f72, dùng 50 answers từ commit 34b1bad của nhóm.
Không sinh lại hoặc sửa answers. RAGAS chạy thật bằng Gemini 3.8 và BGE-M3,
đã lưu artifacts/ragas_50q.json và hoàn thiện doc/reports/failure_clusters.md.
Run timestamp UTC: 2026-10-12T09:52:54.986101+00:00 (ngày 12/10/2026, UTC+7).

## Kết quả

| Nhóm | Số câu | Avg score |
|---|---|---|
| factual | 20 | 0.918184 |
| multi_hop | 20 | 0.709813 |
| adversarial | 10 | 0.743413 |

Nhóm yếu nhất: multi_hop. Metric thấp nhất xuất hiện nhiều nhất: context_recall,
17/50 câu. Matrix đếm mọi câu, không phải số failures theo ngưỡng tuyệt đối.
Bottom 10 ids: 33, 39, 44, 25, 48, 9, 32, 50, 37, 22.
Adversarial mean thấp hơn factual mean; report có phân tích bẫy version,
negation và contradiction để xét bonus A +4. Người chấm xác nhận điểm cuối.

## Kiểm chứng

- Đủ 50 answers, đúng 20/20/10 và nguồn question/reference; tất cả mode llm,
  generation model gpt-4o-mini-2024-07-18; không có contexts rỗng.
- Bốn metric mỗi câu hữu hạn trong [0,1], metadata phiên bản 2/run_kind live,
  evaluator models BAAI/bge-m3 và ag/gemini-3.8-flash; hashes đúng đầu vào.
- Report có bảng metrics, matrix, bottom 10 giữ nguyên Task 3 và phân tích
  answer/contexts/reference của các case đại diện; bổ sung case 41 ngoài bottom
  để chỉ rõ faithfulness không bảo đảm dùng đúng policy hiện hành.
- **96 tests Phase A/schema/support pass** trong virtualenv mới, không bỏ test.
  Lỗi test socketpair Windows trước đây đã được xử lý bằng chạy offline tests
  với quyền loopback; vẫn mock và chặn API ngoài trong tests.

## Môi trường và lệnh tái lập

Windows, Python 3.11.9; .venv-phase-a được tách khỏi packages toàn máy.
Requirements riêng ở requirements/requirements-phase-a.txt và constraints-core.txt,
bao gồm RAGAS 0.1.22, LangChain 0.2.x, PyTorch CPU 2.6.0, datasets 2.21.0,
pyarrow 17.0.0, sentence-transformers 3.4.1. Đã qua import runtime.
Không commit .env, virtualenv hoặc cache model.

```powershell
py -3.11 -m venv .venv-phase-a
.\.venv-phase-a\Scripts\python.exe -m pip install -r requirements/requirements-phase-a.txt -c requirements/constraints-core.txt
.\.venv-phase-a\Scripts\python.exe scripts/run_experiments.py --phase a --live
```

Phase A CLI chỉ yêu cầu key của evaluator Gemini (GEMINI_API_KEY hoặc GOOGLE_API_KEY),
GEMINI_MODEL và GEMINI_OPENAI_BASE_URL trong .env; không yêu cầu thêm OpenAI key.
B/C giữ yêu cầu OpenAI theo runner hiện tại.
Các lệnh live có API calls/chi phí. Khi artifact đã có, validate offline để tránh
chấm lại không cần thiết. scripts/write_phase_a_report.py sẽ ghi lại report từ
JSON và cần bổ sung phần phân tích thủ công; không chạy lại trên report đã hoàn thiện
nếu chưa lưu phần nhận xét để phục hồi.

## Phần bàn giao và giới hạn

Mã Tasks 1–4, CLI/preflight fix, manifest runtime, tests, JSON RAGAS, report và
phần INDIVIDUAL của Nguyên đã được cập nhật. Phase B/C và blueprint thuộc phần
thành viên khác; checker toàn lab có thể còn fail vì các phần đó/TEAM chưa đủ.
Nguyên cần đọc và giải thích mã, số đo và các nguyên nhân lỗi trước khi nộp.
Codex hỗ trợ triển khai/chạy/phân tích; Claude được dừng trước khi có bàn giao.
Không tuyên bố toàn lab hoặc production stack đã hoàn thành.
