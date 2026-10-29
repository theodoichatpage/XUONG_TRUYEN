# Thay đổi

## 0.3.0 — 29/10/2026 — Dịch thuật nâng cao

- Sáu hướng Anh/Trung giản thể/Việt; lưu mỗi ngôn ngữ đích riêng.
- Thuật ngữ có bảng nhập theo cặp ngôn ngữ, cảnh báo từ Latin/chữ Hán và số liệu.
- Dịch theo nhóm có mã đoạn, từ chối thiếu/trùng/sai đoạn, đọc đối chiếu cạnh nhau.
- Rà soát độc lập theo nhóm, xử lý lỗi có lý do, báo cáo gắn với bản dịch; thay nội dung phải rà soát lại.
- Xuất TXT đơn ngữ/song ngữ sau duyệt; giữ bản Anh cũ để tham khảo.
- 50 kiểm thử đạt. Chưa nghiệm thu giao diện Windows hoặc dịch với ChatGPT thật. [Hướng dẫn và nguồn tham khảo](DICH_THUAT_NANG_CAO.md).

## 0.2.0 — 29/10/2026 — Truyện dài

- Dàn ý phân cấp Tập → Tuyến truyện → Kế hoạch chương → Cảnh; kiểm tra cấp cha, phạm vi và liên kết chương. Giữ dàn ý cũ như ghi chú chung.
- Yêu cầu viết chọn tập/tuyến/cảnh liên quan theo chương; chưa liên kết thì dùng phạm vi chương.
- Tóm tắt có phiên bản nội dung riêng và xác nhận nguồn, bỏ dùng khi lỗi thời.
- Nút thắt có trạng thái, mốc dự kiến, chương giải quyết và ghi chú kết quả. Cảnh báo đến/quá mốc; không tự giải quyết.
- Khi viết chương cũ, không đưa ghi chú giải quyết xảy ra ở chương tương lai vào prompt.
- 17 kiểm thử JavaScript và 16 kiểm thử Python đạt. Chưa nghiệm thu giao diện Windows.
- Hướng dẫn: [TRUYEN_DAI.md](TRUYEN_DAI.md).

## 0.1.1 — 29/10/2026 — Độ tin cậy trước khi mở rộng

- Viết lại chương bằng AI sẽ bỏ tóm tắt cũ; giữ bản cũ trong lịch sử. Sửa chương thủ công mà giữ nguyên tóm tắt cũng bỏ tóm tắt đó. Chỉ dùng tóm tắt khi nó gắn đúng nội dung chương; tóm tắt cũ chưa có dấu xác nhận nguồn sẽ được thay bằng nội dung chương trong yêu cầu nối tiếp.
- Kiểm tra tệp nhập: mã bản ghi an toàn, mã/số chương không trùng, kiểu dữ liệu trí nhớ, lịch sử chương, bản dịch và checklist. Chặn các khóa prototype. Escape mã bản ghi và tên truyện khi dựng HTML.
- Sửa tiêu đề, nội dung hoặc ghi chú bản Anh: trở về Chờ duyệt, xóa checklist. Lưu bản thay đổi trước, sau đó mở lại và kiểm tra để duyệt. Server cũng áp dụng quy tắc khi ghi dữ liệu thông thường.
- Tự giữ bản đang soạn vào sessionStorage của tab. Nút **Bản đang soạn** mở lại hồ sơ/bản thảo, bản dịch hoặc yêu cầu/kết quả AI. Giữ qua đóng popup và tải lại trang trong cùng tab; không cam kết phục hồi khi đóng hẳn trình duyệt. Tệp bản tạm JSON là bản cứu nội dung, không phải sao lưu toàn bộ ứng dụng.
- Nếu dữ liệu đã đổi từ lúc giữ bản tạm, mở lại để sao chép và đối chiếu; chặn lưu đè trực tiếp. Bản tạm được giữ một bản cho mỗi loại cửa sổ trong tab; mở và nhập một bản mới cùng loại sẽ thay bản tạm loại đó.
- Trước mỗi lần **Nhập sao lưu**, server lưu dữ liệu trước đó vào bảng backups trong cùng transaction SQLite. Sao lưu lỗi hoặc có xung đột thì không thay dữ liệu. Nút **Sao lưu an toàn** cho tải bản trước để nhập lại. Giữ cả thư mục data khi cập nhật; các bản này không bảo vệ khỏi hỏng hoặc mất ổ đĩa, vẫn cần sao lưu ngoài máy.

### Kiểm tra

12 kiểm thử JavaScript cho ngữ cảnh, bản dịch và giữ bản tạm; 11 kiểm thử Python cho kiểm tra dữ liệu, SQLite, rollback, chống ghi đè và HTTP restore/download. Chưa nghiệm thu thao tác giao diện trên Windows.
