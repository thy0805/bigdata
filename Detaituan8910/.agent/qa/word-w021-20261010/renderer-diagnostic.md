# Kết xuất Word và giới hạn công cụ

Renderer đóng gói render_docx.py đã được thử và không chạy được vì không tìm thấy soffice.exe trong môi trường. Không cài thêm LibreOffice hoặc thay đổi máy để khắc phục.

Theo yêu cầu cập nhật field bằng Microsoft Word, hai bản đã được mở riêng qua Word, cập nhật field và ba mục lục/danh mục, phân trang và xuất PDF nội bộ. PDFium kết xuất ở scale 2 thành 69 PNG mỗi bản; số trang khớp read-back của Word. Đã xem riêng toàn bộ PNG hai bản.

Evidence: word-readback.json, render-pages.json, render/page-001.png đến page-069.png và page-review.md. W01-native.pdf là tên nội bộ của helper xuất, không phải bản Word W01; document trong word-readback.json xác nhận đúng đầu ra W02.1. PDF/PNG và full-text read-back chỉ lưu local, không đưa lên GitHub.

Đã kiểm hiển thị native Word/PDFium; không khẳng định đã kiểm hiển thị trên LibreOffice hoặc mọi renderer bên ngoài. Không chạy lại cập nhật field khi output hash và bằng chứng cuối còn khớp.
