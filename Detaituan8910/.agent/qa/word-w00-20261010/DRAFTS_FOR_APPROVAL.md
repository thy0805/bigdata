# E — Mẫu nguyên văn để Thy/GPT Web duyệt

Đây là các mẫu W00 riêng trong Markdown; **chưa đưa vào DOCX**, không phải các chương đã biên soạn hoàn chỉnh. Văn phong áp dụng từ rule chung, không đưa KLCN186 vào Big Data.

## Lời cảm ơn

Nhóm xin gửi lời cảm ơn đến thầy Nguyễn Thành Ngô, giảng viên học phần Big Data, vì những kiến thức thầy đã truyền đạt trong quá trình giảng dạy. Nội dung học phần cung cấp cơ sở để nhóm tìm hiểu các phương pháp xử lý dữ liệu lớn và vận dụng vào bài toán phân tích, dự báo điện năng tiêu thụ.

Báo cáo có thể còn thiếu sót về nội dung và cách trình bày. Nhóm mong nhận được ý kiến góp ý của thầy để điều chỉnh và hoàn thiện báo cáo.

Nhóm xin chân thành cảm ơn thầy.

**Ghi chú dàn trang ngoài nội dung báo cáo:** Mục tiêu8–9dòng ở style nội dung mẫu. W00 chưa dàn vào Word nên không khẳng định sốdòng thực. W01 phải kiểm saurender, rút câu nếu cần; không thêm lời ca ngợi hoặc kéo bằngEnter. Không khẳng định thầy hướng dẫncode/phân tíchdataset.

## Kết luận

### 1. Kết quả đạt được

Báo cáo thực hiện phân tích dữ liệu tiêu thụ điện năng và dự báo điện năng của giờ kế tiếp từ bộ UCI Individual Household Electric Power Consumption. Apache Flink SQL BATCH xử lý 2.075.259 bản ghi theo phút và tổng hợp thành 34.589 khung giờ, trong đó 34.085 giờ có đủ phép đo hợp lệ. Các giờ không đầy đủ được đánh dấu để phân biệt điện năng ghi nhận với điện năng của một giờ hoàn chỉnh.

Từ dữ liệu theo giờ, quy trình xây dựng 11 đặc trưng lịch sử và lịch thời gian. Mô hình HistGradientBoostingRegressor được huấn luyện trên 22.513 mẫu Train, lựa chọn thông qua Validation và giữ nguyên khi đánh giá trên 4.590 mẫu Test. MAE đạt 0,3221 kWh và RMSE đạt 0,4635 kWh, thấp hơn hai phương pháp Naive và Seasonal Naive 24 giờ trên cùng tập kiểm tra.

Ứng dụng Streamlit gồm ba tab Tổng quan, Phân tích và Dự báo, sử dụng dữ liệu đã xử lý và mô hình đã lưu. Ứng dụng hỗ trợ xem mức tiêu thụ theo thời gian, thông tin về ba nhóm đo phụ và dự báo tại các mốc lịch sử hợp lệ.

### 2. Hạn chế của đề tài

Dữ liệu chỉ ghi nhận một hộ gia đình tại Pháp trong giai đoạn 2006–2010, nên kết quả chưa đại diện cho các hộ khác hoặc nhu cầu điện hiện nay. Đánh giá sử dụng dự báo một bước cuốn chiếu: tại mỗi mốc, mô hình nhận các quan sát thực tế của những giờ trước để dự báo giờ kế tiếp. Đây không phải dự báo liên tục nhiều ngày hoặc nhiều tháng khi không có thêm quan sát.

Ứng dụng chưa kết nối với công tơ cập nhật trực tiếp và chưa được triển khai, kiểm chứng trong môi trường production nhiều máy. Các phép đo thiếu làm giảm số mẫu đủ điều kiện dự báo; quy ước múi giờ và thay đổi giờ mùa hè của nguồn chưa được xác minh.

### 3. Hướng phát triển

Các hướng nghiên cứu tiếp theo gồm bổ sung dữ liệu của nhiều hộ và các giai đoạn mới, đánh giá khả năng dự báo nhiều bước, và xem xét nguồn dữ liệu cập nhật khi có điều kiện thu thập. Việc mở rộng cần xác định lại quy tắc chất lượng dữ liệu, điều kiện đánh giá và yêu cầu vận hành trước khi triển khai.

