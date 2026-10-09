# Bàn giao F01–F04 — 09/10/2026

Phạm vi: Thy duyệt D01–D05 và F01–F04. Đã cài môi trường, chạy Flink SQL thật trên mẫu và kiểm parser. **Chưa chạy tổng hợp full UCI, chưa nghiệm thu F05/F06, chưa train/model/dashboard/Word.**

Handoff cuối `handoff-verification.json`37/37PASS: nguồn/hash,11manifests, SQLhash hiện hành, syntax, tài liệu read-back và cluster còn chạy. Disk16:38 C27823206400byte (~25,91GiB), D224378388480byte (~208,97GiB). Không dùng mật khẩu được gửi trong chat và không chép nó vào file/log dự án.

## Kết quả và ba lớp kiểm

| Lớp | Đã kiểm | Evidence và kết quả |
| --- | --- | --- |
| Cấu trúc | TXT nguyên bytes, CSV9 cột/header, 14 cột hourly, thiếu/thừa cột, metrics/quarantine/duplicate | inputs-manifest.json, smoke-verification.json; không ignore parse errors |
| Ý nghĩa | kW phút /60→kWh; NULL giờ thiếu; zero khác missing; subWh /1000; residual âm không clamp; giờ trống không nối | Oracle Decimal độc lập đọc nguồn, so toàn bộ14 cột của168 giờ mẫu; tolerance1e-10. Fixtures tách khỏi sản phẩm |
| Runtime | Flink2.3.0+Java17, cluster WebUI/REST Windows, SQL BATCH JobID/state/output, rerun | environment-final.json; smoke-verification.json **82/82 PASS**; lần kiểm cuối11 jobs,9FINISHED và2FAILED đúng fixture cấu trúc lỗi; grid rerun giống byte |

Job mẫu thật cuối: `012e738558e523488383da8e5456fe5d` FINISHED; rerun `3aa29bb5c6fee8b17a7e33504b9e1d35` FINISHED. Mẫu10.000 dòng/168 khoảng giờ,2 dòng thiếu phép đo (=14 ô thiếu), không lỗi parse/trùng. Job duration2,108giây và2,135giây chỉ là thời gian engine trên mẫu, không phải benchmark full UCI hoặc tổng thời gian startup/SQL Client.

Job planner lần đầu không có ID và SQL Client vẫn exit0. Đã bỏ CASE với nhánh NULL timestamp khỏi biểu thức parse, giữ TRY_CAST trực tiếp và validator định dạng/ngày, job mới đạt. Không tắt kiểm lỗi để vượt qua QA. Wrapper bắt buộc kiểm REST FINISHED + log không ERROR + validation riêng, không dựa riêng exit code.

Residual từng bị âm giả `-5,55e-17` do trừ DOUBLE tại giá trị0; fixture precision trước sửa có1 cờ âm sai. Đã tính tử số bằng DECIMAL `(power*1000 -60*sum_sub)` trước khi chuyển DOUBLE/chia60; fixture sau sửa0 cờ âm, các cờ âm thật giữ nguyên. Không clamp.

## Môi trường và dung lượng

- WSL2/Ubuntu24.04.5, usercute; Java17.0.20.1+1; Python3.12.3. Hai gói apt được cài theo Thy yêu cầu agent làm giúp. Không dùng/lưu mật khẩu; không sửa quyền Windows, PATH Windows, WSL/Docker/restart.
- Flink2.3.0 c0f8d1a `/home/cute/.local/opt/flink-2.3.0`, archive604828545byte trênD; runtime653947269byte (~624MiB) trênLinux/C. SHA512expected=actual trong runtime-install.json.
- Python venv thử trênD bị ensurepip error; venv cuối `/home/cute/.local/share/uci-flink-qa/venv` trênLinux tạo thành công, pip24.0 exit0. Chưa cài dependency model/UI/PyFlink.
- JM process1GiB, TM process2GiB, mộtTM/hai slot, parallelism1. Đây là ngân sách cấu hình JVM, không phải tổng RAM Windows/WSL và không chứng minh hiệu năng full job.
- C trước cài30785843200byte (~28,67GiB); snapshot16:28 còn27866664960byte (~25,95GiB). D trước225280733184byte,16:28 còn224424382464byte (~209,01GiB). Snapshot cuối trong environment-final.json. Chênh lệch dung lượng C có cả tác vụ nền Windows, không quy toàn bộ cho Flink.
- `data/raw/household_power_consumption.txt`132960755byte, SHA2564259c9d7ece5dbee9ab8d53682baac68d791c864f0f64a52b4043cb3b90894b7 khớp ZIP member. ZIP gốc và7 nguồn Word/PDF đều giữ hash.

## Web UI và khả năng chạy lại

[Flink Web UI](http://localhost:8081) đã trả HTTP200, DOM hiển thị phiên bản2.3.0, mộtTM/hai slot và job FINISHED. Snapshot browser khung bên hẹp chỉ thấy sidebar; không khẳng định đã kiểm trực quan mọi màn hình. Các FAILED hiển thị là fixture thiếu/thừa cột có chủ ý, không phải job dữ liệu thật thất bại.

REST trongWSL NAT bind0.0.0.0 để Windowslocalhost truy cập; Windowslistener chỉ::1:8081 được kiểm16:33. Không thêm Windowsportproxy/firewall, không mở dịch vụ công khai. RPC/TMbind127.0.0.1. Cluster được giữ bằng `cluster.py serve`; chưa tạo systemservice/autostart. READMEpipeline có start/status/stop/sample commands.

## Điểm còn mở

1. **Chờ Thy/GPT Web duyệt F05/F06** để chạy2.075.259 dòng, so fullhourcount/coverage/residual và tất cả giá trị với oracle; không dùng82 checks mẫu làm chứng cứ full dataset đã đạt.
2. D06–D10 cho ML/UI chưa duyệt. Không có model/KPI/MAE/RMSE hay app.
3. F04 wrapper cố ý chỉ cho QAinput≤25k dòng. Khi duyệt F05 mới thiết kế launcher fullinput riêng, không bỏ guard âm thầm.
4. Timestamp giữ lịch nguồn naive. BATCH group-by không chứng minh watermark/checkpoint/streaming replay đã nghiệm thu.

Nguồn công nghệ: [Apache downloads](https://flink.apache.org/downloads/), [CSV format2.3](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/connectors/table/formats/csv/), [SQL datatypes/TRY_CAST](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/data-types/), [config](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/config/).
