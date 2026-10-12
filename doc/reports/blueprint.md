# Blueprint CI/CD cho RAG và guardrails

Nhóm: AnhEm

Người phụ trách: Trần Anh Vũ — 2A202602570

Đây là **đề xuất CI/CD**, không phải workflow đã được triển khai/chạy.
Nguồn kết quả: artifacts/ragas_50q.json, judge_results.json, guard_results.json.
Run timestamp: {{created_at}}; guard models: {{metadata.models.guard}}.
Models generation/evaluator/judge từ A/B: {{models theo từng vai trò và nguồn report}}.

## Kiến trúc và failure action

Input → Presidio → NeMo input → RAG → NeMo output → response.
Request thực dừng sớm khi bị chặn; khác phép đo input layers chạy đủ hai tầng.

| Tầng | Thành phần trong repo | Khi đạt | Failure action (đề xuất) | Log |
|---|---|---|---|---|
| 1. PII input | Presidio + recognizer VN_CCCD, VN_PHONE, EMAIL (`setup_presidio`, `pii_scan`) | Chuyển sang tầng 2 | Chặn request (`blocked_by=presidio`), trả thông báo từ chối chung, không lặp lại PII cho user | Chỉ lưu text đã anonymize và loại entity, không lưu giá trị gốc |
| 2. NeMo input rail | `self check input` trong `guardrails/config.yml`, quyết định theo `result.log.activated_rails` | Chuyển sang RAG | Chặn (`blocked_by=nemo_input`), trả `bot refuse to respond` trong `rails.co` | request id, tên rail đã kích hoạt, latency từng tầng |
| 3. RAG | m1 hierarchical chunking → m5 enrichment → m2 BM25 + bge-m3 (Qdrant) + RRF → m3 bge-reranker-v2-m3 top 3 → generation `gpt-4o-mini` | Có answer `generation_mode=llm` | Không có context: trả “Không tìm thấy”; lỗi LLM: extractive fallback và đánh dấu `generation_mode=extractive_fallback`, `generation_model=null` | Số contexts, mode, model ID provider trả về |
| 4. NeMo output rail | `self check output` | Trả answer nguyên vẹn | Thay answer bằng câu từ chối hoặc bản redact; đặt `flagged_reason` | Lý do chặn, không lưu answer gốc chứa PII |

Nguyên tắc khi guard lỗi: tầng input/output **fail-closed**. Nếu NeMo hoặc provider timeout
hay lỗi, request bị từ chối với thông báo tạm thời thay vì cho đi qua không kiểm tra. Tầng
generation **fail-soft**: dùng extractive fallback, có đánh dấu rõ để monitoring đếm được.

Secrets: `OPENAI_API_KEY`, `GEMINI_API_KEY` chỉ nằm trong `.env` local (đã gitignore). Trong CI
đề xuất dùng repository secrets, không echo ra log. Trước khi commit artifacts, quét `sk-` và
`AIza`; `answers_50q.json` đã quét và không có chuỗi nào.

## Phạm vi và số đo latency

Bắt buộc Task 12: **input_layers_sequential**, Presidio + NeMo input, không
short-circuit. Engines tạo trước đo; có hai warm-up thật không tính vào mẫu.
Percentile nội suy tuyến tính từ raw samples; tổng từ tổng từng sample.

Số mẫu timed: {{n_samples}}; warm-up: {{warmup_runs}};
phương pháp: {{percentile_method}}.

| Layer / scope | P50 ms | P95 ms | P99 ms | Tình trạng |
|---|---|---|---|---|
| Presidio | {{p50}} | {{p95}} | {{p99}} | {{Kết quả đo Task 12}} |
| NeMo input | {{p50}} | {{p95}} | {{p99}} | {{Kết quả đo Task 12}} |
| Input guard sequential | {{p50}} | {{p95}} | {{p99}} | {{Kết quả đo Task 12}} |
| RAG | chưa đo | chưa đo | chưa đo | Ngoài phạm vi bắt buộc |
| NeMo output | chưa đo | chưa đo | chưa đo | Ngoài phạm vi bắt buộc |
| Full guard / short-circuit request | chưa đo | chưa đo | chưa đo | Không suy từ input_guard_ms |

Input-layer budget target: 500ms; kết quả thực tế/budget_ok: {{giá trị và bool}}.
{{Nêu bottleneck nếu vượt target, dựa trên presidio_ms so với nemo_input_ms.}}

Kế hoạch đo phần “chưa đo”:

- **RAG**: bọc `search`, `rerank` và lời gọi generation trong `run_query` bằng
  `time.perf_counter()`, chạy 2 warm-up rồi 50 câu của test set, ghi raw ms từng giai đoạn và
  tính P50/P95/P99 tuyến tính như Task 12. Thời gian wall-clock của `setup_answers` (index
  548.5s, 50 queries 679.6s gồm cả lượt tải reranker đầu tiên) chỉ là quan sát setup, không
  phải số đo percentile.
