# Giai đoạn 1 F01–F04

SOURCE OF TRUTH: Thy gửi yêu cầu trong `C:/Users/thy/.codex/attachments/45ccd38f-dc6e-4fd8-9ed8-a0e40483f6ff/Văn bản đã dán.txt`, chấp thuận D01–D05 ngày09/10/2026 và dừng sau F04; IMPLEMENTATION_PLAN.md; ZIP/audit hash; tài liệu Apache2.3; môi trường kiểm trực tiếp.

ALLOWED: Java17/python3.12-venv; Thy yêu cầu agent cài giúp sau khi báo chưa biết dùng Linux, dùng WSL -u root chỉ cho apt hai gói đã duyệt, không thu mật khẩu/sửa quyền Windows; Flink2.3.0 SHA512 trong home Linux; cluster localhost; TXT làm việc ở data/raw trên D; pipeline SQL và launcher; QA/log/fixture/script trong .agent; tài liệu điều phối/decision liên quan.

FORBIDDEN: F05/full dataset aggregation, F06/full nghiệm thu; train/model/dashboard/Word; đổi ZIP/nguồn; Docker/WSL reinstall/Windows config/restart; thu thập mật khẩu; biến fixture thành dữ liệu sản phẩm.

INVARIANTS: một hộ lịch sử, kW phút → kWh giờ; energy_kwh NULL nếu không đủ60 phút hợp lệ khác nhau; giữ giờ thiếu, không nội suy/clamp; header đủ9 tên, missing khác parse error; fail cấu trúc lỗi/duplicate; không silent-ignore hoặc hardcode audit vào pipeline; raw/output/log trên D.

ACCEPTANCE: phiên bản/checksum/disk thực; REST/UI localhost Windows + TaskManager/slots; SQL job có ID/FINISHED, output khớp phép tính Decimal độc lập; kiểm header/60/59/missing/boundary/parse/duplicate/residual/rerun; hash nguồn không đổi; dừng sau F04 để duyệt.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| S00 | Ghi nhận duyệt/scope và kiểm hiện trạng | Thy + disk | VERIFIED | WSL running2; C30785843200bytes, D225280733184bytes; Thy yêu cầu cài giúp bằng thao tác agent | Root Linux chỉ apt hai gói, không đổi quyền Windows |
| F01 | Java17/venv/Flink2.3.0 | Apache + D01/D02 | VERIFIED | apt-install.json; runtime-install.json SHA512 match; environment-final.json6 commands exit0 | Java17.0.20.1/Python3.12.3, Linux venv pip24.0; không mật khẩu |
| F02 | Cluster/WebUI/TaskManager/slots | D01/Apache | VERIFIED | cluster-state.json; environment-final.json UI/REST200 Windows; browser DOM09/10 hiển thị version2.3/một TM/hai slot/jobFINISHED; native stop/start logs | Browser screenshot ở khung hẹp chỉ thấy sidebar; không kiểm mọi màn UI. Cluster foreground, không service |
| F03 | TXT nguyên bytes và parser SQL | ZIP + D03/D04 | VERIFIED | inputs-manifest.json byte/hash; smoke-verification.json header/missing/structure/quarantine tests | Raw133MB trên D; không full aggregation |
| F04 | Job mẫu thật và fixture đối chiếu | D03/D04/D05 + tests | VERIFIED | smoke-verification.json82/82;11 jobs:9FINISHED,2FAILED đúng ca lỗi;10k thật/168 giờ so14 cột Decimal1e-10 | Rerun grid giống byte; precision residual đúng; fixture QA-only |
| S05 | QA/source guard/handoff | Checkpoint/log/hash | VERIFIED | handoff-verification.json37/37; tám nguồn/rawhash, code syntax,11run manifests/currentSQLhash,8MDread-back và liveREST | Không F05/F06; giới hạn screenshot/UI và full data ghi trong review |
