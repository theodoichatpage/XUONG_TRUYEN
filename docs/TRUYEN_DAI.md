# Vận hành truyện dài — 0.2.0

## 1. Dàn ý phân cấp

Trong **Dàn ý**, tạo lần lượt:

1. **Tập**: phạm vi lớn, ví dụ chương 1–50.
2. **Tuyến truyện** thuộc tập: xung đột hoặc chặng phát triển, ví dụ chương 1–10.
3. **Kế hoạch chương** thuộc tuyến: một số chương duy nhất, ví dụ chương 1.
4. **Cảnh** thuộc kế hoạch chương: cũng số chương đó; dùng Thứ tự để sắp cảnh.

Có thể tạo **Ghi chú chung** cho các chỉ dẫn áp dụng toàn bộ truyện. Các dàn ý của bản cũ chưa có cấp vẫn được giữ như ghi chú chung; người dùng tự phân loại lại, không có dữ liệu cũ bị xóa.

Server kiểm tra cấp cha, phạm vi bao chứa và liên kết cùng bộ truyện. Không cho đổi phạm vi hoặc cấp dàn ý khiến các con và chương hiện tại trở thành liên kết sai. Cần cập nhật các bản ghi liên quan trước.

## 2. Liên kết chương và chọn ngữ cảnh

Trong **Viết chương → Mở bản thảo**, chọn **Liên kết kế hoạch chương** trùng số chương. Yêu cầu ChatGPT sẽ lấy:

- Ghi chú chung.
- Tập và tuyến cha của kế hoạch đã chọn.
- Kế hoạch chương đó và các cảnh con theo thứ tự.
- Hồ sơ, nhân vật, trí nhớ đã xác nhận trước chương hiện tại.
- Tối đa ba chương trước đã duyệt, ưu tiên tóm tắt còn khớp phiên bản.

Nếu chưa liên kết kế hoạch, phần mềm chọn dàn ý có phạm vi chứa số chương. Khi có các tuyến song song cùng phạm vi, nên liên kết rõ để tránh đưa cả những tuyến không liên quan. Dàn ý là ý định tác giả, không phải bằng chứng sự kiện đã xảy ra.

Đây là chọn ngữ cảnh theo liên kết và phạm vi, chưa phải tìm kiếm ngữ nghĩa hoặc hệ thống tự kiểm tra mọi mâu thuẫn. Hồ sơ và toàn bộ ghi nhớ trước chương vẫn do tác giả quản lý, cần tránh đưa quá nhiều dữ liệu hoặc bí mật tương lai vào các trường sự kiện.

## 3. Tóm tắt theo phiên bản nội dung

Mỗi chương có **phiên bản nội dung** riêng, chỉ tăng khi văn bản chương thay đổi. Đổi trạng thái hoặc ghi chú không làm tăng phiên bản nội dung. Phiên bản lưu bản ghi (`revision`) vẫn dùng riêng cho chống nhận kết quả AI lỗi thời.

Sau khi viết/sửa chương:

1. Điền tóm tắt đã đọc lại theo bản hiện tại.
2. Chọn **Đã đối chiếu và xác nhận** ở trường tóm tắt.
3. Lưu chương.

Tóm tắt chỉ được dùng khi toàn văn nguồn và phiên bản đều khớp. Sửa nội dung sẽ bỏ tóm tắt cũ nếu vẫn giữ nguyên văn tóm tắt; tóm tắt mới chưa xác nhận không dùng cho nối chương. Chưa có tóm tắt hợp lệ thì yêu cầu dùng nguyên văn chương trước thay thế. Tóm tắt cũ chưa có số phiên bản cần được người dùng xác nhận lại.

Lịch sử mới giữ cả phiên bản nội dung và thông tin nguồn tóm tắt tại lúc thay đổi. Không tự sửa các chương đã viết ở phía sau; tác giả cần rà soát các chương phụ thuộc khi sửa một chương cũ.

## 4. Sổ nút thắt

Trong **Trí nhớ & nút thắt**, chọn loại **Nút thắt** và điền:

- Chương ghi nhận/gợi mở.
- Nội dung chi tiết đã xuất hiện, không viết kết quả tương lai như thể đã xảy ra.
- Trạng thái: Đã gợi mở / Đang phát triển / Đã giải quyết / Đã bỏ.
- Mốc dự kiến giải quyết (có thể chưa đặt).
- Nếu Đã giải quyết: bắt buộc ghi chương đã giải quyết và kết quả.
- Chỉ xác nhận khi đã đối chiếu với bản thảo.

Trang Viết chương nhắc nút thắt đến/quá mốc tại số chương sau chương đã duyệt cao nhất. Prompt chương bất kỳ dùng chính số chương đó để kiểm tra mốc. Đây là mốc trong truyện, không phải lịch ngày tháng.

Nút thắt chưa xác nhận không dùng làm trí nhớ hay cảnh báo. Khi viết lại một chương ở trước chương giải quyết, prompt không đưa ghi chú kết quả giải quyết tương lai. Tác giả vẫn phải bảo đảm phần mô tả chung và hồ sơ không tiết lộ kết quả tương lai.

Không tự đánh dấu giải quyết hoặc tự đẩy mốc. Trạng thái Đang phát triển/Đã bỏ chưa có lịch sử chuyển trạng thái theo từng chương; nếu tái viết sâu về quá khứ cần tác giả kiểm tra lại.

## 5. Tương thích và kiểm tra

Giữ `data` khi nâng cấp. Định dạng sao lưu vẫn version 1, các trường mới là phần mở rộng có kiểm tra. Bản cũ không cần chuyển cơ sở dữ liệu và không bị phân loại tự động dựa trên suy đoán.

Không dùng lại ứng dụng cũ để sửa tệp của bản mới, vì bản cũ không hiểu trường phiên bản và dàn ý mới. Trước khi cập nhật nên xuất JSON toàn bộ dữ liệu.
