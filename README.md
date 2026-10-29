# Xưởng Truyện — 0.1.0

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
| Dàn ý | Lưu kế hoạch toàn truyện, từng tập và từng chương trong các bản ghi có tiêu đề |
| Viết chương | Ý định chương, bản thảo, tóm tắt, trạng thái và lịch sử thay đổi |
| Trí nhớ & nút thắt | Ghi sự kiện, thời gian, quy tắc và chi tiết gợi mở; xác nhận trước khi dùng làm ngữ cảnh |
| Tiếng Anh & dịch thuật | Bảng thuật ngữ, quy chuẩn Anh ngữ, yêu cầu dịch, đối chiếu và duyệt song ngữ |
| Duyệt & xuất bản | Duyệt chương, xuất TXT, mở Inkstone và ghi link đã đăng |

## Luồng vận hành

Tạo bộ truyện → điền hồ sơ → lập nhân vật và dàn ý → tạo chương → soạn yêu cầu ChatGPT → sao chép và gửi trong ChatGPT → dán kết quả về → chờ duyệt → ghi tóm tắt và trí nhớ đã xác nhận → chương tiếp theo.

Yêu cầu viết chỉ lấy tối đa 3 chương trước đã duyệt, cùng hồ sơ, dàn ý và trí nhớ đã xác nhận trước số chương hiện tại. Đây là ngữ cảnh có cấu trúc, chưa phải tìm kiếm ngữ nghĩa/RAG. Bản AI không ghi đè chương đã duyệt. Có kiểm tra xung đột khi hai tab cùng lưu.

## Tiếng Anh: hai đường sản xuất

- **Viết thẳng tiếng Anh:** đặt ngôn ngữ bộ truyện là English; lập và duyệt dàn ý, rồi tạo từng chương bằng yêu cầu tiếng Anh. Người dùng vẫn duyệt nội dung và ngôn ngữ.
- **Dịch từ tiếng Việt:** duyệt bản gốc trước → nhập bảng thuật ngữ → soạn yêu cầu dịch → nhận JSON → đối chiếu song ngữ → xác nhận 5 mục kiểm tra → xuất bản Anh.

Bản dịch lưu riêng, không thay bản gốc. Khi bản gốc, tiêu đề, bảng thuật ngữ hoặc quy chuẩn thay đổi, bản Anh không được xuất cho tới khi duyệt lại. Đọc [QUY_TRINH_TIENG_ANH.md](docs/QUY_TRINH_TIENG_ANH.md).

## Lưu trữ và sao lưu

Dữ liệu ở `data/xuong-truyen.sqlite3` trên máy. Không xóa thư mục `data` khi cập nhật. Có xuất/nhập JSON toàn bộ dữ liệu; nhập thay thế cần xác nhận. Sao lưu thường xuyên và trước mỗi lần cập nhật. Đây là ứng dụng một người dùng trên máy, chỉ lắng nghe localhost; không đưa server này trực tiếp lên Internet.

## Tình trạng thực tế

**Đã có:** giao diện vận hành, CRUD tạo/sửa các mục, lưu SQLite, sao lưu JSON, bản nháp/lịch sử, chuẩn bị ngữ cảnh ChatGPT, nhận kết quả thủ công, dịch thuật song song và kiểm tra trước xuất TXT.

**Chưa có:** tự động gửi/nhận qua extension, tạo ảnh/bìa, đăng qua API, tài khoản máy chủ, đồng bộ nhiều máy, cron, biên tập viên tiếng Anh tự động hoặc cam kết chất lượng dịch. Gói ChatGPT Plus dùng trong trình duyệt riêng của bạn; phần mềm không sử dụng API trả phí. Extension của Xưởng Nội Dung chưa được tích hợp vào ứng dụng này.

Repository là mã nguồn ứng dụng, không phải đường dẫn web đã triển khai. [Kế hoạch phát triển](docs/KE_HOACH.md).

## Kiểm tra

```sh
node --test tests/core.test.cjs
python -m unittest discover -s tests -p 'test_*.py'
```

Kiểm tra JavaScript cần Node.js; chạy ứng dụng không cần Node.js.
