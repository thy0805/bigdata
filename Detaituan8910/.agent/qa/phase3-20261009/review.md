# Bàn giao Phase3 — Dashboard UCI

Phạm vi: [quyết định Phase3](../../decisions/20261009-phase3-approval.md). Phase2B2 đã được Thy/GPT Web nghiệm thu qua hồ sơ và tính lại metric. Dashboard được triển khai, kiểm kỹ thuật và kiểm bằng trình duyệt; nghiệm thu giao diện của Thy/GPT Web còn chờ. Không bắt đầu Phase4, streaming replay, video hoặc sửa Word.

## 1. Tệp ứng dụng

Thư mục [dashboard](../../../dashboard/README.md) gồm app.py, data_service.py, charts.py, style.css, serve.py, requirements.txt, .streamlit/config.toml và README.md. App có ba tab Tổng quan, Phân tích, Dự báo; bộ lọc ngày áp dụng chung. Backend kiểm nguồn, cache, KPI và inference; charts tạo biểu đồ từ artifact giờ đã nghiệm thu.

## 2. Dependency

Python 3.12.3 trong venv ML hiện có; Streamlit 1.50.0 và Plotly 6.3.0. [Install report](install-report.json) ghi 32 package UI/transitive mới. Pip dry-run và cài đặt có constraints; toàn bộ package cũ không đổi phiên bản, pin ML được giữ và pip check đạt. [Lock](install-lock.txt) ghi phiên bản 32 package, [pip report](pip-install-report.json) ghi nguồn cài. Không cài Docker, không reinstall hệ thống hoặc runtime Flink.

## 3. Khởi động

Chạy trong PowerShell:

```powershell
wsl.exe -d Ubuntu-24.04 --exec /home/cute/.local/share/uci-forecast/venv/bin/python -B /mnt/d/Hoctap/bigdata/Detaituan8910/dashboard/serve.py
```