**Căn cứ ngoài nội dung báo cáo:** metrics-test.json gốcHGB MAE0.3220542588291146/RMSE0.4634874854716987kWh; source auditfull vàfinal manifest. Không có accuracy%, không tuyên bố I04/video hoặc production đã hoàn tất.

## Mẫu thay mục 2.14. Các công nghệ và thư viện sử dụng

Apache Flink 2.3.0 được sử dụng ở chế độ SQL BATCH trên môi trường WSL2/Ubuntu với Java 17. Job đọc tệp dữ liệu UCI hữu hạn, kiểm tra giá trị và dấu thời gian, sau đó nhóm các bản ghi theo từng giờ để tổng hợp điện năng. Đầu ra được lưu thành các tệp CSV phục vụ các bước phân tích và dự báo.

Python được sử dụng cho xử lý dữ liệu sau tổng hợp và xây dựng mô hình. Pandas tổ chức chuỗi theo trục thời gian và tạo đặc trưng; NumPy hỗ trợ tính toán trên các mảng số. HistGradientBoostingRegressor của scikit-learn là mô hình hồi quy được sử dụng trong thực nghiệm. Mô hình được huấn luyện trên Train, lưu bằng joblib và nạp lại khi suy luận; ứng dụng không huấn luyện lại mô hình khi người dùng mở hoặc chuyển tab.

Streamlit xây dựng giao diện gồm Tổng quan, Phân tích và Dự báo; Plotly hiển thị các biểu đồ tương tác. Dashboard đọc dữ liệu theo giờ và kết quả đánh giá đã lưu, đồng thời sử dụng mô hình đã khóa để dự báo tại các mốc lịch sử hợp lệ. Bước huấn luyện và suy luận bằng Python là thành phần riêng, không được thực hiện bên trong job Flink.

Kiến trúc triển khai sử dụng nguồn dữ liệu lịch sử và các tệp kết quả trung gian. Kafka, PyFlink, InfluxDB, TimescaleDB, HDFS và Grafana không phải thành phần của ứng dụng hiện tại. Các cơ chế streaming của Flink được giới thiệu trong phần cơ sở lý thuyết không đồng nghĩa với việc đã triển khai nguồn công tơ trực tiếp.

**Căn cứ ngoài nội dung báo cáo:** SQLfull, `forecasting/prepare_baselines.py`, `forecasting/train_hgb.py`, `forecasting/predictor.py`, `dashboard/data_service.py`, requirements vàfinalmanifest. Phiên bản chi tiết đặt Bảng5.1, không lặp cảbảng trong2.14.

## Mẫu đoạn 3.7. Tổng hợp dữ liệu tiêu thụ điện năng theo thời gian

Thuộc tính Global_active_power biểu thị công suất tác dụng trung bình từng phút, đơn vị kW. Điện năng của một phút được tính bằng công suất nhân với thời lượng 1/60 giờ. Với một khoảng giờ có đủ 60 phép đo hợp lệ, điện năng tiêu thụ được xác định bằng tổng công suất của các phút chia cho 60, đơn vị kWh.

Job Flink SQL BATCH nhóm dữ liệu theo mốc giờ lấy từ dấu thời gian nguồn. Một giờ được xác nhận đầy đủ khi có 60 bản ghi, 60 dấu thời gian phút khác nhau và 60 giá trị công suất hợp lệ. Nếu không đạt các điều kiện này, trường energy_kwh nhận giá trị NULL; tổng của những phút quan sát được vẫn được giữ riêng trong observed_energy_kwh. Quy tắc tại Bảng 3.3 tránh xem điện năng ghi nhận một phần là điện năng của cả giờ.

Kết quả đã kiểm tra gồm 34.589 khung giờ, trong đó 34.085 giờ đầy đủ và 504 giờ không đầy đủ. Trục giờ được giữ liên tục trước khi tạo đặc trưng dự báo. Các mẫu không có đủ giá trị lịch sử hoặc nhãn hợp lệ không được đưa vào tập huấn luyện và đánh giá; không thay các giá trị thiếu bằng 0 hoặc tự nội suy.

**Ghi chú ngoài nội dung báo cáo:** Bảng3.3 là số hiệu đề xuất; W01 phải tạo caption/field và kiểm crossref thực. Đoạn này không tuyên bố dùng TUMBLE, Watermark hoặc keyBy trong jobSQL vì SQLthật dùng `GROUP BY FLOOR(event_time TO HOUR)`.