- **NeMo output**: đo `check_output_rail` trên 4 output cases, lặp đến ≥20 mẫu sau 2 warm-up.
- **Full guard**: đo cả request theo luồng thật (có short-circuit), tách theo nhóm bị chặn ở
  Presidio / NeMo input / đi hết luồng, vì phân phối của từng nhóm khác nhau.

## CI gates đề xuất

- RAGAS faithfulness ≥0.75, avg_score ≥0.65 trên 50 câu.
- Attacks ≥18/20 cho CI đề xuất; clean 8/8 allowed; output cases đúng.
- Full guard P95 <500ms chỉ áp dụng sau khi thực sự đo full guard.

Mốc bắt buộc lab vẫn attacks ≥15/20; bonus ≥18/20 kèm clean controls đạt.

Workflow **chưa triển khai**; repo không có `.github/workflows/`. Đề xuất 3 job:

| Job | Khi chạy | Lệnh | Điều kiện fail |
|---|---|---|---|
| unit | Mỗi PR | `python -m pytest tests/ -q` | pytest exit nonzero (mocks, không gọi API) |
| contract | Mỗi PR | `python scripts/check_lab.py` | checker exit nonzero (schema, provenance, placeholder) |
| eval-live | Thủ công / nightly, có secrets | `python scripts/run_experiments.py --phase a --live`, `--phase b --live`, `--phase c --live --latency-samples 20`, rồi `python scripts/ci_gate.py` | `ci_gate.py` exit 1 khi dưới ngưỡng |

`scripts/ci_gate.py` là script **đề xuất, chưa viết**. Nó sẽ đọc ba JSON và so với
`MIN_FAITHFULNESS=0.75`, `MIN_AVG_SCORE=0.65`, `MIN_ATTACKS_BLOCKED=18`, `MAX_CLEAN_BLOCKED=0`,
in metric nào trượt rồi `sys.exit(1)`. Các biến MIN_* này chưa là quality gate cho đến khi
script tồn tại và được gọi trong CI. Job eval-live có chi phí API nên không chạy trên mỗi PR.
Thêm một bước quét secrets: `grep -rE "sk-|AIza" artifacts/` phải không có kết quả.

## Monitoring và cải tiến

| Metric | Cách lấy | Ngưỡng cảnh báo (đề xuất) | Người xử lý |
|---|---|---|---|
| Tỷ lệ chặn theo tầng (Presidio / NeMo input / NeMo output) | Đếm `blocked_by` theo ngày | Tăng/giảm >2 lần so với tuần trước | Phụ trách guard |
| False positive trên câu sạch | Lấy mẫu ngẫu nhiên request bị chặn để người review hằng tuần | >1/8 trên bộ clean hoặc >5% mẫu review | Phụ trách guard |
| P95 input guard | Raw ms từng tầng như Task 12 | >500ms trong 3 lần đo liên tiếp | Tích hợp |
| Tỷ lệ “Không tìm thấy” | Đếm answers chứa câu này | Baseline hiện tại 9/50; cảnh báo nếu vượt 12/50 | Phụ trách RAG |
| Tỷ lệ extractive fallback | Đếm `generation_mode` | Baseline 0/50; cảnh báo nếu >0 | Tích hợp |
| RAGAS trên 50 câu | Chạy lại Phase A khi đổi corpus/model | faithfulness <0.75 hoặc avg_score <0.65 | Phụ trách eval |

Privacy: log chỉ giữ text đã anonymize bằng Presidio. Không log prompt/answer gốc có PII,
không log API key. Drift: mỗi lần thêm tài liệu vào `data/` phải re-index và chạy lại 50 câu.
Đổi `GENERATION_MODEL` hoặc `JUDGE_MODEL` phải chạy lại Phase A/B trước khi merge.

Giới hạn: bộ 50/20/8/4 nhỏ, mỗi ngưỡng ở trên chỉ là điểm khởi đầu. Một câu sai trong 8 câu
clean đã là 12.5%, nên không dùng các bộ này để kết luận tỷ lệ production.

RAGAS mean/worst distribution: {{giá trị}}.
Cohen’s κ: {{giá trị}}.
Attacks passed: {{số lượng}}/20; clean false_positive_rate: {{giá trị}}.

Cải tiến có thể kiểm tra:

1. OCR hai PDF scan ảnh đang bị bỏ qua (BCTC.pdf, Nghị định 13/2023) rồi chạy lại
   `setup_answers.py --live`; kiểm tra số câu “Không tìm thấy” giảm so với baseline 9/50.
2. Viết `scripts/ci_gate.py` như mục CI gates và chạy thử với ba JSON hiện có; kiểm tra script
   trả exit 1 khi tạm nâng một ngưỡng lên trên giá trị thật.
3. {{Cải tiến từ nhóm lỗi yếu nhất trong failure_clusters.md, kèm cách đo lại.}}
4. {{Cải tiến từ bias_report.md hoặc từ các câu clean/attack sai trong guard_results.json.}}
