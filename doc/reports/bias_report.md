# Đánh giá LLM Judge Phase B

Nhóm: AnhEm

Người phụ trách: Trần Tuấn Cường — 2A202602717

Nguồn: `artifacts/judge_results.json`; run timestamp: 2026-10-12T11:49:46.317796+00:00.
Models generation/judge: generation=['gpt-4o-mini-2024-07-18'], judge=['gemini-flash'].

## Năm cặp A/B và hai lượt

Nguồn cố định: A từ artifacts/answers_50q.json:answer; B từ
fixtures/human_labels_10q.json:model_answer; reference từ fixtures/test_set_50q.json:ground_truth.
Ids: 1, 5, 12, 21, 41. Không đổi nguồn sau khi xem kết quả judge.

| ID | Câu hỏi | Candidate A | Candidate B | Winner Pass 1 | Winner Pass 2 (quy về gốc) | Final Winner | Consistent | Scores Pass 1 (A/B) | Scores Pass 2 (A/B) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Nhân viên được nghỉ bao nhiêu ngày khi kết hôn? | Nhân viên được nghỉ 3 ngày làm việc khi kết hôn. | Nhân viên được nghỉ 3 ngày làm việc có lương khi kết hôn. | B | B | B | True | 0.70 / 0.90 | 0.70 / 0.85 |
| 5 | Muốn mua thiết bị trị giá 55 triệu cần ai phê duyệt? | Cần Tổng Giám đốc (CEO) phê duyệt. | Cần Giám đốc phòng ban phê duyệt. | A | A | A | True | 1.00 / 0.00 | 1.00 / 0.00 |
| 12 | Thưởng Tết tối thiểu cho nhân viên chính thức có từ 6 tháng trở lên là bao nhiêu? | Thưởng Tết tối thiểu cho nhân viên chính thức có từ 6 tháng trở lên là 1 tháng lương. | Nhân viên được thưởng Tết tối thiểu 1 tháng lương. | A | A | A | True | 1.00 / 0.50 | 1.00 / 0.60 |
| 21 | Một nhân viên Senior có 9 năm thâm niên được nghỉ bao nhiêu ngày phép năm và lương trong khoảng nào? | Nhân viên Senior có 9 năm thâm niên được nghỉ tổng cộng **18 ngày phép năm** (15 ngày phép cơ bản + 3 ngày phép cộng thêm cho thâm niên). Lương của nhân viên chính thức được hưởng là có lương cho 18 ngày phép. | Được nghỉ 18 ngày phép (15 cơ bản + 3 thâm niên). Lương Senior từ 20 đến 35 triệu. | B | B | B | True | 0.50 / 1.00 | 0.40 / 1.00 |
| 41 | Nhân viên được nghỉ bao nhiêu ngày phép năm? | Nhân viên chính thức được hưởng **12 ngày phép năm** có lương theo chính sách năm 2023. | Nhân viên được nghỉ 12 ngày phép năm. | A | A | A | True | 0.30 / 0.10 | 0.20 / 0.00 |

Position bias count/rate: 0 case / 0.0% (tất cả 5/5 cặp đều đạt position consistency hoàn hảo giữa hai lượt đảo vị trí).
Verbosity win rate: 0.8 (80.0%); decisive cases: 5 cases (bao gồm 3 case A thắng và A dài hơn: ID 5, 12, 41; 1 case B thắng và B dài hơn: ID 1; 1 case B thắng dù ngắn hơn: ID 21).

