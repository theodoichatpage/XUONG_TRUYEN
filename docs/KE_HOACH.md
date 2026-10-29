# Cấu trúc vận hành và kế hoạch

## Tham khảo InkOS

Tham khảo README của `Narcooo/inkos` ngày 29/10/2026: tách tác phẩm, hồ sơ/nhân vật, lập kế hoạch, viết, duyệt/sửa, trí nhớ và bản dịch; giữ đầu ra AI ở vùng cần kiểm tra. Không nhúng hoặc sao chép mã InkOS. Bản 0.1.0 là phần triển khai riêng tối giản, không đạt đầy đủ năng lực của InkOS.

## Cấu trúc mã nguồn

- `server.py`: server localhost, SQLite, xác thực yêu cầu ghi bằng token phiên, kiểm tra revision để tránh lưu đè giữa các tab.
- `web/index.html`, `web/style.css`: giao diện tiếng Việt, Arial, bố cục desktop/mobile.
- `web/app.js`: bộ truyện, hồ sơ, nhân vật, kế hoạch, chương, trí nhớ, duyệt và xuất TXT.
- `web/core.js`: tạo ngữ cảnh và tiếp nhận bản nháp AI.
- `web/english.js`: quy chuẩn và bảng thuật ngữ, dịch, đối chiếu, duyệt bản Anh.
- `tests/`: kiểm tra ngữ cảnh, bảo vệ bản đã duyệt, lưu dữ liệu và xung đột.
- `data/`: dữ liệu riêng, luôn loại khỏi Git.

## Mô hình lưu trữ

SQLite lưu snapshot dữ liệu với revision toàn cục. Snapshot gồm `books[]`; mỗi book chứa hồ sơ, `characters[]`, `plans[]`, `chapters[]`, `memories[]`, `glossary` và `englishGuide`. Mỗi chapter giữ số chương, intent, body, summary, status, link, revision, history và bản `english` riêng.

`english` chứa title, body, notes, sourceBody, sourceTitle, glossary, guide, checks, status, history. Các snapshot gốc cho biết khi nào cần duyệt lại. Bản này chưa dùng cơ sở dữ liệu quan hệ chuẩn hóa hay tìm kiếm vector; nếu mở rộng nhiều tác phẩm lớn cần đo và chuyển kiến trúc có migration.

## Thứ tự tiếp theo

1. Nghiệm thu chạy Windows và thao tác lưu/khôi phục dữ liệu thực.
2. Tích hợp extension ChatGPT với mã công việc, khóa tab hội thoại, retry và chống ghi đè; không dùng API key.
3. Tự chuẩn bị yêu cầu rà soát độc lập và nhận danh sách lỗi; vẫn cần người duyệt.
4. Dàn ý phân cấp rõ tập/tuyến/cảnh, đồ thị nhân vật, sổ nút thắt có mốc giải quyết và tìm ngữ cảnh liên quan.
5. Tạo bìa, theo dõi lịch đăng và số liệu thực; nghiên cứu triển khai máy chủ có đăng nhập nếu cần dùng nhiều máy.

Không có cron viết lúc máy tắt, không tự đăng Webnovel và không tự kết nối tài khoản ngân hàng.
