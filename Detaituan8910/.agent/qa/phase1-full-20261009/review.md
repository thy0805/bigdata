# Bàn giao F05–F06 — Apache Flink xử lý toàn bộ UCI

Ngày kiểm: 09/10/2026. **F05 và F06 VERIFIED về kỹ thuật. Nghiệm thu toàn bộ Giai đoạn 1 bởi Thy/GPT Web còn PENDING. Giai đoạn 2 chưa được duyệt.**

## 1. Phạm vi và kết quả

Apache Flink 2.3.0, Java 17, WSL2/Ubuntu hiện có thực hiện SQL BATCH trên bản TXT UCI nguyên bytes. Không cài lại môi trường, không Docker, không đổi thiết lập Windows, không restart. Không huấn luyện mô hình, dựng dashboard hoặc sửa Word. Python chỉ dựng trục giờ/sắp xếp đầu ra và tính tham chiếu độc lập trong QA; không thay Flink tổng hợp dữ liệu sản phẩm.

| Chỉ tiêu | Flink và kiểm độc lập |
| --- | ---: |
| Bản ghi dữ liệu theo phút | 2.075.259 |
| Header / tổng dòng gồm header | 1 / 2.075.260 |
| Cột nguồn / cột đầu ra giờ | 9 / 14 |
| Khoảng giờ | 34.589 |
| Giờ đủ 60 phút công suất hợp lệ | 34.085 |
| Giờ không đầy đủ | 504 |
| Giờ không có công suất hợp lệ | 421 |
| Phút thiếu phép đo / ô thiếu | 25.979 / 181.853 |
| Lỗi parse / nhóm timestamp trùng | 0 / 0 |
| Phút residual âm / residual nhỏ nhất | 1.050 / -2,4Wh |

Khoảng quan sát lịch nguồn: 16/12/2006 17:24 đến 26/11/2010 21:02. Timestamp giữ naive, không suy diễn múi giờ hoặc biến dữ liệu lịch sử thành nguồn công tơ trực tiếp. Giờ thiếu giữ `energy_kwh=NULL`, không nội suy; residual âm không clamp.

## 2. Hai lượt full thực tế

| Run ID | Job ID | Trạng thái REST | Thời gian job | SQL Client wall time |
| --- | --- | --- | ---: | ---: |
| 20261009T102201900234-full | 9307ab8abf4d8286245019045ed694ac | FINISHED | 168,015s | 193,495s |
| 20261009T102643175598-rerun | 170801766af83f1b80107c86d91cedfd | FINISHED | 138,444s | 150,508s |

Thời gian job lấy từ REST, wall time gồm khởi động SQL Client/planner và chờ job; không bao gồm toàn bộ kiểm độc lập/hash sau job. Đây là hai phép đo trên máy hiện tại, không phải benchmark so sánh công nghệ. Run ID theo đồng hồ Linux UTC; dữ liệu nguồn không bị chuyển sang UTC.

Mỗi lượt có thư mục riêng, không append hoặc đọc kết quả cũ. Cả CSV theo giờ và nội dung các part hourly/minutes/metrics giống byte giữa hai lượt. Tên part do Flink sinh có thể khác nhau.

## 3. Đối chiếu toàn bộ, không chỉ lấy mẫu

Mỗi run đạt 25/25 nhóm kiểm trong `verification.json` của run. Kiểm bàn giao/rerun/runtime đạt 26/26 trong `handoff-verification.json`. Regression parser ngày có 11/11 trường hợp đạt và job fixture FINISHED; fixture không phải dữ liệu sản phẩm.

