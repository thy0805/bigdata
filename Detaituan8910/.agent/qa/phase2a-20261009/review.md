# Bàn giao Giai đoạn 2A: dữ liệu huấn luyện và baseline

Ngày 09/10/2026. M01–M04 VERIFIED kỹ thuật; chờ Thy/GPT Web nghiệm thu và duyệt lượt B. Phase 1 F01–F06 đã LOCKED qua hồ sơ theo yêu cầu mới. Không triển khai mô hình học máy, đánh giá Test, dashboard hoặc sửa Word.

## 1. Nguồn và bằng chứng

Nguồn duy nhất: [hourly-grid Flink đã nghiệm thu](../../../data/processed/runs/20261009T102201900234-full/hourly-grid.csv), run `20261009T102201900234-full`, SHA256 `8b03f1e3c82a5344c071a19f756cb7ec87fce18cc9a612cd63c4dcf4a8b5b2bc`.

Source gate kiểm checksum, verification 25/25 với trạng thái VERIFIED, run ID, manifest BATCH, không lỗi parse, job FINISHED và 14 cột. Manifest Phase 1 giữ snapshot APPLIED_UNVERIFIED; verification sau đó là bằng chứng QA cuối, không sửa lịch sử manifest.

- [Run chính](../../../data/ml/runs/20261009-phase2a-a/manifest.json), [QA29/29](../../../data/ml/runs/20261009-phase2a-a/verification.json).
- [Rerun](../../../data/ml/runs/20261009-phase2a-b/manifest.json), [QA30/30](../../../data/ml/runs/20261009-phase2a-b/verification.json): 9 artifact tất định giống từng byte, gồm CSV Train/Validation/Test, eligibility, dự báo Validation, schema, split, metric và seal.
- [Checklist](checklist.md), [scope/phê duyệt](../../decisions/20261009-phase2a-approval.md).

QA độc lập đọc CSV giờ Flink bằng Decimal và dictionary timestamp, không đọc raw TXT để tính lại điện năng cho sản phẩm. Hash nguyên bytes của raw chỉ được đọc để kiểm bảo toàn. Tổng 965 file pipeline/Phase 1 outputs/QA/Word/PDF/ZIP/raw giữ nguyên hash, không thêm file vào các vùng đã nghiệm thu. Hai run Flink bị từ chối trước đó vẫn được giữ.

## 2. Dữ liệu và feature schema

Trục nguồn có 34.589 giờ, từ 16/12/2006 17:00 đến 26/11/2010 21:00; 34.085 giờ đầy đủ, 504 giờ energy_kwh=NULL. Giữ lịch nguồn naive; không tự gắn UTC/DST.

Đặt `s=target_hour`: mục tiêu là E(s), điện năng [s,s+1). Tại `prediction_origin=s`, giờ s−1 vừa kết thúc và E(s−1) đã quan sát. Horizon là một giờ, không nhầm origin=s với target của giờ s+1. Ví dụ origin 10:00 dự báo 10:00–11:00 bằng dữ liệu đến hết 09:00–10:00. Đây là giả định dữ liệu giờ trước sẵn có tại origin, chưa mô hình hóa độ trễ hệ thống thu thập.

| Feature | Định nghĩa | Đơn vị |
| --- | --- | --- |
| lag_1_kwh, lag_2_kwh, lag_3_kwh | E(s−1), E(s−2), E(s−3) | kWh |
| lag_24_kwh, lag_168_kwh | E(s−24), E(s−168), tra đúng giờ lịch nguồn | kWh |
| rolling_mean_3_kwh | Trung bình E(s−3)..E(s−1), đủ 3 giờ | kWh |
| rolling_mean_24_kwh | Trung bình E(s−24)..E(s−1), đủ 24 giờ | kWh |
| target_hour_of_day | Giờ mục tiêu 0–23 | Lịch |
| target_day_of_week | Thứ Hai 0 đến Chủ nhật 6 | Lịch |
| target_month | Tháng 1–12 | Lịch |
| target_is_weekend | Thứ Bảy/Chủ nhật 1; còn lại 0 | Cờ |

Tổng 11 feature. Target, split, cờ đủ/lý do loại và timestamp chẩn đoán không nằm trong X. Không có chuẩn hóa/transform cần fit trong lượt A. [Schema máy đọc](../../../data/ml/runs/20261009-phase2a-a/feature-schema.json).

Chỉ dùng mẫu có nhãn và mọi feature bắt buộc đầy đủ. Lag 168 có thể lấy đúng giờ quá khứ cách 168 giờ dù giữa hai mốc có thiếu; không coi các giờ bị thiếu là đã quan sát, không nén trục. Rolling 3/24 phải đủ giờ liên tiếp, không nối qua gap để lấy bù quan sát. [Tài liệu pandas 2.2 về rolling/min_periods](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.DataFrame.rolling.html).

## 3. Phân chia theo thời gian

