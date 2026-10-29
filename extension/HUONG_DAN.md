# Xưởng Truyện ChatGPT Bridge — extension 1.0.0

Dùng cùng Xưởng Truyện từ **0.4.0**. Hai số phiên bản khác nhau: ứng dụng 0.4.0, extension 1.0.0. Đây là extension riêng, không phải extension Xưởng Nội Dung hoặc VIDEO IMAGE STUDIO.

## Cài

1. Giải nén `Xuong_Truyen_Bridge_v1.0.0.zip` thành một thư mục riêng; giữ thư mục này sau khi cài.
2. Chrome: mở `chrome://extensions`. Edge: mở `edge://extensions`.
3. Bật Chế độ nhà phát triển → Tải tiện ích đã giải nén → chọn thư mục có `manifest.json`.
4. Mở Xưởng tại `http://127.0.0.1:7872` hoặc `http://localhost:7872`. Mở ChatGPT trong cùng trình duyệt, cùng profile. Tải lại cả hai tab sau khi cài.
5. Mở popup **Xưởng Truyện × ChatGPT**, bấm Tải lại danh sách, chọn đúng hội thoại, bấm Kết nối tab đã chọn.

Chỉ hỗ trợ cổng 7872 và ChatGPT `https://chatgpt.com/`; nếu đổi cổng phải cập nhật và tải lại extension. Firefox không cài trực tiếp bản Manifest V3 này; dùng Chrome/Edge hoặc sao chép/dán thủ công.

## Vận hành

- **Viết chương:** lưu bản nháp → Soạn yêu cầu ChatGPT → Gửi sang ChatGPT.
- **Dịch/rà soát:** mở đúng nhóm tại tab Dịch thuật → Gửi sang ChatGPT.
- Extension điền yêu cầu có mã công việc. Bạn kiểm tra rồi bấm Gửi tại ChatGPT. Không đổi hội thoại hoặc gửi một tin nhắn khác khi đang chờ.
- Kết quả hoàn tất sẽ được nhận về danh sách **Kết nối ChatGPT**. Bấm Áp dụng sau khi xem. Viết chương luôn về Chờ duyệt, bản dịch/rà soát không tự được duyệt.
- Nếu nhận tự động không chạy: bấm **Nhận kết quả hoàn tất** ở bảng nổi trong ChatGPT, rồi **Nhận lại kết quả** ở Xưởng. Vẫn có thể sao chép/dán thủ công.

Chỉ một công việc đang chạy mỗi lần. Không tự chuyển hội thoại, không tự F5 hoặc chạy hàng loạt. Dừng đồng bộ không dừng việc ChatGPT đang tạo câu trả lời; bạn cần bấm Dừng tại ChatGPT nếu muốn.

## An toàn dữ liệu và giới hạn

- Quyền: đọc danh sách tab để chọn tab ChatGPT; lưu công việc/kết quả trong storage của extension; script chỉ hoạt động trên ChatGPT và hai địa chỉ Xưởng cục bộ nêu trên.
- Không đọc cookie, mật khẩu hoặc khóa API, không gọi API mô hình hoặc API nội bộ ChatGPT. Chỉ điền ô nhập và đọc câu trả lời hiển thị trong trang.
- Mã công việc, tab và đường dẫn hội thoại dùng để tránh nhận nhầm; kết quả đã nhận lưu ở extension cho tới khi Xưởng xác nhận đã lưu SQLite. Kết quả ready/applied không nhận thêm bản trùng.
- Tải lại cùng tab có thể tiếp tục công việc đang giữ. Nếu đóng mất tab ChatGPT thì cần dừng, chọn lại tab và gửi yêu cầu mới; không tự khôi phục toàn bộ sau khi đóng trình duyệt.
- Chrome/Edge, Xưởng và ChatGPT phải mở. Giới hạn gói ChatGPT vẫn áp dụng. Cấu trúc giao diện ChatGPT có thể đổi và làm selector không còn khớp; đã có đường sao chép/dán dự phòng.
- Prompt, checkpoint và kết quả là bản thảo riêng tư; tồn tại trong SQLite, bản sao lưu và extension storage. Không công khai các dữ liệu đó lên GitHub.

Chưa kiểm thử extension đã cài trên tài khoản ChatGPT thực tế. Các kiểm thử tự động dùng mô phỏng giao tiếp, lưu trữ và tình huống nhận nhầm; không thay thế nghiệm thu trên Chrome/Edge của bạn.
