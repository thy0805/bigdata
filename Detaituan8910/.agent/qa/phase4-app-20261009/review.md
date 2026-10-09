# Bàn giao Phase4 — kiểm ứng dụng

Tên đề tài: **Phân tích dữ liệu tiêu thụ điện năng và dự đoán nhu cầu sử dụng điện theo thời gian**.

Phạm vi hiện hành: [quyết định ứng dụng](../../decisions/20261009-phase4-app-scope.md). I04 tạm hoãn theo Thy. **Toàn Phase4 INCOMPLETE**, không tuyên bố PASS toàn giai đoạn. Nghiệm thu của Thy/GPT Web tách khỏi kết quả kiểm kỹ thuật.

## Trạng thái từng mục

| ID | Trạng thái kỹ thuật | Phạm vi đã kiểm | Bằng chứng |
| --- | --- | --- | --- |
| I01 | VERIFIED — tích hợp artifact | Hash raw→Flink→ML→model, 21 nguồn app, KPI và suy luận thật; không chạy lại toàn bộ pipeline | integration-faults.json; technical-verification.json |
| I02 | VERIFIED trong phạm vi dịch vụ | Start/stop/recovery, ownership, cổng bận, lỗi nguồn/package/model và localhost Windows/WSL; cold boot chưa kiểm | stop-app.json, app-off.json, app-recovered.json, stop-flink.json, flink-off.json, final.json, windows-runtime.json |
| I03 | VERIFIED | Ba tab, lọc biên/đảo/ngày thiếu, biểu đồ NULL, KPI Decimal, inference, cache, baseline; hai viewport | technical-verification.json; browser-verification.json; screenshots/ |
| I04 | DEFERRED | Chưa tạo DEMO_RUNBOOK, kịch bản, bài nói hoặc video | Quyết định phạm vi hiện hành |
| I05 | VERIFIED hồ sơ qua gate; Git publication kiểm riêng | Tổng hợp QA, bảo toàn, bản đồ evidence; gói kiểm qua package-verification.json, push/read-back kiểm ở hồ sơ Git | verification126/126; preservation1571/1571; package-verification.json |

## Kết quả kiểm chức năng

- Backend/AppTest: **67/67**, gồm đối chiếu KPI/ba nhóm đo phụ bằng Decimal, 34.589 khung giờ và 504 giá trị điện năng NULL, cache dữ liệu/model, không fit và không quét lại raw trong tương tác app. Bài kiểm kế thừa bộ regression Phase3, chạy mới trong QA4; không phải một kiểm toán độc lập mới toàn bộ thuật toán ML.
- Lineage/lỗi nguồn/môi trường: **17/17**. Bản sao nguồn riêng kiểm file thiếu và model bị đổi byte; app báo lỗi và dừng trước hiển thị kết quả. Phiên bản model/package không đúng bị từ chối.
- Runtime final được chọn: **24/24** = 20 kiểm dịch vụ Linux + 4 kiểm Windows. Dashboard và cluster đã dừng/khởi động lại bằng SIGTERM đúng ownership. Cổng có dịch vụ khác: từ chối start và stop, không tắt dịch vụ khác.
- Browser: **11/11**; tám ảnh được đọc trực tiếp. CSS viewport 1366×768 và 1920×1080, không tràn ngang. Một ảnh thử2049 không dùng làm evidence cuối.
- Tổng các assertion chức năng được chọn: **119/119**. Gate bàn giao/bảo toàn được ghi riêng, không cộng lịch sử kiểm thất bại vào số PASS.
- Gate cuối: **126/126** gồm119 assertion chức năng và7 kiểm bảo toàn/ảnh/link/SQL/sourcegate/phạm vi/mã vận hành. **1.571/1.571 file được giữ nguyên hash**, không có file nguồn/Office thay đổi hoặc mất.

Không phát hiện lỗi chức năng cần sửa trong tám file dashboard đã nghiệm thu. Phần bổ sung là [services.py](../../../operations/services.py) và [hướng dẫn vận hành I02](../../../operations/README.md); không đổi thuật toán hoặc giao diện đã khóa.

## Khởi động và phục hồi

App: http://localhost:8501/; Flink Web UI: http://localhost:8081/. Các địa chỉ localhost chỉ dùng trên máy Thy, không phải website công khai.

Launcher mới giữ cấu hình/log/PID/cache riêng trong `runtime/`, không sửa `pipeline/flink-conf` hoặc QA1. REST mới bind127.0.0.1, riêng Java dùng `-Djava.net.preferIPv4Stack=true`. Windows và Linux đều đã kiểm listener8081/8501 loopback. Cluster sau phục hồi có một TaskManager, hai slot, không có job đang chạy.

Dashboard vẫn có ba tab và suy luận đúng khi cluster Flink tắt: app đọc artifact giờ đã hoàn tất, không gọi Flink theo mỗi thao tác người dùng. Không mô tả đây là pipeline streaming trực tiếp hoặc pipeline chạy lại khi bấm dự báo.

