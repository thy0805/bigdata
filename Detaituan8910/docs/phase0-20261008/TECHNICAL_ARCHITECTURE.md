# Kiến trúc kỹ thuật đề xuất

## Hiện hành — Phase3

[App3tab](../../dashboard/README.md) chạy Streamlit1.50.0/Plotly6.3.0 trong venv ML WSL hiện có;32dependency mới, pin ML cũ không đổi. Windowslocalhost8501 đã kiểm với Linuxbind127.0.0.1. Sourcegate21hash/schema/QA kiểm artifact trước cache; model thật dùng sharedpredictor, không train/scan raw/run pipeline. [QA3](../../.agent/qa/phase3-20261009/review.md)67/67+browser10/10; không đòi cluster đang chạy, job state là evidence lịch sử. Hệ thống chưa autostart/portable/Phase4; mô tả chưa UI và bind0 bên dưới không là hiện trạng dashboard.

## Hiện hành — Phase2B2

[Model cuối](../../models/final/hgb-uci-hourly-v1.0-train-only/manifest.json) LOCKED, cùng estimator Train22513/11 feature/D09 không refit. [Bàn giao](../../.agent/qa/phase2b2-20261009/review.md) QA51/51/Test4590; [hướng dẫn inference](../../forecasting/FINAL_EVALUATION.md) ưu tiên TRAINING cũ khi dùng model cuối. Dùng runtime đã pin; không đổi pipeline hoặc cài mới. App vẫn PROPOSED, Phase3 chưa duyệt. Các mô tả môi trường/tiến độ bên dưới là lịch sử trước2B2; thiết kế chưa triển khai không trở thành hiện trạng.

Ngày cập nhật: 09/10/2026. Phase1 và Phase2A LOCKED qua nghiệm thu hồ sơ. HGB Train-only/Validation2B1 VERIFIED37/37,11 feature/split/eligibility giữ nguyên. D09=max(0,raw) LOCKED, dùng chung predictor, lưu raw/final. [Handoff2B1](../../.agent/qa/phase2b1-20261009/review.md), [hướng dẫn](../../forecasting/TRAINING.md) ưu tiên các đoạn đề xuất Phase0/2A bên dưới. Chưa Test/model cuối/UI.

Runtime ML: Python3.12.3, venv `/home/cute/.local/share/uci-forecast/venv`; NumPy2.2.6/Pandas2.2.3/sklearn1.6.1 và dependency pin giữ nguyên. Code2A/output/QA bất biến. Mới: `forecasting/train_hgb.py`/`predictor.py`, candidate ở `models/runs/20261009-phase2b1-a2/` và b, verifier `.agent/scripts/verify_phase2b1.py`. Không tổng hợp lại raw cho ML, không sửa pipeline. Dừng chờ nghiệm thu2B1/duyệt2B2.

Runtime Java17.0.20.1/Python3.12.3/Flink2.3.0 c0f8d1a tại `/home/cute/.local/opt/flink-2.3.0`, SHA512 khớp; mộtTM/hai slot, JM1GiB/TM2GiB process memory, Windowslocalhost8081. `pipeline/run_full.py` xuất từng run ở `data/processed/runs`, raw/output/log trênD. Python chỉ reindex/oracle, không tổng hợp sản phẩm thay Flink. Parserfull hỗ trợ D/M/YYYY và DD/MM/YYYY, strictcast/roundtrip; SQL/smoke gốc nguyênhash. Không service tự khởi động/model/UI. Nguồn chuẩn `.agent/qa/phase1-full-20261009/`; các đoạn cài/đề xuất Phase0 bên dưới là lịch sử thiết kế, không hướng dẫn reinstall.

## 1. Snapshot Phase0 trước cài — lịch sử lúc15:43

Evidence: [environment.json](../../.agent/qa/phase0-resume-20261009/environment.json), [ghi nhận bổ sung](../../.agent/qa/phase0-resume-20261009/environment-extra.md).

| Thành phần | Kết quả trực tiếp |
| --- | --- |
| Windows | 10.0.26200.9457 |
| WSL | 2.7.14.0, kernel 6.18.33.2-2 |
| Distro | Ubuntu-24.04, Running, VERSION 2 |
| Linux | Ubuntu 24.04.5 LTS, x86_64 |
| User | cute, uid 1000, thuộc nhóm sudo |
| Python Linux | 3.12.3, /usr/bin/python3 |
| pip / ensurepip | Chưa có |
| venv | Có module; chưa có gói python3.12-venv để bootstrap pip |
| Java Linux / JAVA_HOME | Không có executable/gói OpenJDK trong các vị trí đã kiểm; JAVA_HOME rỗng |
| Flink / PyFlink | Không thấy command, package Python hoặc thư mục cài trong /opt, /usr/local, home/.local đã kiểm |
| RAM Linux nhìn thấy | MemTotal 16.215.716 KiB, khoảng 15,46 GiB |
| Trống ổ C / D lúc kiểm | Khoảng 18,34 / 209,90 GiB |
| Windows Python / Java | Miniconda 3.13.13 / Oracle Java 8u401; giữ nguyên |

