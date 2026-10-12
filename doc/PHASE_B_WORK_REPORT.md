# Báo cáo công việc Phase B — Trần Tuấn Cường

- Nhóm: AnhEm.
- Học viên phụ trách: Trần Tuấn Cường — MSSV 2A202602717.
- Ngày cập nhật: 12/10/2026 (UTC+7).
- Phạm vi: Tasks 5, 6, 7, 8 (LLM-as-Judge & Phân tích Thiên lệch / Bias Analysis, 35 điểm + bonus 3 điểm) trong `src/phase_b_judge.py`, chạy thực nghiệm live và hoàn thiện báo cáo `doc/reports/bias_report.md`.
- Nhánh thực hiện: `phase-b` (PR #2 đã merge, commit mã nguồn `cc0ea2d` và commit thực nghiệm `06c12b6`).

---

## 1. Kết quả đã hoàn thành

1. Đã triển khai hoàn thiện 100% mã nguồn cho Phase B trong `src/phase_b_judge.py`, loại bỏ hoàn toàn các tag `# TODO`, đảm bảo typing và contract chuẩn mực.
2. Vượt qua 100% unit tests offline: `8/8 passed in 0.06s` (`tests/test_phase_b.py`).
3. Chạy thành công thực nghiệm live: `python scripts/run_experiments.py --phase b --live`, sinh file bằng chứng chuẩn `artifacts/judge_results.json` (schema Draft 2020-12, format version 2).
4. Phân tích chi tiết và hoàn thiện toàn bộ báo cáo chuyên sâu `doc/reports/bias_report.md`, không còn bất kỳ placeholder nào.
5. Đạt kết quả thực nghiệm:
   - **Position Bias Rate: 0.0%** (5/5 cặp nhất quán tuyệt đối giữa hai lượt đảo vị trí).
   - **Verbosity Win Rate: 80.0%** (4/5 case dài hơn thắng do bổ sung thông tin cốt lõi; case ID 21 ngắn hơn vẫn thắng áp đảo 1.0 vs 0.4 do đúng trọng tâm vế lương).
   - **Cohen's $\kappa = 0.80$** trên 10 câu calibration đối chiếu với chuyên gia con người (mức Substantial Agreement theo Landis & Koch) $\rightarrow$ **Vượt ngưỡng $\kappa > 0.60$, ĐẠT ĐIỀU KIỆN XÉT THƯỞNG BONUS +3 ĐIỂM**.
6. Submission checker `scripts/check_lab.py`: **PASS** `phase_b_judge.py`, **PASS** `Phase B artifact`, **PASS** `doc/reports/bias_report.md`.

---

## 2. Chi tiết các Task thực hiện

| Task | Tên hàm / Thành phần | Mô tả triển khai | Kết quả kiểm tra |
|---|---|---|---|
| **5** | `pairwise_judge(question, answer_a, answer_b, reference)` | Gọi LLM Judge đánh giá so sánh cặp đôi A/B/tie dựa trên 3 tiêu chí: Tính chính xác (Accuracy), Độ đầy đủ (Completeness), Tính súc tích (Conciseness) dựa trên tài liệu `reference`. Trả về JSON gồm `winner` ("A", "B", hoặc "tie"), `reasoning`, và `scores` (A/B trong [0.0, 1.0]). Tích hợp cơ chế fallback bóc tách tham số khi proxy không hỗ trợ `response_format` / `temperature`, strip markdown fences (````json...````), retry backoff khi rate limit. | Pass unit test mock SDK JSON judge; hoạt động trơn tru trong live runner. |
| **6** | `swap_and_average(question, answer_a, answer_b, reference)` | Chấm 2 lượt độc lập: Lượt 1 (A, B) và Lượt 2 (B, A) để phát hiện và khử Position Bias. Quy đổi phán quyết Lượt 2 về hệ quy chiếu ban đầu (A/B gốc). Chỉ công nhận người thắng cuộc khi cả 2 lượt cùng đồng thuận; nếu mâu thuẫn vị trí thì phân xử "tie" và ghi nhận `position_consistent = False`. Trả về đối tượng `JudgeResult`. | Pass unit test 2 lượt hoán đổi (consistent vs inconsistent swap conversion). |
| **7** | `cohen_kappa(judge_labels, human_labels)` | Cài đặt công thức tính hệ số Cohen's $\kappa = \frac{P_o - P_e}{1 - P_e}$ đo lường mức độ đồng thuận thực tế so với ngẫu nhiên giữa phán quyết Judge (0/1) và nhãn chuyên gia con người (`human_labels_10q.json`). Xử lý an toàn các trường hợp biên ($P_e = 1.0$), kiểm soát chặt chẽ giá trị trong đoạn $[-1.0, 1.0]$. | Pass 3 test cases chuẩn: đồng thuận hoàn toàn ($\kappa=1.0$), đối nghịch hoàn toàn ($\kappa=-1.0$), đồng thuận ngẫu nhiên ($\kappa=0.0$). |
| **8** | `bias_report(judge_results)` | Thu thập danh sách `JudgeResult`, tính toán: `total_judged`, `position_bias_count`, `position_bias_rate`, và `verbosity_bias` (tỷ lệ câu trả lời dài hơn thắng trong các case quyết định). Tự động sinh diễn giải định tính (interpretation). Xử lý an toàn khi đầu vào rỗng. | Pass test bias counts, rates và diễn giải ngữ nghĩa. |

---

## 3. Thực nghiệm Live và Bằng chứng số liệu

Thực nghiệm được thực hiện bằng lệnh chính thức:
```powershell
python scripts/run_experiments.py --phase b --live
```

- Nguồn dữ liệu cố định theo đề bài (không sửa đổi sau khi xem kết quả):
  - **Candidate A:** `artifacts/answers_50q.json:answer` (50 answers do pipeline của nhóm sinh ra, `generation_model = gpt-4o-mini-2024-07-18`).
  - **Candidate B:** `fixtures/human_labels_10q.json:model_answer`.
  - **Reference:** `fixtures/test_set_50q.json:ground_truth`.
  - Cặp Pairwise gồm 5 câu ID: `1, 5, 12, 21, 41`.
  - Calibration gồm 10 câu ID: `1, 5, 12, 21, 23, 29, 33, 41, 46, 50` trên đúng `model_answer` gốc. Tuyệt đối **không** đưa `human_label` hay `human_note` vào prompt.
- Judge Model: `gemini-flash` (kết nối qua WebAI-to-API proxy server tại `http://localhost:6969/v1`).
- Artifact xuất ra: `artifacts/judge_results.json` (Format Version 2, Timestamp `2026-10-12T11:49:46.317796+00:00`).

### 3.1. Kết quả 5 cặp so sánh đối đầu (Pairwise Evaluation)

| ID | Câu hỏi | Candidate A | Candidate B | Pass 1 | Pass 2 (quy về gốc) | Final Winner | Consistent | Scores Pass 1 (A/B) | Scores Pass 2 (A/B) |
|:---:|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | Nghỉ kết hôn bao nhiêu ngày? | 3 ngày làm việc | 3 ngày làm việc có lương | **B** | **B** | **B** | **True** | 0.70 / 0.90 | 0.70 / 0.85 |
| **5** | Mua thiết bị 55 triệu ai duyệt? | Tổng Giám đốc (CEO) | Giám đốc phòng ban | **A** | **A** | **A** | **True** | 1.00 / 0.00 | 1.00 / 0.00 |
| **12** | Thưởng Tết tối thiểu nhân viên $\ge$ 6 tháng? | Thưởng Tết tối thiểu cho nhân viên chính thức từ 6 tháng trở lên là 1 tháng lương | Nhân viên được thưởng Tết tối thiểu 1 tháng lương | **A** | **A** | **A** | **True** | 1.00 / 0.50 | 1.00 / 0.60 |
| **21** | Senior 9 năm thâm niên: số ngày phép và khoảng lương? | 18 ngày phép năm; hưởng lương cho 18 ngày phép | Được nghỉ 18 ngày phép. Lương Senior từ 20 đến 35 triệu | **B** | **B** | **B** | **True** | 0.50 / 1.00 | 0.40 / 1.00 |
| **41** | Nhân viên được nghỉ bao nhiêu ngày phép năm? | 12 ngày phép năm theo chính sách năm 2023 | 12 ngày phép năm | **A** | **A** | **A** | **True** | 0.30 / 0.10 | 0.20 / 0.00 |

- **Position Bias:** 0/5 trường hợp bất đồng vị trí $\rightarrow$ **Tỷ lệ Position Bias = 0.0%**. Cả hai lượt phán quyết hoán đổi đều đồng thuận 100%.
- **Verbosity Bias:** Tỷ lệ câu dài hơn thắng là 4/5 (80.0%) trên 5 case có phân thắng bại (decisive cases).

### 3.2. Kết quả Hiệu chuẩn (Binary Calibration với 10 nhãn Human)

| ID | Câu hỏi | Model Answer gốc | Nhãn Judge (0/1) | Nhãn Human (0/1) | Đồng thuận (Agree) | Lý do phán quyết của Judge |
|:---:|---|---|:---:|:---:|:---:|---|
| **1** | Nghỉ kết hôn bao nhiêu ngày? | 3 ngày làm việc có lương khi kết hôn. | **1** | **1** | **True** | Đúng và đủ theo reference (3 ngày có lương). |
| **5** | Mua thiết bị 55 triệu ai duyệt? | Cần Giám đốc phòng ban phê duyệt. | **0** | **0** | **True** | Sai thẩm quyền (hạn mức > 50 triệu phải là CEO). |
| **12** | Thưởng Tết tối thiểu NV $\ge$ 6 tháng? | Thưởng Tết tối thiểu 1 tháng lương. | **1** | **1** | **True** | Đúng mức thưởng tối thiểu 1 tháng lương. |
| **21** | Senior 9 năm: phép năm và mức lương? | 18 ngày phép. Lương 20 đến 35 triệu. | **1** | **1** | **True** | Đúng cả 2 vế: 18 ngày phép và lương 20–35 triệu. |
| **23** | Khóa học 25tr, nghỉ sau 8 tháng? | Hoàn trả 25 triệu vì chưa đủ 1 năm cam kết. | **1** | **1** | **True** | Đúng số tiền bồi hoàn 100% (25 triệu VNĐ). |
| **29** | Tạm ứng 8tr quá 30 ngày: ai duyệt, phạt? | Trưởng phòng duyệt. Phạt 2% tháng / 8 triệu. | **0** | **0** | **True** | Thiếu Kế toán trưởng duyệt ($\ge$ 5tr) và thiếu tính phạt pro-rata. |
| **33** | Manager 12 năm: phụ cấp và phép năm? | Phép: 19 ngày. Phụ cấp: 1.500.000 VNĐ/tháng. | **1** | **1** | **True** | Đúng cả 2 chỉ số: 19 ngày phép và 1.500.000 VNĐ. |
| **41** | Số ngày phép năm? | Nhân viên được nghỉ 12 ngày phép năm. | **0** | **0** | **True** | Dẫn số liệu chính sách cũ 2023 (12 ngày) đã hết hiệu lực. |
| **46** | Thử việc có được nghỉ phép năm? | Không được nghỉ phép, phải xin nghỉ không lương. | **0** | **1** | **False** | Thiếu điều kiện: nghỉ không lương phải được Trưởng phòng phê duyệt. |
| **50** | Manager dùng NordVPN khi WFH? | Được, miễn đảm bảo kết nối an toàn. | **0** | **0** | **True** | Sai chính sách CNTT: cấm hoàn toàn VPN cá nhân. |

### 3.3. Thống kê Cohen's Kappa ($\kappa$)

- **Tỷ lệ đồng thuận quan sát được (Observed Agreement):**
  $$P_o = \frac{9}{10} = 0.90 \quad (90\%)$$
- **Tỷ lệ đồng thuận ngẫu nhiên kỳ vọng (Chance Agreement):**
  - Phân bố Judge: 5 nhãn 1, 5 nhãn 0.
  - Phân bố Human: 6 nhãn 1, 4 nhãn 0.
  $$P_e = (0.5 \times 0.6) + (0.5 \times 0.4) = 0.30 + 0.20 = 0.50 \quad (50\%)$$
- **Hệ số Cohen's Kappa:**
  $$\kappa = \frac{P_o - P_e}{1 - P_e} = \frac{0.90 - 0.50}{1 - 0.50} = \frac{0.40}{0.50} = \mathbf{0.80}$$
- **Đánh giá:** $\kappa = 0.80$ thuộc mức **Substantial Agreement** (0.61 – 0.80) theo phân loại Landis & Koch (1977), tiệm cận mức Almost Perfect Agreement ($> 0.80$). Vượt mốc $\kappa > 0.60$ theo yêu cầu $\rightarrow$ **Đạt điều kiện nhận Bonus +3 điểm**.

---

## 4. Phân tích chuyên sâu & Ca biên (Edge Cases)

### 4.1. Bản chất của hiện tượng Verbosity Bias trong thực nghiệm
Mặc dù số liệu thống kê ghi nhận tỷ lệ câu dài hơn thắng là 80.0% (4/5 case), phân tích nội dung chứng minh rằng Judge không thiên vị độ dài một cách cơ học:
- **ID 1:** B dài hơn A vì bổ sung thuộc tính pháp lý trọng yếu *"có lương"*.
- **ID 12:** A dài hơn B vì duy trì điều kiện tiền đề *"nhân viên chính thức từ 6 tháng trở lên"*, tránh gây hiểu lầm rằng mọi đối tượng (kể cả dưới 6 tháng) đều được thưởng cả tháng lương.
- **ID 41:** Cả hai câu đều lấy số liệu chính sách cũ 2023 (12 ngày), nhưng A dài hơn vì minh bạch hóa nguồn *"theo chính sách năm 2023"*, giúp người đọc nhận biết ngữ cảnh thời gian.
- **Đặc biệt tại ID 21 (Minh chứng phản biện then chốt):**
  - Candidate B ngắn hơn Candidate A rất nhiều (77 ký tự so với 227 ký tự).
  - Tuy nhiên Candidate B vẫn giành chiến thắng áp đảo (điểm 1.0 vs 0.4–0.5) vì B trả lời đúng cả hai vế (18 ngày phép và khoảng lương 20–35 triệu VNĐ), trong khi Candidate A tuy dài dòng nhưng trả lời sai vế lương (diễn giải thành việc hưởng lương ngày phép).
  - **Kết luận:** Mô hình Judge ưu tiên thông tin chính xác và đầy đủ (Information Density) chứ không ưu tiên độ dài văn bản hình thức.

### 4.2. Phân tích trường hợp bất đồng duy nhất (Question ID 46)
- **Bối cảnh:** Câu hỏi *"Nhân viên thử việc có được nghỉ phép năm không?"*
- **Model Answer:** *"Nhân viên thử việc không được nghỉ phép năm và phải xin nghỉ không lương nếu cần."*
- **Sự khác biệt trong phán quyết:**
  - Chuyên gia con người gán nhãn **1** (chấp nhận) vì đánh giá câu trả lời đã nắm được tinh thần cốt lõi: không có phép năm, phải nghỉ không lương.
  - LLM Judge gán nhãn **0** (từ chối) vì phát hiện thiếu sót điều kiện hành chính bắt buộc trong quy chế: việc nghỉ không lương *"phải được Trưởng phòng phê duyệt"*.
- **Bài học rút ra:** LLM-as-Judge có xu hướng kiểm tra quy chế văn bản với tính khắt khe câu chữ cao hơn con người. Trong hệ thống production, cần thiết lập cơ chế **Human-in-the-loop** đối với các ca biên, điểm số tiệm cận ngưỡng hoặc khi hai lượt hoán đổi không đạt đồng thuận (tie).

---

## 5. Giải pháp Kỹ thuật & Hạ tầng Hỗ trợ (WebAI-to-API)

Trong quá trình triển khai thực nghiệm live, nhóm đối mặt với rào cản hạn ngạch nghiêm ngặt của Google Gemini Free Tier (5 Requests/Phút và tối đa 20 Requests/Ngày dẫn đến lỗi HTTP 429 sau vài lượt gọi). Để giải quyết triệt để vấn đề này mà không vi phạm nguyên tắc bảo mật và quy chế lab:

1. **Thiết lập WebAI-to-API Gateway cục bộ:**
   - Triển khai dịch vụ proxy thông qua Docker container `web_ai_server` tại `127.0.0.1:6969`.
   - Kết nối trực tiếp tài khoản Google Pro của học viên (`__Secure-1PSID`, 48.000+ credits khả dụng).
   - Tối ưu hóa `docker-compose.yml` trên nền tảng Windows với named volume `webai_runtime` và quyền thực thi `user: root`, khắc phục hoàn toàn lỗi phân quyền volume trên Windows NTFS.
   - Đóng gói script tự động `start.bat` và `stop.bat` để phục vụ tái sử dụng lâu dài.
2. **Khả năng phục hồi (Resilience) trong mã nguồn (`src/phase_b_judge.py`):**
   - Do proxy gateway trung gian không hỗ trợ các tham số mở rộng `response_format` và `temperature` (trả về lỗi HTTP 400 `unsupported_parameter`), mã nguồn đã được bổ sung khối try-except để tự động bóc tách các tham số này khi gặp lỗi.
   - Tự động làm sạch định dạng markdown code block (````json ... ````) trước khi parse JSON, đảm bảo quá trình trích xuất kết quả luôn thành công.
   - Cài đặt cơ chế retry tuần tự với exponential backoff khi gặp sự cố đường truyền mạng.

---

## 6. Kiểm chứng đã thực hiện

### 6.1. Kiểm tra Unit Tests offline
```powershell
.venv\Scripts\python.exe -m pytest tests/test_phase_b.py -v
```
**Kết quả:** `8 passed in 0.06s` (Đạt 100% tests của Phase B).

### 6.2. Kiểm tra toàn diện toàn bộ Test Suite của kho mã nguồn
```powershell
.venv\Scripts\python.exe -m pytest tests/ -m "not integration" -q
```
**Kết quả:** `116 passed, 3 deselected in 3.57s` (Tất cả unit tests trong toàn bộ dự án đều vượt qua, không có bất kỳ test nào thất bại).

### 6.3. Kiểm tra Hợp đồng Nộp bài (Submission Checker)
```powershell
.venv\Scripts\python.exe scripts/check_lab.py
```
**Kết quả kiểm tra liên quan đến Phase B:**
- `PASS phase_b_judge.py` (Không còn tag `# TODO`, tuân thủ đúng signature).
- `PASS Phase B artifact` (Hợp lệ JSON schema Draft 2020-12, format_version=2, đầy đủ metadata, hashes xác thực).
- `PASS doc/reports/bias_report.md` (Không còn placeholder, số liệu khớp hoàn toàn với artifact).

---

## 7. Minh chứng Đóng góp Cá nhân & Bàn giao

- **Học viên:** Trần Tuấn Cường — MSSV: 2A202602717.
- **Vai trò:** Phụ trách độc lập toàn bộ Phase B (LLM-as-Judge & Bias Analysis).
- **Danh mục file bàn giao:**
  1. Mã nguồn: [src/phase_b_judge.py](file:///d:/VinAI/K4-L3-DAY24-AnhEm-Eval-Guard/src/phase_b_judge.py) (Tasks 5, 6, 7, 8).
  2. Bằng chứng thực nghiệm: [artifacts/judge_results.json](file:///d:/VinAI/K4-L3-DAY24-AnhEm-Eval-Guard/artifacts/judge_results.json) (5 cặp pairwise, 10 lượt calibration, Cohen's $\kappa = 0.80$).
  3. Báo cáo phân tích: [doc/reports/bias_report.md](file:///d:/VinAI/K4-L3-DAY24-AnhEm-Eval-Guard/doc/reports/bias_report.md).
  4. Báo cáo công việc cá nhân: [doc/PHASE_B_WORK_REPORT.md](file:///d:/VinAI/K4-L3-DAY24-AnhEm-Eval-Guard/doc/PHASE_B_WORK_REPORT.md).
  5. Cập nhật phân công & tự kiểm chứng: [doc/TEAM.md](file:///d:/VinAI/K4-L3-DAY24-AnhEm-Eval-Guard/doc/TEAM.md) (mục `TranTuanCuong-2A202602717`).
- **Cam kết liêm chính học thuật:** Toàn bộ số liệu thực nghiệm được sinh ra từ lượt chạy live thật với mô hình; tuyệt đối không đưa nhãn chuyên gia vào prompt đánh giá; không chỉnh sửa câu trả lời của candidate sau khi xem kết quả đánh giá; tuân thủ đầy đủ quy định sử dụng công cụ AI trợ giúp theo chính sách môn học.
