# Bàn giao W01.1 — sửa nhỏ sau rà soát GPT Web

## Kết luận

Word W01.1 VERIFIED trong phạm vi sửa nhỏ; chờ Thy/GPT Web nghiệm thu. Không mở W02. Bản mới vẫn 67 trang, 18 bảng, 7 khung ảnh đen, 5 Equation, 3 mục lục/danh mục tự động và 21 tài liệu tham khảo có hyperlink. Hai bìa, font/style, hình và số liệu giữ nguyên W01.

## Thay đổi

- Mục 5.15–5.16 và nhãn/caption Bảng 5.3 dùng văn phong báo cáo thay ngôn ngữ điều phối nội bộ. Giữ rõ 119 phép kiểm chức năng/vận hành và 7 phép kiểm hồ sơ, không trình bày 126 là toàn bộ kiểm chức năng.
- Rút gọn vài chú nguồn ở Chương 3–5 và một lời dẫn hình; không viết lại chương hoặc bổ sung số liệu.
- Bảng 3.1: ngắt mềm đơn vị Time theo cụm. Bảng 5.1: ngắt tên mô hình tại ranh giới HistGradient/BoostingRegressor. Tên, đơn vị, cỡ chữ, hình học bảng không đổi.
- Diff chính xác: [CHANGES.md](CHANGES.md), [changes.json](changes.json), 18 điểm sửa; live field và số caption giữ nguyên.

## Ba lớp kiểm

1. Cấu trúc: 18 bảng, 5 công thức, 7 khung đen/media byte-identical; styles/numbering/theme, section/header/footer và field instructions bảo toàn. 37 guard nguồn nguyên hash.
2. Ngữ nghĩa: đúng whitelist văn bản/ô bảng; số liệu và bảng ML không đổi; không còn cụm điều phối mục tiêu trong Chương 3–5; không nâng phạm vi kiểm thử. 37/37 phép kiểm thuộc Word đạt.
3. Artifact: Word native cập nhật field và đọc lại 67 trang; probe thêm/xóa bảng, hình, heading/TOC trên bản QA đạt 9/9, không đổi hash output. Đã xem riêng 67 ảnh cuối; 9 trang đổi, 58 trang giống pixel. Bảng 5.3 mới xuất hiện đúng trong danh mục.

Font được kiểm lại theo mẫu trường trong Mauwword, không chỉ dựa vào W01 cũ. Xem [font-audit.json](font-audit.json), [field-probe.json](field-probe.json), [page-review.md](page-review.md), [final-verification.json](final-verification.json).

## Giới hạn và lịch sử kiểm — cần đọc

- Snapshot ngoài phạm vi Word: 1.568/1.571 file đọc được khớp hash, không có file đọc được bị đổi/mất. Ba đường dẫn python/python3/python3.12 của venv-probe Phase1 là reparse links không đọc được ở Windows/WSL (“No such device”). Trạng thái kiểm snapshot là INCOMPLETE, không tuyên bố 1.571/1.571 lần này. Không sửa môi trường; không thấy thay đổi dữ liệu/model từ guard nguồn.
- Raw verification tổng hợp giữ INCOMPLETE 37 PASS + 1 INCOMPLETE. Gate Word riêng VERIFIED dựa trên 37 kiểm Word, 9 field probe và 67 trang đã rà. Đây không phải nghiệm thu của Thy/GPT Web.
- Trang 10 danh mục thuật ngữ còn cách ngắt tên HGB chưa đẹp từ W01. Giống pixel nguồn, ngoài hai ô bảng được phép sửa; không sửa trang đầu đã khóa. Không có lỗi thị giác mới được phát hiện.
- Giữ verification-attempt1/preservation-attempt1, không sửa lịch sử FAIL thành PASS. Hai báo lỗi bookmark/field cũ là so ID TOC tự sinh: Word cập nhật sinh 114 ID mới. Kiểm cuối đối chiếu tên bookmark ổn định, ánh xạ 114 ID một-một, vị trí và toàn bộ field code, tất cả PAGEREF trỏ đích tồn tại.
- Không chạy lại Flink, train/refit, tính lại metric Test hoặc sửa app. Lịch tuần/phân công chưa chốt vẫn trống. W02/PPT/demo chưa được phép.

## File Word gửi trực tiếp

`D:\Hoctap\bigdata\Detaituan8910\BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx`

SHA-256: `fafe4d7485601ba667a468990c1c80e188bf0e7126dd3edaf51059dfca3e2006`.

W01 nguồn: SHA-256 `4a47523a0bfe9c2a035df66c9fedff2e33a776dcb8c2ec01b50be8dd0d33f591`, checkpoint `d66a3c9`. Không ghi đè. DOCX/PDF/PNG/fulltext/probe copy không phát hành GitHub; chỉ hồ sơ kiểm và helper. Thy cần gửi DOCX trực tiếp kèm link review này.

## Điểm dừng

Dừng chờ Thy/GPT Web duyệt W01.1. Không coi W02 được phê duyệt từ việc W01.1 VERIFIED.
