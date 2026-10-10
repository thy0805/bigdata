# W02 — thay đổi trước và sau

Chỉ 14 đoạn thân bài có span/câu dẫn được bỏ, cùng một ô phân công Phát. Chỉ số paragraph là zero-based trong OOXML nguồn.

## Paragraph 416

**Trước:** Hai cột Date và Time xác định thời điểm đo; bảy cột còn lại ghi các đại lượng điện. Tên cột, ý nghĩa và đơn vị được giữ tương ứng với mô tả UCI tại Bảng 3.1. Dữ liệu ngày có cả dạng ngày/tháng một hoặc hai chữ số, nên việc phân tích không chỉ dựa vào chuỗi mẫu của ngày đầu.

**Sau:** Hai cột Date và Time xác định thời điểm đo; bảy cột còn lại ghi các đại lượng điện. Tên cột, ý nghĩa và đơn vị được giữ tương ứng với mô tả UCI. Dữ liệu ngày có cả dạng ngày/tháng một hoặc hai chữ số, nên việc phân tích không chỉ dựa vào chuỗi mẫu của ngày đầu.

## Paragraph 424

**Trước:** Kết quả kiểm tra toàn bộ dữ liệu và kết quả theo giờ được tổng hợp tại Bảng 3.2. Kiểm tra timestamp không phát hiện thời điểm không hợp lệ hoặc trùng. Các khoảng thiếu phép đo có thể kéo dài nhiều ngày; khoảng liên tiếp dài nhất được ghi nhận là 7.226 phút.

**Sau:** Kiểm tra timestamp không phát hiện thời điểm không hợp lệ hoặc trùng. Các khoảng thiếu phép đo có thể kéo dài nhiều ngày; khoảng liên tiếp dài nhất được ghi nhận là 7.226 phút.

## Paragraph 436

**Trước:** Quy tắc tại Bảng 3.3 phân biệt kết quả ghi nhận một phần với điện năng giờ đầy đủ. Flink SQL BATCH nhóm theo FLOOR(event_time TO HOUR); không sử dụng keyBy, TUMBLE hoặc watermark để chốt cửa sổ.

**Sau:** Quy tắc tổng hợp phân biệt kết quả ghi nhận một phần với điện năng giờ đầy đủ. Flink SQL BATCH nhóm theo FLOOR(event_time TO HOUR); không sử dụng keyBy, TUMBLE hoặc watermark để chốt cửa sổ.

## Paragraph 439

**Trước:** Kết quả tạo 34.589 khung giờ, gồm 34.085 giờ đầy đủ và 504 giờ không đầy đủ. Tập theo giờ và các cột chất lượng là đầu vào của bước phân tích và tạo đặc trưng. Hình 3.1 dành cho hình minh họa đầu ra tổng hợp theo giờ.

**Sau:** Kết quả tạo 34.589 khung giờ, gồm 34.085 giờ đầy đủ và 504 giờ không đầy đủ. Tập theo giờ và các cột chất lượng là đầu vào của bước phân tích và tạo đặc trưng.

## Paragraph 443

**Trước:** Thống kê trên dữ liệu giờ đã lưu được trình bày tại Bảng 3.4. Tổng điện năng quan sát gồm các phút hợp lệ của cả giờ đầy đủ và không đầy đủ. Ngược lại, giá trị trung bình, thấp nhất và cao nhất trong bảng chỉ sử dụng 34.085 giờ đầy đủ.

**Sau:** Tổng điện năng quan sát gồm các phút hợp lệ của cả giờ đầy đủ và không đầy đủ. Ngược lại, giá trị trung bình, thấp nhất và cao nhất chỉ sử dụng 34.085 giờ đầy đủ.

## Paragraph 455

**Trước:** Hình 3.2 dành cho biểu đồ điện năng theo giờ. Dashboard cho phép thay đổi khoảng ngày; tiêu đề và chú thích cần được đọc cùng phạm vi lọc, thay vì sử dụng một tổng điện năng không ghi giai đoạn.

**Sau:** Dashboard cho phép thay đổi khoảng ngày; tiêu đề và chú thích cần được đọc cùng phạm vi lọc, thay vì sử dụng một tổng điện năng không ghi giai đoạn.

## Paragraph 475

**Trước:** Bộ 11 đặc trưng và thứ tự sử dụng được trình bày tại Bảng 4.1. Năm lag tham chiếu chính xác mốc s−1, s−2, s−3, s−24 và s−168 giờ. Hai rolling lấy 3 hoặc 24 khoảng giờ ngay trước s, sau khi dịch chuỗi về quá khứ.

**Sau:** Năm lag tham chiếu chính xác mốc s−1, s−2, s−3, s−24 và s−168 giờ. Hai rolling lấy 3 hoặc 24 khoảng giờ ngay trước s, sau khi dịch chuỗi về quá khứ.

