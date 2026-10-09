# Phê duyệt Phase3 — Dashboard

Nguồn: attachment `0ece5ac5-8207-409e-9d6d-785f6e3a1911/Văn bản đã dán.txt`, đã đọc đầy đủ. Thy/GPT Web nghiệm thu2B2 qua hồ sơ và tính lại metric từ CSV, chưa trực tiếp load model tại GPT Web. Cho phép Streamlit+Plotly trong WSL2.

ALLOWED: thư mục dashboard mới; UI dependency thực sự cần trong venv ML hiện có với constraints giữ pin; launcher app; QA/script/log/screenshot mới; tài liệu điều phối liên quan.

FORBIDDEN: sửa model/dữ liệu/code/QA các phase cũ; fit/train/tuning hoặc rerun Test/pipeline; reinstall hệ thống, firewall/LAN/Docker; Word/Chương2/Phase4/replay/video.

SOURCE OF TRUTH: final `models/final/hgb-uci-hourly-v1.0-train-only/` SHA f4c33c54b026a3c81312dff9c9623c7dad33a3f9df4986ecd8693b7267d8749c; Flink run20261009T102201900234-full; Phase2A-a; Phase2B2-a/QA VERIFIED; APP_UI_SPEC và yêu cầu mới ưu tiên.

INVARIANTS: một hộ/lịch sử/kWh/11 feature/D09/finalmodelTrain-only, fixed Test4590 metrics; đúng3tab; dữ liệu giờ thiếu không nối gap, không thay NULL bằng0; không nhãn target trong inference; artifact/hash/schema sai hiển thị lỗi; không fit/raw scan/Flink job khi tương tác; chỉ localhost8501 và không LAN.

ACCEPTANCE: sourcegatehash/QA; dependency constraints; app chạy WSLLinux, Windowslocalhost8501; KPI đối chiếu hourly, inference khớp output; kiểm filter/gap/empty/đầu-cuối/schema/cache/no-fit/bảo toàn; screenshots trình duyệt thực nếu hỗ trợ; UI laptop/16:9; bàn giao9mục và dừng chờ duyệt.

Quyết định Minimal ưu tiên phần ảnh/GSAP/AIDA marketing của skill gpt-taste. Giữ typography/bố cục/contrast, không thêm landing page hoặc ảnh trang trí. Streamlit và Plotly không thay công việc Flink; Pandas chỉ lọc/thống kê artifact giờ đã nghiệm thu.
