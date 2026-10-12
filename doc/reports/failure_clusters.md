# Phân tích lỗi Phase A

Nhóm: AnhEm
Người phụ trách: Trần Võ Hoàng Nguyên — 2A202602551.

Nguồn: artifacts/ragas_50q.json và artifacts/answers_50q.json.
Run timestamp: 2026-10-12T09:52:54.986101+00:00.
Generation models: gpt-4o-mini-2024-07-18.
Evaluator models: BAAI/bge-m3, ag/gemini-3.8-flash.
Generation modes: LLM 50/50; extractive fallback 0/50.

Bảng và trích xuất bằng chứng được tạo offline từ JSON đã validate. Diagnosis theo metric là giả thuyết; cần đọc các trường hợp bên dưới để xác nhận nguyên nhân.

## Điểm theo distribution

| Metric | factual (20) | multi_hop (20) | adversarial (10) |
|---|---|---|---|
| faithfulness | 0.950000 | 0.585000 | 0.800000 |
| answer_relevancy | 0.897736 | 0.712587 | 0.598653 |
| context_precision | 0.991667 | 0.929167 | 0.900000 |
| context_recall | 0.833333 | 0.612500 | 0.675000 |
| avg_score | 0.918184 | 0.709813 | 0.743413 |

## Bottom 10

| Rank | ID | Question | Distribution | Avg score | Worst metric | Diagnosis | Suggested fix |
|---|---|---|---|---|---|---|---|
| 1 | 33 | Nhân viên Manager có thâm niên 12 năm: tổng phụ cấp hàng tháng và số ngày phép năm theo v2024 là bao nhiêu&#63; | multi_hop | 0.33333333332291665 | faithfulness | Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference. | Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng. |
| 2 | 39 | So sánh yêu cầu mật khẩu giữa policy v1.0 và v2.0 về độ dài tối thiểu, thời hạn đổi và MFA. | multi_hop | 0.3749999999875 | answer_relevancy | Giả thuyết theo metric: Answer doesn't match question. Cần đối chiếu answer, contexts và reference. | Improve prompt template; chạy lại evaluation để kiểm chứng. |
| 3 | 44 | Bao lâu phải đổi mật khẩu một lần&#63; | adversarial | 0.3749999999875 | faithfulness | Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference. | Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng. |
| 4 | 25 | Lương thử việc của nhân viên Junior mức cao nhất là bao nhiêu&#63; | multi_hop | 0.39583333332604165 | answer_relevancy | Giả thuyết theo metric: Answer doesn't match question. Cần đối chiếu answer, contexts và reference. | Improve prompt template; chạy lại evaluation để kiểm chứng. |
| 5 | 48 | Nhân viên thử việc có được hưởng bảo hiểm sức khỏe PVI không&#63; | adversarial | 0.41666666665416663 | faithfulness | Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference. | Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng. |
| 6 | 9 | Nam nhân viên được nghỉ bao nhiêu ngày khi vợ sinh con&#63; | factual | 0.499999999975 | faithfulness | Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference. | Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng. |
| 7 | 32 | Nhân viên mới cấp Manager có thời hạn thử việc 90 ngày, đang trong tháng thứ 3, có BẮT BUỘC tham dự buổi đào tạo nội bộ của phòng ban không&#63; Tại sao&#63; | multi_hop | 0.499999999975 | faithfulness | Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference. | Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng. |
| 8 | 50 | Nhân viên Manager có thể dùng VPN cá nhân (như NordVPN) khi WFH để tăng bảo mật thêm không&#63; | adversarial | 0.624999999975 | answer_relevancy | Giả thuyết theo metric: Answer doesn't match question. Cần đối chiếu answer, contexts và reference. | Improve prompt template; chạy lại evaluation để kiểm chứng. |
| 9 | 37 | Nhân viên tự ý xóa malware khỏi máy và chia sẻ thông tin sự cố này trên Slack nội bộ. Vi phạm những chính sách nào cụ thể&#63; | multi_hop | 0.6415099690187076 | faithfulness | Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference. | Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng. |
| 10 | 22 | Nếu cần mua một chiếc laptop 30 triệu cho nhân viên mới, ai phê duyệt và cần gì từ phòng CNTT&#63; | multi_hop | 0.6699178019334796 | context_recall | Giả thuyết theo metric: Missing relevant chunks. Cần đối chiếu answer, contexts và reference. | Improve chunking or add BM25; chạy lại evaluation để kiểm chứng. |

## Bằng chứng cho từng câu yếu

### Câu 33: Nhân viên Manager có thâm niên 12 năm: tổng phụ cấp hàng tháng và số ngày phép năm theo v2024 là bao nhiêu&#63;

Answer thực tế: Không tìm thấy.