## Paragraph 480

**Trước:** Train, Validation và Test là ba đoạn nối tiếp theo thời gian. Tỷ lệ 70%/15%/15% được áp dụng trên trục 34.589 giờ trước khi lọc mẫu hợp lệ. Khoảng trục giờ và số mẫu sử dụng được đối chiếu tại Bảng 4.2.

**Sau:** Train, Validation và Test là ba đoạn nối tiếp theo thời gian. Tỷ lệ 70%/15%/15% được áp dụng trên trục 34.589 giờ trước khi lọc mẫu hợp lệ.

## Paragraph 495

**Trước:** Bảng 4.3 trình bày kết quả Validation trên 4.727 mẫu. HGB có MAE 0,3694 kWh và RMSE 0,5306 kWh, thấp hơn hai baseline trên đoạn này. Đây là căn cứ lựa chọn candidate trước khi mở kết quả Test.

**Sau:** HGB có MAE 0,3694 kWh và RMSE 0,5306 kWh, thấp hơn hai baseline trên đoạn này. Đây là căn cứ lựa chọn candidate trước khi mở kết quả Test.

## Paragraph 499

**Trước:** Bảng 4.4 trình bày kết quả Test cố định trên 4.590 mốc. HGB có MAE 0,3221 kWh và RMSE 0,4635 kWh; Naive lần lượt 0,3858 và 0,5845 kWh; Seasonal Naive 24 giờ lần lượt 0,5036 và 0,7526 kWh.

**Sau:** HGB có MAE 0,3221 kWh và RMSE 0,4635 kWh; Naive lần lượt 0,3858 và 0,5845 kWh; Seasonal Naive 24 giờ lần lượt 0,5036 và 0,7526 kWh.

## Paragraph 507

**Trước:** Biểu đồ trên tập Test đối chiếu đường điện năng thực tế và đường HGB theo cùng timestamp, như vị trí minh họa tại Hình 4.1. Bộ lọc thời gian chỉ thay đổi phần kết quả được hiển thị; MAE/RMSE công bố vẫn là kết quả của toàn tập Test cố định.

**Sau:** Biểu đồ trên tập Test đối chiếu đường điện năng thực tế và đường HGB theo cùng timestamp. Bộ lọc thời gian chỉ thay đổi phần kết quả được hiển thị; MAE/RMSE công bố vẫn là kết quả của toàn tập Test cố định.

## Paragraph 523

**Trước:** Bảng 5.1 ghi công nghệ và vai trò thực tế. Flink cùng Python chạy trong Ubuntu trên WSL2; trình duyệt Windows truy cập ứng dụng qua localhost. Đây là cấu hình cục bộ, không phải triển khai phân tán nhiều máy hoặc dịch vụ đám mây.

**Sau:** Flink cùng Python chạy trong Ubuntu trên WSL2; trình duyệt Windows truy cập ứng dụng qua localhost. Đây là cấu hình cục bộ, không phải triển khai phân tán nhiều máy hoặc dịch vụ đám mây.

## Paragraph 559

**Trước:** Phân tích hỗ trợ điện năng theo thời gian, profile theo giờ trong ngày, ngày trong tuần, tháng và ba nhóm đo phụ. Các thao tác và quy tắc dữ liệu của từng tab được đối chiếu tại Bảng 5.2.

**Sau:** Phân tích hỗ trợ điện năng theo thời gian, profile theo giờ trong ngày, ngày trong tuần, tháng và ba nhóm đo phụ.

## Paragraph 574

**Trước:** Phạm vi kiểm thử ở Bảng 5.3 gồm chuỗi UCI → dữ liệu giờ Flink → feature → model → dashboard. Kết quả ghi nhận 119/119 phép kiểm chức năng và vận hành đạt, cùng 7/7 phép kiểm hồ sơ và bảo toàn sản phẩm đạt, tổng cộng 126/126. Nhóm kiểm hồ sơ không được tính là kiểm thử chức năng. Kết quả phản ánh trạng thái hệ thống tại thời điểm kiểm tra.

**Sau:** Phạm vi kiểm thử gồm chuỗi UCI → dữ liệu giờ Flink → feature → model → dashboard. Kết quả ghi nhận 119/119 phép kiểm chức năng và vận hành đạt, cùng 7/7 phép kiểm hồ sơ và bảo toàn sản phẩm đạt, tổng cộng 126/126. Nhóm kiểm hồ sơ không được tính là kiểm thử chức năng. Kết quả phản ánh trạng thái hệ thống tại thời điểm kiểm tra.

## Paragraph ô phân công

**Trước:** (ô trống)

**Sau:** Chương 3, 4, 5; lập trình hệ thống; báo cáo Word và xử lý, trình bày dữ liệu bằng Excel.