### Diễn giải chi tiết về Position Bias và Verbosity Bias
1. **Về Position Bias:** Tỷ lệ inconsistency là 0.0% cho thấy khi áp dụng phương pháp swap-and-average, mô hình judge không bị thiên lệch bởi thứ tự xuất hiện của các phương án trả lời (A hay B). Cả hai lượt đánh giá đều đưa ra kết luận đồng thuận tuyệt đối về bên chiến thắng.
2. **Về Verbosity Bias:** Về mặt số liệu thống kê, tỷ lệ câu dài hơn thắng là 80% (4/5 case). Tuy nhiên, khi phân tích sâu nội dung từng câu trả lời:
   - Ở ID 1, B dài hơn A vì bổ sung thuộc tính cốt lõi 'có lương' được quy định trong chính sách.
   - Ở ID 12, A dài hơn B vì giữ nguyên điều kiện phạm vi 'nhân viên chính thức từ 6 tháng trở lên', giúp câu trả lời chính xác, tránh ngộ nhận cho nhân viên dưới 6 tháng.
   - Ở ID 41, cả hai câu đều dẫn chính sách cũ (12 ngày), nhưng A dài hơn vì chỉ rõ 'theo chính sách năm 2023', giúp người đọc nhận biết ngữ cảnh thời gian.
   - Đặc biệt ở ID 21, Candidate B ngắn hơn Candidate A (77 ký tự so với 227 ký tự) nhưng B vẫn chiến thắng áp đảo (điểm 1.0 so với 0.4 - 0.5) vì B trả lời đúng cả hai vế (phép năm và mức lương 20-35 triệu), trong khi A dài hơn nhưng lạc đề ở vế lương.
   - Do đó, câu trả lời dài hơn thắng trong thực nghiệm này xuất phát từ việc cung cấp thông tin đầy đủ, chính xác hơn chứ không phải do judge ưu tiên độ dài một cách máy móc.

## Calibration đúng model_answer

Helper đánh giá đúng question/model_answer đang có trong fixtures/human_labels_10q.json;
không lấy answer mới của pipeline. Prompt chỉ nhận question, answer, reference.
Không gửi human_label, human_note hoặc phân bố nhãn human vào prompt.

| ID | Câu hỏi | Model Answer gốc | Nhãn Judge (0/1) | Lý do phán quyết của Judge | Nhãn Human (0/1) | Agree |
|---|---|---|---|---|---|---|
| 1 | Nhân viên được nghỉ bao nhiêu ngày khi kết hôn? | Nhân viên được nghỉ 3 ngày làm việc có lương khi kết hôn. | 1 | Hoàn toàn chính xác theo reference, nêu rõ 3 ngày làm việc có lương. | 1 | True |
| 5 | Muốn mua thiết bị trị giá 55 triệu cần ai phê duyệt? | Cần Giám đốc phòng ban phê duyệt. | 0 | Sai thẩm quyền phê duyệt: hạn mức 55 triệu (> 50 triệu) phải do Tổng Giám đốc (CEO) duyệt. | 0 | True |
| 12 | Thưởng Tết tối thiểu cho nhân viên chính thức có từ 6 tháng trở lên là bao nhiêu? | Nhân viên được thưởng Tết tối thiểu 1 tháng lương. | 1 | Đúng mức thưởng Tết tối thiểu 1 tháng lương cho đối tượng thâm niên từ 6 tháng trở lên. | 1 | True |
| 21 | Một nhân viên Senior có 9 năm thâm niên được nghỉ bao nhiêu ngày phép năm và lương trong khoảng nào? | Được nghỉ 18 ngày phép (15 cơ bản + 3 thâm niên). Lương Senior từ 20 đến 35 triệu. | 1 | Tính đúng và đủ cả hai vế: 18 ngày phép năm và khoảng lương 20 đến 35 triệu VNĐ. | 1 | True |
| 23 | Nhân viên được tài trợ khóa học 25 triệu, nghỉ việc sau 8 tháng. Phải hoàn trả bao nhiêu? | Hoàn trả 25 triệu vì chưa đủ 1 năm cam kết. | 1 | Đúng số tiền bồi hoàn 100% (25 triệu) do vi phạm cam kết làm việc dưới 12 tháng. | 1 | True |
| 29 | Nhân viên tạm ứng 8 triệu, chưa thanh toán sau 30 ngày. Ai phê duyệt và phí phạt là bao nhiêu? | Trưởng phòng phê duyệt. Phạt 2% tháng trên 8 triệu. | 0 | Thiếu thẩm quyền Kế toán trưởng (khoản >= 5 triệu) và phạt thiếu tính pro-rata theo ngày quá hạn. | 0 | True |
| 33 | Nhân viên Manager có thâm niên 12 năm: tổng phụ cấp hàng tháng và số ngày phép năm? | Phép: 19 ngày. Phụ cấp: 1.500.000 VNĐ/tháng. | 1 | Tính chính xác cả hai chỉ số: 19 ngày phép (15 + 4) và phụ cấp chức vụ Manager 1.500.000 VNĐ. | 1 | True |
| 41 | Nhân viên được nghỉ bao nhiêu ngày phép năm? | Nhân viên được nghỉ 12 ngày phép năm. | 0 | Dùng số liệu chính sách cũ 2023 (12 ngày) đã hết hiệu lực thay vì chính sách 2024 (15 ngày). | 0 | True |
| 46 | Nhân viên thử việc có được nghỉ phép năm không? | Nhân viên thử việc không được nghỉ phép năm và phải xin nghỉ không lương nếu cần. | 0 | Thiếu điều kiện then chốt theo quy định: việc nghỉ không lương bắt buộc phải được Trưởng phòng phê duyệt. | 1 | False |
| 50 | Nhân viên Manager có thể dùng VPN cá nhân (NordVPN) khi WFH không? | Được, miễn là đảm bảo kết nối an toàn. | 0 | Trả lời sai chính sách CNTT: cấm hoàn toàn VPN cá nhân, bắt buộc dùng VPN WireGuard công ty. | 0 | True |

