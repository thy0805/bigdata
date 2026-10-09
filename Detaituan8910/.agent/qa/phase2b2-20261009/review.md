# Bàn giao Phase2B2 — Final Test

Ngày 09/10/2026. Thy/GPT Web nghiệm thu Phase2B1 qua hồ sơ và phê duyệt lựa chọn HGB Train-only; không refit Train + Validation. Kết luận kỹ thuật Phase2B2: **PASS — VERIFIED 51/51 kiểm tra**. Nghiệm thu của Thy/GPT Web là bước riêng; Phase3 chưa được phê duyệt.

## 1. Model cuối, phiên bản và checksum

Phiên bản: `hgb-uci-hourly-v1.0-train-only`. [Model cuối](../../../models/final/hgb-uci-hourly-v1.0-train-only/model.joblib), [manifest LOCKED](../../../models/final/hgb-uci-hourly-v1.0-train-only/manifest.json), dung lượng 154.146 byte.

SHA-256 final: `f4c33c54b026a3c81312dff9c9623c7dad33a3f9df4986ecd8693b7267d8749c`.

Candidate gốc: `models/runs/20261009-phase2b1-a2/candidate.joblib`; SHA-256 `94ed8c4e493025ae363a3cc6fb1b0639ef2368264966b5bda190303e98a95c38`, không ghi đè. Bản cuối giữ cùng estimator đã fit 22.513 mẫu Train và 11 feature. Chỉ metadata wrapper thay đổi để đặt version/final_locked; vì vậy hash final khác candidate. Fingerprint estimator của hai bản cùng `c9474b1121b103f58b9c7d78bd88e13bae146bc5`; dự báo raw/final giống tuyệt đối.

Cấu hình giữ nguyên: squared_error, learning_rate=0.05, max_iter=200, max_leaf_nodes=15, min_samples_leaf=30, l2_regularization=1.0, max_bins=255, early_stopping=False, random_state=42. Python3.12.3/scikit-learn1.6.1; dependency đầy đủ trong manifest. Không refit hoặc thử cấu hình khác.

## 2. Kết quả HGB trên Test

4.590 giờ hợp lệ; MAE **0.3220542588291146 kWh**, RMSE **0.4634874854716987 kWh**. Metric chính thức dùng prediction_final. Raw và final bằng nhau trên Test.

Phạm vi timestamp hợp lệ: 2010-04-24 17:00:00 đến 2010-11-26 20:00:00. Trục Test có 5.189 giờ; 599 giờ không đủ điều kiện đã bị loại theo policy2A khóa trước Test, không theo sai số mô hình. [Metrics đầy đủ](../../../models/runs/20261009-phase2b2-a/metrics-test.json).

## 3. Hai baseline trên cùng Test

| Model | Số mẫu | MAE Test (kWh) | RMSE Test (kWh) |
| --- | ---: | ---: | ---: |
| HGB | 4590 | 0.3220542588291146 | 0.4634874854716987 |
| Naive | 4590 | 0.3857869426289034 | 0.5845200373928800 |
| Seasonal Naive24 | 4590 | 0.5036366739288308 | 0.7526481217054579 |

Naive dùng điện năng giờ trước; Seasonal Naive24 dùng cùng giờ ngày trước. Tất cả dùng đúng 4.590 target_hour và D09 đồng nhất. HGB thấp hơn Naive khoảng 16.52% MAE và 20.71% RMSE trên tập này. Đây là so sánh tại bộ dữ liệu/split hiện hành, không phải bảo đảm cho hộ khác.

## 4. Validation so với Test

| Model | MAE Validation | RMSE Validation | MAE Test | RMSE Test |
| --- | ---: | ---: | ---: | ---: |
| HGB | 0.3694427311570533 | 0.5306058050415966 | 0.3220542588291146 | 0.4634874854716987 |
| Naive | 0.45927228686270355 | 0.6828109073989009 | 0.3857869426289034 | 0.5845200373928800 |
| Seasonal Naive24 | 0.6597176503772654 | 0.9503385628415242 | 0.5036366739288308 | 0.7526481217054579 |