- Raw được đọc lại độc lập bằng Python/Decimal cho từng run; tổng hợp tham chiếu chỉ dùng để kiểm, không ghi đè đầu ra Flink.
- So đủ 34.589 giờ × 14 cột = 484.246 trường mỗi run. Timestamp/count/boolean/NULL exact; không có sai khác vượt ngưỡng. Đã kiểm 2.188 ô NULL, không biến NULL thành 0.
- Sai số tuyệt đối lớn nhất của `observed_energy_kwh` và `energy_kwh`: **1e-15 kWh**, thấp hơn ngưỡng1e-8 kWh. Ba tổng nhóm đo phụ có sai khác 0 theo Decimal trên chuỗi xuất.
- Kiểm toàn bộ 2.075.259 dòng phút: timestamp/parse flag/missing count, các giá trị power/submeter/residual, dấu residual và các trường raw được giữ. Sai số residual tối đa6,6666666667e-15 Wh, không có dấu âm giả hoặc mất cờ âm.
- Bitmap timestamp xác nhận đủ mọi phút, không trùng; fingerprint đa tập SHA256 của 9 trường raw khớp. Đây là kiểm nội dung trường, tách khỏi checksum byte file nguồn.
- Tám nguồn DOCX/PDF/ZIP giữ checksum; raw và SQL/smoke F04 giữ nguyên. SQL thực thi khớp generator full, chỉ hai biểu thức đọc ngày khác bản mẫu.

Ba lớp kiểm: cấu trúc/schema/đếm/hash; ngữ nghĩa/đơn vị/NULL/residual so raw độc lập; runtime RESTFINISHED/log/CSV thực tế và rerun riêng. Không nghiệm thu chỉ từ exit code 0.

## 4. Lỗi phát hiện và sửa

Hai run đầu `20261009T101221593425-full` và `20261009T101440768187-rerun` có job FINISHED nhưng bị từ chối vì **1.716.480 parse_error**. Raw UCI chứa cả ngày D/M/YYYY và DD/MM/YYYY; mẫu10k ở tháng 12/2006 không bao phủ ngày/tháng một chữ số. Parser mẫu dùng vị trí chuỗi cố định nên không nhận đúng các dòng hợp lệ này.

Launcher full sửa riêng việc đọc từng thành phần ngày và padding trước cast, đồng thời cho ngày/tháng 1–2 chữ số. Giữ kiểm cast/roundtrip để bắt ngày không tồn tại. Regression kiểm cả `1/1/2007`, `01/01/2007`, ngày nhuận hợp lệ và ngày sai như 31/2. [Hàm SQL chính thức Flink2.3](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/functions/built-in-functions/).

Không thay công thức tính điện năng, điều kiện đủ 60 phút, xử lý missing, residual, strict CSV, source bytes hoặc smoke guard 25k. File `pipeline/hourly.sql` và `pipeline/run_smoke.py` giữ hash ban đầu; hai biểu thức parser được sửa trong launcher full, có SQL thực thi theo run để truy vết. Hai output bị từ chối không có hourly-grid.csv; log/parts và rejected.json được giữ, không dùng làm sản phẩm.

## 5. Artifact, checksum và vị trí

Thư mục sản phẩm chính:

`D:\Hoctap\bigdata\Detaituan8910\data\processed\runs\20261009T102201900234-full`

Bản chạy lại:

`D:\Hoctap\bigdata\Detaituan8910\data\processed\runs\20261009T102643175598-rerun`

Mỗi thư mục có `hourly-grid.csv` 3.217.812 byte, `flink-parts/`, `manifest.json`, `verification.json`. Manifest là snapshot sau chạy với APPLIED_UNVERIFIED; trạng thái QA cuối ở verification.json là VERIFIED. Không sửa ngược snapshot để giả vờ QA có trước thời điểm kiểm. Sau này chỉ dùng run có verification VERIFIED và được Thy/GPT Web chấp thuận.

| Artifact | SHA256 |
| --- | --- |
| hourly-grid.csv cả hai run | 8b03f1e3c82a5344c071a19f756cb7ec87fce18cc9a612cd63c4dcf4a8b5b2bc |
| Raw TXT | 4259c9d7ece5dbee9ab8d53682baac68d791c864f0f64a52b4043cb3b90894b7 |
| ZIP gốc | 9f84b46ade8a2d8e1286ec4b2b6c2987a45a755c59f263be3b3b3d10dfbda3ff |
| SQL F04 giữ nguyên | 424b084c2c776b1d253ca272527c61734a7e64f6be9df6e2dd2a55f96e3966f3 |
| Smoke launcher giữ nguyên | 35713f95b960b876efa7a8a4fc0a90c9ce69ffd7e34330f46e06b00c8f98b4e9 |

