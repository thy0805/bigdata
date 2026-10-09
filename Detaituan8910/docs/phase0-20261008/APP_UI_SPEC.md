# Đặc tả giao diện ứng dụng

## Hiện hành — Phase3 đã triển khai và kiểm kỹ thuật

[Dashboard](../../dashboard/README.md) giữ3tab theo phê duyệt; [hồ sơ3](../../.agent/qa/phase3-20261009/review.md) có67/67 kỹ thuật,10/10browser và ảnh thật laptop/16:9. Bộ lọc/KPI/gap/inference dùng artifact Flink và finalmodel đã khóa, không fit. Thy/GPT Web chưa nghiệm thu giao diện; không chuyển Phase4/Word/replay. Các trạng thái chưa có app bên dưới là lịch sử thiết kế.

## Hiện hành — Phase2B2; UI chưa được triển khai

[Bàn giao2B2](../../.agent/qa/phase2b2-20261009/review.md) VERIFIED51/51; final model LOCKED sau QA, Test4590 đã đánh giá. HGB Test MAE0.3220542588291146/RMSE0.4634874854716987kWh. UI khi được duyệt dùng [final inference contract](../../forecasting/FINAL_EVALUATION.md), predictor/D09 và artifact thật; không gán metric Validation thành Test. Chờ nghiệm thu2B2 và duyệt Phase3; không có dashboard/Streamlit/Plotly trong2B2. Các khối tiến độ cũ dưới đây là lịch sử, bố cục3tab vẫn PROPOSED.

Ngày cập nhật: 09/10/2026. UI vẫn PROPOSED, chưa có app. Phase1/2A LOCKED; HGB candidate2B1 đã fit Train và đánh giá Validation VERIFIED37/37, [handoff2B1](../../.agent/qa/phase2b1-20261009/review.md). D09 LOCKED, UI sau này phải gọi predictor raw/final dùng chung; không clip riêng UI. Test chưa đánh giá, model cuối chưa khóa; không gắn nhãn metric Validation thành Test. Chờ nghiệm thu2B1/duyệt2B2 và UI riêng.

## 1. Phạm vi và stack

Một hộ UCI, điện năng kWh theo giờ, dự báo một giờ kế tiếp từ mốc lịch sử. Ba tab: Tổng quan, Phân tích, Dự báo. UI Minimal nền trắng/xám xanh nhạt, card trắng, viền mảnh, xanh dương chủ đạo, font hỗ trợ tiếng Việt; không neon, gradient đậm hoặc sidebar lớn. Bố cục kiểm trên laptop và màn chiếu 16:9.

Đề xuất Streamlit + Plotly; chưa chuyển sang React. Các thiết kế dữ liệu/API/model tuân thủ [TECHNICAL_ARCHITECTURE](TECHNICAL_ARCHITECTURE.md).

## 2. Tab Tổng quan

- Bộ chọn ngày lịch sử theo phạm vi dataset; lọc cùng một khoảng cho toàn bộ KPI và biểu đồ.
- KPI 1: **Điện năng ghi nhận (kWh)**, tổng observed_energy_kwh của các phút có thật trong phạm vi, kèm độ phủ. Không gọi tổng thực đầy đủ khi có thiếu.
- KPI 2: **Trung bình giờ đầy đủ (kWh/giờ)**, tổng energy_kwh của giờ đầy đủ chia số giờ đầy đủ; NULL nếu không có giờ đủ.
- KPI 3: **Điện năng giờ cao nhất (kWh)**, max energy_kwh trên các giờ đầy đủ, kèm timestamp; NULL nếu không có giờ đủ.
- Biểu đồ điện năng giờ, giữ khoảng trống tại giờ thiếu; không vẽ đường nối xuyên qua gap như có quan sát.
- Ba nhóm đo phụ: tổng năng lượng ghi nhận theo nhóm, độ phủ riêng và tên khu vực đúng UCI. Không gán riêng cho máy giặt/tủ lạnh.
- Card dự báo từ mốc lịch sử hợp lệ: mốc biết dữ liệu, khoảng giờ mục tiêu, giá trị kWh, tên model. Nếu thiếu feature/model thì ghi rõ lý do, không cho số giả.