Windows mở [http://localhost:8501](http://localhost:8501). Launcher kiểm cổng, chỉ bind127.0.0.1 và không dừng dịch vụ khác. Giữ cửa sổ chạy; Ctrl+C để dừng. Phiên foreground không phải autostart/production service. Hướng dẫn chi tiết tại [README](../../../dashboard/README.md).

## 4. Runtime

HTTP health từ Windows đạt200/ok; trình duyệt mở app, chuyển cả ba tab, lọc ngày, chọn giờ và chạy inference bằng nút thật. 127.0.0.1 hoạt động với Windowslocalhost ở lượt này, không cần bind0, portproxy hoặc mở firewall. Flink cluster không là điều kiện mở dashboard: jobFINISHED/BATCH hiển thị từ manifest lịch sử, không khẳng định cluster đang chạy.

## 5. Ảnh app thật

| Tab | 1920×1080 | Laptop1366×769 |
| --- | --- | --- |
| Tổng quan | [Ảnh](screenshots/overview-1920.jpg) | [Ảnh](screenshots/overview-laptop-final.jpg) |
| Phân tích | [Ảnh](screenshots/analysis-1920-final-v3.jpg) | [Ảnh](screenshots/analysis-laptop-final.jpg) |
| Dự báo | [Ảnh](screenshots/forecast-1920-final.jpg) | [Ảnh](screenshots/forecast-laptop-final.jpg) |

[Chất lượng dữ liệu](screenshots/analysis-quality-1920.jpg), [mốc đầu Test](screenshots/first-test-forecast.jpg). Ảnh lấy trực tiếp từ trình duyệt, không dùng mockup. Viewport được xác nhận qua DOM; devicePixelRatio1.1 làm kích thước yêu cầu khác CSS viewport, đã dùng clip rõ để không cắt cạnh phải. Laptop cuộn dọc để xem phần dưới; không tràn ngang.

Ảnh thử cũ, ảnh trắng do render chưa xong và ảnh biểu đồ tháng trước sửa không được chọn làm bằng chứng cuối hoặc đưa vào gói bàn giao.

## 6. QA và lỗi

[Kiểm kỹ thuật cuối](technical-verification-v3.json):67/67, gồm AST/no-fit, sourcegate21 hash, schema/mask, cache hit/invalidation, oracle Decimal, gap/empty, đầu-cuối, label perturbation, input11feature, real model, AppTest10lượt và bảo toàn976 file.

[Kiểm trình duyệt](browser-verification.json):10/10 hiện hành, chuyển tab/filter/inference/baseline, laptop/16:9 và nhãn tháng. Một phép kiểm ban đầu dùng locator chữ không giới hạn tab đã chọn card Tổng quan đang ẩn; hồ sơ giữ lần này trong history, kiểm lại trong tab Dự báo đang hiển thị đạt. Đây là lỗi locator QA, không phải sai số mô hình.

Lỗi hiển thị phát hiện: Plotly tự nhận chuỗiYYYY-MM là thời gian, khi chỉ có một tháng đã xuất hiện tick dưới microsecond. Trục tháng đã đổi thành category và kiểm bằng oracle/ảnh. Source module được nạp lại bằng khởi động lại riêng app, không restart WSL/Windows. Captions có opacity mặc định0.6 đã đổi thành1, card nền trắng; dataframe/button sử dụng API width hiện hành.

Chưa phát hiện lỗi chức năng trong phạm vi đã kiểm. Chưa kiểm mobile hoặc máy chiếu vật lý; chỉ kiểm viewport1920×1080. Chưa đóng gói portable/autostart. [Tổng hợp QA](verification.json)96/96=67kỹ thuật+10browser+19handoff/runtime; không thay thế kiểm kỹ thuật/model các phase trước. Handoff lần đầu bị gate chặn vì thiếu cách ghi4.590 trong review và phép tách header context sai; đã bổ sung phạm vi mẫu và sửa delimiter đọc block hiện hành. Hồ sơ FAIL giữ trong attempts/handoff-a1, không có source/model/data lỗi.

## 7. KPI và dự báo

Khoảng mặc định20–26/11/2010: điện năng ghi nhận190.54173333333333404kWh;165/166giờ đầy đủ, trung bình1.1545151515151515kWh/giờ, đỉnh5.626833333333334kWh tại20/11/201018:00. Có9.903/9.960phút hợp lệ, coverage99.42771084337349%;57phút ở biên chưa ghi nhận, không phải57phút mất phép đo trong file. Oracle đọc CSV giờ bằng Decimal độc lập với Pandas, kiểm toàn bộ/biên/khoảng mặc định/đảo ngày và từng nhóm đo.

Inference tại timestamp đầu/giữa/cuối Test khớp output đã lưu trong precision1e-10 của kiểm app; input đúng thứ tự11feature, không có nhãn. Đổi nhãn mục tiêu thành−9999 không đổi dự báo. Backend dùng sharedpredictor/D09, không fit. Nút tại26/11/201020:00 hiển thị1.931kWh; thực tế1.164kWh chỉ để đối chiếu sau dự báo.

Metric chính thức đọc artifact2B2 trên toàn bộ4.590mẫu, không tính lại hoặc lựa chọn mô hình:

| Model | MAE kWh | RMSE kWh | Số mẫu |
| --- | --- | --- | --- |
| HGB | 0.3220542588291146 | 0.4634874854716987 | 4590 |
| Naive | 0.3857869426289034 | 0.58452003739288 | 4590 |
| Seasonal Naive24 | 0.5036366739288308 | 0.7526481217054579 | 4590 |

## 8. Bảo toàn và lineage

ModelSHA-256 `f4c33c54b026a3c81312dff9c9623c7dad33a3f9df4986ecd8693b7267d8749c` tại models/final/hgb-uci-hourly-v1.0-train-only; Train-only22.513, scikit-learn1.6.1, schema11/D09 giữ nguyên. HourlySHA `8b03f1e3c82a5344c071a19f756cb7ec87fce18cc9a612cd63c4dcf4a8b5b2bc`; TestSHA `f9785b91f46c43bbb22c08c98294cd32739f75e5df0218e355baa53d5fbd3574`. Sourcegate kiểm chuỗi Flink→Phase2A→final→prediction/metric; model/schema/hash sai hiển thị lỗi và dừng.

67/67 ghi fit_calls0, forbidden_io0 và976/976file trước Phase3 giữ hash, gồm nguồn, pipeline, data, model, Word và QA cũ. Không đọc dữ liệu phút để vẽ app, không chạy lại Flink, train hoặc official Test evaluation. Kiểm inference vài mốc và AppTest không phải một đợt đánh giá/tuning Test mới.

Ngoại lệ audit lịch sử9cacheFlink mất và68ngoại lệ=16archive+52blobStorage vẫn là ngoại lệ tại snapshot cũ; không phục hồi cache hay sửa ngược hồ sơ. Trạng thái VERIFIED là tại thời điểm kiểm, không cam kết file tạm bất biến mãi.

## 9. Giới hạn và nghiệm thu

Thiết kế giữ Minimal nền sáng/card trắng, không thêm GSAP/ảnh trang trí. Bộ lọc rỗng hoặc thiếu giờ cho trạng thái giải thích; không thay thiếu bằng0 hoặc nối gap. Giới hạn: một hộ lịch sử, không xác minh timezone/DST, không công tơ trực tiếp, không dự báo hiện tại2026 và không dự báo nhiều tháng thiếu quan sát mới. Scientific CSV guidance được dùng để giữ đơn vị, coverage và phân biệt artifact Flink với oracle.

Nguồn mô tả nhóm đo: [UCI chính thức](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption). Cơ chế cache/test tham khảo [Streamlit caching](https://docs.streamlit.io/develop/concepts/architecture/caching), [AppTest](https://docs.streamlit.io/develop/api-reference/app-testing); gap theo [Plotly line charts](https://plotly.com/python/line-charts/). Package cục bộ1.50.0 là nguồn kiểm API đang chạy, không giả định mọi API mới trong tài liệu1.65 áp dụng.

Phase3 VERIFIED kỹ thuật và hình render, chưa LOCKED nghiệm thu giao diện. Gói gửi GPT Web: Phase3_Dashboard_Handoff_20261009_FINAL.zip; gói trước FINAL là snapshot trước checkpoint cuối. Có model cuối, featureTest, outputTest, hourly và ảnh thật; không phải portable app. Manifest của gói FINAL là nguồn ưu tiên cho checksum file sau checkpoint; final-package-verification.json ghi kết quả đọc lại. Điểm dừng: Thy/GPT Web duyệt ảnh/app/QA. Chưa Phase4, streaming replay, video, Word hoặc Chương2 của Hậu.