Reference: Phụ cấp tháng: ăn trưa 1.000.000 + điện thoại Manager 500.000 = 1.500.000 VNĐ. Phép năm v2024: 15 ngày cơ bản + 4 ngày thâm niên (12÷3=4) = 19 ngày phép.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc tài liệu nghi_phep_nam_v2024.md, có hiệu lực thay thế phiên bản 1.0 từ ngày 01/01/2023, nói về số ngày phép năm của nhân viên chính thức.

Mỗi nhân viên chính thức được hưởng **15 ngày phép năm** có lương, tăng từ 12 ngày so với chính sách năm 2023. Chính sách này thay thế hoàn toàn phiên bản 1.0 ban hành ngày 01/01/2023.
## Thâm niên công tác
- Context 2: Đoạn văn thuộc tài liệu Chính sách nghỉ phép năm v2023, quy định về số ngày phép năm và cách tính cho nhân viên.

Mỗi nhân viên chính thức được hưởng **12 ngày phép năm** có lương. Số ngày phép được tính theo năm dương lịch từ 01/01 đến 31/12. Nhân viên vào công ty giữa năm sẽ được tính pro-rata theo số tháng làm việc thực tế.
## Thâm niên công tác
- Context 3: Đoạn văn thuộc tài liệu 'nghi_phep_nam_v2024.md' và nói về quy định cộng thêm ngày phép năm theo thâm niên làm việc.

Nhân viên có thâm niên từ **3 năm trở lên** được cộng thêm **1 ngày phép** cho mỗi 3 năm làm việc liên tục. Ví dụ: nhân viên 9 năm thâm niên được 18 ngày phép (15 + 3).
## Quy định sử dụng

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng.

### Câu 39: So sánh yêu cầu mật khẩu giữa policy v1.0 và v2.0 về độ dài tối thiểu, thời hạn đổi và MFA.

Answer thực tế: Không tìm thấy.

Reference: v1.0 (đã hết hiệu lực): tối thiểu 8 ký tự, đổi mỗi 90 ngày, không yêu cầu MFA. v2.0 (hiện hành): tối thiểu 12 ký tự, đổi mỗi 120 ngày, MFA bắt buộc cho tất cả: email, VPN và hệ thống nội bộ.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc Chính sách mật khẩu v1.0, thông báo về việc thay đổi phiên bản chính sách và thời gian hết hiệu lực.

Chính sách này đã được thay thế bởi Chính sách mật khẩu v2.0 từ ngày 01/07/2024. Vui lòng tham khảo phiên bản mới để biết quy định hiện hành.
- Context 2: Đoạn văn thuộc tài liệu mat_khau_v2.md, quy định về yêu cầu và tiêu chuẩn đặt mật khẩu hệ thống.

