# Vận hành dịch vụ dự án

`services.py` chạy trong Ubuntu-24.04 trên WSL2, dùng Flink2.3.0/Java17 và môi trường Python đã khóa. Không cài thêm package, huấn luyện, tổng hợp lại dataset hoặc thay artifact.

## Khởi động từ PowerShell

Dashboard và Flink là hai tiến trình riêng. Mỗi lệnh `start` cần một terminal giữ mở; đây không phải dịch vụ tự khởi động cùng Windows.

```powershell
wsl -d Ubuntu-24.04 -- python3 -B /mnt/d/Hoctap/bigdata/Detaituan8910/operations/services.py app start
```

App: http://localhost:8501/. Dashboard đọc dữ liệu giờ và model đã khóa; không cần cluster Flink chạy để xem artifact và thực hiện suy luận.

```powershell
wsl -d Ubuntu-24.04 -- python3 -B /mnt/d/Hoctap/bigdata/Detaituan8910/operations/services.py flink start
```

Flink Web UI: http://localhost:8081/. Lệnh chỉ khởi động cluster một TaskManager/hai slot; không nộp job hay tạo dữ liệu sản phẩm mới. Job đã hoàn tất có thể hết hạn trong lịch sử Web UI. Hồ sơ job gốc nằm trong manifest và QA Phase1.

## Trạng thái và dừng

```powershell
wsl -d Ubuntu-24.04 -- python3 -B /mnt/d/Hoctap/bigdata/Detaituan8910/operations/services.py app status
wsl -d Ubuntu-24.04 -- python3 -B /mnt/d/Hoctap/bigdata/Detaituan8910/operations/services.py flink status
wsl -d Ubuntu-24.04 -- python3 -B /mnt/d/Hoctap/bigdata/Detaituan8910/operations/services.py app stop
wsl -d Ubuntu-24.04 -- python3 -B /mnt/d/Hoctap/bigdata/Detaituan8910/operations/services.py flink stop
```

`status` báo cổng và PID được nhận diện theo executable, owner và đường dẫn dự án; occupied không đồng nghĩa dịch vụ đã sẵn sàng. `stop` chỉ gửi SIGTERM tới tiến trình đã xác minh; từ chối dừng cluster có job đang hoạt động. Không force-kill hoặc tự dừng WSL.

## Lỗi và giới hạn đã kiểm

- Cổng8081/8501 bận: từ chối khởi động; không tự đổi cổng hoặc tắt tiến trình khác.
- Không có tiến trình đúng ownership: từ chối stop dù cổng có listener.
- Thiếu hoặc sai checksum artifact: app báo lỗi nguồn và không hiển thị tab/kết quả thay thế.
- Sai phiên bản package/model: artifact gate từ chối. Không tự nâng cấp môi trường để bỏ qua gate.
- Cấu hình runtime mới nằm trong `.agent/qa/phase4-app-20261009/runtime`; không sửa cấu hình pipeline đã nghiệm thu. REST bind127.0.0.1 và Java `preferIPv4Stack=true` khắc phục forwarding loopback trong phiên WSL đã kiểm. Không thay firewall/portproxy.
- Log/PID/cache runtime không phải artifact bất biến. Các hồ sơ Phase1–3 vẫn giữ nguyên byte.
- Kiểm khởi động lại dịch vụ và invocation WSL mới đã thực hiện; chưa kiểm cold boot WSL/Windows hoặc autostart. Không shutdown/reboot máy để thực hiện lượt QA này.

Nguồn kiểm: [bàn giao ứng dụng Phase4](../.agent/qa/phase4-app-20261009/review.md). Tài liệu này là hướng dẫn vận hành I02, không phải DEMO_RUNBOOK/I04.
