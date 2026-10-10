# Diff trước/sau W01.1

18 sửa đúng whitelist: 11 nhánh văn bản, 5 ô nhãn Bảng 5.3, 2 chỗ ngắt dòng mềm. Không đổi giá trị số hoặc cỡ chữ. Nội dung field REF/SEQ/STYLEREF được giữ.

Các đoạn có field chỉ liệt kê nhánh prose sửa, không phải toàn paragraph. `changes.json` là diff máy đọc được.

## 1. 3.2 chú nguồn Bảng 3.1

Trước:

> Nguồn: UCI Machine Learning Repository; đối chiếu DATA_AUDIT của tệp gốc.

Sau:

> Nguồn: UCI Machine Learning Repository; kết quả khảo sát tệp dữ liệu gốc.

## 2. 3.4 chú nguồn Bảng 3.2

Trước:

> Nguồn: audit toàn tệp và verification của lượt Flink toàn bộ dữ liệu.

Sau:

> Nguồn: kết quả kiểm tra toàn bộ tệp gốc và đối chiếu đầu ra Apache Flink.

## 3. 3.8 chú nguồn Bảng 3.4

Trước:

> Nguồn: thống kê đọc từ hourly-grid.csv đã khóa; không chạy lại Flink.

Sau:

> Nguồn: thống kê từ tệp điện năng theo giờ do Apache Flink tạo.

## 4. 5.11 bỏ lời điều phối số hiệu hình

Trước:

>  dành cho nội dung này; số hiệu được đặt trước các ảnh chức năng ở những mục tiếp theo.

Sau:

>  dành cho nội dung này.

## 5. 5.12 chú nguồn Bảng 5.2

Trước:

> Nguồn: dashboard/app.py, data_service.py, predictor.py và QA trình duyệt đã kiểm.

Sau:

> Nguồn: dashboard/app.py, data_service.py, predictor.py và kết quả kiểm thử trên trình duyệt.

## 6. 5.15 phân biệt119 chức năng/vận hành và7 hồ sơ

Trước:

>  gồm chuỗi UCI → dữ liệu giờ Flink → feature → model → dashboard. Hồ sơ ứng dụng ghi nhận 126/126 kiểm đạt trong phạm vi I01, I02, I03 và I05; nhóm kiểm chức năng/vận hành có 119 kiểm, còn bảy kiểm liên quan gate bàn giao. Các kiểm này là bằng chứng tại thời điểm thực hiện, không bảo đảm runtime luôn hoạt động về sau.

Sau:

>  gồm chuỗi UCI → dữ liệu giờ Flink → feature → model → dashboard. Kết quả ghi nhận 119/119 phép kiểm chức năng và vận hành đạt, cùng 7/7 phép kiểm hồ sơ và bảo toàn sản phẩm đạt, tổng cộng 126/126. Nhóm kiểm hồ sơ không được tính là kiểm thử chức năng. Kết quả phản ánh trạng thái hệ thống tại thời điểm kiểm tra.

## 7. Caption Bảng 5.3

Trước:

> . Phạm vi kiểm thử ứng dụng trong hồ sơ Phase 4

Sau:

> . Phạm vi kiểm thử và đối chiếu hồ sơ hệ thống

## 8. 5.15 chú nguồn Bảng 5.3

Trước:

> Nguồn: checklist/review/verification Phase4-app; snapshot kiểm, không bao gồm I04 hoặc coldboot.

Sau:

> Nguồn: kết quả kiểm thử ứng dụng và đối chiếu hồ sơ; chưa kiểm tra khởi động lại toàn bộ Windows/WSL.

## 9. 5.15 kết quả kiểm riêng phần giới thiệu dữ liệu

Trước:

> Lượt chỉnh phần giới thiệu dữ liệu có hồ sơ riêng 75 kiểm kỹ thuật và bảy kiểm trình duyệt ở 1366 × 768/1920 × 1080. Không cộng các lượt QA này thành số trường hợp độc lập không trùng.

Sau:

> Phần giới thiệu dữ liệu được kiểm tra riêng bằng 75 phép kiểm kỹ thuật và 7 phép kiểm trên trình duyệt ở 1366 × 768/1920 × 1080. Các số lượt kiểm này được báo cáo riêng, không cộng với đợt kiểm trước để tránh đếm trùng.

## 10. 5.16 giữ phạm vi và giới hạn vận hành

Trước:

> Kiểm thử đã xác nhận các tab, bộ lọc, chỉ số, biểu đồ và suy luận trong phạm vi dữ liệu khóa. Các phép thử nguồn/model/cổng kiểm khả năng báo lỗi và tránh dừng tiến trình không thuộc hệ thống. Khởi động, dừng và phục hồi dịch vụ đã được kiểm ở môi trường cục bộ; coldboot Windows/WSL và autostart chưa được kiểm chứng hoặc triển khai.

Sau:

> Kiểm thử đã xác nhận các tab, bộ lọc, chỉ số, biểu đồ và suy luận trong phạm vi dữ liệu đã xác minh. Các phép thử lỗi nguồn dữ liệu, mô hình và cổng kiểm tra khả năng báo lỗi và tránh dừng tiến trình không thuộc hệ thống. Khởi động, dừng và phục hồi dịch vụ đã được kiểm trong môi trường cục bộ; việc khởi động lại toàn bộ Windows/WSL chưa được kiểm thử và tự khởi động dịch vụ chưa được triển khai.

## 11. 5.16 bỏ I04/Phase4/VERIFIED, giữ giới hạn

Trước:

> I04 về kịch bản demo vẫn tạm hoãn, nên không kết luận toàn bộ Phase 4 đã hoàn tất. Kết quả kỹ thuật VERIFIED và việc người dùng nghiệm thu là hai trạng thái khác nhau. Báo cáo không có phép đo benchmark nhiều máy, kiểm tải production hoặc cam kết độ sẵn sàng dịch vụ.

Sau:

> Kịch bản trình diễn chưa được chuẩn bị trong phạm vi thực hiện. Kết quả kiểm thử kỹ thuật không thay thế việc nghiệm thu của người dùng. Hệ thống chưa được đo hiệu năng trên nhiều máy, kiểm thử tải trong môi trường vận hành thực tế hoặc đánh giá độ sẵn sàng dịch vụ.

## 12. Bảng 5.3 ô0,0

Trước:

> Nhóm kiểm

Sau:

> Nhóm kiểm tra

## 13. Bảng 5.3 ô1,0

Trước:

> Lineage / integration

Sau:

> Đối chiếu nguồn / tích hợp

## 14. Bảng 5.3 ô5,2

Trước:

> Ba tab, các tương tác và ảnh QA

Sau:

> Ba tab, tương tác và đối chiếu ảnh giao diện

## 15. Bảng 5.3 ô6,0

Trước:

> Gate bàn giao

Sau:

> Đối chiếu hồ sơ

## 16. Bảng 5.3 ô6,2

Trước:

> Hồ sơ và kiểm bảo toàn trong lượt bàn giao

Sau:

> Kiểm tính đầy đủ hồ sơ và bảo toàn sản phẩm

## 17. Bảng 3.1 đơn vị Time

Trước:

> Giờ:phút:giây

Sau:

> Giờ:phút: ↵ giây

## 18. Bảng 5.1 tên mô hình HGB

Trước:

> HistGradientBoostingRegressor

Sau:

> HistGradient ↵ BoostingRegressor
