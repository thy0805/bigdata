# Model cuối và quy trình Final Test

Nguồn hiện hành: [phê duyệt2B2](../.agent/decisions/20261009-phase2b2-approval.md), [bàn giao](../.agent/qa/phase2b2-20261009/review.md), [QA51/51](../.agent/qa/phase2b2-20261009/verification.json).

## Artifact đã kiểm

Model `../models/final/hgb-uci-hourly-v1.0-train-only/model.joblib`; [manifest](../models/final/hgb-uci-hourly-v1.0-train-only/manifest.json) LOCKED. SHA-256 `f4c33c54b026a3c81312dff9c9623c7dad33a3f9df4986ecd8693b7267d8749c`. Bundle giữ estimator candidate Train22513, 11 feature đúng thứ tự, D09 và training_split=train. final_locked=True/refit=False; không huấn luyện mới.

Input: DataFrame chỉ chứa `feature_columns` theo [schema](../data/ml/runs/20261009-phase2a-a/feature-schema.json), hữu hạn và đủ quá khứ. Gọi `predictor.predict_bundle(bundle, features)` để nhận raw/final; không truyền target/meta hoặc clip riêng ở UI. Target E(s) cho[s,s+1), origin=s, quan sát qua s−1. Chỉ nạp model nguồn tin cậy, kiểm SHA-256 trước joblib.load. Dependency dùng theo manifest: Python3.12.3/scikit-learn1.6.1 và các bản pin, venv `/home/cute/.local/share/uci-forecast/venv` trong Ubuntu-24.04.

Test4590 đã đánh giá chính thức một lần. [Prediction](../models/runs/20261009-phase2b2-a/predictions-test.csv), [metrics](../models/runs/20261009-phase2b2-a/metrics-test.json). HGB MAE0.3220542588291146/RMSE0.4634874854716987 kWh; baselines trong cùng JSON. 0 dự báo âm, D09 không đổi metric ở lượt này. Nạp lạnh candidate/final trong tiến trình khác dự báo giống tuyệt đối.

## Lệnh đã thực hiện, không chạy lại để chọn model

Trong WSL, từ root dự án: runtime Python là `/home/cute/.local/share/uci-forecast/venv/bin/python`.

1. `python -B forecasting/evaluate_final.py preflight`: kiểm nguồn, load/Validation, lưu selection-lock và pretest. Đã VERIFIED17/17. Chặn ghi đè khóa đã tồn tại.
2. `python -B forecasting/evaluate_final.py evaluate`: mở Test sau pretest; tạo journal và run riêng; không fit. Đã thực hiện số1, chặn nếu journal hoặc output tồn tại.
3. `python -B .agent/scripts/verify_phase2b2.py`: oracle Decimal/timestamp/schema, inference tiến trình riêng, bảo toàn, QA44/44 trước đóng gói, final/package QA51/51. Đã thực hiện; không chạy lại vì output độc quyền đã có.

Tái kiểm inference mà không fit/scoring có thể dùng `--cold-model` và `--cold-output` của verifier, nhưng output phải là file QA mới và chỉ chạy khi có yêu cầu kiểm cụ thể. Không thay artifact/testmetric đã nghiệm thu hoặc tự tạo lượt đánh giá mới. Nếu lỗi kỹ thuật mới, giữ lịch sử, ghi lý do và phạm vi trước chạy lại; không thay cấu hình theo Test.

## Giới hạn và cổng tiếp theo

Một hộ lịch sử; đánh giá one-step rolling origin với quan sát thực tế mới tại mỗi mốc, không multi-month open-loop. Calendar nguồn naive, chưa xác minh DST/latency. 599 giờ Test không đủ điều kiện loại theo policy đã khóa trước Test. Không suy rộng sang hộ khác hoặc công tơ thời gian thực.

Phase3/UI chưa được phê duyệt. README/TRAINING cũ là hướng dẫn các bước2A/2B1; khi dùng model cuối ưu tiên tài liệu này và handoff2B2. Không dashboard, Word hoặc replay trong scope2B2.
