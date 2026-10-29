# Xưởng Truyện — 0.3.0

Ứng dụng tiếng Việt để quản lý và sản xuất truyện dài kỳ, hướng tới đăng tiếng Anh trên Webnovel. Tham khảo **cách phân chia công việc** của [InkOS](https://github.com/Narcooo/inkos), phần triển khai trong repository này được viết riêng; không sao chép mã nguồn, thương hiệu hay prompt InkOS.

## Chạy trên Windows

1. Cài Python 3.10 trở lên từ python.org nếu máy chưa có.
2. Tải repository bằng **Code → Download ZIP**, giải nén.
3. Chạy **MO_XUONG_TRUYEN.bat**. Trình duyệt mở tại `http://127.0.0.1:7872`.
4. Giữ cửa sổ chạy chương trình; đóng cửa sổ để dừng.

Không cần npm, API key hoặc dịch vụ cơ sở dữ liệu. Chạy từ terminal: `python server.py`.

## Các khu vực vận hành

| Khu vực | Công việc |
|---|---|
| Thư viện truyện | Tạo và chọn bộ truyện; thống kê số chương, số chương chờ duyệt |
| Hồ sơ truyện | Tiền đề, thể loại, ngôn ngữ, giọng văn, thế giới, quy tắc, độc quyền |
| Nhân vật | Vai trò, mục tiêu, tính cách, quan hệ và chi tiết cần nhất quán |
| Dàn ý | Cây Tập → Tuyến truyện → Kế hoạch chương → Cảnh, phạm vi và liên kết chương |
| Viết chương | Ý định chương, bản thảo, tóm tắt, trạng thái và lịch sử thay đổi |
| Trí nhớ & nút thắt | Sự kiện và nút thắt có trạng thái, chương gợi mở, mốc giải quyết và cảnh báo quá mốc |
| Dịch thuật Anh · Trung · Việt | Sáu hướng dịch, bảng thuật ngữ theo cặp, đối chiếu theo đoạn, rà soát độc lập, duyệt và xuất song ngữ |
| Duyệt & xuất bản | Duyệt chương, xuất TXT, mở Inkstone và ghi link đã đăng |

## Luồng vận hành

Tạo bộ truyện → điền hồ sơ → lập nhân vật và dàn ý → tạo chương → soạn yêu cầu ChatGPT → sao chép và gửi trong ChatGPT → dán kết quả về → chờ duyệt → ghi tóm tắt và trí nhớ đã xác nhận → chương tiếp theo.

Yêu cầu viết chọn dàn ý liên quan theo liên kết chương, lấy tối đa 3 chương trước đã duyệt và chỉ dùng tóm tắt khớp phiên bản nội dung. Trí nhớ lấy các mục đã xác nhận trước chương hiện tại. Xem [hướng dẫn truyện dài](docs/TRUYEN_DAI.md). Đây là ngữ cảnh có cấu trúc, chưa phải tìm kiếm ngữ nghĩa/RAG. Bản AI không ghi đè chương đã duyệt. Có kiểm tra xung đột khi hai tab cùng lưu.

## Dịch thuật Anh – Trung – Việt

Chọn ngôn ngữ nguồn/đích và giọng văn, duyệt thuật ngữ → dịch lần lượt các nhóm đoạn → rà soát từng nhóm bằng lượt AI riêng → đối chiếu song ngữ, sửa và xử lý lỗi → duyệt → xuất TXT đơn ngữ/song ngữ. Hỗ trợ Trung giản thể; không dịch tự động qua API.

Bản gốc và mỗi ngôn ngữ đích lưu riêng. Nguồn, quy chuẩn hoặc thuật ngữ đổi thì phải rà soát lại. Xem [hướng dẫn dịch nâng cao và các dự án tham khảo](docs/DICH_THUAT_NANG_CAO.md).

## Lưu trữ và sao lưu

Dữ liệu ở `data/xuong-truyen.sqlite3` trên máy. Không xóa thư mục `data` khi cập nhật. Có xuất/nhập JSON toàn bộ dữ liệu; nhập thay thế cần xác nhận. Sao lưu thường xuyên và trước mỗi lần cập nhật. Trước mỗi lần nhập JSON, ứng dụng tự giữ dữ liệu cũ; mở **Sao lưu an toàn** để tải lại bản trước. Nút **Bản đang soạn** giữ nội dung qua đóng popup hoặc tải lại cùng tab. Xem [thay đổi và giới hạn](docs/CHANGELOG.md). Đây là ứng dụng một người dùng trên máy, chỉ lắng nghe localhost; không đưa server này trực tiếp lên Internet.

## Tình trạng thực tế

**Đã có:** giao diện vận hành, CRUD tạo/sửa các mục, lưu SQLite, sao lưu JSON, bản nháp/lịch sử, chuẩn bị ngữ cảnh ChatGPT, nhận kết quả thủ công, dịch thuật song song và kiểm tra trước xuất TXT.

**Chưa có:** tự động gửi/nhận qua extension, tạo ảnh/bìa, đăng qua API, tài khoản máy chủ, đồng bộ nhiều máy, cron, mô hình biên tập tự chạy hoặc cam kết chất lượng dịch. Gói ChatGPT Plus dùng trong trình duyệt riêng của bạn; phần mềm không sử dụng API trả phí. Extension của Xưởng Nội Dung chưa được tích hợp vào ứng dụng này.

Repository là mã nguồn ứng dụng, không phải đường dẫn web đã triển khai. [Kế hoạch phát triển](docs/KE_HOACH.md).

## Kiểm tra

```sh
node --test tests/*.test.cjs
python -m unittest discover -s tests -p 'test_*.py'
```

Kiểm tra JavaScript cần Node.js; chạy ứng dụng không cần Node.js.
