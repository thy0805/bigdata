# Rà soát và bàn giao Phase0 ngày 09/10/2026

Structural: đủ năm Markdown, UTF-8 không ký tự thay thế/tiếng Thái, code fences cân bằng, liên kết nội bộ tồn tại. Tổng đếm/hash trích trong audit khớp JSON.

Semantic: đọc lại toàn bộ năm MD; đối chiếu audit script/full JSON, hai giờ mẫu Decimal, nguồn UCI/Apache/Microsoft/sklearn/Streamlit và metadata PyPI. Phân biệt kW/Wh/kWh, incomplete với observed energy, timestamp lịch nguồn, residual âm chưa có nguyên nhân chắc chắn. Không dùng feature tương lai; HGB early stopping mặc định được tắt trong đề xuất để tránh validation ngẫu nhiên. Thiết kế được kiểm tính nhất quán, không được tự coi đã phê duyệt.

Artifact/runtime: Linux thực thi qua WSL2; path C/D, HTTPS200, cmd.exe interop, Windows HTTP tới WSL đúng token và server thử exit0. Verifier đọc artifact cuối, hash nguồn giữ và official HTTP links đạt; kết quả chi tiết documents-verification.json. Không cài Flink, không test dependency install hoặc job; không train/app/Word. Không kiểm độc lập mọi dòng UCI lần thứ hai; tái sử dụng full scan với hash đúng.

Bảo toàn: tám nguồn trong manifest full audit giữ SHA-256. Không sửa ZIP/DOCX/PDF/mẫu/slide/script thuyết trình, Windows settings, VMware hoặc distro. Các script mới chỉ là probe/QA trong .agent, không pipeline.

Hiện hành: checklist phase0-resume-20261009; năm MD docs/phase0-20261008. Các ảnh lỗi WSL/DISM và ghi chú timer/Antigravity trước đó là lịch sử, không dùng suy ra môi trường hiện tại. Flink/PyFlink chưa tìm thấy trong PATH/package/các vị trí thường dùng đã kiểm; không kết luận đã quét mọi thư mục máy.

Pending: duyệt D01–D05 trong OPEN_DECISIONS. Sau duyệt bắt đầu F01 cài Java17/Flink2.3.0 trong WSL, kiểm dung lượng C/sudo và không thay Windows. Không chạy F01 trong lượt này.
