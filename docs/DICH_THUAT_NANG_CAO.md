# Dịch thuật nâng cao Anh – Trung – Việt — 0.3.0

## Đã tham khảo gì

Ngày 29/10/2026, tham khảo tài liệu repository gốc:

| Dự án | Cách làm học hỏi | Áp dụng trong Xưởng |
|---|---|---|
| [bilingual_book_maker](https://github.com/yihong0618/bilingual_book_maker) | Dịch và đọc đối chiếu theo đoạn, đầu ra song ngữ | Mã đoạn ổn định, bản gốc/dịch cạnh nhau, xuất TXT song ngữ |
| [TranslateBooksWithLLMs – Glossary](https://github.com/hydropix/TranslateBooksWithLLMs/blob/main/docs/GLOSSARY.md) | Thuật ngữ theo từng nhóm, ranh giới từ Latin và chuỗi con cho chữ Hán | Bảng thuật ngữ theo cặp ngôn ngữ, lọc mục liên quan và cảnh báo thiếu cách viết đích |
| [BookLLM](https://github.com/purecodework/bookllm) | Tách dịch, rà soát và chỉnh văn, có thể dùng lượt/mô hình khác kiểm tra | Công việc dịch và công việc rà soát riêng; chỉ sửa bản dịch khi tác giả quyết định |

Chỉ học phương pháp; không nhúng, cài đặt hoặc sao chép mã nguồn các dự án này. BookLLM liệt kê Anh/Trung và một số ngôn ngữ khác, không phải bằng chứng đã kiểm thử tiếng Việt. Việc hỗ trợ Việt trong Xưởng là cấu hình và mã riêng, không kế thừa bảo đảm chất lượng từ dự án nào.

## Nguyên tắc

- Hỗ trợ sáu hướng giữa `en`, `zh`, `vi`. `zh` trong bản này là **Trung giản thể**, chưa có cấu hình phồn thể riêng.
- Vẫn dùng ChatGPT trong trình duyệt bằng sao chép/dán. Không tự gửi yêu cầu, không cần API key, không tự gọi dịch vụ dịch thuật.
- Giữ bản gốc và từng ngôn ngữ đích riêng. Nguồn luôn là chương gốc đã duyệt; không âm thầm dùng bản dịch đích làm nguồn cho chiều dịch khác. Muốn đổi nguồn phải có bản gốc đúng ngôn ngữ đó.
- Chọn ngôn ngữ nguồn đúng với nội dung, không chỉ dựa vào tên bộ truyện. Giá trị mặc định đoán từ trường Ngôn ngữ là tiện ích, không phải nhận dạng ngôn ngữ tự động.

## 1. Cấu hình

Mở **Dịch thuật Anh · Trung · Việt → Ngôn ngữ, thuật ngữ & giọng văn**.

Chọn ngôn ngữ nguồn và đích khác nhau. Điền quy chuẩn từng ngôn ngữ: Anh Mỹ/Anh Anh, ngôi kể, thì, giọng thoại; Trung giản thể, tên phiên âm/dịch nghĩa, danh xưng; Việt với xưng hô, âm Hán–Việt, ngôn ngữ vùng miền. Đây là chỉ dẫn cần tác giả quyết định, không tự suy ra giới tính hay thứ bậc nhân vật.

Bảng thuật ngữ có các cột nguồn, đích, cách viết gốc, cách dịch chuẩn và ghi chú. Một tên có thể có cách dịch khác nhau cho mỗi hướng. Hai dòng cùng nguồn/đích và cùng thuật ngữ nguồn bị từ chối để tránh mâu thuẫn. Không tự đảo chiều bảng thuật ngữ vì một cách dịch không nhất thiết đảo ngược được.

Bảng tiếng Anh cũ vẫn được giữ như chỉ dẫn bổ sung cho đích Anh. Không tự phân tích thành bảng mới; người dùng tự chuyển và giải quyết các mục mâu thuẫn. Thuật ngữ gợi ý/biến thể/ngữ cảnh đặc biệt cần tác giả duyệt trước khi đưa vào bảng.

## 2. Dịch từng nhóm

Duyệt chương gốc trước. Văn bản được chia theo dòng trống thành đoạn `p0001`, `p0002`... Mỗi nhóm tối đa 8 đoạn hoặc khoảng 6.000 ký tự nguồn; không cắt giữa một đoạn. Một đoạn đơn quá dài vẫn nằm nguyên trong một nhóm và có thể vượt giới hạn này, nên tác giả cần ngắt đoạn tự nhiên trước khi dịch nếu ChatGPT không xử lý nổi.

Bấm **Dịch nhóm N**, sao chép yêu cầu và gửi trong ChatGPT. Prompt chứa hướng dịch, giọng văn, thuật ngữ liên quan, hồ sơ khái quát, đoạn nguồn trước và bản dịch trước (nếu có). Nội dung truyện được đánh dấu là dữ liệu, không phải lệnh. Hoàn tất các nhóm dịch trước khi chạy rà soát.

JSON kết quả có dạng:

```json
{"title":"The Key","segments":[{"id":"p0001","target":"Complete paragraph translation.","notes":""}]}
```

Phải có đủ đúng mã đoạn của nhóm, không trùng, không thêm và không bỏ. Trả về thiếu/sai thì không áp dụng nửa kết quả; sửa yêu cầu hoặc gửi lại. Ghi chú mơ hồ cần người đọc xem, không coi chuỗi JSON hợp lệ là chứng nhận dịch đúng.

Bản đã dịch được lưu theo ngôn ngữ đích và có lịch sử; có thể dừng và tiếp tục nhóm khác. Chưa có hàng đợi chạy tự động hoặc đồng bộ extension.

## 3. Rà soát độc lập

Bấm **Rà soát nhóm N** sau khi đã có bản dịch. Gửi yêu cầu bằng một cuộc hội thoại hoặc lượt biên tập riêng nếu muốn giảm thiên kiến tự đánh giá. Phần mềm không xác minh người dùng thực sự dùng mô hình khác.

Báo cáo trả về:

```json
{"complete":true,"issues":[{"pid":"p0001","severity":"major","explanation":"Mô tả lỗi cụ thể bằng tiếng Việt","suggestion":"Target-language correction"}]}
```

Mức độ: critical/major/minor. Nếu chưa kiểm tra đầy đủ phải `complete:false`; Xưởng từ chối coi đây là báo cáo hoàn tất. Báo cáo có mã đoạn ngoài nhóm bị từ chối. Mảng issues rỗng chỉ có nghĩa AI không nêu lỗi, không chứng minh bản dịch hoàn hảo.

Trong **Đối chiếu & biên tập**:

- Đọc bản gốc và bản dịch cạnh nhau theo đoạn.
- Sửa các lỗi được nêu hoặc bác bỏ sau khi kiểm tra; ghi rõ lý do/cách xử lý.
- Sửa tiêu đề, đoạn dịch hoặc ghi chú chương rồi lưu sẽ đưa về Chờ duyệt, bỏ checklist và báo cáo cũ. Cần rà soát lại toàn bộ nhóm trên bản mới.
- Rà soát đầy đủ các nhóm, xử lý mọi vấn đề và hoàn thành 5 mục kiểm tra trước khi duyệt.

Báo cáo gắn với toàn bộ bản dịch tại thời điểm rà soát; việc sửa một đoạn làm các báo cáo còn lại lỗi thời để tránh duyệt nhầm một tổ hợp chưa được kiểm tra.

## 4. Kiểm tra máy và giới hạn

**Chặn:** thiếu tiêu đề, thiếu đoạn đích, sai số/mã/nội dung đoạn nguồn, toàn văn không khớp các đoạn, thiếu báo cáo hiện hành, còn vấn đề chưa xử lý hoặc thiếu checklist khi duyệt.

**Cảnh báo để người dùng xem:** thuật ngữ nguồn có mặt nhưng cách viết đích không thấy; đoạn đích giống nguyên văn; chữ số nguồn không thấy trong bản dịch; đích Anh/Việt còn chữ Hán. Có thể là cảnh báo đúng hoặc tên riêng/cách viết số bằng chữ hợp lệ. Không tự sửa, không tự chấm điểm chất lượng.

Các kiểm tra chưa phát hiện được mọi trường hợp sai nghĩa, thiếu một mệnh đề bên trong đoạn, đổi chủ thể, sai giới tính, xưng hô, tên phiên âm, ẩn dụ hoặc chữ số đã đổi cách viết. Không có COMET/BLEU/LaBSE, không huấn luyện mô hình riêng, không kiểm thử chất lượng văn chương trên bộ truyện thực tế. Dịch ngược chưa được tự động hóa; có thể nhờ AI đối chiếu thủ công nhưng không thay biên tập song ngữ.

## 5. Xuất và tương thích

Xuất bản ngôn ngữ đích TXT hoặc song ngữ TXT chỉ khi bản dịch đã duyệt, nguồn vẫn được duyệt, nguồn/quy chuẩn/thuật ngữ còn khớp và mọi điều kiện rà soát vẫn đạt.

Đổi quy chuẩn mà toàn văn nguồn không đổi: giữ các đoạn dịch để rà soát lại, bỏ dấu duyệt cũ. Nguồn thay đổi: mở khung đoạn mới, giữ bản cũ trong lịch sử khi lưu. Bản Anh từ 0.2 vẫn còn ở trường cũ và được hiển thị để tham khảo trong biên tập đích Anh; chưa tự căn lại vì số đoạn giống nhau cũng không chứng minh căn đoạn đúng.

Dữ liệu mới ở `chapter.translations.en/zh/vi`; cấu hình ở `book.translationConfig`. Định dạng sao lưu vẫn version 1. Giữ thư mục data và xuất JSON trước khi nâng cấp; không dùng lại bản cũ để sửa dữ liệu mới.

## Kiểm tra phát triển

27 kiểm thử JavaScript và 23 kiểm thử Python đạt, gồm sáu hướng ngôn ngữ, từ Latin/chữ Hán, batch, thiếu/trùng đoạn, báo cáo lỗi, điều kiện duyệt, dữ liệu sai và lưu phiên bản. Câu ví dụ đa ngữ trong fixture do lập trình viên cung cấp, dùng kiểm tra dữ liệu/quy trình, không phải đánh giá mô hình dịch thực tế. Chưa nghiệm thu thao tác giao diện Windows hoặc dịch qua tài khoản ChatGPT thật.
