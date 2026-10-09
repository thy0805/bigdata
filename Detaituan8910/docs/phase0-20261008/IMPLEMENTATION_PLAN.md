# Kế hoạch triển khai có cổng nghiệm thu

## Hiện hành — Phase3 chờ nghiệm thu

Thy đã nghiệm thu2B2 và duyệt3 theo [decision](../../.agent/decisions/20261009-phase3-approval.md). [Checklist3](../../.agent/qa/phase3-20261009/checklist.md) là canonicalU00–U05 VERIFIED:67/67 kỹ thuật+10/10browser+19/19handoff/runtime=96/96. Bước tiếp theo Thy/GPT Web duyệt ảnh/app/QA từ gói FINAL, không tự bắt đầu Phase4/Word/replay/video. Mốc chờ duyệt3 hoặc chưa app dưới đây là lịch sử.

## Hiện hành — Phase2B2 VERIFIED kỹ thuật

Thy đã nghiệm thu2B1 và duyệt2B2, chọn candidate không refit. Canonical [checklist2B2](../../.agent/qa/phase2b2-20261009/checklist.md), [bàn giao](../../.agent/qa/phase2b2-20261009/review.md). T00–T05 VERIFIED, pretest17/17, QA51/51, Test4590 một lần/final LOCKED; docprecheck62/62/17MD và documents-verification.json. Phase3 vẫn TODO/chưa duyệt. Bước tiếp theo bàn giao và chờ Thy/GPT Web nghiệm thu2B2/duyệt3, không tự mở app/Word/replay. Bảng tiến độ và các câu chờ2B2 bên dưới là lịch sử trước duyệt2B2.

Ngày cập nhật: 09/10/2026. Phase1 và Phase2A LOCKED qua nghiệm thu hồ sơ. [Phase2B1](../../.agent/qa/phase2b1-20261009/review.md) VERIFIED37/37, [scope](../../.agent/decisions/20261009-phase2b1-approval.md), [checklist](../../.agent/qa/phase2b1-20261009/checklist.md). HGB đúng một cấu hình, Train22513/Validation4727/11feature, D09 LOCKED; MAE0.3694427311570533/RMSE0.5306058050415966 kWh,0âm. Dừng chờ nghiệm thu2B1 và duyệt2B2, chưa Test metrics/model cuối/dashboard/Word. QA các pha cũ giữ nguyên; các trạng thái chờ2A bên dưới là lịch sử.

## 1. Nguồn và trạng thái

Nguồn quyết định: Thy; [DATA_AUDIT](DATA_AUDIT.md), [kiến trúc](TECHNICAL_ARCHITECTURE.md), [UI](APP_UI_SPEC.md), [quyết định mở](OPEN_DECISIONS.md). Checklist khảo sát thực thi: [R00–R05](../../.agent/qa/phase0-resume-20261009/checklist.md).

| Giai đoạn | Đầu vào | Sản phẩm và evidence bắt buộc | Trạng thái hiện tại | Cổng duyệt |
| --- | --- | --- | --- | --- |
| 0. Khảo sát/thiết kế | ZIP, môi trường, quyết định Thy | Full audit + hash/kiểm mẫu; môi trường WSL; năm MD đọc lại | VERIFIED; D01–D05 LOCKED | D01–D05 đã được Thy duyệt |
| 1. Pipeline Flink | Thiết kế được duyệt | Runtime, SQL job thật, hourly output, manifest/log/UI, kiểm độc lập | LOCKED F01–F06 | Thy/GPT Web đã nghiệm thu qua hồ sơ |
| 2A. Chuẩn bị và baseline | Hourly output đã nghiệm thu | Feature, split, baseline Validation và leakage/rerun tests | LOCKED M01–M04 | Thy/GPT Web đã nghiệm thu qua hồ sơ |
| 2B1. Học máy/Validation | Artifact2A bất biến | HGB Train-only, so Validation, D09, save/load/tái lập | VERIFIED37/37 | Chờ nghiệm thu và duyệt model/config cho2B2 |
| 2B2. Test/model chính thức | Model/config được duyệt từ2B1 | Đánh giá Test một lần; model chính thức/metric/provenance | TODO / chưa duyệt | Không tự mở Test |
| 3. Dashboard | Dữ liệu và model đã kiểm | App ba tab, UI/KPI/time filter tests | TODO | Thy duyệt UI |
| 4. Tích hợp | Pipeline/model/app | Chạy end-to-end lại, chứng minh Flink và app thật | TODO | Thy/GPT Web duyệt |
| 5. Demo/báo cáo | Kết quả thật | Video, hướng dẫn, ghi kết quả vào Ch3–5 đúng source | TODO | Nhóm duyệt trước nộp |

