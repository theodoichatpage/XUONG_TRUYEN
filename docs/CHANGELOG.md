# Thay đổi

## 0.1.1 — 29/10/2026 — Độ tin cậy trước khi mở rộng

- Viết lại chương bằng AI sẽ bỏ tóm tắt cũ; giữ bản cũ trong lịch sử. Sửa chương thủ công mà giữ nguyên tóm tắt cũng bỏ tóm tắt đó. Chỉ dùng tóm tắt khi nó gắn đúng nội dung chương; tóm tắt cũ chưa có dấu xác nhận nguồn sẽ được thay bằng nội dung chương trong yêu cầu nối tiếp.
- Kiểm tra tệp nhập: mã bản ghi an toàn, mã/số chương không trùng, kiểu dữ liệu trí nhớ, lịch sử chương, bản dịch và checklist. Chặn các khóa prototype. Escape mã bản ghi và tên truyện khi dựng HTML.
- Sửa tiêu đề, nội dung hoặc ghi chú bản Anh: trở về Chờ duyệt, xóa checklist. Lưu bản thay đổi trước, sau đó mở lại và kiểm tra để duyệt. Server cũng áp dụng quy tắc khi ghi dữ liệu thông thường.
- Tự giữ bản đang soạn vào sessionStorage của tab. Nút **Bản đang soạn** mở lại hồ sơ/bản thảo, bản dịch hoặc yêu cầu/kết quả AI. Giữ qua đóng popup và tải lại trang trong cùng tab; không cam kết phục hồi khi đóng hẳn trình duyệt. Tệp bản tạm JSON là bản cứu nội dung, không phải sao lưu toàn bộ ứng dụng.
- Nếu dữ liệu đã đổi từ lúc giữ bản tạm, mở lại để sao chép và đối chiếu; chặn lưu đè trực tiếp. Bản tạm được giữ một bản cho mỗi loại cửa sổ trong tab; mở và nhập một bản mới cùng loại sẽ thay bản tạm loại đó.
- Trước mỗi lần **Nhập sao lưu**, server lưu dữ liệu trước đó vào bảng backups trong cùng transaction SQLite. Sao lưu lỗi hoặc có xung đột thì không thay dữ liệu. Nút **Sao lưu an toàn** cho tải bản trước để nhập lại. Giữ cả thư mục data khi cập nhật; các bản này không bảo vệ khỏi hỏng hoặc mất ổ đĩa, vẫn cần sao lưu ngoài máy.

### Kiểm tra

12 kiểm thử JavaScript cho ngữ cảnh, bản dịch và giữ bản tạm; 11 kiểm thử Python cho kiểm tra dữ liệu, SQLite, rollback, chống ghi đè và HTTP restore/download. Chưa nghiệm thu thao tác giao diện trên Windows.
