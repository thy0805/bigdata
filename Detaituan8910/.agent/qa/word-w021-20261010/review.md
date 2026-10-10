# Bàn giao W02.1

VERIFIED kỹ thuật; **chờ Thy/GPT Web nghiệm thu**, không tự khóa Word.

File gửi trực tiếp: `D:\Hoctap\bigdata\Detaituan8910\BaoCao_PhanTich_DuDoan_DienNang_UCI_W02_1_v1_20261010.docx`

SHA-256: `db0cf6ef43ae2887e76ebf10711c3bd425961b00b940f99f0963e16df2223788`. Số trang Microsoft Word và bản render: **69**. Không có DOCX/PDF/PNG/full-text trên GitHub.

W02.1 chỉ đổi lịch từ 5 cột/10 tuần trống thành 4 cột/3 tuần và bỏ 21 cụm ngày truy cập. 65/69 trang giống pixel W02; chỉ trang 3, 67, 68, 69 đổi. 17 bảng còn lại, toàn bộ hình/crop/công thức/nội dung chương giữ nguyên.

## Kết quả kiểm tra

- Cấu trúc và ngữ nghĩa: 48/48 PASS tại verification.json. Final-verification.json bổ sung kiểm artifact và rà riêng 69 PNG; không sửa trạng thái lịch sử trong raw evidence.
- 18 bảng, 5 công thức native, 3 mục lục/danh mục tự động, 8 caption hình và 15 caption bảng; field không lỗi, đích PAGEREF còn tồn tại.
- Bảy hình thật đúng slot, không ảnh đen; giữ tỷ lệ/crop Word, caption cùng trang. Hình 1.1 và hai logo bìa không thay.
- Bỏ dẫn hình/bảng thừa bằng 14 diff whitelist; giữ phương pháp, số liệu, công thức. Danh sách trước/sau: ../word-w02-20261010/CHANGES.md và changes.json.
- Phát: Chương 3, 4, 5; lập trình hệ thống; báo cáo Word; xử lý, trình bày dữ liệu Excel. Không điền tỷ lệ đóng góp.
- Bảo toàn 37 nguồn/sản phẩm/mẫu theo hash; không train/refit, đổi metric, chạy Flink hoặc sửa ứng dụng. Không ghi đè Word nguồn.

## Bảy hình và nguồn

| Caption | Trang vật lý | Nguồn local QA W02 |
| --- | --- | --- |
| Hình 3.1. Đầu ra điện năng và chất lượng dữ liệu theo giờ | 46 | hourly-table.png; sáu bản ghi thật trong hourly-table-records.json |
| Hình 3.2. Điện năng tiêu thụ theo giờ trong khoảng thời gian lựa chọn | 48 | source-images/image6.png, crop biểu đồ Tổng quan |
| Hình 4.1. Đối chiếu điện năng thực tế và dự báo HGB trên tập Test | 53 | source-images/image5.png, crop biểu đồ Thực tế/HGB |
| Hình 5.1. Giao diện Tổng quan của ứng dụng | 59 | source-images/image6.png, Tổng quan |
| Hình 5.2. Phần giới thiệu bộ dữ liệu và đặc trưng dự báo | 60 | source-images/image7.png, dataset UCI và 11 đặc trưng |
| Hình 5.3. Giao diện Phân tích dữ liệu tiêu thụ điện năng | 62 | source-images/image8.png, Phân tích |
| Hình 5.4. Giao diện Dự báo điện năng của giờ kế tiếp | 63 | source-images/image9.png, Dự báo |

Image-registry-final.json ghi part/relationship/hash thực tế sau khi Word lưu, không dùng relationship ID authoring làm mapping cuối. H3.1 là ảnh bảng từ sáu dòng CSV thật, có giờ đầy đủ/thiếu/NULL; H3.2 là crop đúng đồ thị trong ảnh Tổng quan của Thy. Không dùng ảnh mạng.

## Lịch và tài liệu tham khảo ở bản cuối W02.1

Lịch đúng Tuần/Nội dung công việc/Thành viên/Trạng thái. Tuần 1 cả nhóm đã thực hiện; tuần 2 Phát đã thực hiện theo phân công trực tiếp và artifact xử lý/mô hình; tuần 3 cả nhóm đang thực hiện/phối hợp rà soát, chuẩn bị trình bày. Đây là tổ chức đầu việc đề xuất, không nhật ký ba tuần lịch sử được xác minh; không gán ngày hoặc nhận đã thuyết trình.

Bỏ 21 cụm “Truy cập ngày 08/10/2026.”, giữ 21 nguồn đánh số, tác giả, năm công bố, DOI, phiên bản, URL và hyperlink. Mẫu trường có ví dụ ngày truy cập, chưa thấy quy định bắt buộc. Kiểm hyperlink là cấu trúc DOCX/URL được bảo toàn, không phải kiểm HTTP mới của 21 website.

## Giới hạn và điểm dừng

Trang 10 còn ngắt tên dài trong glossary như nguồn; ngoài scope nên giữ. Chữ phụ ảnh toàn dashboard cần zoom; không cắt KPI/trục/đơn vị. Native Word/PDFium đã kiểm; renderer đóng gói thiếu soffice, không tuyên bố đã kiểm mọi renderer. Cache/runtime toàn máy không được audit lại; preservation chỉ 37 nguồn chuẩn nêu trong final gate.

Các snapshot APPLIED_UNVERIFIED trong changes/verification/word-readback là lịch sử bước trước rà thị giác; gate hiện hành là final-verification.json và page-review.md. Dừng chờ duyệt W02.1, không chuyển PowerPoint/demo/code.