Đơn vị kWh. Validation có 4.727 mẫu từ 2009-09-20 13:00:00 đến 2010-04-24 16:00:00. Cả ba model có metric Test thấp hơn Validation; hai giai đoạn khác khoảng lịch và mẫu hợp lệ, nên chưa kết luận nguyên nhân là mô hình được cải thiện. Model không thay đổi sau Validation. [Nguồn Validation](../../../models/runs/20261009-phase2b1-a2/metrics-validation.json).

## 5. Dự báo âm và D09

Policy: `prediction_final = max(0, prediction_raw)` qua predictor dùng chung, không sửa target hoặc residual đo đếm.

| Model | Âm raw | Min raw Test (kWh) | Dự báo đổi bởi D09 | MAE giảm | RMSE giảm |
| --- | ---: | ---: | ---: | ---: | ---: |
| HGB | 0 | 0.20239101624522457 | 0 | 0 | 0 |
| Naive | 0 | 0.1951 | 0 | 0 | 0 |
| Seasonal Naive24 | 0 | 0.1951 | 0 | 0 | 0 |

Validation cũng có 0 dự báo thô âm, D09 không đổi metric của ba model. Kiểm fixture âm/zero/dương và từ chối NaN/Inf/mảng sai chiều đạt. Không suy ra D09 luôn không có tác động trên dữ liệu tương lai.

## 6. Leakage, nguồn gốc và save/load

[Selection lock](selection-lock.json) được lưu trước nhật ký Test; [pretest](pretest-verification.json) đạt 17/17, nạp candidate tái tạo chính xác 4.727 Validation, 0 lần parse giá trị Test và 0 fit trước khóa. Việc hash nhị phân Test trước khóa không được coi là tính metric. Nhật ký [bắt đầu](evaluation-started.json)/[kết thúc](evaluation-completed.json) ghi một lượt đánh giá chính thức.

Test SHA-256 `f9785b91f46c43bbb22c08c98294cd32739f75e5df0218e355baa53d5fbd3574`. Flink nguồn run `20261009T102201900234-full`, hourly SHA-256 `8b03f1e3c82a5344c071a19f756cb7ec87fce18cc9a612cd63c4dcf4a8b5b2bc`. Phase2A manifest SHA-256 `5dcb28841635e3b525bed1998c70b669a295a630d61c8ea3e63c9af7b06375fc`. Manifest giữ liên kết/hash 9 artifact ML và candidate.

Oracle độc lập kiểm trục 34.589 giờ, 504 giờ NULL, exact mask Test và 11 feature/target của mọi mẫu. Lag/rolling lấy đúng timestamp quá khứ, không nối qua giờ thiếu. Calendar là thông tin đã biết ở origin. Target E(s) thuộc [s,s+1); origin=s, quan sát gần nhất E(s−1). Kiểm thay target/future tại origin không đổi feature hiện tại; thay cột nhãn Test không đổi prediction. Cột target không được truyền vào estimator.predict; sai thứ tự/nhãn thừa bị từ chối.

Save/load bản cuối được kiểm trong tiến trình riêng: sai khác raw/final lớn nhất 0 kWh; fingerprint estimator khớp candidate. Không gọi fit trong đánh giá, kiểm độc lập hoặc đóng gói. [QA đầy đủ](verification.json), [oracle metric Decimal45](metric-oracle.json).

## 7. Tái lập, bảo toàn và lỗi

[Candidate cold-load](reproducibility-candidate.json) và [final cold-load](reproducibility-final.json) dự báo lại bằng fixed model, khớp saved predictions từng giá trị; đây là kiểm tái lập inference, không đánh giá nhiều cấu hình hoặc chọn model lại. SHA-256 của raw/final float64 cùng `edb2b8a4063f6a651c4b61e17604288d04f2c621138ffae6d18e3f77f54e9fe3`. Thư viện MAE/RMSE được đối chiếu bằng Decimal45 độc lập, sai lệch dưới 1e-12 kWh cho raw/final cả ba model.

