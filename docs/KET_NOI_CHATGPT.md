# Tích hợp ChatGPT — 0.4.0

Ứng dụng 0.4.0 kết nối extension **Xưởng Truyện Bridge 1.0.0**. Không dùng chung extension của các Studio khác.

## Luồng

Mở yêu cầu viết/dịch/rà soát → lưu job/checkpoint trong SQLite → extension điền prompt vào đúng tab → người dùng bấm Gửi → extension chờ câu trả lời hoàn tất → lưu tạm ở extension → Xưởng lưu kết quả ready → xác nhận nhận → người dùng xem/Áp dụng → kiểm tra nguồn/ngữ cảnh → lưu bản chờ duyệt.

Job được lưu trước khi gửi. Có lỗi sẽ giữ trạng thái và thông báo, không báo hoàn thành giả. Một kết quả chỉ được áp dụng một lần. Viết chương bị chặn nếu đích đã duyệt; các thay đổi bản thảo, nguồn dịch, quy chuẩn hoặc ngữ cảnh liên quan sau khi gửi đều chặn ghi đè.

Trạng thái chính: queued, waiting_send, ready, applied, stopped, error. Trạng thái xử lý ChatGPT chỉ là thông tin bổ sung từ extension, không chứng minh nội dung đã được lưu.

## Các tệp

- `extension/`: Manifest V3, popup chọn tab, content scripts và service worker.
- `web/bridge-core.js`: checkpoint và kiểm tra áp dụng cho ba loại công việc.
- `web/chatgpt-bridge.js`: kết nối trang Xưởng, danh sách job, nhận/áp dụng, dừng và nhận lại.
- `job_data.py`: kiểm tra dữ liệu job khi lưu hoặc nhập sao lưu.
- `web/downloads/Xuong_Truyen_Bridge_v1.0.0.zip`: bản cài extension, tải từ giao diện hoặc GitHub.

Có nút Gửi sang ChatGPT ngay trong Yêu cầu sản xuất. Bản sao chép/dán vẫn hoạt động độc lập khi không cài extension.

## Phạm vi hiện tại

Chỉ viết văn bản, dịch và nhận báo cáo rà soát. Chưa tạo ảnh, tự bấm Gửi, tự F5, đổi tab thay người dùng hoặc tự điều phối nhiều nhóm liên tiếp. Không đưa server localhost lên Internet; không triển khai máy chủ trong bước này.

Hướng dẫn cài, quyền và xử lý sự cố: [extension/HUONG_DAN.md](../extension/HUONG_DAN.md).

## Kiểm tra

47 kiểm thử JavaScript và 26 kiểm thử Python đạt, gồm origin/tab/hội thoại, nhận trùng, ACK sau lưu, dừng, checkpoint viết/dịch/rà soát, chống ghi đè và lưu job qua tải lại dữ liệu. Chưa cài extension và nghiệm thu trên ChatGPT thực tế; selectors cần được xác nhận trên trình duyệt của người dùng.
