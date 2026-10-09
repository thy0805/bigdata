# D — Kế hoạch bảng và hình, chưa chèn vào Word

Mọi số hiệu dưới đây là dự kiến theo thứ tự vị trí; W01 phải kiểm lại sau khi Thy duyệt. Không đổi/bỏ 4 bảng và Hình 1.1 hiện có. Không tạo ảnh đen hoặc chụp ảnh mới trong W00.

## Bảng dự kiến

| Số bảng | Mục | Caption / nội dung cần có | Nguồn chuẩn | Đơn vị, phạm vi và dẫn chiếu |
| --- | --- | --- | --- | --- |
| Bảng 3.1 | 3.2 | Thuộc tính dữ liệu UCI: đúng 9 tên cột Anh, nghĩa Việt, đơn vị | UCI S01 + DATA_AUDIT + bảng UI đã duyệt | Date/Time; kW công suất tác dụng; reactive kW **theo mô tả UCI**; V; A; Sub1–3 Wh/phút. Không tự đổi reactive sang kVAr. Văn bản trước bảng giải thích khác công suất/điện năng. |
| Bảng 3.2 | 3.4 | Kết quả kiểm tra chất lượng dữ liệu: 2.075.259 phút, 25.979 phút thiếu, 34.589 giờ, 34.085 đầy đủ, 504 không đầy đủ, 421 zero-valid-power-hour, 1.050 residual âm; timestamp liên tục/duy nhất | Phase1 full verification/audit | Toàn dataset 16/12/2006–26/11/2010. Phân biệt dòng/phút/giờ/ô thiếu; không cộng các nhóm có thể giao nhau. |
| Bảng 3.3 | 3.7 | Quy tắc tổng hợp: `observed_energy_kwh = SUM(power_kw)/60`; complete khi 3 count đều 60; `energy_kwh` NULL nếu không complete; sub Wh/1000; residual và cờ âm | SQL full `hourly_base`, INSERT hourly_sink | kWh/giờ mục tiêu; tổng một phần chỉ là ghi nhận. Ghi rõ giờ đầu/cuối partial. Không nhân 60 hoặc gán missing=0. |
| Bảng 3.4 | 3.8 | Thống kê điện năng trong một phạm vi xác định: số giờ, đủ/thiếu, tổng ghi nhận, mean giờ đủ, min/max giờ đủ và timestamp | `hourly-grid.csv`; cùng quy tắc `dashboard/data_service.py` | Phải trích thực tế read-only khi W01. Nếu dùng khoảng UI mặc định 20–26/11/2010 phải ghi rõ khoảng, không gọi toàn dataset. Không điền bảng bằng số ước lượng. |
| Bảng 4.1 | 4.4 | 11 đặc trưng, tên Anh/Việt, đơn vị, nguồn giờ quá khứ và encoding lịch | feature-schema.json | 5 lag 1/2/3/24/168, mean3/24, hour0–23,dow0–6,month1–12,weekend0/1; target không là feature. Dẫn bảng sau giải thích origin=s. |
| Bảng 4.2 | 4.5 | Ranh giới Train/Validation/Test, số giờ toàn trục, số mẫu hợp lệ, số bị loại | split-summary.json | Train trục: 16/12/2006 17:00–20/09/2009 12:00, 24.212 giờ/22.513 hợp lệ; Val: 20/09/2009 13:00–24/04/2010 16:00, 5.188/4.727; Test: 24/04/2010 17:00–26/11/2010 21:00, 5.189/4.590. Mốc hợp lệ đầu Train 23/12/2006 18:00; cuối Test 26/11/2010 20:00. |
| Bảng 4.3 | 4.7–4.8 | Cấu hình HGB Train-only đã khóa | model-config.json run2B1-a2 + train_hgb.py + final manifest | squared_error; learning_rate0.05; max_iter200; max_leaf_nodes15; min_samples_leaf30; l2_regularization1.0; max_bins255; early_stoppingFalse; random_state42; sklearn1.6.1. Không gọi là tuning tối ưu nếu không có thử nghiệm. |
| Bảng 4.4 | 4.9–4.10 | Sai số Test HGB và hai baseline, cùng 4.590 timestamp | metrics-test.json | kWh; HGB MAE0,3221/RMSE0,4635; Naive0,3858/0,5845; SeasonalNaive24h0,5036/0,7526. Giữ giá trị đầy đủ trong artifact, không accuracy%. Nêu selection bằng Validation trước Test. |
| Bảng 4.5 | 4.11 | Một số dự báo và quan sát thực tế, origin, interval mục tiêu và sai số | predictions-test.csv đã lưu | 5 dòng thực liên tiếp trong một khoảng được công bố, không chọn riêng các mẫu đẹp. Chỉ đọc kết quả cũ, không chạy Test lại. Không nhất thiết có bảng nếu chỉ lặp biểu đồ Hình4.1. |
| Bảng 5.1 | 5.2 | Thành phần và vai trò triển khai, phiên bản, đầu vào/đầu ra | SQL, final manifest, requirements, launcher | WSL2/Ubuntu,Java17,Flink2.3 SQLBATCH,Python3.12.3/Pandas2.2.3/NumPy2.2.6/sklearn1.6.1,Streamlit1.50/Plotly6.3; CSV/joblib. Mục2.14 chỉ mô tả văn xuôi, tránh lập bảng stack giống hệt hai lần. |
| Bảng 5.2 | 5.11–5.14 | Chức năng Tổng quan / Phân tích / Dự báo và điều kiện đầu vào | dashboard/app.py,data_service.py,charts.py tại0d7aa09 | Filter ngày, coverage/KPI/chuỗi/submeter; profile giờ/ngày/tháng; inference lịch sử và metric. Expander dữ liệu gồm9/11cột, không thêm tab chính. |
| Bảng 5.3 | 5.15–5.16 | Kết quả kiểm thử theo hạng mục và giới hạn | QA4 verification; UI guide technical/browser QA | I01 lineage17, backend67, runtime20+Windows4,browser11,handoff7 ở snapshot QA4=126; UI mới75 vàbrowser7 riêng. Chỉ ghi gate đã kiểm, không cộng trùng các phép kiểm giữa snapshot. |
| Bảng 5.4 (tùy chọn) | 5.17 | Phạm vi đã có/chưa có | Phạm vi phase4 và source map | Nếu đoạn hạn chế đã đủ thì bỏ bảng này. Một hộ lịch sử, no live2026/multistep/production; I04 DEFERRED,coldboot/autostart chưa kiểm, job cũ có thể hết REST lưu trữ. |

