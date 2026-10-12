# Phối hợp Codex và Claude Code: Phase A của Trần Võ Hoàng Nguyên

> Cập nhật: người dùng đã dừng Claude và giao Codex hoàn thiện toàn bộ Phase A.
> Phân công bên dưới là lịch sử phối hợp, không còn là nhiệm vụ đang chờ Claude.
> Codex đã implement src/phase_a_analysis.py và tests/test_phase_a_analysis.py.
> Trạng thái bàn giao hiện tại nằm trong doc/PHASE_A_STATUS.md.

## Mục tiêu và phạm vi

Học viên: Trần Võ Hoàng Nguyên, MSSV 2A202602551, nhóm AnhEm.
Hoàn thiện Tasks 1–4 (30 điểm) và báo cáo failure_clusters của lab Day24.
Codex điều phối phần Phase A và review; Claude Code thực hiện Tasks 3–4.
Đây là phân công giữa hai công cụ hỗ trợ học viên, không thay trưởng nhóm thật
Trần Anh Vũ và không thay phân công Phase B/C của nhóm.

Người dùng sẽ mở Claude Code trong repo này, giao đọc file này và báo Codex
khi Claude hoàn tất. Không cần gửi tin nhắn tự động giữa hai công cụ.

## Đọc trước khi làm

- doc/TEAM.md: phân công thật của nhóm (đã lấy từ origin/docs).
- doc/ASSIGNMENT.md: Phase A, Tasks 1–4.
- doc/RUBRIC.md: Phase A 30 điểm, bonus và các điều kiện mất điểm.
- doc/PIPELINE_INTERFACE.md và doc/REPORT_SCHEMAS.md.
- src/phase_a_ragas.py: RagasResult, RagasEvaluation và exporter đã cung cấp.
- tests/test_phase_a.py: contracts hiện có.
- src/report_contracts.py: validate_phase_a.
- doc/reports/failure_clusters.md: nội dung báo cáo phải có sau live run.

## Quyền sở hữu file khi làm song song

| Người thực hiện | Công việc | File được sửa/tạo |
|---|---|---|
| Codex | Tasks 1–2, wrapper tích hợp Tasks 3–4, tương thích m4, kiểm tra nguồn/metrics, review và live/report khi có dữ liệu | src/phase_a_ragas.py, src/m4_eval.py, config.py (chỉ sửa cấu hình evaluator cần thiết), tests/test_phase_a_adapter.py |
| Claude Code | Tasks 3–4, kiểm thử phân tích, ghi bàn giao | src/phase_a_analysis.py (tạo mới), tests/test_phase_a_analysis.py (tạo mới), doc/PHASE_A_CLAUDE_HANDOFF.md (tạo mới) |

Quan trọng: hai công cụ cùng dùng một working tree. Claude KHÔNG sửa
src/phase_a_ragas.py, m4, config, TEAM, reports hoặc tests có sẵn. Codex sẽ
gọi hai hàm từ module helper do Claude tạo; public API của lab vẫn giữ nguyên.
Không checkout/switch/reset/stash/pull/merge, không commit/push khi chưa có yêu cầu
riêng từ người dùng. Không ghi đè thay đổi local của người khác.
Không làm Phase B/C, không đổi corpus/fixtures/schema/checker hoặc nới tests để pass.

## Giao diện Claude phải implement

Tạo src/phase_a_analysis.py, chỉ dùng Python standard library, không API/model.

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.phase_a_ragas import RagasResult

def bottom_10(results: list[RagasResult]) -> list[dict]:
    ...

def cluster_analysis(results: list[RagasResult]) -> dict:
    ...
