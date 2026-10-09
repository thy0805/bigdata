# Duyệt F05–F06 ngày 09/10/2026

Nguồn: Thy gửi yêu cầu trong `C:/Users/thy/.codex/attachments/0a0ec96e-7c14-4cd8-9c13-cb89b6dfb073/Văn bản đã dán.txt`; đã đọc đầy đủ. Thy chấp nhận F01–F04, duyệt full UCI, kiểm độc lập và chạy lại; dừng sau F06 để nghiệm thu Giai đoạn 1.

ALLOWED: launcher full riêng; raw UCI chỉ đọc; output từng run trong data/processed/runs; oracle/log/manifest/QA trong .agent; tài liệu điều phối liên quan.

FORBIDDEN: sửa file SQL/smoke guard gốc đã kiểm hoặc thay phương pháp tính; sửa ZIP/raw/Word; reinstall WSL/Java/Flink, Docker, Windows/restart; model/train/dashboard/Giai đoạn 2; thu hoặc lưu mật khẩu.

Sửa lỗi trong scope F05 theo yêu cầu gốc: lượt full đầu và rerun có 1.716.480 parse_error do ngày D/M/YYYY không zero-pad. Launcher full chuẩn hóa riêng hai biểu thức đọc ngày bằng SPLIT_INDEX/LPAD và regex1–2 chữ số; giữ file SQL/smoke nguyên hash, toàn bộ aggregation/NULL/residual và strict validation. Đây là hỗ trợ định dạng có thật trong raw, không bỏ lỗi hoặc đổi công thức để vượt kiểm thử. Hai output lỗi không được promote.

SOURCE OF TRUTH: duyệt Thy; SQL hash `424b084c2c776b1d253ca272527c61734a7e64f6be9df6e2dd2a55f96e3966f3`; inputs-manifest.json F04; ZIP/raw; full audit Phase0; D01–D05.

INVARIANTS: một hộ lịch sử, naive timestamp; kW phút → kWh giờ; target NULL khi chưa đủ60 phút hợp lệ; không nội suy/clamp; residual giữ dấu; Python chỉ reindex/kiểm độc lập, Flink tạo tổng hợp sản phẩm; per-run không trộn output.

ACCEPTANCE: full job FINISHED với ID/version/log; hash nguồn giữ nguyên; 100% giờ×14 cột so raw độc lập, NULL/count/timestamp exact, năng lượng sai số tuyệt đối ≤1e-8kWh; phút/residual; rerun riêng tương đương; RAM/C/D evidence; dừng chờ.
