# Bàn giao Giai đoạn 2B1: HGB và Validation

Trạng thái kỹ thuật: VERIFIED qua 37/37 kiểm thử mô hình và47/47 kiểm tài liệu, đọc lại18 Markdown. Thy/GPT Web chưa nghiệm thu2B1 hoặc duyệt2B2. Phase2A được Thy nghiệm thu dựa trên hồ sơ, không mô tả GPT Web đã chạy kiểm thử tại máy.

## 1. Cấu hình và môi trường thực tế

Model `hgb-uci-hourly-v0.1-candidate`, scikit-learn1.6.1, Python3.12.3 trong venv `/home/cute/.local/share/uci-forecast/venv`. NumPy2.2.6, Pandas2.2.3, SciPy1.15.3, joblib1.5.1, threadpoolctl3.6.0. Toàn bộ dependency khớp pin của Phase2A; pip check đạt. Không cài thêm gói hoặc thay Java/Flink/WSL.

| Tham số | Giá trị |
| --- | --- |
| loss | squared_error |
| learning_rate | 0.05 |
| max_iter | 200 |
| max_leaf_nodes | 15 |
| min_samples_leaf | 30 |
| l2_regularization | 1.0 |
| max_bins | 255 |
| early_stopping | False |
| random_state | 42 |

Chỉ fit 22.513 mẫu Train với 11 feature đúng thứ tự đã nghiệm thu. 200 vòng boosting thực thi, không early stopping hoặc random split. Các tham số mặc định còn lại nằm trong [model-config.json](../../../models/runs/20261009-phase2b1-a2/model-config.json). `validation_fraction=0.1` là mặc định được ghi lại, không được dùng khi early_stopping=False. Giới hạn threadpool2, không phải thay tham số mô hình. Một cấu hình duy nhất, hai lượt cùng cấu hình phục vụ kiểm tái lập, không hyperparameter search.

Run chính `20261009-phase2b1-a2`, lặp `20261009-phase2b1-b`. Thời gian fit ghi nhận lần lượt0,243831109 và0,222643464 giây; đây chỉ là fit trên bảng đặc trưng đã chuẩn bị, không bao gồm xử lý hơn hai triệu bản ghi hoặc toàn bộ quy trình QA. Peak RSS của tiến trình chính181.076 KiB, không phải tổng RAM của hệ thống.

## 2. Kết quả HGB trên Validation

4.727 timestamp, từ20/09/2009 13:00 đến24/04/2010 16:00 theo lịch nguồn. Target E(s) là điện năng trong[s,s+1), origin=s sau khi quan sát xong giờ trước; một bước dự báo cuốn chiếu sử dụng quá khứ thực tế đã quan sát, không phải dự báo nhiều bước từ một mốc duy nhất.

HGB: **MAE0,3694427311570533 kWh; RMSE0,5306058050415966 kWh**. Metric chính thức dùng prediction_final sau D09. Nhãn target, split và eligibility không thay đổi. Test4.590 mẫu chưa được đánh giá.

## 3. So sánh trên cùng timestamp và nhãn

| Mô hình | Số mẫu Validation | MAE (kWh) | RMSE (kWh) |
| --- | --- | --- | --- |
| HGB | 4.727 | 0,3694427312 | 0,5306058050 |
| Naive | 4.727 | 0,4592722869 | 0,6828109074 |
| Seasonal Naive24 | 4.727 | 0,6597176504 | 0,9503385628 |

Dự báo hai baseline giữ đúng giá trị Phase2A. Kiểm toàn bộ timestamp, origin, target_end và target trước so sánh, không chọn riêng đoạn HGB có điểm tốt. [Metric đầy đủ](../../../models/runs/20261009-phase2b1-a2/metrics-validation.json), [dự báo raw/final](../../../models/runs/20261009-phase2b1-a2/predictions-validation.csv).

## 4. Dự báo âm và D09

D09 LOCKED: `prediction_final=max(0,prediction_raw)`. HGB có **0 dự báo thô âm**, giá trị nhỏ nhất0,2407157168875143 kWh. Hai baseline cũng có0 giá trị âm. D09 thay đổi0 dự báo và giảm MAE/RMSE0 kWh trong lượt này; raw và final có cùng metric. Vẫn lưu cả hai cột, không bỏ policy vì chưa gặp âm.

Fixture QA riêng[-0,12;0;0,8] trả[0;0;0,8]; NaN/Inf và chiều dữ liệu sai bị từ chối. Fixture không được dùng làm dữ liệu nghiên cứu. Hàm `forecasting/predictor.py` giữ chính sách chung và chặn sai thứ tự/schema feature. Test và inference sau này phải gọi cùng hàm này; chúng chưa được triển khai hoặc đánh giá ở2B1.

## 5. Lưu và nạp model

[Candidate](../../../models/runs/20261009-phase2b1-a2/candidate.joblib), 154.086 byte, SHA256`94ed8c4e493025ae363a3cc6fb1b0639ef2368264966b5bda190303e98a95c38`. Bundle chứa estimator, thứ tự feature, D09, phiên bản và nguồn; `final_locked=false`, `training_split=train`.