## 3. Tab Phân tích

- Mức tiêu thụ trung bình theo giờ trong ngày và ngày trong tuần, tính trên giờ đầy đủ, kèm số mẫu mỗi nhóm.
- Xu hướng tháng hoặc giai đoạn: tổng ghi nhận và coverage; tránh kết luận tháng ít quan sát tiêu thụ thấp hơn chỉ vì thiếu.
- Ba nhóm đo phụ dùng bar/line so sánh, không mặc định phần “khác” bằng 0.
- Chất lượng dữ liệu: số phút thiếu, giờ đủ/không đủ, khoảng thiếu dài và residual âm. Khối mở rộng nêu cách tính, không chiếm toàn trang.
- Không có giờ đủ trong bộ lọc: trạng thái rỗng có giải thích, không chia cho 0.

## 4. Tab Dự báo

Đặt `E_t` là điện năng giờ `[t,t+1)`. Tại mốc `t+1` biết E_t và dữ liệu cũ hơn, dự đoán E_(t+1) của giờ `[t+1,t+2)`. Hiển thị cả thời điểm chốt thông tin và khoảng mục tiêu để tránh nhầm timestamp.

- Chọn mốc lịch sử trong tập kiểm thử có đầy đủ feature; không chọn mốc tương lai hôm nay.
- Model chạy inference từ feature có sẵn tại mốc đó; không đọc điện năng mục tiêu làm đầu vào.
- Biểu đồ thực tế/dự báo dùng cùng tập test hợp lệ; phần thực tế chỉ hiện để đối chiếu sau dự báo.
- MAE/RMSE đơn vị kWh: là metric của tập test công bố với khoảng ngày, số mẫu và tên model, không giả vờ thay đổi theo bộ lọc khi chưa tính lại rõ phạm vi.
- Model info: phiên bản thư viện, features, train/validation/test range, nguồn job Flink, model artifact version.
- Thêm baseline vào so sánh khi Giai đoạn 2 tạo được kết quả thật; chưa khẳng định model tốt hơn baseline.

Số âm từ model nếu có phải được xử lý theo chính sách nghiệm thu đã công bố, không âm thầm đổi giá trị chỉ trên giao diện rồi giữ metric cũ. Chính sách này chưa quyết định.

## 5. Dữ liệu, caching và trạng thái

App đọc hourly artifact và metadata đã nghiệm thu. Cache dữ liệu theo hash/phiên bản artifact bằng st.cache_data; nạp model bằng st.cache_resource và không mutate model dùng chung. [Hướng dẫn caching chính thức](https://docs.streamlit.io/develop/concepts/architecture/caching).

Chuyển tab/bộ lọc không giải nén ZIP, không chạy full Flink job hoặc train lại. Khi thay artifact/model, cache phải nhận phiên bản mới. Kết quả inference cũng phải gắn đúng feature schema và model version; không tái sử dụng sai mốc.

Khối chi tiết mở rộng nêu: dataset lịch sử, một hộ, công thức điện năng, độ phủ, Flink Job ID/run time và đường dẫn artifact. Không cần tab kỹ thuật thứ tư. Trạng thái FINISHED chỉ được hiển thị từ manifest/log đã kiểm, không gõ cố định.

## 6. Tiêu chí UI và demo

Ba tab hoạt động, bộ lọc thống nhất, số trên KPI khớp dữ liệu đã xử lý, đơn vị/độ phủ/timestamp rõ. Kiểm mốc thiếu, bộ lọc rỗng, đầu/cuối dữ liệu và cache đổi phiên bản. Không vỡ bố cục hoặc chữ tiếng Việt. Demo gồm app và Flink Web UI/log thật; lịch sử replay không được mô tả là live công tơ.

UI chỉ bắt đầu sau duyệt Giai đoạn 3; không triển khai trong khảo sát hiện tại.
