# Đối chiếu answers thật trước khi xem điểm RAGAS

Nguồn: artifacts/answers_50q.json, được sinh trong commit 34b1bad và đưa vào main
qua commit 4404f72. Đã validate với fixtures/test_set_50q.json: đúng 50 ids,
20 factual / 20 multi_hop / 10 adversarial, không có contexts rỗng. Cả 50 câu có
generation_mode=llm và generation_model=gpt-4o-mini-2024-07-18.

Các nhận xét dưới đây dựa trên answer/contexts/reference thật đã lưu, không phải
điểm RAGAS và không phải danh sách bottom 10. Giữ nguyên dữ liệu để evaluation;
không sửa answers sau khi nhìn thấy lỗi.

## Các nhóm lỗi có bằng chứng nội dung

| Câu | Bằng chứng | Nhận xét nguyên nhân và hướng kiểm chứng |
|---|---|---|
| 9 | Answer nói không tìm thấy; context 1 có sinh con nam giới nghỉ 5 ngày làm việc liên tục | Có thông tin trả lời trong retrieval nhưng generation không sử dụng. Kiểm chứng prompt đọc cả ba contexts và nhận diện cách diễn đạt vợ sinh con/sinh con nam giới |
| 21 | Answer tính đúng 18 ngày phép nhưng không đưa khung lương Senior 20–35 triệu; cả ba contexts là chính sách phép năm | Retrieval chưa đủ hai chủ đề của câu multi-hop. Dùng query decomposition và hợp nhất chunks của phép năm với bảng lương trước generation |
| 22 | Answer lấy Kế toán trưởng từ context tạm ứng; context mua sắm chỉ có hàng dưới 5 triệu, thiếu hàng 5–50 triệu và điều kiện 3 báo giá | Retrieval nhiễu giữa quy trình tạm ứng và mua sắm; generation áp dụng nhầm thẩm quyền. Cần parent-child/table-aware chunks và metadata theo quy trình |
| 24 | Answer tính 300.000; reference là 50.000 cho 5 ngày quá hạn. Context có 2%/tháng và hạn 15 ngày nhưng không chứa quy ước pro-rata 30 ngày/tháng | Retrieval thiếu đoạn công thức, generation tự tính cả tháng. Bổ sung lấy parent quanh công thức, kiểm thử số ngày quá hạn và phép tính theo reference |
| 25 | Answer không tìm thấy; có tỷ lệ 85% nhưng context bảng lương bắt đầu từ Senior, không có hàng Junior | Retrieval thiếu hàng Junior 12–20 triệu, nên chưa đủ căn cứ tính 17 triệu. Không ép model trả đáp án khi thiếu context; sửa chunking bảng trước |
| 29 | Answer tính 160.000 thay vì 80.000 cho 15 ngày quá hạn; context không chứa công thức pro-rata | Tương tự câu 24: thiếu quy ước tính phí và suy luận số sai. Giữ trường hợp để kiểm tra cải tiến retrieval/công thức |
| 32 | Answer không tìm thấy; context 1 nói người mới trong 6 tháng đầu bắt buộc đào tạo, context 2 có thử việc Manager tối đa 90 ngày | Các điều kiện liên quan đã được retrieval; generation không kết hợp tháng thứ 3 với phạm vi 6 tháng. Kiểm thử suy luận điều kiện, không quy tất cả lỗi multi-hop cho retrieval |
| 33 | Answer không tìm thấy; ba contexts chỉ về phép năm, có cả bản cũ/mới, thiếu phụ cấp | Retrieval thiếu chủ đề phụ cấp; phần phép vẫn có thể tính từ context v2024. Hướng sửa là lấy đủ nguồn và trả từng phần có căn cứ, ghi rõ phần thiếu |
| 37 | Answer khẳng định nhân viên không báo cáo dù câu hỏi chỉ nói tự xóa malware và chia sẻ Slack; dùng nhãn Tối mật rộng hơn thông tin đã nêu | Generation bổ sung sự kiện không được câu hỏi hỗ trợ và có nguy cơ khái quát nhãn dữ liệu. Cần tách nghĩa vụ phải báo cáo khỏi kết luận đã không báo cáo |
| 39 | Answer không tìm thấy; contexts thiếu chu kỳ 90/120 ngày và không có toàn bộ yêu cầu v1/MFA v2 | Retrieval chưa đủ cho câu so sánh. Lấy nhiều đoạn theo từng mục của cả hai phiên bản, không chỉ chọn ba đoạn đầu liên quan |
| 41 | Context 1 có phép v2023 là 12 ngày; context 2 nêu v2024 là 15 ngày và thay thế v1; answer vẫn chọn 12 ngày | Bẫy phiên bản đã xuất hiện trong retrieval và thông tin mới cũng có. Generation ưu tiên bản cũ, có thể liên quan thứ tự; chưa thử swap context nên chưa kết luận position bias |
| 44 | Context 2 có đổi mật khẩu 120 ngày, context 3 nói v1 đã thay thế; answer không tìm thấy | Generation bỏ qua căn cứ hiện hành trong context. Kiểm thử yêu cầu ưu tiên phiên bản hiệu lực và trích nguồn |
| 48 | Context 1 ghi nhân viên thử việc chưa được hưởng PVI; answer không tìm thấy | Thông tin phủ định có sẵn nhưng generation không chuyển thành answer. Kiểm thử nhận diện chưa/không, loại trừ và câu trả lời phủ định có căn cứ |
| 50 | Context 1 cấm VPN cá nhân, context 3 bắt buộc WireGuard; answer không tìm thấy | Câu hỏi nghe hợp lý nhưng vi phạm policy; retrieval có bằng chứng cấm. Generation cần xử lý mâu thuẫn giữa giả định người hỏi và quy định |

## Điểm cần lưu ý khi đọc metric

- Faithfulness cao không bảo đảm answer đúng phiên bản hiện hành: câu 41 có
  thể được context v2023 hỗ trợ nhưng vẫn sai reference v2024.
- Một câu không tìm thấy không tự chứng minh retrieval thất bại: câu 9/32/44/48/50
  có thông tin liên quan trong contexts; câu 25/33/39 lại thiếu một số ý quan trọng.
- Sai phép tính có thể đi cùng thiếu công thức trong contexts; cần phân biệt
  thiếu thông tin với việc model không áp dụng thông tin đã có.
- Những case trên chưa khẳng định điểm thấp nhất. Sau live run mới xác định
  bottom 10 và chọn các case đại diện để viết failure_clusters.md.

## Cải tiến có thể kiểm chứng

1. Giữ cả policy cũ và mới trong corpus; thêm metadata phiên bản/hiệu lực và
   yêu cầu generation nêu rõ bản áp dụng. So sánh câu 41/44/49 trước và sau.
2. Chunking giữ hàng và tiêu đề bảng; khi một child là bảng hoặc công thức,
   lấy parent tương ứng. Kiểm thử câu 22/24/25/29.
3. Query decomposition cho câu nhiều chủ đề, retrieval riêng từng ý rồi rerank
   và hợp nhất nguồn. Kiểm thử câu 21/33/39, theo dõi precision để tránh tăng nhiễu.
4. Prompt kiểm tra đủ ý và phủ định trước khi trả không tìm thấy; không thêm
   sự kiện không có trong câu hỏi/context. Kiểm thử câu 9/32/37/48/50.
5. Mọi cải tiến cần sinh answers mới và chạy evaluation mới có hash phù hợp;
   không cập nhật report cũ hoặc tự sửa điểm metric.