Nạp lại trong lượt chạy và tiến trình verifier riêng cho cùng4.727 dự báo raw/final, so sánh chính xác từng giá trị, max chênh lệch0 kWh. Chỉ nạp artifact tự tạo và đã đối chiếu hash; không mở joblib không rõ nguồn. Lưu candidate không đồng nghĩa đã khóa model cuối.

## 6. Leakage, tái lập và bảo toàn

- Structural: đúng22513 Train/4727 Validation,11 feature theo schema; target/timestamp không vào X. Source gate kiểm hash, môi trường và trạng thái VERIFIED bằng so sánh tuyệt đối.
- Semantic: verifier độc lập bắt lời gọi fit của lượt lặp; X/y khớp toàn bộ Train đã nghiệm thu. Audit gate không cho chương trình huấn luyện đọc Validation trước khi fit hoàn tất; Test bị chặn. Feature engineering không làm lại, kế thừa QA trục giờ, gap và future perturbation của Phase2A qua artifact bất biến.
- Artifact/runtime: Decimal45 chữ số tính lại MAE/RMSE toàn bộ4.727 dòng cho ba mô hình, cả raw/final; sai khác với metric thư viện trong ngưỡng1e-12 kWh. Save/load đạt. Hai lượt có model, predictions CSV, metrics JSON và config JSON **giống từng byte**. Runtime time/RSS và manifest chứa thời điểm riêng không yêu cầu giống byte.
- Bảo toàn933 file kiểm nguồn, gồm Word/PDF/ZIP/raw, pipeline, output và hồ sơ Phase1/2A; không ghi đè chúng. Test chỉ được đọc nhị phân để kiểm SHA256 trong kiểm bảo toàn, không parse/huấn luyện/chọn model/tính metric.
- Snapshot cũ965 đường dẫn có68 file `flink-tmp/archivedApplicationStore-*` đã thay đổi hoặc không còn trước task;897 còn lại khớp hash. Không che giấu việc này bằng tuyên bố965 file vẫn nguyên trạng. Không sửa hoặc tái tạo cache runtime. [Preflight](preflight-notes.md), [preservation](preservation-before.json).

[Verification37/37](verification.json), [fit witness](fit-witness.json), [checklist](checklist.md), [manifest chính](../../../models/runs/20261009-phase2b1-a2/manifest.json), [QA companion của run](../../../models/runs/20261009-phase2b1-a2/verification.json). Manifest giữ snapshot APPLIED_UNVERIFIED lúc tạo; companion verification xác nhận kiểm cuối. Run a ban đầu bị gate chặn trước fit, không có model/metric, giữ để truy vết; không dùng làm kết quả.

Nguồn ML: Phase2A `20261009-phase2a-a`; nguồn Flink `20261009T102201900234-full`, job`9307ab8abf4d8286245019045ed694ac`, hourly-grid SHA256`8b03f1e3c82a5344c071a19f756cb7ec87fce18cc9a612cd63c4dcf4a8b5b2bc`. Không tổng hợp lại raw bằng Pandas thay cho Flink. Quy tắc scientific research của skill được áp dụng để giữ bảng dữ liệu phẳng, đơn vị kWh và tách nguồn/processed/results, không tạo workbook Excel ngoài yêu cầu.

## 7. HGB có vượt baseline không?

**Có, trên Validation này.** So Naive, MAE giảm19,56% và RMSE giảm22,29%, tính bằng`100×(1−error_HGB/error_Naive)`. HGB cũng thấp hơn Seasonal Naive24 ở cả hai metric. Đây không phải phần trăm “độ chính xác” và chưa chứng minh kết quả trên Test hoặc dữ liệu hộ khác.

## 8. Đề xuất cho2B2 và điểm dừng

Đề xuất chọn HGB với đúng cấu hình trên,11 feature và D09 đã duyệt để chuyển2B2. Cần Thy/GPT Web nghiệm thu kết quả Validation và duyệt model/config trước mở Test. Không thử cấu hình thứ hai. Chưa refit Train+Validation; nếu muốn đổi tập fit phải quyết định trước Test vì candidate hiện chỉ fit Train.

Sau duyệt, bước đầu2B2 là ghi lựa chọn model/config bất biến, kiểm seal/hash Test và hợp đồng origin; sau đó mới đánh giá Test một lần với chính sách final giống Validation, so baseline trên cùng mask và lưu model chính thức. Không thực hiện bước này trong lượt2B1.

Không có dashboard, sửa Word, số liệu Test hoặc model cuối LOCKED. [Hướng dẫn huấn luyện](../../../forecasting/TRAINING.md). Hồ sơ và checkpoint đã cập nhật để tiếp tục từ2B2 sau phê duyệt.

## Nguồn kỹ thuật

[HGB, early stopping và tham số theo scikit-learn1.6.1](https://scikit-learn.org/1.6/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html). [Lưu model, môi trường và rủi ro nạp pickle/joblib](https://scikit-learn.org/1.6/model_persistence.html). [NumPy maximum](https://numpy.org/doc/2.2/reference/generated/numpy.maximum.html). Số liệu thực nghiệm trong tài liệu lấy từ artifact/QA local được liên kết, không lấy từ tài liệu thư viện.