Hai foreground holder đang dùng cho dịch vụ; chưa có autostart/daemon production. Không shutdown WSL hoặc Windows để kiểm cold boot. Dung lượng volume vật lý hiện hành nằm trong `windows-runtime.json`, không dùng dung lượng trống ảo của VHD làm bằng chứng.

## Dữ liệu và model giữ nguyên

UCI: một hộ tại Pháp, lịch sử 2006–2010. Dữ liệu gốc 2.075.259 phút; output Flink 34.589 giờ, 34.085 giờ đầy đủ, 504 giờ không đầy đủ. Điện năng của giờ không đầy đủ giữ NULL; tổng ghi nhận của các phút hợp lệ không được coi là điện năng đầy đủ.

HGB final `hgb-uci-hourly-v1.0-train-only`, Train22.513 mẫu, 11 feature đúng thứ tự; D09=max(0,prediction_raw). Không train/refit/tuning hoặc đánh giá lại toàn bộ Test. Chỉ kiểm suy luận một số mốc đã khóa, đối chiếu dự báo lưu.

| Model | MAE Test (kWh) | RMSE Test (kWh) |
| --- | ---: | ---: |
| HGB | 0.3220542588291146 | 0.4634874854716987 |
| Naive | 0.3857869426289034 | 0.58452003739288 |
| Seasonal Naive24 | 0.5036366739288308 | 0.7526481217054579 |

Nguồn: [metric2B2 đã khóa](../../../models/runs/20261009-phase2b2-a/metrics-test.json), cùng 4.590 timestamp. Đây là dự báo một bước cuốn chiếu với quá khứ thực tế được cập nhật, không phải dự báo nhiều tháng không nhận quan sát mới.

## Ngoại lệ và lịch sử kiểm

1. REST chi tiết job full gốc trả404 do lịch sử đã hết hạn. Manifest/verification Phase1 đã lưu trạng thái FINISHED/BATCH và hash nguồn; I01 dùng chuỗi artifact đã nghiệm thu, không tuyên bố job cũ hiện còn xem được trong Web UI. Không chạy lại full Flink để làm đẹp lịch sử.
2. `flink-recovered.json` là **lượt thử thất bại được giữ nguyên**: Java bind IPv4-mapped IPv6 không được Windows forward; assertion nhận diện listener cũng chưa xử lý dạng mapped. Sau sửa riêng JAVA_TOOL_OPTIONS, `final.json` và `windows-runtime.json` mới là evidence phục hồi hiện hành. Không sửa evidence cũ thành PASS.
3. Harness runtime có một lỗi đọc metadata `model_version` thay vì `version`, đã sửa trước ghi `flink-off.json`; artifact model không đổi.
4. Trình duyệt có rerun bất đồng bộ và lịch ngày nổi. Chỉ kết luận sau trạng thái cuối; ảnh đầu Test có bộ lọc15/04–24/04/2010 và mốc17:00, không ghi nhầm khoảng lọc chỉ một ngày.
5. Snapshot cũ: 924/933 file còn khớp, 9 cache runtime mất; 68 ngoại lệ lịch sử gồm16archive/52blobStorage. Không phục hồi cache hoặc sửa QA cũ. Snapshot QA4 kiểm riêng1.571 file sản phẩm/nguồn/Office, loại cache/log/PID và tài liệu điều phối được phép đổi; kết quả cuối trong preservation.json.

Preflight đầy đủ chứa inventory tiến trình của máy, chỉ lưu nội bộ. GitHub/ZIP chỉ có `preflight-public.json` và bằng chứng dự án đã chọn; không gửi toàn bộ process/network inventory, fixture lỗi, runtime cache hoặc Office.

## Nguồn để viết báo cáo và các phần chưa triển khai

[REPORT_EVIDENCE_MAP.md](REPORT_EVIDENCE_MAP.md) chỉ rõ số liệu, biểu đồ, kiến trúc và evidence Chương3–5/đồng bộ Chương2. Đây là bản đồ nguồn, chưa viết Word hoặc slide.

Chưa triển khai: nguồn công tơ sống, streaming replay, pipeline dự báo online tự động, forecast nhiều hộ, recursive nhiều bước, cold boot/autostart, deployment công khai, kiểm hiệu năng nhiều máy. Không biến các phần này thành chức năng đã hoàn thành.

## Bàn giao và điểm dừng

Đọc `verification.json`, `preservation.json`, `browser-verification.json`, `package-verification.json`, rồi đối chiếu JSON riêng từng mục. Gói local: `Phase4_App_QA_20261009.zip`; chỉ hồ sơ kiểm và mã vận hành, không phải bộ cài portable.

GitHub: repo thy0805/bigdata, đường dẫn `Detaituan8910/.agent/qa/phase4-app-20261009/`. Commit phát hành xác định qua Git/remote-readback sau push, không tự ghi một hash chưa tồn tại.

Dừng để Thy/GPT Web kiểm ứng dụng. I04 vẫn DEFERRED; Word/Chương2 của Hậu/PowerPoint giữ nguyên; không tự mở Phase5.