951/951 file trong guard của lượt này giữ hash trước/sau; không phát hiện thay đổi sản phẩm giai đoạn trước. Ngoại lệ audit trước duyệt: 924/933 file khớp, 9 cache runtime đã mất (3 archive và 6 blobStorage). 68 ngoại lệ snapshot cũ gồm 16 archive và 52 blobStorage, không chỉ archive. Không phục hồi hoặc sửa hồ sơ QA cũ. VERIFIED là tại thời điểm kiểm, không bảo đảm cache luôn bất biến. [Guard đầu lượt](preservation-before.json).

Test đã được chuẩn bị và kiểm cấu trúc trong Phase2A, không phải chưa từng đọc. Hồ sơ trước2B2 không ghi nhận dùng Test để fit, chọn tham số hoặc tính metric.

Một lỗi cú pháp mã mới được sửa trước khi chạy preflight, chưa mở Test hoặc tạo khóa; [ghi nhận](preflight-notes.md). Lượt Test chính thức hoàn tất lần1, không cần rerun đánh giá. Không còn kiểm thất bại trong 51 kiểm kỹ thuật; kiểm tài liệu bàn giao được báo riêng.

## 8. Artifact cho Giai đoạn3 khi được duyệt

Đường dẫn dựa trên root `D:/Hoctap/bigdata/Detaituan8910`:

- Model/manifest: `models/final/hgb-uci-hourly-v1.0-train-only/`.
- [Predictions Test](../../../models/runs/20261009-phase2b2-a/predictions-test.csv), schema: target_hour, prediction_origin, target_end, latest_observed_hour, target_energy_kwh; raw/final cho hgb, naive, seasonal_naive_24. 4.590 dòng, đơn vị kWh.
- Run/metrics/companion QA: `models/runs/20261009-phase2b2-a/`.
- Dữ liệu Flink: `data/processed/runs/20261009T102201900234-full/hourly-grid.csv`.
- Schema/split/eligibility: `data/ml/runs/20261009-phase2a-a/`.
- Predictor giữ nguyên `forecasting/predictor.py`; [hướng dẫn model cuối](../../../forecasting/FINAL_EVALUATION.md).

Venv đã khóa `/home/cute/.local/share/uci-forecast/venv`, chạy với distro `Ubuntu-24.04`. App sau này không được fit/quét raw khi chuyển tab. Inference chọn mốc lịch sử hợp lệ, dùng 11 feature theo schema và model cuối/D09 chung.

## 9. Giới hạn khoa học

Dữ liệu một hộ gia đình lịch sử, không đại diện nhiều hộ. Không có validation đa fold hoặc khoảng tin cậy thống kê; chỉ một cấu hình được duyệt. Kết quả phụ thuộc split và mask giờ đủ feature/target, không chứng minh chất lượng tại giờ thiếu dữ liệu.

Đây là dự báo một bước cuốn chiếu: tại mỗi origin nhận thêm điện năng quá khứ thực tế đã quan sát. Không phải dự báo liên tục nhiều tháng mà không nhận quan sát mới. Giả định điện năng giờ trước đã sẵn sàng tại origin, chưa mô hình hóa độ trễ đo/truyền. Timestamp giữ lịch nguồn không timezone; chưa xác minh DST. Không dự báo điện năng hiện tại, không streaming công tơ trực tiếp.

Nguồn kỹ thuật thư viện: [RMSE scikit-learn1.6](https://scikit-learn.org/1.6/modules/generated/sklearn.metrics.root_mean_squared_error.html), [Model persistence](https://scikit-learn.org/1.6/model_persistence.html). Chỉ nạp artifact local có hash kiểm và môi trường phiên bản tương ứng; không nạp joblib không rõ nguồn.

## 10. Kết luận và điểm dừng

**Phase2B2 PASS kỹ thuật; 51/51 kiểm, pretest17/17 và kiểm trước đóng gói44/44. Final manifest LOCKED.** HGB thấp hơn hai baseline trên cùng Test4590; không refit, không dùng Test để chọn lại mô hình.

Điểm dừng: bàn giao, chờ Thy/GPT Web nghiệm thu2B2 và duyệt Phase3. Chưa tạo dashboard, chưa cài Streamlit/Plotly, chưa sửa Word, chưa streaming replay. [Checklist](checklist.md), [QA tài liệu](documents-verification.json) là nguồn trạng thái bàn giao cuối.
