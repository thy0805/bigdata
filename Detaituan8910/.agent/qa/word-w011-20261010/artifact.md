# Hợp đồng sửa nhỏ W01.1

REFERENCE: D:/Hoctap/bigdata/Detaituan8910/BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx; SHA4a47523a0bfe9c2a035df66c9fedff2e33a776dcb8c2ec01b50be8dd0d33f591;67 trang;3 sections. Source render67PNG/word-summary/field QA của W01 hiện còn trên disk.

SOURCE OF TRUTH: reference W01 về hình thức; quyết định W01.1 về từ ngữ; kiểm thử119 chức năng/vận hành +7 hồ sơ, không đổi scope/kết quả.

Typography/geometry/preserve: kế thừa nguyên W01 đã khớp mẫu Mauwword. TNR13/18/14/12 theo vai trò;A4/lề trái3.5cm/lề khác2.5cm;3sections/footer theo relationship;hai bìa/khung/logo;18 bảng và5 Equation;23 caption/18REF/3TOC/list/69 H2;21 refs/hyperlinks;media parts/drawings nguyên. Không dùng preset mới, không giảm font toàn bảng.

Editable slots: w:body paragraphs đúng nội dung nguồn tại index418,426,445,554,561,574–576,578,580–581; chỉ w:t có prose. REF W01_T53 và SEQ/STYLEREF ở caption giữ nguyên. Bảng3.1(row2,col2) và5.1(row5,col2) chèn soft break ở ranh giới từ/camel-case, không đổi tên/đơn vị khi bỏ linebreak. Bảng5.3 sửa nhãn nội bộ ở header/row1/row5/row6, không sửa cột kết quả17/67/20/4/11/7. Index0-based và giá trị trước phải khớp tuyệt đối trước patch.

FIELD RULE: làm việc trên output mới; native Word update tất cả fields,TOC vàlist rồi PDF. Có thể chuẩn hóa XML/cache; semantic diff bỏ field cache, không bỏ prose. Không xóa field hoặc materialize chúng thành chữ tĩnh.

FIDELITY: sourcehash giữ; trước native update chỉ document.xml đổi; sau update kiểm style/num/section/header/footer/field code/bookmarks/math/media/cells/paragraphs thực. Render toàn bộ bằng pipeline native đã chẩn đoán tại W01 (bundled LibreOffice không khả dụng); so page pixel, xem riêng PNG cuối. Không công bố PDF/PNG/fulltext dump. Bản W01.1 còn7 khung đen, không phải bản nộp cuối.