## 2. Giai đoạn 1 — trạng thái hiện hành

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence cần có | Phụ thuộc |
| --- | --- | --- | --- | --- | --- |
| F01 | Cài Java17/Flink2.3.0 và venv support tối thiểu | Apache + D01/D02 | VERIFIED | runtime-install/environment-final/apt-install.json | Thy yêu cầu agent cài giúp |
| F02 | Start/stop cluster và Windows Web UI | Apache local install | VERIFIED | REST/UI200, mộtTM/hai slot, browserDOM/job list; screenshot chỉsidebar vì khung hẹp | F01 |
| F03 | Xác thực bản TXT làm việc, schema và parser | ZIP/raw hash + D03/D04 | VERIFIED | rawhash, strictschema/header/quarantine/duplicate tests | F01 |
| F04 | Job nhỏ từ dữ liệu thật + ca biên kiểm thử | DATA_AUDIT và công thức | VERIFIED | 11jobs,82/82PASS;10k thật168giờ so14cột, rerun giống byte | F02/F03 |
| F05 | Chạy full UCI bằng Flink | F04 đã VERIFIED + Thy duyệt | VERIFIED | Hai jobFINISHED,2075259rows/34589hours/0parseerrors,25/25 mỗirun | SQL/smoke gốc không đổi; fullparser nhậnD/M/YYYY |
| F06 | Đối chiếu độc lập, chạy lại và handoff | Audit gốc + oracle độc lập | LOCKED | 484246trường và2075259phút mỗirun;grid/part byteidentical,26/26handoff | Thy/GPT Web đã chấp nhận qua hồ sơ |

Bước tiếp theo hiện hành: nghiệm thu2B1 và duyệt HGB/config cho2B2; không tự Test metrics/refit. Phase1 giữ nguyên. Hướng dẫn pipeline ở pipeline/README.md, model ở forecasting/TRAINING.md. Hai full đầu bị parser mẫu không nhận D/M/YYYY; launcher full sửa hai biểu thức đọc ngày, giữ SQL/smoke và phương pháp tính,11/11datecases đạt. Hai output lỗi không promote.

Các lệnh dưới đây là kế hoạch Phase0 lưu để tham khảo, không phải hướng dẫn chạy lại apt/download. Hai gói/runtime đã cài. Hướng dẫn launcher thực tế ở `pipeline/README.md`; dùng foreground `serve` thay start invocation ngắn.

```text
sudo apt-get update
sudo apt-get install openjdk-17-jdk-headless python3.12-venv
java -version
bin/flink --version
bin/start-cluster.sh
bin/sql-client.sh -f <duong_dan_job_da_kiem.sql>
bin/stop-cluster.sh
```

Việc tải/kiểm SHA-512 và giải nén binary vào thư mục user nằm giữa install Java và kiểm Flink. Không dùng glob hoặc đường dẫn unresolved để xóa bản cài cũ. Nếu tải/dependency lỗi, giữ log và sửa đúng nguyên nhân; không âm thầm thay công nghệ.

## 3. Bài kiểm thử Flink

Các fixture nhân tạo chỉ phục vụ kiểm công thức/ca biên, tách khỏi dữ liệu sản phẩm, không đưa lên dashboard hoặc làm số liệu thực nghiệm.

| Ca | Kỳ vọng |
| --- | --- |
| 60 phút công suất 1 kW | 1 kWh, complete=true |
| 59 phút hợp lệ và một phép đo thiếu | valid_count=59; energy_kwh=NULL; observed giữ tổng có thật |
| 60 dòng hoàn toàn thiếu phép đo | valid_count=0; observed và energy đều NULL; giờ vẫn tồn tại |
| Ranh giới xx:59 → giờ kế tiếp | Hai bucket đúng, không cộng nhầm |
| Header, dấu ?, ô rỗng, parse sai | Header nhận diện riêng; missing khác parse error; lỗi được ghi nhận |
| Timestamp trùng | Validation thất bại; không tăng đủ giờ bằng bản ghi trùng |
| Submeter 10 Wh mỗi phút đủ 60 phút | 0,6 kWh cho nhóm; count=60 |
| Residual âm | Raw residual và flag được giữ, không clamp |
| Giờ đầu raw / giờ đầy đủ mẫu | 17:00: 36 phút, observed 2,5337333333; 18:00: 60 phút, energy 3,6322 |
| Rerun vào run_id mới | Kết quả nội dung tương đương; không đọc/trộn output lần trước |

