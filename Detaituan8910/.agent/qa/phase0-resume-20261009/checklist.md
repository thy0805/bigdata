# Giai đoạn 0 tiếp tục sau khi WSL2 được cài ở phiên khác

ALLOWED: kiểm môi trường và nguồn dữ liệu chỉ đọc; hoàn thiện năm Markdown trong docs/phase0-20261008; tạo QA/script kiểm tra và cập nhật context/PLAN/DOC_INDEX liên quan.

FORBIDDEN: cài lại WSL hoặc cài Docker/Flink/Java/package trong lượt này; thay đổi Windows, power setting hoặc restart; sửa Word, ZIP, tài liệu thành viên hoặc source cũ; chạy pipeline, train model, dựng dashboard; chuyển Giai đoạn 1 khi chưa duyệt.

SOURCE OF TRUTH: yêu cầu tiếp tục của Thy ngày 09/10/2026; file trên đĩa; audit toàn bộ dataset-audit.json; kiểm môi trường trực tiếp; tài liệu chính thức.

INVARIANTS: UCI một hộ; dữ liệu phút thành kWh theo giờ; dự báo giờ kế tiếp; giữ khoảng thiếu và tránh leakage; Flink xử lý thực tế ở Giai đoạn 1; UI Minimal ba tab; không Docker.

ACCEPTANCE: kiểm WSL và Linux độc lập; đối chiếu hash ZIP và mẫu tính độc lập với full audit, không quét lại nặng; năm tài liệu có nguồn và tách kết quả đã kiểm khỏi thiết kế; read-back, kiểm liên kết nội bộ và hash nguồn; dừng chờ duyệt.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| R00 | Khôi phục nguồn hiện hành và scope | context/PLAN/index/rule, Thy | VERIFIED | Đọc nguồn project/root, scope này và audit script; không có Git root | Không dùng snapshot 00:52 làm hiện trạng |
| R01 | WSL, Linux, toolchain, đường dẫn và kết nối | Probe chỉ đọc | VERIFIED | environment.json: WSL2/Ubuntu24.04.5/Python3.12.3; HTTPS200, interop0, localhost token200/exit0; environment-extra.md | Java/pip/Flink Linux chưa có; đây không phải cluster test |
| R02 | Hash và kiểm độc lập mẫu UCI | ZIP và dataset-audit.json | VERIFIED | dataset-verification.json: 13/13; 10.000 dòng mẫu, Decimal hai giờ, span/count invariants, tám hash nguồn | Tái sử dụng full scan, không kiểm độc lập lại mọi dòng |
| R03 | Đối chiếu phiên bản và nguồn thiết kế | Apache/Microsoft/UCI/sklearn/Streamlit | VERIFIED | Nguồn chính thức linked trong năm MD; HTTP nguồn kiểm trong documents-verification.json; wheel cp312 trong environment.json | Chỉ VERIFIED nguồn/đối chiếu; thiết kế chưa duyệt hoặc cài thử |
| R04 | Năm tài liệu | Yêu cầu Giai đoạn 0 | VERIFIED | docs/phase0-20261008 gồm đủ năm MD; read-back toàn bộ; hash/links/Unicode/count checks | Không model/job/dashboard/Word |
| R05 | Verify, bảo toàn và handoff | QA/read-back/hash | VERIFIED | documents-verification.json 42/42; review.md; phối hợp nguồn hiện hành đã đồng bộ và đọc lại | Chờ Thy/GPT Web duyệt D01–D05; không tự chuyển GĐ1 |
