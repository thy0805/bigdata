# Nghiệm thu Phase3 và phê duyệt Phase4

Nguồn: attachment `d0264844-2d3b-4641-a223-e633f0b0acc6/Văn bản đã dán.txt`, Thy gửi ngày09/10/2026.

Phase3 ACCEPTED qua hồ sơ: GPT Web kiểm 54/54 hash gói FINAL, tám ảnh, metric Test và KPI. QA kỹ thuật96/96 được nghiệm thu; UI, mô hình và artifact các giai đoạn trước giữ nguyên.

ALLOWED: chỉ I01–I05, kiểm tích hợp lineage/runtime/inference/UI; công cụ start/status/stop, runbook, log/ảnh/QA mới. Nếu cần rerun Flink phải tạo run_id riêng, không thay nguồn app. Được phép điều chỉnh font trình bày nếu cần và QA lại.

FORBIDDEN: train/refit/tuning Test, đổi dữ liệu/feature/D09/model, sửa Word/Chương2, PowerPoint, video chính thức, replay/Kafka, thay Windows/firewall, kill dịch vụ khác hoặc restart máy/WSL.

SOURCE OF TRUTH: artifact Flink chuẩn, Phase2A và model Train-only cuối; code/ảnh/QA Phase3 đã nghiệm thu; yêu cầu I01–I05 trong attachment.

INVARIANTS: 11feature,22.513Train,4.590Test, model checksum, giờ thiếuNULL, metric chính thức cố định, dữ liệu lịch sử và chế độ BATCH. Runtime cache không coi là dữ liệu sản phẩm bất biến.

ACCEPTANCE: kiểm lineage, start/recovery, ba tab/inference, DEMO_RUNBOOK và bằng chứng thực tế; mỗi mục có PASS/FAIL/INCOMPLETE. Chỉ hoàn tất khi đọc lại/test/runtime hoặc ảnh phù hợp. Dừng chờ nghiệm thu Phase4, không tự Phase5.

I01–I05 hiện TODO; phê duyệt không đồng nghĩa đã kiểm hoặc đã hoàn tất.