```

Nếu cần DIAGNOSTIC_TREE từ phase_a_ragas, import bên trong hàm để tránh circular
import. Không import heavyweight dependencies. Không mutate list hay records đầu vào.

### Task 3: bottom_10 (7 điểm)

- Sort tăng theo RagasResult.avg_score, lấy tối đa 10; dữ liệu 50 câu phải ra 10.
- Bảo toàn thứ tự đầu vào khi điểm bằng nhau (stable sort).
- Mỗi row có rank (1..N), question_id, distribution, question, avg_score,
  worst_metric, diagnosis, suggested_fix.
- worst_metric dùng property của RagasResult; không tự đổi thứ tự tie-break.
- Giữ độ chính xác avg_score, hoặc round 4 chữ số phù hợp tolerance checker.
- diagnosis/fix không rỗng, dựa trên diagnostic tree; nêu là gợi ý chẩn đoán
  nếu chưa đọc answer/contexts/reference, không khẳng định chắc nguyên nhân.
- [] trả []; input ít hơn 10 trả đúng số lượng, không bịa thêm rows.
- Không tạo điểm/answers/context hay sửa chúng để có kết quả đẹp.

### Task 4: cluster_analysis (8 điểm)

- Matrix có đủ 4 keys: faithfulness, answer_relevancy, context_precision,
  context_recall; mỗi key có factual/multi_hop/adversarial, kể cả khi count=0.
- Mỗi result đếm đúng một ô theo result.worst_metric và distribution.
- Đây là thống kê mọi câu, KHÔNG coi mọi câu là failure. Tổng cột của 50 câu
  là 20/20/10 và không phải chỉ số chất lượng.
- distribution_avg_scores: mean của avg_score cho từng nhóm có dữ liệu;
  bỏ nhóm rỗng khỏi mean và việc chọn nhóm yếu, không tự gán chất lượng 0.
- dominant_failure_distribution: nhóm có mean thấp nhất, không chọn count lớn nhất.
- dominant_failure_metric: metric có tổng count theo hàng lớn nhất.
- insight: giải thích được nhóm yếu/mean và metric hay thấp nhất, nêu hướng sửa
  và cần kiểm chứng bằng nội dung. Không kết luận nguyên nhân từ metric đơn lẻ.
- Tie-break deterministic: nhóm theo factual, multi_hop, adversarial;
  metric theo thứ tự DIAGNOSTIC_TREE đang có trong phase_a_ragas.
- [] trả matrix toàn 0, distribution_avg_scores={}, hai dominant fields=None,
  insight giải thích chưa có dữ liệu. Empty output chỉ phục vụ edge case;
  không phải report nộp hợp lệ cho 50 câu.

## Tests Claude cần chạy

Tạo tests/test_phase_a_analysis.py với marker student; test helper trực tiếp.
Kiểm tra sorted/capped/bảo toàn input; matrix tổng counts; nhóm ít câu nhưng
mean thấp nhất; nhóm rỗng không được chọn; empty; tie-break nếu cần.
Giữ tests có sẵn nguyên vẹn. Mock/synthetic inputs chỉ dùng trong tests.

```powershell
python -m pytest tests/test_phase_a_analysis.py -q
python -m pytest tests/test_phase_a.py -k "bottom or cluster or weakest" -q
```

Public wrappers có thể chưa kịp được Codex cập nhật khi Claude bắt đầu;
nếu helper tests pass mà wrapper tests fail, ghi rõ và bàn giao, không tự sửa
file do Codex sở hữu. Không yêu cầu full suite Phase B/C phải pass vì ngoài phạm vi.

## Trạng thái đầu vào và thực nghiệm

Lúc giao việc, artifacts chỉ có .gitkeep, chưa có answers_50q.json.
Trưởng nhóm thật phụ trách sinh answers; Codex theo dõi dependency này.
Claude không sinh mock artifact, không chép ground_truth thành answer,
không chạy live/API hay setup/indexing. Chỉ Codex tích hợp chạy Phase A thật
sau khi 50 answers và evaluator/models/keys đã sẵn sàng, tránh chạy trả phí hai lần.

```powershell
python scripts/run_experiments.py --phase a --live
```

Sau đó Codex hoàn thiện failure_clusters.md từ số đo thật: bảng metrics/means,
10 bottom rows, matrix, đối chiếu nội dung các câu đại diện, hướng sửa và giới hạn.
Bonus +4 nếu adversarial mean < factual mean và có phân tích bẫy; không cố làm
adversarial tệ đi. Unit/mock pass không thay live run.

## Bàn giao của Claude

Ghi doc/PHASE_A_CLAUDE_HANDOFF.md:

1. Files đã tạo, các hàm và quyết định edge/tie cases.
2. Lệnh tests thực sự đã chạy, số pass/fail và lỗi còn lại.
3. Rubric Tasks 3–4 đã đáp ứng thế nào.
4. Giới hạn: chẩn đoán tự động chưa xác nhận nguyên nhân; chưa chạy live.
5. Hạng mục cần Codex review/tích hợp.

Không ghi secrets, không khẳng định toàn lab hoàn thành. Báo người dùng
"Claude đã hoàn thành Tasks 3–4; hãy báo Codex kiểm tra".

## Review Codex sau khi người dùng báo Claude xong

- Đọc diff và helper, kiểm tra không sửa file ngoài phạm vi.
- Chạy tất cả Phase A tests và tests bổ sung hai bên.
- Đối chiếu sorting, nguồn bottom rows, matrix/means, tie-break và insight.
- Chạy support/schema regressions liên quan Phase A.
- Khi có answers thật: chạy live A, validate schema/hash/metadata/counts.
- Hoàn thiện report và mục AI hỗ trợ/INDIVIDUAL của Nguyên bằng bằng chứng thật;
  chưa chạy thì không điền số đo hoặc khai đã làm.
- Bàn giao source, artifact, report và kết quả kiểm tra cho học viên/trưởng nhóm.

## Cập nhật của Codex

Đã giao file này trước khi sửa Tasks 1–2. Kết quả triển khai và tests của Codex
sẽ được cập nhật bên dưới trong phiên này; Claude chỉ đọc file này.

Tasks 1–2 đã implement trong src/phase_a_ragas.py. Public wrappers Tasks 3–4
đã gọi module src.phase_a_analysis mà Claude sẽ tạo; hiện helper chưa có.
Đã bổ sung GEMINI_OPENAI_BASE_URL bị thiếu trong config và metadata evaluator
trong m4; evaluation lỗi sẽ báo lỗi, không trả điểm 0 hoặc danh sách rỗng giả.
Chưa có .env hoặc artifacts/answers_50q.json nên chưa chạy live hay điền report.

Kiểm tra Codex đã chạy:

```powershell
python -m pytest tests/test_phase_a_adapter.py tests/test_phase_a.py -k "not bottom and not cluster and not weakest" -q
```

Kết quả: 20 passed, 4 deselected. Các tests bottom/cluster còn chờ helper của Claude.
