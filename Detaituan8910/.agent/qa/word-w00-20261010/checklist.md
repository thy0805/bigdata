# W00 Khảo sát và đề xuất hoàn thiện Word

SOURCE CHECKPOINT: Git0d7aa09; yêu cầu Thy trong attachment605b9ea4; Word v3 và chương2 thực tế trong Downloads. App được Thy/GPT Web nghiệm thu theo yêu cầu mới; QA cũ giữ snapshot, I04 DEFERRED.

ALLOWED: đọc Word/code/schema/artifact/QA; tạo hồ sơ khảo sát Markdown/JSON/helper và preview tài liệu trong QA mới; cập nhật điều phối W00.

FORBIDDEN: sửa/tạo Word đầu ra hoặc ghép Ch2; thêm ảnh đen/ảnh app; sửa code/app/data/model/pipeline/PPT/rule hiện có; train/refit/Testeval/replay/I04. Không chuyển W01/W02 trước phê duyệt.

SOURCE OF TRUTH: artifact/code/QA tại Git0d7aa09; Word v3 chọn sau inventory; Hậu HoanChinh trong Downloads; mẫu Mauwword. Rule chung hiện có chỉ áp dụng văn phong, không nội dung KLCN.

INVARIANTS: hai bìa/nhóm3/thầy Nguyễn Thành Ngô; outline5chương; UCI một hộ/phút→kWh giờ/FlinkSQL BATCH; HGB Train-only/schema11/D09/Test4590/metric khóa; source originals giữ bytes.

ACCEPTANCE: đọc đủ nguồn; bảng14mục Ch2 với trích câu và code/evidence; phương án toànWord/bảng+hình/mẫu lời cảmơn-kếtluận-2.14-Ch3/4/kếhoạchW01; cấu trúc+nội dung+preview; hash bảo toàn; bàn giao và dừng chờ duyệt.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| W00-01 | Xác minh nguồn/phạm vi | Git, Word, rule, template | VERIFIED | verification.json: nguồn DOCX nguyên hash/CRC; W00_REVIEW.md phần A | Không chỉnh DOCX |
| W00-02 | Rà toàn Word và 14 mục Hậu | DOCX/text/preview | VERIFIED | CHAPTER2_REVIEW.md: 14 hàng có trích đoạn/vị trí; đọc đủ contact sheet 37 trang chính và 13 trang Hậu | Preview chính tái sử dụng sau kiểm cùng hash; Hậu export Word read-only |
| W00-03 | Đối chiếu thực nghiệm | SQL/schema/model/metric/QA/code | VERIFIED | evidence-map.json; verification.json: 35/35, 21 chữ ký nguồn và 1.571/1.571 hash bảo toàn | Chỉ đọc metric đã khóa; không rerun hoặc fit |
| W00-04 | Phương án/mẫu/bảng+hình/W01 | Nguồn đã xác minh | VERIFIED | W00_REVIEW.md, TABLE_FIGURE_PLAN.md, DRAFTS_FOR_APPROVAL.md, SOURCES.md đã đọc lại | 8 vị trí hình PLANNED, chưa tạo ảnh đen; mẫu văn bản chưa chèn Word |
| W00-05 | QA/handoff/checkpoint | Read-back/hash/preview | VERIFIED | verification.json; context/PLAN/DOC_INDEX và HANDOFF_FOR_GPT_WEB.md | VERIFIED cho hồ sơ W00, không phải Word hoàn thiện; chờ duyệt W01 |

## Điểm dừng và giới hạn

- Chưa có Word W01 mới; không sửa, ghép hoặc ghi đè bất kỳ DOCX nguồn nào.
- Chưa nghiệm thu văn bản mẫu hoặc phương án bố cục: Thy/GPT Web cần duyệt W01 trước khi áp dụng.
- Không thay code ứng dụng, dữ liệu, schema, mô hình, metric Test, PowerPoint hoặc I04.
- Guard 1.571 file lấy app.py đã được chấp thuận ở Git 0d7aa09 làm mốc cho UI mới; không tuyên bố app.py bất biến so với snapshot trước khi sửa expander.
- Preview hỗ trợ và dump Word giữ local, không đưa DOCX/PDF hay thông tin bìa lên GitHub. Hồ sơ Markdown/JSON là sản phẩm bàn giao của lượt này.