Cohen’s κ: 0.80 (đạt mức Substantial Agreement theo thang đo Landis-Koch, vượt ngưỡng bonus 0.60).
Observed/chance agreement và diễn giải:
- Tỷ lệ đồng thuận quan sát được (Observed Agreement): P_o = 9/10 = 0.90 (90%).
- Tỷ lệ đồng thuận ngẫu nhiên kỳ vọng (Chance Agreement): Với phân bố Judge gồm 5 nhãn 1 và 5 nhãn 0, Human gồm 6 nhãn 1 và 4 nhãn 0:
  P_e = (5/10 * 6/10) + (5/10 * 4/10) = 0.30 + 0.20 = 0.50.
- Hệ số Cohen's kappa: κ = (P_o - P_e) / (1 - P_e) = (0.90 - 0.50) / (1 - 0.50) = 0.40 / 0.50 = 0.80.

## Giới hạn và cách dùng judge

1. **Phân tích trường hợp bất đồng duy nhất (Question ID 46):**
   - Con người chấm nhãn 1 vì câu trả lời đã nêu đúng ý chính: nhân viên thử việc không có phép năm và phải nghỉ không lương nếu cần.
   - LLM Judge chấm nhãn 0 vì khắt khe hơn: phát hiện thiếu điều kiện ràng buộc thủ tục hành chính là 'phải được Trưởng phòng phê duyệt'.
   - Điều này phản ánh tính chất của LLM Judge: có xu hướng kiểm tra quy chuẩn điều kiện câu chữ nghiêm ngặt hơn so với người đánh giá thông thường.
2. **Giới hạn thực nghiệm:**
   - Tập mẫu hiệu chuẩn (10 câu) và tập pairwise (5 cặp) còn tương đối nhỏ so với quy mô production.
   - Việc phụ thuộc vào prompt đánh giá và nhiệt độ (temperature=0) đảm bảo tính tái lập nhưng vẫn có khả năng sai lệch đối với các trường hợp suy luận đa tầng phức tạp hoặc xung đột chính sách giữa các phiên bản.
   - **Nguồn gốc model judge:** `gemini-flash` là alias của proxy WebAI-to-API chạy local (`http://localhost:6969/v1`, xem `doc/PHASE_B_WORK_REPORT.md`), không phải model ID chính thức của Google API. Nhóm chưa xác minh model và phiên bản thực sự phía sau alias này, nên κ=0.80 và các tỷ lệ bias chỉ gắn với lượt chạy qua proxy đó; đổi sang judge chính thức (ví dụ `gpt-4o-mini` hoặc Gemini API) cần chạy lại Phase B và so sánh.
   - **Thay đổi helper `judge_binary`** (`src/experiment_support.py`): chỉ thêm retry khi gặp 429, bóc khối ```json và fallback bỏ `response_format`/`temperature` nếu endpoint không hỗ trợ. Prompt `BINARY_SYSTEM_PROMPT` và dữ liệu gửi đi (question, model_answer, reference) giữ nguyên; không gửi human_label/human_note. Nếu fallback được kích hoạt thì lượt đó không còn đảm bảo temperature=0.
3. **Khuyến nghị vận hành:**
   - Không nên xem kết quả từ LLM-as-Judge là chân lý tuyệt đối thay thế con người.
   - Cần kết hợp kỹ thuật swap-and-average định kỳ để giám sát position bias.
   - Thiết lập quy trình Human-in-the-loop: tự động chuyển các câu trả lời có độ tin cậy thấp, các trường hợp bất đồng giữa hai lượt judge (tie), hoặc các trường hợp điểm biên sang cho chuyên gia nhân sự/CNTT hậu kiểm.
