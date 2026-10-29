# XUONG_TRUYEN — kho tiêu chuẩn/module phụ cho Xưởng Nội Dung

> **Định vị chính thức:** repository này KHÔNG phải web/phần mềm độc lập cần tiếp tục phát triển. Web sản phẩm là **Xưởng Nội Dung** tại `theodoichatpage/XUONG_NOI_DUNG`. Mã local Python/SQLite và extension cũ được giữ lại làm **tham chiếu/nguồn di trú**, không phải kiến trúc đích.

## Vai trò

XUONG_TRUYEN lưu các tiêu chuẩn vận hành và module đã thử nghiệm để tái sử dụng trong mục **Bộ truyện / Webnovel** của Xưởng Nội Dung:

- Dàn ý phân cấp: **Tập → Tuyến truyện → Kế hoạch chương → Cảnh**.
- Tóm tắt gắn với phiên bản nội dung chương; không dùng tóm tắt cũ sau khi nội dung đổi.
- Trí nhớ và nút thắt có trạng thái, chương gợi mở, mốc dự kiến, chương/kết quả giải quyết.
- Dịch **English ↔ 中文（简体） ↔ Tiếng Việt** theo 6 chiều.
- Bảng thuật ngữ theo cặp ngôn ngữ.
- Chia đoạn có mã, dịch theo nhóm, kiểm tra thiếu/trùng/sai mã đoạn.
- Rà soát độc lập theo nhóm; lỗi phải có lý do và trạng thái xử lý trước khi duyệt.
- Bảo vệ bản đã sửa, lịch sử và sao lưu.
- AI chỉ tạo bản nháp; **không tự đăng truyện khi chưa duyệt**.

## Kiến trúc đích

`XUONG_NOI_DUNG` là nơi duy nhất chứa giao diện sản phẩm và ChatGPT Bridge dùng thực tế. XUONG_TRUYEN không tạo hosting, server hoặc extension mới. Các module ở `web/`, `server.py`, `translation_data.py`, `job_data.py`, `extension/` và `MO_XUONG_TRUYEN.bat` là di sản từ prototype local, giữ nguyên để đối chiếu và nhập dữ liệu cũ.

ChatGPT dùng qua **Xưởng ChatGPT Bridge** của XUONG_NOI_DUNG và tài khoản ChatGPT trên trình duyệt; không bắt buộc API trả phí. Extension `Xuong_Truyen_Bridge_v1.0.0` trong repo này đã **ngừng là extension chính**, chỉ giữ để tham chiếu kiểm thử cũ.

## Tài liệu chuẩn

- `docs/TRUYEN_DAI.md` — quy trình truyện dài, dàn ý, trí nhớ, nút thắt và phiên bản tóm tắt.
- `docs/DICH_THUAT_NANG_CAO.md` — dịch Anh/Trung giản thể/Việt, thuật ngữ, chia nhóm và rà soát.
- `docs/QUY_TRINH_TIENG_ANH.md` — quy trình tiếng Anh cũ, dùng để đối chiếu.
- `docs/KET_NOI_CHATGPT.md` — tài liệu bridge prototype; không phải hướng dẫn cài extension chính hiện tại.
- `tests/` — kiểm thử mô phỏng của các quy tắc/module cũ.

## Di trú dữ liệu local

Không xóa `data/xuong-truyen.sqlite3`. Khi chuyển sang Xưởng Nội Dung:

1. Mở prototype local cũ chỉ để xuất JSON `{ "version": 1, "books": [...] }`.
2. Trên Xưởng Nội Dung mở **Webnovel → Truyện dài & dịch thuật → Nhập dữ liệu local**.
3. Xưởng kiểm tra định dạng, tạo bản sao dữ liệu web trước khi nhập, đối chiếu ID/dấu vân tay để tránh nhập trùng.
4. Dữ liệu local vẫn giữ nguyên; nhập là thao tác sao chép, không phải di chuyển/xóa.

## Nguyên tắc phát triển tiếp

Mọi tính năng sản phẩm mới phải triển khai ở `XUONG_NOI_DUNG`. Chỉ cập nhật repository này khi cần bổ sung tiêu chuẩn, prompt, fixture kiểm thử hoặc tài liệu tham chiếu. Không hồi sinh web `127.0.0.1:7872`, không tạo hosting riêng, không tạo extension thứ hai.

## Mốc tham chiếu

Prototype local hoàn chỉnh gần nhất trước khi đổi kiến trúc: commit `1996ce12e8d5c322fe08bd1921148398bba78836`. Mốc này dùng để đối chiếu, **không dùng để rollback HEAD tương lai**.