Full job: 2.075.259 dòng dữ liệu (không tính header), 34.589 giờ, 34.085 giờ đầy đủ, 504 giờ không đủ, 421 giờ không có công suất, 1.050 residual âm. Các số này là oracle đối chiếu từ audit, không hardcode vào logic để vượt test. So sánh count/timestamp/NULL đúng tuyệt đối, năng lượng tolerance tối đa 1e-8 kWh; nếu xuất DECIMAL làm tròn khác phải giải thích và thống nhất precision trước.

Phép tính Python tham chiếu độc lập được phép trong test GĐ1, đọc raw riêng, so tất cả giờ với Flink. Nó không tạo hourly data thay cho Flink dùng trong sản phẩm. Không thông báo F06 VERIFIED chỉ vì Job FINISHED.

## 4. Thiết kế Giai đoạn 2 — lịch sử trước duyệt2B1

M01–M04 đã VERIFIED với feature schema11 cột, không nội suy, nguồn giờ Flink duy nhất. Artifact `data/ml/runs/20261009-phase2a-a`, rerun `20261009-phase2a-b`. Naive Validation MAE0.45927228686270355/RMSE0.6828109073989009kWh; SeasonalNaive24 MAE0.6597176503772654/RMSE0.9503385628415242kWh, cùng4727 mẫu. Đối chiếu Decimal toàn bộfeature/Validation,965 file nguồn giữ hash; Test chưa đánh giá. [Hướng dẫn thực thi](../../forecasting/README.md). Các đoạn đề xuất dưới đây mô tả thiết kế gốc; cấu hình HGB/D09 cần duyệt trước lượt B.

Target E_(t+1), features chỉ có E_t và lịch/quá khứ tại mốc cuối giờ t. Đề xuất lag theo vị trí target: 1, 2, 3, 24, 168 giờ; rolling 3/24 giờ quá khứ; giờ mục tiêu và ngày trong tuần biết trước. Dùng timestamp join hoặc shift trên full hourly grid; không shift chuỗi đã drop giờ thiếu.

Naive dự báo bằng E_t, Seasonal Naive bằng năng lượng cùng giờ ngày trước. Một model đầu tiên đề xuất HistGradientBoostingRegressor, random_state cố định, không bắt buộc XGBoost/LSTM. Cấu hình ban đầu **early_stopping=False** để tránh validation ngẫu nhiên mặc định; chọn tham số trên validation theo thời gian, không nhìn test. [Tham số early_stopping/validation_fraction của sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html). Nếu đổi model, ghi quyết định và lý do trước train.

Đề xuất chia 70/15/15 theo trục giờ mục tiêu trước khi loại mẫu thiếu, publish ngày cắt và số mẫu thật sau tạo features. Không random split. Fit transform trên train; validation chọn cấu hình; chỉ dùng test cuối cùng để đánh giá. Validation/test được dùng lịch sử đã quan sát trước mỗi mốc dự báo trong chế độ one-step rolling; không phải dự báo multi-step mà biết trước tương lai. [Ví dụ chính thức sklearn về lag và đánh giá theo thời gian](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html).

Kiểm leakage2A đã đạt: feature điện năng trước target, origin đúng đầu khoảng mục tiêu, không nén trục/gap, future/Test perturbation không thay đầu ra Validation. Metric baseline có thật, chỉ Validation. Save/load học máy thuộc2B chưa triển khai; chưa có model đã fit hoặc metric Test.

## 5. Giai đoạn 3–5 và rủi ro

UI theo APP_UI_SPEC; kiểm KPI/coverage và forecast timestamp với artifacts nghiệm thu, cache không train/quét raw. Tích hợp chạy lại từ hướng dẫn trên máy, Web UI/log chứng minh job thật; quay video sau hệ thống hoạt động. Viết Word từ output thật ở GĐ5, không chỉnh Word ở Phase0.

Rủi ro: C còn ít dung lượng trong khi WSL nằm trên C; sudo/network khi cài; parser SQL cần smoke-test; source thiếu dài; timezone chưa rõ; model có thể không thắng baseline; cổng localhost có thể thay đổi. Mỗi rủi ro có evidence và stop condition; không cài lại WSL để chữa lỗi dependency Java/Python, không thêm tính năng ngoài phạm vi.

## 6. Điểm dừng Phase0 — lịch sử

Năm Markdown đã được đọc lại và kiểm bằng verifier; bàn giao Thy/GPT Web. Chỉ sau phê duyệt Giai đoạn 1 mới F01. Nếu quyết định ở OPEN_DECISIONS chưa được duyệt, giữ TODO; không tự coi đề xuất là LOCKED.
