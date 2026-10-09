# Ghi nhận môi trường bổ sung 09/10/2026

Kiểm đọc trực tiếp bằng PowerShell, không sửa registry hoặc settings:

- HKCU\Software\Microsoft\Windows\CurrentVersion\Lxss: DistributionName Ubuntu-24.04; Version2; DefaultUid1000; BasePath C:\Users\thy\AppData\Local\wsl\{2fb8f216-2366-481a-b3a3-7dffcdeccdb6}.
- Get-Command python: C:\Users\thy\miniconda3\python.exe; --version: Python3.13.13.
- Get-Command java: C:\Program Files (x86)\Common Files\Oracle\Java\javapath\java.exe; java -version: Oracle1.8.0_401.
- Get-NetTCPConnection Listen lọc LocalPort8081/8501: không có kết quả tại thời điểm kiểm. ss -ltn Linux trong environment.json cũng không có hai cổng này.
- Các kết quả WSL/Linux/network/hash máy đọc được trong environment.json và dataset-verification.json. Không cài phần mềm, sửa power/timer, đóng tài liệu, giải nén dataset, chạy job hoặc thay đổi registry.

Đây là snapshot, không bảo đảm các cổng/dung lượng sẽ giữ nguyên trong lượt triển khai sau.