Tổng đề xuất: 12 bảng mới ưu tiên, 1 bảng giới hạn tùy chọn. Khi bỏ Bảng4.5 hoặc5.4, cập nhật lại SEQ/crossref thực chứ không để lỗ đánh số. Bảng lớn có thể chia nội dung hợp lý theo mục, không ép font nhỏ hoặc landscape tự động.

## Sổ vị trí hình dự kiến

Chiều rộng nội dung A4 là 15 cm theo lề mẫu. Khung 14,5 cm chừa khoảng an toàn. Kích thước là đề xuất; khi W02 phải giữ tỷ lệ thật hoặc điều chỉnh registry/caption, không kéo méo ảnh. Các trạng thái hiện tại đều là **PLANNED — W01 CHƯA TẠO PLACEHOLDER**. Sau W01 chuyển thành `PLACEHOLDER — CHƯA CHÈN ẢNH THẬT`, không VERIFIED bằng chứng ứng dụng.

| ID | Chương/mục | Số hình | Caption | Nội dung ảnh thật cần chụp ở W02 | Nguồn ứng dụng/artifact | Kích thước khung | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IMG-01 | 3.2 | Hình 3.1 | Cấu trúc dữ liệu tiêu thụ điện năng gốc từ UCI | Header và vài dòng nguồn thật, đủ9cột; không có thông tin máy/tài khoản không liên quan | `data/raw/household_power_consumption.txt`, chỉ đọc; không chụp file có thể lộ dữ liệu ngoài phạm vi | 14,5×6 cm | PLANNED; tùy chọn nếu Bảng3.1 đủ |
| IMG-02 | 3.7 | Hình 3.2 | Kết quả tổng hợp điện năng theo giờ bằng Apache Flink SQL BATCH | Bảng đầu ra hour_start/counts/complete/energy; có giờ thiếu để minh họaNULL; không dựng bảng bằng oracle thay output | Hourly-grid run full đã khóa. Không rerun để tái tạoJobID; statusFINISHED lấy evidence lưu nếu cần | 14,5×7 cm | PLANNED |
| IMG-03 | 3.9–3.11 | Hình 3.3 | Điện năng theo giờ trong khoảng lịch sử được lựa chọn | Biểu đồ với khoảng ngày hiển thị, trục kWh, khoảng thiếu giữ trống và coverage | Tab Tổng quan hoặc Phân tích dùng artifact thật | 14,5×8,2 cm | PLANNED |
| IMG-04 | 4.12 | Hình 4.1 | Điện năng thực tế và dự báo HGB trên một phần tập Test | Hai đường actual/predicted với khoảngTest cụ thể, trục kWh và timestamp. Caption không nói biểu đồ con chứa cả4.590 điểm nếu chỉ đang chọn một khoảng | Tab Dự báo + predictions-test.csv; model khóa | 14,5×8,2 cm | PLANNED |
| IMG-05 | 5.11 | Hình 5.1 | Giao diện tab Tổng quan của ứng dụng phân tích điện năng | Filter,KPI,biểu đồ và dự báo trong cùng trạng thái đã chọn; không SHA/JobID | Streamlit localhost8501, tabTổngquan | 14,5×8,2 cm | PLANNED |
| IMG-06 | 5.12 | Hình 5.2 | Giao diện tab Phân tích hiển thị thống kê theo thời gian | Biểu đồ profile giờ/ngày/tháng và trạng thái khoảng ngày thống nhất | Streamlit tabPhântích | 14,5×8,2 cm | PLANNED |
| IMG-07 | 5.13–5.14 | Hình 5.3 | Giao diện tab Dự báo và kết quả suy luận HGB tại một mốc lịch sử | Origin/giờmục tiêu/dự báo/quan sát nếu có/MAE-RMSE; không gọi dự báohiện tại | Streamlit tabDựbáo | 14,5×8,2 cm | PLANNED |
| IMG-08 | 5.11 | Hình 5.4 | Phần giới thiệu dữ liệu UCI và các đặc trưng dự báo trong ứng dụng | Expander mở, chọn subtab phù hợp. Nếu ảnh ghép2subtab cần ghi rõ ghép và cùngruntime; có thể chụp2ảnh và cập nhật số hiệu thay vì ép dài | Expander UI đã duyệt tại0d7aa09 | 14,5×9 cm | PLANNED |

Nếu Thy bỏ IMG-01, Hình3.2/3.3 phải thành3.1/3.2 theo vị trí còn lại. Nếu chia IMG-08 thànhhaihình, cập nhật số hình/crossref và xin chốt registry trước W02. Không tạo diagram mạng thay pipeline thật. Hình1.1 hiện có giữ nguyên, sơ đồ kiến trúc Ch5 có thể diễn giải bằng văn bản hoặc một diagram mới được duyệt riêng, không tự thêm cho đủ trang.

Mỗi vị trí ảnh W01 có label placeholder rõ ở registry và bản bàn giao. Văn bản có thể mô tả chức năng từ evidence nhưng không được nói “ảnh chụp chứng minh…” khi vẫn là khungđen. Word W01 không phải bản cuối để nộp khi chưa thay đủ ảnh.
