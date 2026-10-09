# Phê duyệt Giai đoạn 2A ngày 09/10/2026

SOURCE OF TRUTH: yêu cầu Thy trong attachment `896b429e-73e1-4588-91c2-71fd76124e60/Văn bản đã dán.txt`, hồ sơ Phase1 và hourly-grid của run `20261009T102201900234-full`.

Phase1 F01–F06 LOCKED theo nghiệm thu qua hồ sơ của Thy/GPT Web; không phải kiểm toán độc lập mới. Chỉ M01–M04 được duyệt. D06, D08, D10 được áp dụng; D07 chốt baseline và chia tập, HistGradientBoosting chỉ là đề xuất cho lượt B. D09 vẫn PENDING.

ALLOWED: `forecasting/` mới, `data/ml/runs/` mới, QA/support mới `.agent/qa/phase2a-20261009/`, `.agent/scripts/` liên quan, venv Python3.12 riêng trong home WSL và dependency ML tối thiểu, Markdown điều phối/thiết kế liên quan.

FORBIDDEN: sửa pipeline/Phase1 artifacts/raw/Word/PDF; huấn luyện mô hình học máy; dự đoán hoặc đánh giá Test; dashboard; Docker/reinstall WSL/Flink/restart/thay Windows.

INVARIANTS: nguồn duy nhất hourly-grid SHA256 `8b03f1e3c82a5344c071a19f756cb7ec87fce18cc9a612cd63c4dcf4a8b5b2bc`; cần verification VERIFIED và manifest đúng run. Không đọc raw để tạo dữ liệu ML. NULL không bằng 0. Thời gian naive nguồn. Split 70/15/15 trên toàn trục giờ mục tiêu trước lọc đủ điều kiện. Baseline cùng mask ML trên Validation; không metric Test.

SEMANTICS: target_hour=s biểu diễn năng lượng [s,s+1), prediction_origin=s (cuối giờ s−1). Lag k lấy E(s−k); rolling w lấy toàn bộ w giờ s−w đến s−1. Đủ điều kiện khi target, 5 lag và rolling3/24 đều đầy đủ. Không bắt buộc 168 giờ trung gian đều đủ: lag168 là phép tra đúng timestamp, không nối chuỗi đã bỏ NULL. Rolling không được vượt giờ thiếu để lấp đủ số phần tử.

ACCEPTANCE: schema/NULL/grid và source gate đạt; oracle độc lập kiểm feature trên tất cả giờ, baseline/metric trên Validation; synthetic gap/future perturbation/boundary tests; hai run byte-identical các output tất định; nguồn/pipeline/Phase1 giữ hash; read-back tài liệu. Dừng sau M04 và báo cấu hình lượt B đề xuất, D09 cần duyệt.