WSL đọc được `/mnt/d/Hoctap/bigdata/Detaituan8910` và ZIP trong `/mnt/c/Users/thy/Downloads`. Linux gọi cmd.exe Windows thành công. Windows nhận HTTP 200 và token đúng từ máy chủ kiểm tra tạm trong WSL; máy chủ đã kết thúc exit 0. HTTPS từ Linux đến PyPI trả 200. Đây là kiểm kết nối, không phải Flink Web UI đã chạy.

Cổng 8081/8501 chưa thấy listener Windows hoặc Linux tại thời điểm kiểm. WSL1 báo optional component chưa bật; không cần bật WSL1 cho phương án WSL2. Lỗi đăng ký WSL cũ được coi là đã giải quyết ở mức runtime do Linux thực thi thành công; không suy đoán chuỗi thao tác sửa của phiên khác.

## 2. Thiết kế được duyệt và kế hoạch cài tại Phase0

Đề xuất Apache Flink **2.3.0 standalone + Java 17 Linux**, khởi động cluster cục bộ và gửi SQL job bằng SQL Client. Apache khuyến nghị Java 17, hỗ trợ Java 21 ở mức experimental; không dùng Java Windows 8 làm runtime Linux. [Java compatibility](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/java_compatibility/), [bản phát hành](https://flink.apache.org/downloads/).

Sau khi được duyệt, cài tối thiểu `openjdk-17-jdk-headless` và `python3.12-venv` trong Ubuntu. Gói venv phục vụ môi trường Python riêng; không cần thay Python hệ thống hoặc cài pip toàn cục. Nếu sudo yêu cầu mật khẩu, Thy nhập trong terminal; không gửi mật khẩu vào chat. Không thay PATH/JAVA_HOME Windows, không restart.

Flink binary đề xuất đặt `/home/cute/.local/opt/flink-2.3.0`. Ghi checksum SHA-512 theo Apache trước giải nén và phiên bản JDK thực tế vào manifest. JAVA_HOME chỉ thiết lập trong launcher Linux của dự án. Không chọn bản master/snapshot hoặc tải lại các công cụ đã có. Cài đặt chưa được thực hiện ở lượt này.

PyFlink **2.3.0** là lựa chọn tương thích về gói phát hành với Python **3.12 x86_64 Linux**: [metadata PyPI](https://pypi.org/pypi/apache-flink/2.3.0/json) có wheel cp312 manylinux; [hướng dẫn Apache](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/getting-started/local_installation/) cũng liệt kê Python 3.12. Tuy nhiên chưa thử giải dependency/cài/import trên máy. Với SQL Client, PyFlink không bắt buộc; đề xuất chưa cài để giảm phụ thuộc ở bước đầu. Nếu sau này cần Python API, dùng venv riêng và phiên bản Flink/PyFlink khớp 2.3.0, kiểm thêm dependency và job smoke-test; không coi có wheel là runtime đã tương thích.

## 3. Luồng xử lý và trách nhiệm

`UCI ZIP/TXT → Flink đọc, xác thực, tổng hợp giờ → CSV theo giờ + manifest → Python EDA/đặc trưng/mô hình → Streamlit/Plotly`.

| Lớp | Trách nhiệm | Không làm |
| --- | --- | --- |
| Chuẩn bị đầu vào | Xác minh hash, giải nén một bản TXT làm việc; giữ raw gốc | Không tiền tổng hợp giờ bằng Pandas |
| Flink SQL | Đọc CSV phân cách ;, xử lý thiếu/kiểu số/thời gian, tổng hợp và cờ độ phủ | Không huấn luyện mô hình |
| Dữ liệu trung gian | Các file part CSV của Flink, manifest job/source/version, schema rõ | Không ngầm coi part có thứ tự toàn cục |
| Python | Kiểm đầu ra, dựng trục giờ, EDA, lag/rolling và mô hình | Không che lỗi thiếu hoặc nối qua gap |
| Dashboard | Đọc dữ liệu giờ và model đã lưu, lọc và suy luận | Không quét ZIP hoặc train lại khi đổi tab |

Đề xuất dùng Python 3.12 trong một venv WSL cho ML/UI ở các giai đoạn sau, cùng môi trường chạy xuyên suốt; Windows dùng trình duyệt để xem. Chưa cài các package ML/UI trong Giai đoạn 1 nếu chưa cần.

## 4. Thiết kế job đầu tiên

Nguồn filesystem mặc định hữu hạn; chọn `execution.runtime-mode = BATCH` cho raw file cố định. Flink hỗ trợ batch/streaming nhưng dữ liệu hữu hạn không đồng nghĩa bắt buộc batch. [Filesystem](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/connectors/table/filesystem/), [execution mode](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/execution_mode/).

Đọc chín trường dạng STRING để `?` và ô rỗng không gây mất bản ghi. Metadata header phải nhận diện bằng cả chín tên cột đúng, không coi header là bản ghi lỗi. Không giả định có tùy chọn CSV bỏ dòng đầu khi chưa kiểm; không bật ignore-parse-errors để âm thầm bỏ dữ liệu. CSV và filesystem có sẵn cho SQL Client. [CSV format](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/connectors/table/formats/csv/).

Parse timestamp lịch nguồn, chuyển chuỗi số có kiểm soát sang DECIMAL; `?`/rỗng thành NULL. Bản ghi cấu trúc lỗi làm kiểm thử thất bại; timestamp/numeric sai khác missing phải được đếm và xuất quarantine, không biến lỗi parse thành 0. Công thức đầy đủ theo [DATA_AUDIT](DATA_AUDIT.md).

Nhóm theo đầu giờ `[h,h+1)` tính count, distinct minute count, valid count, năng lượng ghi nhận, năng lượng đầy đủ, ba nhóm đo phụ và residual flag. Không bỏ giờ thiếu trước export. Duplicate timestamp phải làm cổng xác thực thất bại; không tự lấy trung bình các bản ghi trùng.

Vòng đầu dùng group aggregation trên timestamp hour bucket. Chưa có job kiểm Event Time watermark, Allowed Lateness hoặc checkpoint recovery. Không ghi những cơ chế đó đã demo trong báo cáo. Replay lịch sử dạng streaming chỉ xem xét sau pipeline bounded ổn định và được duyệt riêng; không gọi replay là công tơ trực tiếp.

Đầu ra Flink là thư mục CSV nhiều part có schema khai báo trong manifest, không dùng ORDER BY toàn bộ raw data hoặc kỳ vọng một file có header/thứ tự sẵn. Python sau đó đọc các part, kiểm unique hour, sắp xếp/reindex trục giờ và có thể lưu Parquet cho UI; không tính lại tổng hợp phút cho sản phẩm.

## 5. Vị trí dữ liệu và dung lượng

Project nằm trong `D:\Hoctap\bigdata\Detaituan8910` (WSL `/mnt/d/Hoctap/bigdata/Detaituan8910`). Dữ liệu thực tế ở `data/raw`, `data/processed/runs/<run_id>`; log/QA trong `.agent/`, code ở `pipeline/`. Run không đạt kiểm dữ liệu không có hourly-grid để sử dụng. Trạng thái thực thi manifest là snapshot APPLIED_UNVERIFIED; kết quả QA sau đó ở verification.json, không sửa lịch sử manifest để giả vờ đã kiểm trước khi kiểm.

WSL distro hiện nằm trên C tại `C:\Users\thy\AppData\Local\wsl\{2fb8f216-2366-481a-b3a3-7dffcdeccdb6}`. Linux df báo dung lượng filesystem ảo gần 1 TB không đồng nghĩa ổ C thật còn dung lượng đó. Không di chuyển distro trong lượt này. Đề xuất giữ TXT 133 MB và output trên D, chỉ runtime/venv nhỏ trong ext4 Linux; theo dõi C trước tải dependency, không tăng .wslconfig hoặc RAM tự động. Chạy file /mnt/d có thể khác hiệu năng ext4; đo ở Giai đoạn 1 rồi mới cân nhắc copy, không kết luận tốc độ trước thử.

## 6. Quan sát và nghiệm thu

Khởi đầu một TaskManager, hai slot, song song mặc định 1; đề xuất JobManager khoảng 1 GiB, TaskManager 2 GiB, không tuyên bố mức này đã đủ cho full job. Kiểm memory và log trong smoke-test trước thay cấu hình.

Cluster dùng `bin/start-cluster.sh`; SQL dùng `bin/sql-client.sh -f <script.sql>`; dừng bằng `bin/stop-cluster.sh`. Windows truy cập `http://localhost:8081`; ghi lại REST overview/jobs, Job ID, trạng thái FINISHED, plan, log và hash đầu ra. [Apache local installation](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/getting-started/local_installation/), [WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking).

Không mở firewall LAN hoặc expose internet để demo. Cổng 8501 dành UI giai đoạn sau. Probe localhost hiện đạt không bảo đảm 8081/8501 sẽ luôn trống; kiểm lại lúc chạy. Chi tiết nghiệm thu và cổng duyệt ở [IMPLEMENTATION_PLAN](IMPLEMENTATION_PLAN.md).
