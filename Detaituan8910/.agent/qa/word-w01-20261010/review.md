# Bàn giao W01 — Word 67 trang

**VERIFIED kỹ thuật; chờ Thy/GPT Web nghiệm thu. Không phải bản nộp cuối vì còn 7 khung ảnh đen chờ W02.**

File Word gửi trực tiếp, không có trong GitHub:

`D:\Hoctap\bigdata\Detaituan8910\BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx`

SHA-256: `4a47523a0bfe9c2a035df66c9fedff2e33a776dcb8c2ec01b50be8dd0d33f591`

## Đã thực hiện

- Ghép đủ 14 mục Chương 2 của Hậu, sửa có chọn lọc theo W00; giữ Chương 1 ngoài bốn đoạn đã duyệt, bốn bảng/hình/công thức gốc.
- Hoàn thành Mở đầu, Chương 3–5, Kết luận và Lời cảm ơn 9 dòng từ dữ liệu/kết quả đã khóa. Không tạo số liệu, train/refit/Test evaluation hoặc chạy Flink mới.
- Thêm 11 bảng và 7 khung đen; 18 bảng tổng/15 bảng caption, 8 hình caption gồm 1 hình gốc. Sửa 5.6–5.8 theo SQL BATCH, không gán KeyBy/Watermark/window streaming cho pipeline đã chạy.
- Giữ hai bìa, khung, logo, nhóm và giảng viên. Font khớp mẫu trường Mauwword. Mục lục và danh mục/numbering/REF thật hoạt động.
- Không còn [n] trong thân bài; cuối báo cáo 21 mục tham khảo có hyperlink thật.

## Bằng chứng cần đọc

1. [final-verification.json](final-verification.json): tổng hợp từng lớp kiểm, không cộng chồng các số kiểm thành một thành tích mới.
2. [verification.json](verification.json), [field-probe.json](field-probe.json): 69/69 cấu trúc/ngữ nghĩa và 9/9 live insert/delete trên QA copy. File verification.json là gate trung gian; trạng thái hoàn tất nằm ở final-verification.json.
3. [page-review.md](page-review.md), [visual-verification.json](visual-verification.json), [font-audit.json](font-audit.json): xem riêng đủ 67 trang và so font mẫu. PDF/PNG/read-back toàn văn giữ local.
4. [CHAPTER_CHANGES.md](CHAPTER_CHANGES.md), [content-changelog.json](content-changelog.json): Ch1 bốn đoạn, Ch2 67 bản ghi thay/chuẩn hóa trên 14 mục, Ch5 ba tiêu đề.
5. [TABLE_FIGURE_LIST.md](TABLE_FIGURE_LIST.md), [image-registry.json](image-registry.json), [word-summary.json](word-summary.json): caption, vị trí trang và khung W02.
6. [REFERENCE_REVIEW.md](REFERENCE_REVIEW.md), [reference-audit.json](reference-audit.json): 21 hyperlink, 18 HTTP200; ba hạn chế truy cập được ghi riêng.
7. [manifest.json](manifest.json), [preflight.json](preflight.json), [preservation.json](preservation.json): 30 nguồn khóa và 1.571/1.571 artifact giữ hash.
8. [format-final.md](format-final.md), [checklist.md](checklist.md): sửa số theo chương/flow và lịch sử gate 66/69 được bảo toàn.

## Còn chờ

Thy/GPT Web duyệt W01; W02 ảnh thật cần yêu cầu riêng. Lịch làm việc đã diễn ra, công việc Phát và tỷ lệ đóng góp chưa có xác nhận nên giữ ô trống. Ba hạn chế URL không được mô tả thành mọi nguồn đều full-text mở. Coldboot/autostart vẫn theo giới hạn QA ứng dụng cũ. I04 DEFERRED, toàn Phase4 không được tuyên bố hoàn tất.

**Điểm dừng: không tự W02, Word vòng mới, PowerPoint, demo/video hoặc thay app/data/model.**