Split trên toàn 34.589 giờ mục tiêu trước loại mẫu: floor(0,70N)=24.212; floor(0,85N)=29.400. Không random split. Các mốc trong bảng là giờ bắt đầu khoảng mục tiêu, hai đầu bao gồm.

| Tập | Trục giờ mục tiêu | Giờ trên trục | Mẫu đủ điều kiện | Bị loại |
| --- | --- | ---: | ---: | ---: |
| Train | 16/12/2006 17:00 → 20/09/2009 12:00 | 24.212 | 22.513 | 1.699 |
| Validation | 20/09/2009 13:00 → 24/04/2010 16:00 | 5.188 | 4.727 | 461 |
| Test | 24/04/2010 17:00 → 26/11/2010 21:00 | 5.189 | 4.590 | 599 |
| Tổng | Toàn trục nguồn | 34.589 | 31.830 | 2.759 |

Mẫu Train hợp lệ đầu tiên là 23/12/2006 18:00 do lag 168 và giờ nguồn đầu thiếu. Test hợp lệ cuối là 26/11/2010 20:00; giờ 21:00 thiếu bị loại. Các mẫu hợp lệ không nhất thiết liên tục bên trong khoảng ngày này.

Validation là one-step rolling origin: tại mỗi mốc, các giá trị thực ở những giờ trước mốc đã được quan sát và được phép dùng. Không diễn giải đây là dự báo nhiều bước từ 20/09/2009 bằng toàn bộ nhãn Validation tương lai. Nhãn Train cuối 12:00–13:00 đã sẵn có tại origin Validation đầu 13:00. [Ví dụ sklearn về đánh giá theo thời gian và nguy cơ shuffled split](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html).

Test được chuẩn bị nhãn/feature và kiểm cấu trúc bằng nguồn giờ nhưng chưa tạo prediction, chưa tính metric, chưa dùng lựa chọn feature/tham số. [Seal](../../../data/ml/runs/20261009-phase2a-a/holdout/seal.json) là quy tắc quy trình, không phải mã hóa. Không tạo điểm Test giả để lấp báo cáo.

## 4. Những mẫu bị loại

[eligibility.csv](../../../data/ml/runs/20261009-phase2a-a/eligibility.csv) giữ đủ 34.589 giờ và toàn bộ lý do. Bảng dưới dùng lý do ưu tiên đầu tiên theo thứ tự cố định, vì một mẫu có thể đồng thời thiếu nhiều feature; không cộng các count chồng lấn để suy ra số mẫu loại.

| Lý do chính | Số giờ |
| --- | ---: |
| Thiếu nhãn mục tiêu | 504 |
| Chưa đủ lịch sử 168 giờ, nhãn có thật | 166 |
| Thiếu lag1 | 67 |
| Thiếu lag2 | 67 |
| Thiếu lag3 | 67 |
| Thiếu lag24 | 209 |
| Thiếu lag168 | 501 |
| Thiếu rolling24 sau các kiểm trên | 1.178 |
| Tổng bị loại | 2.759 |

Rolling 3 thiếu cũng được ghi trong lý do chồng lấn; không xuất hiện thành lý do chính vì ít nhất một lag 1/2/3 đã thiếu trước đó. 168 giờ đầu không đủ lịch sử; hai giờ trong đó còn thiếu nhãn nên lý do chính insufficient_history chỉ có 166. Tổng 2.759 mẫu loại gồm 504 nhãn thiếu và 2.255 nhãn đầy đủ nhưng không đủ feature.

Vùng thiếu dài nhất đã xác nhận ở Phase 1 là 17/08/2010 21:02 đến 22/08/2010 21:27, dài 7.226 phút. Trong lưới giờ, 121 giờ từ 17/08 21:00 đến 22/08 21:00 không đủ. QA lượt A kiểm vùng này không có mẫu hợp lệ; giờ kế tiếp không được gán lag 1/rolling 24 bằng 0 hoặc dùng shift đã bỏ NULL. Không quét lại phút để tính lại con số 7.226.

## 5. Baseline trên Validation

Hai baseline dùng cùng 4.727 timestamp đủ toàn bộ feature và nhãn của schema ML, không dùng tập mẫu rộng hơn riêng cho từng baseline. Naive=lag1; Seasonal Naive24=lag24. Đây là hai quy tắc không cần fit mô hình.

| Baseline | MAE (kWh) | RMSE (kWh) | Số mẫu Validation |
| --- | ---: | ---: | ---: |
| Naive | 0,4592722869 | 0,6828109074 | 4.727 |
| Seasonal Naive24 | 0,6597176504 | 0,9503385628 | 4.727 |

Naive có sai số thấp hơn trên phạm vi Validation/mask này; chưa kết luận cho Test hoặc mô hình chưa huấn luyện. Không dùng tỷ lệ “accuracy” tự quy đổi từ MAE/RMSE. [Metric nguyên precision](../../../data/ml/runs/20261009-phase2a-a/metrics-validation.json), [dự báo từng giờ Validation](../../../data/ml/runs/20261009-phase2a-a/predictions-validation.csv).