QA/log:

`D:\Hoctap\bigdata\Detaituan8910\.agent\qa\phase1-full-20261009`

Trong `runs/<run_id>/`: SQL thực thi, log SQL Client, REST details/plan/exceptions/config, metrics/manifest, resources.jsonl/resource-summary.json và verification.json. Manifest ghi checksum từng part và CSV; handoff-verification.json ghi thêm checksum script/SQL/log/manifest/QA. Log cluster hiện có vẫn ở QA smoke, không đổi cấu hình/log path của cluster đã kiểm.

## 6. RAM và dung lượng

Hai run ghi 253.340.074 byte sản phẩm mỗi run, tổng506.680.148 byte (~483,21 MiB), chưa tính manifest/QA nhỏ. Phần lớn là 246.870.071 byte dữ liệu phút giữ để kiểm và truy vết. Có thể dùng CSV giờ nhỏ cho giai đoạn sau; không cần app quét lại raw/phút.

Lấy mẫu mỗi 3 s: tổng RSS của các JVM quan sát cao nhất 3.904.696.320 byte ở run đầu (~3,64 GiB),4.115.120.128 byte ở rerun (~3,83 GiB). Đây là RSS cộng các tiến trình Java, có thể tính trùng trang nhớ dùng chung và bỏ qua đỉnh giữa hai lần đo; không phải RAM peak toàn Windows. Linux MemAvailable thấp nhất cả hai lượt 11.779.817.472 byte (~10,97 GiB); swap không dùng trong các snapshot được ghi.

Run đầu C free 28.201.496.576→27.961.999.360 byte, D free 242.620.379.136→242.337.009.664 byte. Rerun C free 27.961.802.752→27.958.829.056 byte, D free 242.336.989.184→242.080.296.960 byte. Giá trị cuối được kiểm lại bằng Windows Get-PSDrive: C27.956.445.184 byte (~26,04 GiB), D242.080.260.096 byte (~225,45 GiB) lúc17:32. Dùng volume C/D thật, không lấy dung lượng VHD ảo 1 TB. Các biến thiên còn chịu tác động Windows/tác vụ khác, không quy toàn bộ cho Flink.

## 7. Chạy lại và điểm dừng

Hướng dẫn có lệnh PowerShell trong `pipeline/README.md`: kiểm cluster trước, giữ holder serve nếu cần; chạy `pipeline/run_full.py --label full` hoặc `--label rerun`; đợi launcher exit 0 và manifest, rồi chạy `.agent/scripts/verify_full_pipeline.py <run_id>`. Không chạy hai full launcher cùng lúc. Launcher kiểm source hash/runtime/cổng job, dung lượng và timeout; mỗi lần tạo thư mục mới. Không cần sudo hoặc mật khẩu.

Windows REST cuối: Flink 2.3.0, một TaskManager/hai slot, 0 job running. Cluster foreground hiện còn được giữ, không phải service tự khởi động; nếu đóng holder/WSL phải kiểm lại, không suy ra nó luôn sống.

Giới hạn chưa kiểm: streaming/replay trực tiếp, watermark/late-data, checkpoint recovery, ML accuracy, UI/demo end-to-end và Word Chương 3–5. Batch group-by đã chạy không chứng minh các chức năng đó. Hai run đầu lỗi còn được giữ để truy vết, không bị xóa.

**Kết luận: F05/F06 đạt các kiểm kỹ thuật đã duyệt. Dừng tại Giai đoạn 1, chờ Thy/GPT Web nghiệm thu trước mọi công việc Phase2.**
