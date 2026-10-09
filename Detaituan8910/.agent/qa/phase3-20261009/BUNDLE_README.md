# Gói duyệt Phase3

Gói ZIP chứa mã dashboard, hồ sơ QA hiện hành, tám ảnh trình duyệt được chọn và artifact đã khóa phục vụ kiểm độc lập: model/manifest, hourly-grid/manifest/verification, Test features/schema và predictions/metric2B2. Các checksum nguồn được ghi trong verification.json và manifest của gói.

Đây là gói nghiệm thu, không phải ứng dụng portable hoặc installer. Sourcegate app trên máy Thy kiểm thêm các artifact/QA của các phase trước; một số không được sao chép vào gói để tránh đóng gói toàn dự án. Không dùng gói để train lại, lựa chọn mô hình hoặc official Test evaluation lần nữa.

Nguồn đọc đầu tiên: review.md, verification.json, technical-verification-v3.json, browser-verification.json và ảnh cuối trong bảng review. Model dùng scikit-learn1.6.1/Python3.12.3; nếu môi trường người kiểm khác phiên bản thì không khẳng định đã xác minh load/inference chỉ từ đọc manifest.

Thy/GPT Web nghiệm thu giao diện còn PENDING. Không coi gói này là phê duyệt Phase4/Word/replay/video.
