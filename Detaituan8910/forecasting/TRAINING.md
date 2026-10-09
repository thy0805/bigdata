# HGB Train-only và Validation

Phạm vi hiện hành: [phê duyệt2B1](../.agent/decisions/20261009-phase2b1-approval.md). Phase2A đã LOCKED. Không sửa `prepare_baselines.py`, `requirements.txt`, `README.md` hoặc dữ liệu/QA cũ.

Kết quả chính: [models/runs/20261009-phase2b1-a2](../models/runs/20261009-phase2b1-a2/manifest.json); lặp [run b](../models/runs/20261009-phase2b1-b/manifest.json). [Bàn giao8 mục](../.agent/qa/phase2b1-20261009/review.md), [QA37/37](../.agent/qa/phase2b1-20261009/verification.json).

## Hợp đồng dữ liệu

Nguồn duy nhất `data/ml/runs/20261009-phase2a-a`,11 feature đúng schema,22513 Train/4727 Validation. Dự báo E(s) trong[s,s+1) tại origin=s, dữ liệu mới nhất E(s−1). Không tạo lại feature hoặc impute gap. Test4590 mẫu không dùng trong2B1.

`train_hgb.py` chỉ nhận run-id mới, không nhận đường dẫn Test hoặc tùy chọn tham số mô hình. Cấu hình đã duyệt cố định; chương trình từ chối run đã có. Hash source/pin dependency phải khớp. Chỉ đọc Train trước fit; Validation được kiểm hash/đọc sau fit, Test bị audit gate chặn. Guard bảo vệ quy trình chạy này, không phải cơ chế mã hóa hay phân quyền hệ điều hành cho Test.

Chạy lại khi được giao, không cần chạy để xem kết quả đã có. Từ PowerShell:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc 'OMP_NUM_THREADS=2 /home/cute/.local/share/uci-forecast/venv/bin/python /mnt/d/Hoctap/bigdata/Detaituan8910/forecasting/train_hgb.py --run-id 20261009-phase2b1-new'
```

Không dùng lại tên run chính hoặc lặp. Script QA đã chạy tạo bằng chứng riêng; không chạy lại verifier để ghi đè hồ sơ đã bàn giao. 37 kiểm thử không có nghĩa37 lần huấn luyện: chỉ một fit chính và một fit cùng cấu hình để kiểm tái lập.

## D09 và model ứng viên

`predictor.predict_bundle(bundle, X)` trả raw và final; X phải đúng11 cột/thứ tự, không kèm target/metadata. D09=`max(0,raw)`, không sửa target và không xử lý riêng UI. Metric chính thức trên final; raw lưu để đối chiếu. Reject NaN/Inf, không biến lỗi dữ liệu thành0.

Bundle `candidate.joblib` có estimator/schema/policy/provenance/version. Chỉ nạp file tự tạo và kiểm hash, trong cùng môi trường pin; joblib không an toàn với file không đáng tin. Chưa có model chính thức, chưa refit Train+Validation, chưa Test hoặc dashboard. Test/inference sau này phải giữ cùng D09 và feature contract.

Manifest APPLIED_UNVERIFIED là snapshot lúc tạo; `verification.json` riêng xác nhận QA cuối VERIFIED. Bản config đầy đủ ghi cả mặc định sklearn, không dùng validation_fraction khi early_stopping=False.