Mật khẩu phải có tối thiểu **12 ký tự**, bao gồm ít nhất 1 chữ hoa, 1 chữ thường, 1 số và 1 ký tự đặc biệt (!@#$%^&*). Khuyến khích sử dụng passphrase dài hơn 16 ký tự.
## Xác thực đa yếu tố (MFA)
- Context 3: Đoạn văn thuộc Chính sách mật khẩu (Phiên bản 1.0, ngày hiệu lực 01/01/2022) nói về phần yêu cầu mật khẩu và trạng thái đã bị thay thế.

# Chính sách mật khẩu (Phiên bản cũ)
> Phiên bản: 1.0 | Ngày hiệu lực: 01/01/2022 | Phòng ban: CNTT | Trạng thái: ĐÃ THAY THẾ bởi v2.0
## Yêu cầu mật khẩu

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: Answer doesn't match question. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Improve prompt template; chạy lại evaluation để kiểm chứng.

### Câu 44: Bao lâu phải đổi mật khẩu một lần&#63;

Answer thực tế: Không tìm thấy.

Reference: Theo v2.0 HIỆN HÀNH: mỗi 120 ngày. Chính sách v1.0 (đã hết hiệu lực) là 90 ngày. Câu trả lời đúng là 120 ngày.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc tài liệu Quản lý mật khẩu (phiên bản v1), quy định về chu kỳ và điều kiện thay đổi mật khẩu.

Mật khẩu phải được thay đổi **mỗi 90 ngày**. Hệ thống sẽ tự động nhắc nhở trước 7 ngày. Mật khẩu mới không được trùng với 3 mật khẩu gần nhất.
## Lưu ý
- Context 2: Đoạn văn thuộc tài liệu mat_khau_v2.md, nói về chính sách thay thế và quy định bảo mật mật khẩu.

Mật khẩu phải được thay đổi **mỗi 120 ngày**. Hệ thống tự động nhắc nhở trước 14 ngày. Mật khẩu mới không được trùng với 5 mật khẩu gần nhất. Tài khoản bị khóa sau 5 lần nhập sai liên tiếp.
## Chính sách thay thế
- Context 3: Đoạn văn thuộc Chính sách mật khẩu v1.0, thông báo về việc thay đổi phiên bản chính sách và thời gian hết hiệu lực.

Chính sách này đã được thay thế bởi Chính sách mật khẩu v2.0 từ ngày 01/07/2024. Vui lòng tham khảo phiên bản mới để biết quy định hiện hành.

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng.

### Câu 25: Lương thử việc của nhân viên Junior mức cao nhất là bao nhiêu&#63;

Answer thực tế: Không tìm thấy.

Reference: Junior cao nhất là 20.000.000 VNĐ/tháng. Lương thử việc = 85% × 20.000.000 = 17.000.000 VNĐ/tháng.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc tài liệu Bảng lương 2024, nói về chủ đề mức lương thử việc theo các cấp bậc nhân sự.

| Senior (P3-P4) | 20.000.000 - 35.000.000 |
| Lead (P5) | 35.000.000 - 50.000.000 |
| Manager (M1-M2) | 45.000.000 - 70.000.000 |
## Lương thử việc
- Context 2: Đoạn văn thuộc tài liệu quy định về thử việc (thu_viec.md), nói về chế độ lương, phụ cấp và quyền lợi nghỉ phép của nhân viên thử việc.

Nhân viên thử việc được nhận **85% mức lương** của cấp bậc tương ứng theo bảng lương công ty. Phụ cấp ăn trưa được áp dụng đầy đủ từ ngày đầu tiên.
## Quyền lợi trong thử việc
Nhân viên thử việc **KHÔNG được nghỉ phép năm**.
- Context 3: Đoạn văn thuộc tài liệu bang_luong_2024.md nói về chính sách điều chỉnh lương cho nhân viên trong và sau thời gian thử việc.

Nhân viên trong thời gian thử việc được nhận **85% lương** của cấp bậc tương ứng. Sau khi hoàn thành thử việc, lương được điều chỉnh lên 100% kể từ ngày ký hợp đồng chính thức.
## Điều chỉnh lương

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: Answer doesn't match question. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Improve prompt template; chạy lại evaluation để kiểm chứng.

### Câu 48: Nhân viên thử việc có được hưởng bảo hiểm sức khỏe PVI không&#63;

Answer thực tế: Không tìm thấy.

Reference: KHÔNG. Nhân viên thử việc chưa được hưởng gói PVI. Chỉ được tham gia BHXH bắt buộc. Đây là negation trap — pipeline hay nhầm vì tài liệu PVI không đề cập rõ exclusion.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc tài liệu quy định về thử việc, nói về chế độ nghỉ phép và các quyền lợi bảo hiểm của nhân viên thử việc.

Trường hợp cần nghỉ việc riêng, nhân viên thử việc phải xin nghỉ không lương và được trưởng phòng phê duyệt.
Nhân viên thử việc được tham gia bảo hiểm xã hội bắt buộc nhưng chưa được hưởng gói bảo hiểm sức khỏe PVI.
## Đánh giá thử việc
- Context 2: Đoạn văn thuộc tài liệu bảo hiểm sức khỏe, nói về gói bảo hiểm sức khỏe toàn diện và hạn mức chi trả cho nhân viên.

Công ty cung cấp gói bảo hiểm sức khỏe toàn diện qua **PVI Insurance** cho tất cả nhân viên chính thức. Hạn mức bảo hiểm: **200.000.000 VNĐ/năm** bao gồm nội trú, ngoại trú và nha khoa.
## Gói gia đình
- Context 3: Đoạn văn thuộc chính sách bảo hiểm sức khỏe, quy định về thủ tục khám chữa bệnh và thanh toán bồi hoàn bảo hiểm.

Nhân viên xuất trình thẻ bảo hiểm PVI tại các bệnh viện/phòng khám trong danh sách liên kết. Trường hợp khám ngoài danh sách, nhân viên thanh toán trước và nộp hồ sơ bồi hoàn trong vòng 30 ngày. Thời gian xử lý bồi hoàn: 10-15 ngày làm việc.

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng.

### Câu 9: Nam nhân viên được nghỉ bao nhiêu ngày khi vợ sinh con&#63;

Answer thực tế: Không tìm thấy.

Reference: Nam nhân viên được nghỉ 5 ngày làm việc liên tục khi vợ sinh con, không trừ vào phép năm.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc tài liệu quy định về nghỉ phép đặc biệt (nghi_phep_dac_biet.md) và nói về số ngày nghỉ cho các sự kiện gia đình.

- **Tang lễ** (cha mẹ, vợ/chồng, con): 3 ngày làm việc
- **Sinh con** (nam giới): 5 ngày làm việc liên tục
- **Con kết hôn**: 1 ngày làm việc
## Hồ sơ cần thiết
- Context 2: Đoạn văn thuộc tài liệu nghi_phep_nam_v2024.md, có hiệu lực thay thế phiên bản 1.0 từ ngày 01/01/2023, nói về số ngày phép năm của nhân viên chính thức.

Mỗi nhân viên chính thức được hưởng **15 ngày phép năm** có lương, tăng từ 12 ngày so với chính sách năm 2023. Chính sách này thay thế hoàn toàn phiên bản 1.0 ban hành ngày 01/01/2023.
## Thâm niên công tác
- Context 3: Đoạn văn thuộc Chính sách nghỉ phép đặc biệt (phiên bản 1.1, hiệu lực 01/03/2024) quy định về số ngày nghỉ có lương trong trường hợp kết hôn.

# Chính sách nghỉ phép đặc biệt
> Phiên bản: 1.1 | Ngày hiệu lực: 01/03/2024 | Phòng ban: Nhân sự
## Các trường hợp được nghỉ phép đặc biệt
Nhân viên được nghỉ có lương trong các trường hợp sau đây mà không trừ vào phép năm:
- **Kết hôn**: 3 ngày làm việc

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng.

### Câu 32: Nhân viên mới cấp Manager có thời hạn thử việc 90 ngày, đang trong tháng thứ 3, có BẮT BUỘC tham dự buổi đào tạo nội bộ của phòng ban không&#63; Tại sao&#63;

Answer thực tế: Không tìm thấy.

Reference: Có, BẮT BUỘC. Theo chính sách đào tạo nội bộ, nhân viên mới trong 6 tháng đầu phải tham gia tất cả các buổi đào tạo của phòng ban. Nhân viên tháng thứ 3 (đang thử việc) vẫn nằm trong phạm vi 6 tháng đầu.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc tài liệu Đào tạo nội bộ (dao_tao_noi_bo.md) và nói về quy định số lượng buổi đào tạo tối thiểu cũng như đối tượng bắt buộc tham gia.

Mỗi phòng ban phải tổ chức tối thiểu **2 buổi đào tạo/quý** về chuyên môn hoặc kỹ năng mềm. Nhân viên mới (trong 6 tháng đầu) **bắt buộc** tham gia tất cả các buổi đào tạo của phòng ban.
## Ngân sách đào tạo
- Context 2: Đoạn văn thuộc tài liệu quy định về thử việc, nói về thời gian thử việc tiêu chuẩn và cho các vị trí quản lý.

Thời gian thử việc tiêu chuẩn là **60 ngày** kể từ ngày bắt đầu làm việc. Đối với vị trí quản lý cấp cao (Manager trở lên), thời gian thử việc có thể kéo dài đến 90 ngày.
## Lương thử việc
- Context 3: Đoạn văn thuộc tài liệu quy định về thử việc (thu_viec.md), nói về chế độ lương, phụ cấp và quyền lợi nghỉ phép của nhân viên thử việc.

Nhân viên thử việc được nhận **85% mức lương** của cấp bậc tương ứng theo bảng lương công ty. Phụ cấp ăn trưa được áp dụng đầy đủ từ ngày đầu tiên.
## Quyền lợi trong thử việc
Nhân viên thử việc **KHÔNG được nghỉ phép năm**.

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng.

### Câu 50: Nhân viên Manager có thể dùng VPN cá nhân (như NordVPN) khi WFH để tăng bảo mật thêm không&#63;

Answer thực tế: Không tìm thấy.

Reference: KHÔNG. Chính sách VPN v1.3 cấm sử dụng VPN cá nhân (NordVPN, ExpressVPN) trong mạng công ty. Bắt buộc dùng VPN WireGuard của công ty. Đây là policy contradiction trap — câu hỏi nghe hợp lý nhưng vi phạm chính sách.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc tài liệu quy định truy cập vpn_truy_cap.md và nói về các nguyên tắc bảo mật khi sử dụng VPN.

- Ngắt kết nối VPN khi không sử dụng
- Không sử dụng VPN cá nhân (NordVPN, ExpressVPN) trong mạng công ty
- Phiên VPN tự động ngắt sau 12 giờ, cần đăng nhập lại
- Context 2: Đoạn văn thuộc tài liệu 'lam_viec_tu_xa.md', quy định về chế độ làm việc từ xa và các yêu cầu kỹ thuật liên quan.

Nhân viên chính thức được phép làm việc từ xa tối đa **2 ngày/tuần**. Lịch WFH phải được đăng ký và phê duyệt bởi quản lý trực tiếp vào **thứ Hai** đầu tuần.
## Yêu cầu kỹ thuật
- Kết nối **VPN** bắt buộc khi làm việc từ xa
- Context 3: Đoạn văn thuộc tài liệu vpn_truy_cap.md, quy định về việc sử dụng và quản lý tài khoản VPN của công ty.

Công ty sử dụng **WireGuard VPN** với mã hóa xác thực **ChaCha20-Poly1305**. Tất cả kết nối từ xa bắt buộc qua VPN. Nhân viên tải cấu hình VPN từ IT Portal hoặc liên hệ helpdesk@cty.vn.
## Quản lý tài khoản VPN

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: Answer doesn't match question. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Improve prompt template; chạy lại evaluation để kiểm chứng.

### Câu 37: Nhân viên tự ý xóa malware khỏi máy và chia sẻ thông tin sự cố này trên Slack nội bộ. Vi phạm những chính sách nào cụ thể&#63;

Answer thực tế: Nhân viên đã vi phạm các chính sách sau:

1. Không báo cáo sự cố bảo mật trong vòng 1 giờ qua email hoặc hotline CNTT, vi phạm quy định về thời hạn và kênh thông báo khi phát hiện rủi ro an ninh mạng.
2. Tự ý xử lý malware mà không có sự hướng dẫn của đội CNTT, vi phạm quy định không tự ý xử lý sự cố bảo mật.
3. Chia sẻ thông tin sự cố trên các kênh Slack nội bộ, vi phạm nguyên tắc chia sẻ thông tin Tối mật theo chính sách phân loại dữ liệu.

Reference: Vi phạm 2 chính sách: (1) Quy trình xử lý sự cố bảo mật: tuyệt đối không tự xử lý, phải báo cáo trong 1 giờ qua helpdesk@cty.vn — vi phạm này có thể bị kỷ luật đến sa thải. (2) Chính sách phân loại dữ liệu: thông tin sự cố bảo mật thuộc Bí mật/Tối mật, chỉ được chia sẻ theo need-to-know, không chia sẻ rộng rãi.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc tài liệu quy trình bảo mật sự cố, quy định về thời hạn và kênh thông báo khi phát hiện rủi ro an ninh mạng.

Khi phát hiện hoặc nghi ngờ sự cố bảo mật, nhân viên **phải báo cáo trong vòng 1 giờ** qua email **helpdesk@cty.vn** hoặc hotline CNTT nội bộ (ext. 9999). Tuyệt đối **không tự ý xử lý malware** hoặc tìm cách khắc phục mà không có sự hướng dẫn của đội CNTT.
- Context 2: Đoạn văn thuộc chính sách phân loại dữ liệu và bảo mật sự cố, quy định về việc xử lý và bảo vệ thông tin Tối mật.

thông tin liên quan mã nguồn core, bí mật thương mại hoặc kế hoạch M&A thuộc **Tối mật** theo chính sách phân loại dữ liệu.
Chỉ chia sẻ cho người cần xử lý theo nguyên tắc need-to-know, không đăng rộng rãi trên các kênh Slack nội bộ.
## Trách nhiệm
- Context 3: Đoạn văn thuộc quy chế bảo mật, quy định về hình thức kỷ luật khi nhân viên không báo cáo hoặc tự ý xử lý sự cố.

Không báo cáo sự cố hoặc tự ý xử lý sẽ bị xem là vi phạm nghiêm trọng quy chế bảo mật và có thể bị kỷ luật theo mức cảnh cáo hoặc sa thải.

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: LLM hallucinating. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Tighten system prompt, lower temperature; chạy lại evaluation để kiểm chứng.

### Câu 22: Nếu cần mua một chiếc laptop 30 triệu cho nhân viên mới, ai phê duyệt và cần gì từ phòng CNTT&#63;

Answer thực tế: Phê duyệt sẽ cần có sự đồng ý của Kế toán trưởng vì giá trị đơn hàng là 30 triệu VNĐ (trên 5.000.000 VNĐ). Trước khi đề xuất, cần có xác nhận của phòng CNTT về cấu hình kỹ thuật của chiếc laptop.

Reference: Laptop 30 triệu nằm trong khoảng 5-50 triệu nên cần Giám đốc phòng ban (Director) phê duyệt. Cần đính kèm ít nhất 3 báo giá (trên 10 triệu). Mua sắm thiết bị CNTT cần xác nhận cấu hình kỹ thuật từ phòng CNTT trước khi đề xuất.

Contexts đã truy xuất:

- Context 1: Đoạn văn thuộc tài liệu mua sắm thiết bị CNTT (tài liệu mua_sam.md), nói về quy định kỹ thuật và thủ tục cho đơn hàng khẩn cấp.

Mua sắm thiết bị CNTT (laptop, server, phần mềm) cần có xác nhận của phòng CNTT về cấu hình kỹ thuật trước khi đề xuất. Đơn hàng khẩn cấp có thể bỏ qua yêu cầu 3 báo giá nhưng phải có giải trình bằng văn bản.
- Context 2: Đoạn văn thuộc quy định về tạm ứng, trình bày về thẩm quyền phê duyệt các mức tiền tạm ứng khác nhau trong doanh nghiệp.

Tạm ứng dưới 5.000.000 VNĐ: trưởng phòng phê duyệt. Từ 5.000.000 VNĐ trở lên: cần thêm phê duyệt Kế toán trưởng.
- Context 3: Đoạn văn thuộc Quy trình mua sắm (Phiên bản 2.2, hiệu lực từ 01/04/2024) quy định về thẩm quyền phê duyệt đơn hàng.

# Quy trình mua sắm
> Phiên bản: 2.2 | Ngày hiệu lực: 01/04/2024 | Phòng ban: Hành chính & Tài chính
## Thẩm quyền phê duyệt
| Giá trị đơn hàng | Người phê duyệt |
|-------------------|-----------------|
| Dưới **5.000.000 VNĐ** | Trưởng phòng (Manager) |

Giả thuyết cần kiểm chứng: Giả thuyết theo metric: Missing relevant chunks. Cần đối chiếu answer, contexts và reference.
Cải tiến đề xuất: Improve chunking or add BM25; chạy lại evaluation để kiểm chứng.

## Matrix và nhóm yếu nhất

| Worst metric | factual | multi_hop | adversarial |
|---|---|---|---|
| faithfulness | 1 | 10 | 2 |
| answer_relevancy | 12 | 3 | 2 |
| context_precision | 2 | 0 | 1 |
| context_recall | 5 | 7 | 5 |

Nhóm multi_hop có avg_score trung bình thấp nhất (0.7098). context_recall là metric thấp nhất ở 17/50 câu. Matrix thống kê mọi câu, không khẳng định tất cả đều là failures; tổng cột chỉ là số câu. Cần đọc answer/contexts/reference để xác định nguyên nhân. Hướng kiểm chứng: Improve chunking or add BM25.

## Bẫy adversarial, cách cải tiến và giới hạn

Adversarial mean=0.743413; factual mean=0.918184; điều kiện số liệu adversarial < factual: đạt.

Bẫy có sẵn trong corpus gồm phép năm v2023/v2024, mật khẩu v1/v2, phủ định quyền lợi thử việc và việc cấm VPN cá nhân. Cần đối chiếu các contexts đã lấy và answer để phân biệt retrieval sai phiên bản với generation bỏ qua điều kiện. Chênh lệch mean không tự chứng minh pipeline nhận ra version conflict và chưa đủ kết luận bonus.

Nếu context thiếu thông tin, thử chunking/hybrid search/top-k; nếu context nhiễu, thử reranking/metadata phiên bản; nếu context đúng mà answer sai, siết prompt và yêu cầu trích dẫn. Chỉ chọn cải tiến sau khi đọc bằng chứng, chạy lại trên cùng 50 câu, so sánh bốn metric và kiểm tra không làm giảm chất lượng nhóm khác.

Giới hạn: 50 câu, điểm phụ thuộc evaluator/model và generation fallback; worst_metric không phải kết luận nhân quả. Nhận xét nguyên nhân cụ thể đã được đối chiếu ở phần dưới; các đề xuất cải tiến chưa được triển khai/chạy lại trong lần evaluation này. AI hỗ trợ mã và tổng hợp số liệu; không tạo số đo hoặc thay answer bằng ground truth.


## Phân tích nguyên nhân đã đối chiếu từ bằng chứng thật

Bottom 10 gồm ids **33, 39, 44, 25, 48, 9, 32, 50, 37, 22** theo đúng thứ tự JSON.
Có 6 câu multi_hop, 3 adversarial và 1 factual. Bảy câu trả lời nguyên văn
không tìm thấy (33, 39, 44, 25, 48, 9, 32), còn câu 50 cũng là một abstention.
Các diagnosis/fix trong bảng Task 3 ở trên được giữ nguyên từ exporter;
phần sau xác nhận hoặc điều chỉnh giả thuyết bằng nội dung, không sửa số đo JSON.

| Câu | Đối chiếu answer/contexts/reference | Kết luận có bằng chứng và hướng sửa |
|---|---|---|
| 33 | Answer không tìm thấy; contexts chỉ chứa phép năm v2023/v2024 và thâm niên, không có phụ cấp Manager. Faithfulness=0, relevancy=0, recall=0,5 | Retrieval thiếu chủ đề phụ cấp; generation còn bỏ qua phần phép có thể tính từ v2024. Tách query thành phép/phụ cấp, hợp nhất nguồn; trả từng phần có căn cứ và ghi rõ phần thiếu |
| 39 | Answer không tìm thấy; contexts có độ dài v2, trạng thái thay thế và tiêu đề MFA, nhưng thiếu chu kỳ 90/120 ngày, yêu cầu v1 và nội dung MFA. Recall=0, relevancy=0, faithfulness=1 | Retrieval chưa đủ dữ kiện để so sánh. Faithfulness=1 của lời từ chối không chứng minh trả lời tốt. Lấy parent/những đoạn riêng cho từng phiên bản và từng tiêu chí |
| 44 | Answer không tìm thấy; context 2 nêu 120 ngày, context 3 xác nhận v1 đã bị thay thế. Recall=1 nhưng faithfulness=0 và relevancy=0 | Retrieval có thông tin hiện hành; lỗi generation bỏ qua căn cứ và version precedence. Yêu cầu nêu bản hiệu lực và dẫn đoạn chu kỳ 120 ngày |
| 25 | Answer không tìm thấy; contexts có 85% nhưng bảng lương bắt đầu từ Senior, thiếu hàng Junior cao nhất 20 triệu. Recall=0, relevancy=0, faithfulness=1 | Retrieval thiếu hàng Junior; không ép model suy ra 17 triệu khi chưa có căn cứ. Giữ hàng/tiêu đề bảng trong chunk hoặc lấy parent bảng lương |
| 48 | Answer không tìm thấy; context 1 ghi thử việc chưa được hưởng PVI, context 2 dành PVI cho nhân viên chính thức. Faithfulness=0, relevancy=0 | Generation bỏ sót phủ định/điều kiện loại trừ có sẵn. Kiểm thử nhận diện chưa/không và yêu cầu trả lời phủ định với căn cứ |
| 9 | Answer không tìm thấy; context 1 ghi sinh con nam giới 5 ngày làm việc liên tục. Precision=1, recall=1, faithfulness=0, relevancy=0 | Lỗi generation hoặc ánh xạ cách diễn đạt vợ sinh con/sinh con nam giới; không quy lỗi cho retrieval. Prompt cần đọc các bullets về sự kiện gia đình |
| 32 | Answer không tìm thấy; context 1 bắt buộc người mới trong 6 tháng đầu tham dự, context 2 có thử việc Manager tối đa 90 ngày. Precision=1, recall=1 nhưng faithfulness/relevancy=0 | Retrieval đủ các điều kiện; generation không kết hợp tháng thứ 3 với phạm vi 6 tháng. Yêu cầu lập luận điều kiện ngắn và chỉ dùng dữ liệu câu hỏi/context |
| 50 | Answer không tìm thấy; context 1 cấm VPN cá nhân, context 3 có WireGuard. Faithfulness=1, precision=1 nhưng relevancy=0, recall=0,5 | Generation không xử lý giả định nghe hợp lý nhưng trái policy. Đây là bẫy mâu thuẫn; faithfulness cao của abstention không thay thế đánh giá có trả lời đúng câu hỏi không |
| 37 | Answer khẳng định không báo cáo và gọi việc chia sẻ là dữ liệu Tối mật; câu hỏi chỉ nêu tự xóa malware và chia sẻ Slack. Context về Tối mật đang nói mã nguồn/bí mật thương mại/M&A. Faithfulness=0,3333 | Generation thêm sự kiện chưa được nêu và khái quát nhãn dữ liệu. Phải tách nghĩa vụ báo cáo khỏi kết luận đã không báo cáo, dùng đúng phạm vi của mỗi đoạn policy |
| 22 | Answer dùng Kế toán trưởng từ context tạm ứng cho mua laptop 30 triệu. Context mua sắm chỉ có hàng dưới 5 triệu và lưu ý CNTT, thiếu hàng 5–50 triệu. Recall=0,3333, faithfulness=0,5 | Retrieval nhiễu giữa hai quy trình, đồng thời thiếu hàng bảng cần thiết; generation áp dụng nhầm thẩm quyền. Filter theo quy trình và lấy parent đầy đủ của bảng mua sắm |

### Vì sao multi_hop yếu nhất

Multi_hop có mean **0,709813**, faithfulness **0,585** và context_recall
**0,6125**. Trong matrix, 10/20 câu của nhóm có faithfulness là metric thấp nhất,
7/20 có context_recall thấp nhất. Những case 21/22/25/33/39 chứng minh thiếu
nguồn, thiếu hàng bảng hoặc nhiễu chủ đề; câu 32 chứng minh có retrieval đủ nhưng
suy luận/generation thất bại. Vì vậy cần sửa cả retrieval lẫn generation,
không gộp toàn bộ lỗi multi-hop thành lỗi tìm tài liệu.

context_recall là metric thấp nhất ở **17/50** câu toàn bộ bộ test; đây là
thống kê tương đối trong từng câu, không phải 17 failures theo một ngưỡng tuyệt đối.
Tổng cột 20/20/10 chỉ xác nhận số câu, không phải cơ sở chọn nhóm yếu.

### Bẫy phiên bản và điều kiện bonus A

Adversarial mean **0,743413 < factual mean 0,918184**, chênh lệch khoảng
**0,174771**. Điều kiện số liệu bonus +4 đạt trong lần chạy này; các bẫy được
phân tích bằng case thật bên dưới. Quyết định điểm cuối do người chấm xác nhận.

- **Câu 41, ngoài bottom 10:** answer chọn 12 ngày v2023 dù context 2 nêu
  v2024 là 15 ngày và thay thế v1. Faithfulness=1, precision=1, recall=0,3333,
  mean=0,792194. Answer có thể được tài liệu cũ hỗ trợ mà vẫn sai phiên bản
  hiện hành; faithfulness không bảo đảm correctness/version precedence.
  Context cũ đứng đầu là dấu hiệu cần kiểm thử, chưa chạy đảo thứ tự nên chưa
  kết luận nguyên nhân là position bias.
- **Câu 44:** cả chu kỳ cũ 90 ngày và hiện hành 120 ngày có trong contexts,
  nhưng answer từ chối. Cần đọc đoạn thay thế để chọn đúng phiên bản, không
  xóa tài liệu v1 khỏi corpus.
- **Câu 48:** thông tin chưa được hưởng PVI nằm ngay trong context thử việc;
  answer không chuyển điều kiện loại trừ thành câu trả lời phủ định.
- **Câu 50:** đề xuất VPN cá nhân để tăng bảo mật nghe hợp lý nhưng trái câu
  cấm rõ trong policy. Retrieval đúng chưa đủ để generation trả lời đúng.
- **Câu 49, ngoài bottom 10:** answer phân biệt đúng 12 ngày v2023 và 15 ngày
  v2024, nhưng recall chỉ 0,3333 vì reference còn chứa chi tiết thâm niên.
  Cần đọc câu hỏi/reference trước khi diễn giải điểm thấp, tránh coi mọi ý phụ
  trong reference là yêu cầu thiết yếu của người hỏi.

### Cải tiến ưu tiên và cách kiểm chứng

1. Giữ nguyên corpus cũ/mới; thêm metadata hiệu lực, yêu cầu trả lời theo phiên
   bản được hỏi hoặc hiện hành nếu không nêu. Kiểm thử riêng câu 41/44/49 và
   thử đảo thứ tự contexts để kiểm tra mức nhạy với vị trí.
2. Giữ hàng bảng và công thức cùng tiêu đề hoặc lấy parent tương ứng. Kiểm thử
   câu 22/25 và bổ sung lấy đoạn pro-rata của tạm ứng cho câu 24/29.
   Câu 24 trả 300.000 thay vì 50.000; câu 29 trả 160.000 thay vì 80.000.
   Chúng không thuộc bottom 10 nhưng là lỗi nội dung rõ và có faithfulness
   lần lượt 0,3333 và 0,1667.
3. Query decomposition cho câu nhiều chủ đề, retrieval từng ý rồi rerank và
   hợp nhất có giới hạn. Theo dõi cả precision lẫn recall, không chỉ tăng top_k.
4. Prompt kiểm tra đủ ý, phủ định và phạm vi policy trước khi nói không tìm
   thấy; không thêm sự kiện không có trong câu hỏi/context. Kiểm thử 9/32/37/48/50.
5. Khi thử sửa, sinh một bộ answers mới từ pipeline và chạy lại bốn metrics
   trên cùng 50 câu; giữ report cũ làm baseline, dùng source hashes đúng và
   so sánh theo nhóm/case. Các cải tiến trên chưa được chạy thử trong baseline này.

## Điều kiện chạy và giới hạn kết luận

- Windows/Python 3.11.9, virtualenv riêng .venv-phase-a; pip check và import
  RAGAS/datasets/sentence-transformers/PyTorch đã qua. Runtime được pin trong
  requirements/requirements-phase-a.txt; không thay environment Python chung.
- Evaluator LLM dùng model ID cấu hình ag/gemini-3.8-flash qua endpoint người
  dùng cung cấp; embedding local BAAI/bge-m3. Generation của 50 answers đã lưu
  là gpt-4o-mini-2024-07-18, không phải Gemini evaluator.
- RAGAS 0.1.22 chạy bốn metric trên đủ 50 câu, 200 phép đo; answer_relevancy
  strictness=1 do endpoint Gemini không hỗ trợ n>1 trong adapter. Đây là một
  lượt evaluation; chưa đo độ biến thiên giữa các lượt/model/prompt.
- Không có NaN, missing rows hoặc số tự điền; source hashes khớp hai JSON đầu
  vào. Không sinh lại/sửa answers, không xóa policy cũ để làm điểm đẹp.
- Không chạy lại pipeline indexing/generation trên máy này vì đã có answers
  thật từ trưởng nhóm; report đánh giá đúng bộ answers đó.
- Abstention có thể được evaluator cho faithfulness 0 hoặc 1; ví dụ 25/39/50
  có faithfulness=1 nhưng relevancy=0. Vì vậy luôn đọc đồng thời bốn metric
  và nội dung. Bộ 50 câu nhỏ, chưa đủ xác nhận production readiness.
- AI hỗ trợ mã, tests, chạy và tổng hợp/phân tích bằng chứng. Học viên cần đọc,
  giải thích và kiểm chứng nội dung trước khi nộp theo chính sách AI của lớp.
