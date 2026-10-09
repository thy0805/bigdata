# Dữ liệu dự báo và baseline Giai đoạn 2A

M01–M04 đã thực thi và kiểm tra. Chưa huấn luyện mô hình học máy, chưa đánh giá Test, chưa có dashboard. Nguồn duy nhất là output Flink `20261009T102201900234-full`, không tổng hợp lại dữ liệu phút.

## Môi trường và chạy lại

Python3.12.3 WSL, venv `/home/cute/.local/share/uci-forecast/venv`. Dependency pin trong requirements.txt, đã cài bằng wheel và kiểm `pip check`. Không phụ thuộc Flink cluster đang chạy để đọc artifact đã nghiệm thu.

Trong Ubuntu, từ `/mnt/d/Hoctap/bigdata/Detaituan8910`:

```bash
/home/cute/.local/share/uci-forecast/venv/bin/python forecasting/prepare_baselines.py --run-id ten-run-moi
/home/cute/.local/share/uci-forecast/venv/bin/python .agent/scripts/verify_phase2a.py --run-id ten-run-moi --compare-run 20261009-phase2a-a
```

Run ID phải mới; chương trình từ chối ghi đè thư mục đã tồn tại. Verifier dùng preservation-before.json đã lưu để kiểm Phase1 giữ nguyên. Không chạy lại snapshot để thay baseline bảo toàn.

## Hợp đồng dữ liệu

`target_hour=s`: năng lượng mục tiêu của [s,s+1). `prediction_origin=s`: giờ trước vừa kết thúc, thông tin E(s−1) đã quan sát. Tất cả đặc trưng điện năng phải có hour_start ≤ s−1. Lịch của giờ mục tiêu biết trước, không dùng phép đo mục tiêu.

11 feature: lag1/2/3/24/168 kWh, rolling mean3/24 kWh, giờ trong ngày, ngày trong tuần, tháng, cờ cuối tuần. Lag lấy đúng timestamp; rolling cần đủ các giờ liên tiếp. Không fill/interpolate NULL hoặc dùng observed_energy_kwh của giờ thiếu làm nhãn giờ đầy đủ.

Lag168 có thể tham chiếu đúng một giờ cách đó168 giờ dù các giờ trung gian có thiếu; đây không phải shift chuỗi đã bỏ NULL. Rolling không bỏ qua các khoảng thiếu để ghép đủ số quan sát. Quy tắc đầy đủ/mask được chốt trước so sánh baseline.

Split trước lọc: floor(70%×N), floor(85%×N) trên toàn trục mục tiêu. Validation dùng lịch sử thực đã biết trước mỗi mốc dự báo one-step, kể cả các giờ Validation trước đó; không phải dự báo nhiều giờ liên tục từ một mốc duy nhất. Không fit transform hoặc lựa chọn tham số trên Test.

## Artifact hiện hành

Run chính `data/ml/runs/20261009-phase2a-a/`, rerun `20261009-phase2a-b/`.

- `train.csv`, `validation.csv`: nhãn mục tiêu và 11 feature đầy đủ, timestamp và thông tin origin.
- `holdout/test.csv`, `holdout/seal.json`: dữ liệu Test chuẩn bị sẵn, chỉ kiểm cấu trúc/đặc trưng/độ đầy đủ. Seal là quy tắc quy trình, không phải mã hóa hoặc ngăn truy cập bằng hệ điều hành. Không có dự báo/metric Test.
- `eligibility.csv`: giữ toàn bộ34.589 giờ, split/cờ/lý do loại. NULL không bị biến thành0.
- `predictions-validation.csv`, `metrics-validation.json`: chỉ4.727 timestamp Validation chung hai baseline và schema ML.
- `feature-schema.json`, `split-summary.json`, `manifest.json`: đơn vị, phiên bản, nguồn/hash/cutoff. Manifest là snapshot APPLIED_UNVERIFIED sau ghi file; verification.json là QA cuối.
- `verification.json`: run chính29/29; rerun30/30 có kiểm byte-identical9 artifact tất định.

Bản bàn giao: [.agent/qa/phase2a-20261009/review.md](../.agent/qa/phase2a-20261009/review.md). Dừng chờ Thy/GPT Web duyệt Phase2B và D09.
