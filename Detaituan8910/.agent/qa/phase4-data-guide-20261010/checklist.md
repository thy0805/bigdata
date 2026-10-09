# UI giới thiệu dữ liệu và dự báo

SOURCE CHECKPOINT: local/remote main2da758a34f28be5ea24ce47bc1ddd74dcb5e1627; DATA_AUDIT.md; feature-schema.json; UCI chính thức.

ALLOWED: thay riêng expander cuối dashboard/app.py; QA và ảnh mới; tài liệu điều phối/bàn giao; push thông thường.

FORBIDDEN: thay checksum backend, data/model/schema/split/metric, pipeline, biểu đồ/KPI/forecast; train/refit/Testeval; Word/PPT/I04/video/replay.

INVARIANTS: ba tab chính;9 cột gốc khác11 feature; thứ tự feature khóa; Wh theo phút cho nhóm đo phụ, công suất phản kháng giữ kW theo UCI; raw2.075.259/Flink34.589/34.085đủ/504thiếu; expander mặc định đóng. SHA/job/version chỉ ẩn trong UI, không xóa hệ thống xác thực.

ACCEPTANCE: diff chỉ expander; hai bảng đối chiếu nguồn/schema; hồi quy/no-fit/sourcegate/preservation; browser hai viewport1366×768 và1920×1080/ảnh không tràn; Git remote read-back. Nghiệm thu Thy/GPT Web riêng; I04 DEFERRED.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| G01 | Khôi phục phạm vi/nguồn | Git2da758a, audit/schema/UCI | VERIFIED | Đã đọc nguồn và Git local/remote | Repo sạch trước sửa |
| G02 | Expander và hai bảng | app.py, nguồn đã khóa | VERIFIED | Exact prefix/footer diff với Git2da758a; hai bảng đọc lại | Chỉ một file UI |
| G03 | Nội dung/hồi quy/bảo toàn | Schema, oldQA/test backend | VERIFIED | technical-verification.json75/75;1570/1570 bảo toàn | Một file app được phép đổi; không sửa history QA |
| G04 | Browser hai viewport/ảnh | App đang chạy | VERIFIED | browser-verification.json7/7;4JPEG đã kiểm | Hai attempt giữ lịch sử; viewport đã reset |
| G05 | Handoff/Git | QA/diff/index/remote | APPLIED_UNVERIFIED | review.md;publication-receipt.json sau push | Chờ kiểm index/push/read-back; nghiệm thu user riêng |
