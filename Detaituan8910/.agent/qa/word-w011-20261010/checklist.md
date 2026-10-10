# Checklist W01.1

Canonical scope: ../../decisions/20261010-word-w011-scope.md. W01 giữ nguyên; chỉ tạo bản mới.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| S01 | Nguồn/hash/scope/slots | W01 d66a3c9; Thy | VERIFIED | artifact.md; preflight;37 guard nguồn khớp | Không ghi đè nguồn |
| S02 | Thay lời nội bộ và2 line break | W01, evidence119+7 | VERIFIED | changes.json;CHANGES.md;18 điểm exact whitelist | Không đổi số liệu |
| S03 | Field/read-back/bảo toàn Word | Native Word và W01 | VERIFIED trong phạm vi Word | 37/37 Word checks;field-probe9/9 | Snapshot ngoài Word INCOMPLETE1568/1571,3 link runtime unreadable;0 changed/missing |
| S04 | Render/so ảnh/rà trang | Bản W01.1 cuối | VERIFIED | page-review;page-diff;visual67/67;9 đổi/58giốngpixel | Trang10 lỗi thẩm mỹ có sẵn ngoài scope;không W02 |
| S05 | Bàn giao/Git/checkpoint/dừng | Gate cuối | VERIFIED | review;manifest;publication-initial59b68e3 remote34/34;index0findings | ACCEPTED chờ duyệt;receipt local kiểm HEAD cuối sau cập nhật checkpoint |
