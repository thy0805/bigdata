# Checklist phát hành GitHub

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| G00 | Repo/scope/quyền/phạm vi | Thy + GitHub get_repo | VERIFIED | repo public trống, permissions.push=true; decision | Không tự tạo/đổi visibility |
| G01 | Danh sách chọn lọc/scan/bảo toàn | .gitignore + file hiện hành | VERIFIED | inventory.json PASS242file/19.131.985byte/0findings; verify-index-1.json | Không raw/Office/cache/secret; scan không chứng minh tuyệt đối |
| G02 | Stage/commit và blob đúng byte | source SHA-256 + Git index | VERIFIED | verify-index-1.json PASS4/4,244blob bằng disk; source_signature PASS21; commit31a7703 | .gitattributes -text; report QA được thêm sau snapshot |
| G03 | Push thường + remote read-back | origin main + commit SHA | VERIFIED | remote-readback-1.json PASS5/5,main=31a770347d18328782fbefe8880ddb1830bb3e8e | Push không force; tài liệu bàn giao bổ sung ở commit tiếp |
| G04 | Đồng bộ checkpoint/handoff rõ vị trí | README/PLAN/DOC_INDEX | VERIFIED | Đọc lại HANDOFF_FOR_GPT_WEB.md/README và checkpoint; verify-index-2.json sau cập nhật | Phase4 được duyệt, chưa done |

Report index và remote là snapshot theo commit được ghi trong report; không tự nói snapshot commit đầu kiểm nội dung của commit bổ sung. Lượt đọc lại cuối được ghi local ở remote-readback-final.json và trong kết quả chat, không thêm một commit tự tham chiếu checksum.
