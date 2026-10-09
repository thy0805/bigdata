# Bàn giao giao diện giới thiệu dữ liệu — 10/10/2026

Trạng thái kỹ thuật: **VERIFIED**. Nghiệm thu Thy/GPT Web: **PENDING**. I04 vẫn DEFERRED; toàn Phase4 INCOMPLETE.

## Thay đổi

Chỉ mã sản phẩm `dashboard/app.py` thay đổi, trong expander cuối trang. Tên mới là **Tìm hiểu bộ dữ liệu và cách AI dự báo**, mặc định thu gọn. Phần giới thiệu ghi ngắn về một hộ gia đình tại Sceaux, Pháp, giai đoạn lịch sử, số dòng/cột/tần suất và liên kết UCI chính thức.

Hai tab nhỏ trong expander tách **Dữ liệu gốc** (9 cột, nghĩa tiếng Việt, đơn vị) và **Đặc trưng dự báo** (11 tên tiếng Anh theo thứ tự schema đã khóa, nghĩa tiếng Việt). Các đặc trưng được tạo từ điện năng theo giờ và lịch, không phải cột gốc. Điện năng mục tiêu tính bằng kWh. Không thêm dữ liệu mẫu hoặc tab chính.

SHA-256, Job ID, version nội bộ và biểu thức D09 không còn trình bày trong expander. Metadata, kiểm checksum và suy luận vẫn giữ nguyên. Công suất phản kháng giữ đơn vị **kW theo UCI**, không tự đổi thành kVAr. Ba nhóm đo phụ được mô tả theo khu vực, không phải ba thiết bị hoặc ba hộ.

## Kiểm tra và nguồn

- [QA kỹ thuật](technical-verification.json): **75/75**. Kiểm schema/thứ tự/diễn giải, nguồn 21 hash, checksum sai bị chặn, suy luận model lưu, no-fit, khoảng thiếu, dữ liệu rỗng và hồi quy KPI/biểu đồ.
- [QA trình duyệt](browser-verification.json): **7/7**, gồm hai bảng ở CSS viewport 1366×768 và 1920×1080, khả năng thu gọn, mặc định đóng và liên kết nguồn. Bốn JPEG có kích thước thực tương ứng và đã kiểm bằng mắt, không tràn ngang.
- Bảo toàn **1.570/1.570** file thuộc snapshot QA4 sau khi loại đúng một file UI được phép sửa. Không tuyên bố 1.571 file đều bất biến. Prefix trước expander và footer sau expander bằng nguồn Git `2da758a`; chỉ block giới thiệu thay đổi.
- Nguồn nội dung: `docs/phase0-20261008/DATA_AUDIT.md`, schema `data/ml/runs/20261009-phase2a-a/feature-schema.json`, hourly-grid Flink đã khóa và [UCI chính thức](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption).
- Hồi quy dùng `.agent/scripts/verify_data_guide.py`, đọc và điều chỉnh verifier cũ trong bộ nhớ; không ghi đè script hoặc hồ sơ QA cũ. Không fit/refit, Test evaluation hoặc job Flink mới.
- [Gate bàn giao](handoff-verification.json): **31/31**, kiểm lại nguồn/hash được bảo vệ, ảnh, diff và nội dung QA. [Index scan](index-verification.json): snapshot 308 file trước khi thêm chính receipt này; byte index bằng disk, không phát hiện mẫu credential/secret và không có raw/Office/runtime trong phạm vi phát hành.

## Ảnh để duyệt

| Nội dung | Laptop 1366×768 | Màn hình 1920×1080 |
| --- | --- | --- |
| Dữ liệu gốc | [Ảnh](screenshots/raw-laptop.jpg) | [Ảnh](screenshots/raw-desktop.jpg) |
| Đặc trưng AI | [Ảnh](screenshots/features-laptop.jpg) | [Ảnh](screenshots/features-desktop.jpg) |

Hai lần kiểm ban đầu chưa đạt được giữ trong browser-verification: viewport thực nhỏ hơn do zoom 110%, và truy vấn visibility trong animation đóng khung. Kết quả cuối đo lại đúng viewport; không sửa ứng dụng để chữa lỗi kiểm tra. Ảnh thử sai kích thước chỉ giữ local.

## Giới hạn và bước tiếp theo

Không đổi theme, chart, KPI, forecast, backend, model, schema, split, metric Test, pipeline hoặc dữ liệu; không sửa Word/PPT/I04/video. Không chạy lại các phase cũ hoặc cold boot. App đã được khởi động lại riêng để tải mã UI mới; Flink không bị dừng.

Git publication được kiểm riêng bằng receipt sau push; receipt local `publication-receipt.json` ghi commit thực tế và read-back, không đưa vào commit để tránh vòng tự tham chiếu. Đọc HEAD/remote thực tế khi tiếp tục, không suy ra publication từ việc có mã.

**Điểm dừng:** Thy/GPT Web mở khung cuối trang để duyệt nội dung và hình thức. Không tự chuyển sang báo cáo, slide hoặc demo.
