# Xưởng Truyện

Web sản xuất truyện dài: ý tưởng → cốt truyện & Story Bible → viết chương (ChatGPT qua Bridge, hoặc Sudowrite qua Adapter) → chấm, sửa → đăng Webnovel.

- Web tĩnh trong `dist/` (Vercel, `vercel.json`), dữ liệu lưu trong trình duyệt.
- `window.XUONG_SITE='story'` trong `dist/index.html` chỉ bật phần Truyện. Mã gốc tách từ XUONG_NOI_DUNG (18/11/2026).
- Extension: `extension/` (ChatGPT Bridge), `extension-publisher/` (Sudowrite Adapter). Đóng gói: `scripts/package-extension.py`, `scripts/package-publisher.py`.
- Test: `node --test tests/*.test.cjs`.

Chuyển dữ liệu từ Xưởng Nội Dung: ở web cũ bấm **Sao lưu dữ liệu**, rồi ở web này mở Cài đặt → Dữ liệu → **Khôi phục dữ liệu** và chọn file vừa tải.