MAE/RMSE được đối chiếu với tổng trị tuyệt đối/bình phương và căn bậc hai bằng Decimal độc lập trên toàn 4.727 mẫu; các dự báo còn được đối chiếu theo timestamp nguồn. [API RMSE sklearn 1.6](https://scikit-learn.org/1.6/modules/generated/sklearn.metrics.root_mean_squared_error.html).

## 6. Kiểm thử và môi trường

Structural: schema 14 cột nguồn, trục giờ/NULL/count, 11 feature, số mẫu và cutoffs, source/output/code/requirements hashes, metadata và seal.

Semantic: dictionary timestamp/Decimal đối chiếu 34.589 giờ × 11 feature và eligibility/origin/target; đọc lại toàn bộ CSV đã lưu, kể cả Test chỉ ở phạm vi chuẩn bị dữ liệu. Tolerance số học 2e-14 kWh. Baseline/metric độc lập trên Validation. Feature điện năng đều thuộc giờ trước target; lịch target biết trước.

Runtime/artifact: hai lượt chạy thật, 29/29 và 30/30 bài kiểm. Ca thiếu/zero/compressed-axis/rolling coverage/đầu-cuối/gap/split đều đạt. Thay target và tương lai bằng giá trị khác không làm thay feature tại mốc; thay các giá trị Test không làm thay dự báo hay metric Validation. Không có fit/fit_transform/partial_fit trong mã Phase 2A. Có 9 artifact tất định byte-identical giữa hai run; manifest có run ID/thời điểm tạo khác có chủ ý.

G06 đọc lại đủ 16 tài liệu hiện hành; [38/38 kiểm tài liệu](documents-verification.json) đối chiếu link, UTF-8, số mẫu, mốc cắt, metric và phạm vi với artifact. Trạng thái checklist được parse đúng ô và so sánh bằng tuyệt đối, không để APPLIED_UNVERIFIED khớp nhầm VERIFIED.

Python 3.12.3, NumPy 2.2.6, Pandas 2.2.3, scikit-learn 1.6.1; các dependency bắc cầu pin trong [requirements](../../../forecasting/requirements.txt). Venv riêng `/home/cute/.local/share/uci-forecast/venv`, kích thước logic 357.785.166 byte (khoảng 341 MiB); không thay Python Windows/hệ thống hoặc venv QA Flink. `pip check` đạt. [Install report](install-report.json) ghi wheel URL/hash từ PyPI; pin phiên bản để tái lập, không tuyên bố đây là phiên bản mới nhất.

Ổ C trước cài có 27.951.398.912 byte trống, sau QA có 27.642.818.560 byte (khoảng 25,74 GiB); D có 242.049.794.048 byte. Biến thiên C có thể gồm hoạt động Windows khác, không quy toàn bộ cho venv. Không Docker/reinstall/restart/đổi cấu hình Windows. Không cần cluster Flink đang chạy để đọc output đã kiểm; không coi kiểm lượt A là test streaming/checkpoint recovery.

## 7. Đề xuất lượt B, chưa thực hiện

Một cấu hình HistGradientBoostingRegressor ban đầu: `loss=squared_error`, `learning_rate=0.05`, `max_iter=200`, `max_leaf_nodes=15`, `min_samples_leaf=30`, `l2_regularization=1.0`, `max_bins=255`, `early_stopping=False`, `random_state=42`. Calendar để numeric, không đổi feature schema/categorical trong cùng phép so sánh; giới hạn hai thread khi chạy nếu được duyệt. Đây là cấu hình khởi đầu chưa fit, không phải cấu hình tốt nhất đã chứng minh.

`early_stopping=False` tránh tập validation nội bộ ngẫu nhiên khi số mẫu lớn; chọn cấu hình bằng Validation thời gian riêng. [API HistGradientBoosting1.6](https://scikit-learn.org/1.6/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html). Đề xuất fit chỉ Train rồi so Validation trên đúng4.727 mẫu. Không mở tìm kiếm tham số rộng ngoài scope mới được duyệt.

Quyết định cần Thy/GPT Web: phê duyệt Phase2B và chính sách D09 trước fit/đánh giá cuối. Có thể chọn giữ dự báo thô và báo số âm, hoặc dùng clip0 như một bước pipeline được công bố, áp dụng nhất quán khi Validation/Test/inference. Không tự chọn, không âm thầm sửa riêng số trên UI. Baseline hiện dùng điện năng không âm nên lượt A chưa phát sinh quyết định này.

Sau khi cấu hình/chính sách được khóa mới đánh giá Test và kiểm lưu/nạp model trong phạm vi lượt B được duyệt. Nếu model không thắng baseline, báo đúng kết quả; không sửa split hoặc xem Test để tìm cấu hình có điểm đẹp hơn.

NEXT EXACT ACTION: Thy/GPT Web duyệt bản bàn giao M01–M04 và D09/Phase2B. Giữ nguyên artifact lượt A; chưa fit HGB, chưa metric Test, chưa dashboard/Word.
