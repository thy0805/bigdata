# Phase4 — phạm vi ứng dụng được Thy xác nhận

Yêu cầu trực tiếp09/10/2026: tiếp tục I01/I02/I03/I05, tạm hoãn I04. Quyết định này ưu tiên yêu cầu runbook trong approval4 cũ.

ALLOWED: kiểm lineage UCI→Flink→ML→Dashboard; kiểm khởi động/phục hồi dịch vụ riêng của dự án; fault-injection trong bản sao riêng; QA kỹ thuật/browser/resource/preservation; code vận hành mới và sửa lỗi app nếu có bằng chứng; hồ sơ bàn giao mới, ZIP và push thông thường tới thy0805/bigdata.

FORBIDDEN: train/refit/tuning Test; thay dataset/schema/metric/model; sửa Word/Chương2/PPT; DEMO_RUNBOOK/kịch bản/bài nói/video; replay/công nghệ mới; Windows/WSL reboot/firewall/LAN; kill tiến trình không thuộc dự án; sửa artifact/evidence cũ đã nghiệm thu.

SOURCE OF TRUTH: model cuối Train-only/11feature/D09, hourly-grid Flink, Phase2A và Test metric đã khóa; code/ảnh/QA3; trạng thái runtime đọc trực tiếp; Git commit0e442f6 là checkpoint publication trước task.

INVARIANTS: raw/Office/QA/data/model các phase trước không đổi byte; cache/log/pid runtime là ngoại lệ ghi riêng. Flink BATCH/lịch sử/một hộ/kWh; NULL/gap không ép0. Không sử dụng Test để lựa chọn model.

ACCEPTANCE: I01 lineage/hash và tích hợp artifact thật; I02 ownership/port/start-stop/recovery/fault-source; I03 ba tab/KPI/filter/gap/inference thật/ảnh hai viewport; I05 read-back/preservation/evidence có nguồn và giới hạn. Các kiểm không thể thực hiện phải INCOMPLETE. I04 DEFERRED và toànPhase4 INCOMPLETE đến phê duyệt riêng.

Không shutdown WSL để giả lập cold boot; báo rõ chỉ kiểm invocation mới trên distro đang chạy. Dừng sau phần ứng dụng để Thy/GPT Web kiểm, không Phase5.
