# W01 hoàn thiện nội dung Word

Scope: ../../decisions/20261010-word-w01-approval.md. Checkpoint W00 ff0e5d7. Nguồn v3/Hậu/mẫu và code/artifact được khóa; chỉ đầu ra Word W01 mới, helper/QA/điều phối được sửa.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| W01-01 | Source/hash/template/contract | W00, v3, Hậu, mẫu, rule | VERIFIED | preflight.json30 guard; font-audit.json | Nguồn nguyên hash |
| W01-02 | Nội dung 5 chương và phần đầu/cuối | Hậu và nguồn thực nghiệm | VERIFIED | verification.json; CHAPTER_CHANGES.md | Ch1 chỉ4 đoạn; Ch2 đủ14 mục |
| W01-03 | Bảng/Equation/placeholder/caption/REF | SQL/schema/predictions + registry | VERIFIED | verification.json69/69; image-registry.json | 11 bảng mới,7 khung đen;5 native Equation |
| W01-04 | Style/numbering/TOC/list/section/footer | Word v3 và mẫu | VERIFIED | field-probe.json9/9; font-audit.json | Hai bìa nguyên; insert/delete numbering đúng |
| W01-05 | Render và rà mọi trang | DOCX đầu ra | VERIFIED | page-review.md; visual-verification.json67 trang | Lời cảm ơn9 dòng thực |
| W01-06 | Preservation/handoff/Git/stop | Source guard và final artifact | VERIFIED | preservation.json1571/1571; final-verification.json; review.md; publication486e8b3 remote50/50 | Receipt local kiểm HEAD cuối; acceptance PENDING/W02 chưa mở |
