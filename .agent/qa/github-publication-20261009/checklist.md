# Checklist phát hành GitHub

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| G00 | Repo/scope/quyền/phạm vi | Thy + GitHub get_repo | VERIFIED | repo public trống, permissions.push=true; decision | Không tự tạo/đổi visibility |
| G01 | Danh sách chọn lọc/scan/bảo toàn | .gitignore + file hiện hành | IN_PROGRESS | Chưa có inventory.json | Không raw/Office/cache/secret |
| G02 | Stage/commit và blob đúng byte | source SHA-256 + Git index | TODO | Chưa có verification | .gitattributes -text |
| G03 | Push thường + remote read-back | origin main + commit SHA | TODO | Chưa push | Không force |
| G04 | Đồng bộ checkpoint/handoff rõ vị trí | README/PLAN/DOC_INDEX | APPLIED_UNVERIFIED | Đã ghi; chờ đọc lại | Phase4 được duyệt, chưa done |
