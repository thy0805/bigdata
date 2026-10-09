# W00 — Phương án hoàn thiện báo cáo điện năng

Ngày khảo sát: 10/10/2026. Source checkpoint: `0d7aa0909dd77e2bdc9a4a5e28896a6fb4184ad2`.

**Chỉ khảo sát và đề xuất. Chưa sửa DOCX, chưa ghép Chương 2, chưa tạo khung ảnh đen, chưa chụp ảnh ứng dụng. W01/W02 chờ Thy và GPT Web phê duyệt.**

Ứng dụng, dữ liệu, mô hình và UI được Thy/GPT Web nghiệm thu theo yêu cầu W00. Đây là quyết định của người dùng, không phải một lượt chạy lại QA. I04 vẫn DEFERRED; toàn Phase 4 chưa hoàn tất.

## Thứ tự đọc hồ sơ

1. Tệp này: A — hiện trạng; C — phương án toàn báo cáo; F — kế hoạch và quyết định W01.
2. [CHAPTER2_REVIEW.md](CHAPTER2_REVIEW.md): B — rà đủ 14 mục của Hậu, có trích câu, vị trí và hướng xử lý.
3. [TABLE_FIGURE_PLAN.md](TABLE_FIGURE_PLAN.md): D — bảng dữ liệu và sổ vị trí hình, chưa tạo ảnh.
4. [DRAFTS_FOR_APPROVAL.md](DRAFTS_FOR_APPROVAL.md): E — nguyên văn mẫu Lời cảm ơn, Kết luận, 2.14 và 3.7.
5. [SOURCES.md](SOURCES.md), [evidence-map.json](evidence-map.json), [verification.json](verification.json): căn cứ và giới hạn kiểm tra.

## A. Hiện trạng và nguồn chuẩn

### Nguồn đã xác định trên đĩa

| Nguồn | Vị trí thực tế | Vai trò và kết quả |
| --- | --- | --- |
| Báo cáo chính | `D:\Hoctap\bigdata\Detaituan8910\BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx` | Bản báo cáo hợp lệ mới nhất tìm được trong project, Downloads và attachment liên quan. Hash khớp QA v3 cũ; 37 trang. Chưa phải bản đầy đủ để nộp. |
| Chương 2 hoàn chỉnh của Hậu | `C:\Users\thy\Downloads\HAULYVUNHAN_Chuong2_CoSoLyThuyet_HoanChinh.docx` | Tên thực tế không có `(1)`. Mở Word read-only và xuất preview: 13 trang, đủ 2.1–2.14, 152 đoạn; không bảng, ảnh, Equation OMML hoặc Heading outline thật. |
| Chương 2 outline trong project | `HAULYVUNHAN_Chuong2_CoSoLyThuyet.docx` | Chỉ 15 đoạn tiêu đề; không dùng thay bài hoàn chỉnh. |
| Chương 1 nguồn của Khôi | `KhoiTuan Tong Quan Bai Toan Chuong 1.docx` | Nguồn lịch sử để truy vết; báo cáo v3 đã ghép, bổ sung 1.3 và sửa công thức/caption. Không ghép lại từ đầu. |
| Mẫu trường | `D:\Hoctap\bigdata\Mauwword\Mau bao cao_Do an_Khoa luan_2025.docx` | Chỉ lấy thể thức, hai bìa, heading/caption/TOC. Không copy chương mẫu, trang nhận xét hoặc đề tài mẫu nếu chưa được yêu cầu. |
| Quy tắc hiện có | `D:\Hoctap\bigdata\.agent\rule.md` | Đang có 16 dòng quy tắc KLCN186 và là thay đổi có sẵn của người dùng. Không sửa hoặc commit tệp này; chỉ áp dụng nguyên tắc văn phong chung. |
| Quy tắc chung bổ sung | `C:\Users\thy\Downloads\rule.md` | Tên thực tế không có `(1)`; 168 dòng quy tắc viết trung tính. Không áp dụng nghiệp vụ Laravel/PostgreSQL/KLCN. |

Hash và cấu trúc nguồn nằm trong `sources.json`/`*-inspection.json` tại thư mục QA local. Các bản dump chứa thông tin bìa và đường dẫn riêng chỉ giữ local, không phát hành GitHub.

### Cấu trúc báo cáo chính

- 37 trang; 3 section; 92 đề mục outline gồm các phần đầu và mục con. Năm chương có lần lượt 11, 14, 13, 14, 17 mục: 69 mục trong chương, cộng 5 mục Mở đầu và 3 mục Kết luận thành 77 mục cấp 2.
- 7 bảng thực: lịch tuần, phân công, thuật ngữ và 4 bảng Chương 1. Chỉ 4 bảng nội dung có caption Bảng 1.1–1.4.
- 3 drawing ảnh: hai logo bìa và một hình nội dung Hình 1.1. Không nhầm thành 3 hình học thuật.
- 3 công thức OMML ở Chương 1; 3 TOC field: mục lục, danh mục hình, danh mục bảng. Có 16 nguồn đánh số và 16 hyperlink ở cuối; không có marker `[n]` trong phần nội dung theo cấu trúc đã kiểm.

| Phần | Trang vật lý trong preview v3 | Hiện trạng |
| --- | --- | --- |
| Hai bìa | 1–2 | Bìa ngoài có khung, bìa trong không khung; logo, tên đề tài, nhóm 3 người, thầy Nguyễn Thành Ngô. Giữ nguyên tên/MSSV đã xác nhận, không đổi tên bìa theo người đang trò chuyện. |
| Lịch tuần / phân công | 3–4 | Lịch 10 tuần trống; việc của Phát còn trống, tỷ lệ đóng góp cả ba chưa có căn cứ. Không tự điền lịch sử hoặc phần trăm. |
| Lời cảm ơn | 5 | Chỉ tiêu đề. |
| Mục lục / thuật ngữ / danh mục | 6–12 | Field và cache có sẵn; thuật ngữ 2 trang, mục lục 3 trang. Cần cập nhật sau khi thêm nội dung. |
| Mở đầu | 13 | 5 đề mục, chưa có nội dung. |
| Chương 1 | 14–26 | Có nội dung, 4 bảng, 1 hình, 3 công thức; giữ phần đúng, sửa tối thiểu các đoạn định hướng đã lỗi thời. |
| Chương 2 | 27–28 | Chỉ outline; bài Hậu là nguồn riêng 13 trang, chưa được nhập. |
| Chương 3–5 | 29–34 | Mỗi chương 2 trang outline; chưa có nội dung thực nghiệm. |
| Kết luận | 35 | Ba đề mục trống. |
| Tài liệu tham khảo | 36–37 | 16 nguồn/hyperlink. Không có trang trắng hoàn toàn bất thường trong contact sheet; các trang rất thưa là khung chưa viết, không phải bằng chứng có nội dung. |

Không cộng 37 + 13 để dự đoán số trang cuối: Chương 2 mới thay phần outline và việc dàn trang/cập nhật TOC sẽ làm số trang thay đổi.

### Thể thức và QA thị giác

Mẫu trường quy định A4; trái 3,5 cm, phải/trên/dưới 2,5 cm; Times New Roman; nội dung 13 pt, giãn 1,3 dòng, before/after 6 pt; chữ bảng 12 pt, giãn 1,3, before/after 0; lặp hàng tiêu đề bảng. Chương 18 pt in hoa đậm căn giữa; mục 1.1 là 14 pt; mục 1.1.1 là 13 pt. Caption bảng trên, hình dưới, đánh số theo chương.

Bìa v3 giữ vai trò cỡ chữ theo mẫu bìa, không áp dụng cỡ 13/18 cho mọi chữ trên bìa. Thân bài hiện kế thừa style và một số direct formatting; W01 phải resolve cả docDefaults/style/run, không suy luận thiếu thuộc tính trực tiếp là thiếu font.

Đã xem contact sheet đủ 37 trang v3 và 13 trang Hậu; xem lớn riêng bìa 1–2, trang 20 (MAE/RMSE), 26 (Hình 1.1), trang 8 của Hậu. MAE v3 có cặp dấu trị tuyệt đối bình thường; caption Hình 1.1 hiển thị đúng. Không sửa lại lỗi đã khắc phục chỉ vì bản trích text của Equation không thể hiện đủ ký hiệu.

Preview v3 được **tái sử dụng** từ QA trước vì DOCX có cùng hash, không tuyên bố vừa reflow/render mới 37 trang. Bài Hậu được preview mới bằng Word read-only, không Save và không Update Field vào nguồn. Đây là QA khảo sát, chưa phải QA bố cục Word tương lai. Hậu có heading xanh và công thức ASCII, cần chuyển sang style/Equation của báo cáo khi W01 được duyệt.

## C. Phương án toàn báo cáo

| Phần | Giữ | Đề xuất thực hiện trong W01 | Điều kiện / căn cứ |
| --- | --- | --- | --- |
| Bìa | Hai bìa, khung/logo, tên đề tài, thành viên, MSSV, giảng viên | Chỉ kiểm và bảo toàn; không làm lại bìa đang đúng | Mẫu trường + v3 + xác nhận trước của Thy |
| Lịch tuần / phân công | Bảng và việc của Hậu/Khôi đang có | Để trống các ô lịch sử/đóng góp chưa xác nhận; chỉ điền sau khi Thy cung cấp | Không suy từ commit thành lịch làm nhóm hoặc tỷ lệ đóng góp |
| Lời cảm ơn | Tiêu đề / vị trí | Dùng mẫu E sau duyệt; 8–9 dòng là mục tiêu dàn trang, kiểm khi render | Chỉ cảm ơn thầy giảng dạy học phần |
| Mở đầu | 5 mục | Viết cô đọng mục tiêu, phạm vi một hộ/UCI/kWh giờ/horizon 1; phương pháp và bố cục theo sản phẩm thật | Không đặt mục tiêu Kafka/online/production |
| Chương 1 | Lý luận, 1.3, 4 bảng, Hình 1.1 và 3 Equation | Minimal diff 1.10–1.11; bổ sung HGB ngắn ở 1.8 nếu duyệt; lý thuyết các mô hình khác vẫn là các hướng tiếp cận | Không đưa mọi phương pháp trong Bảng 1.3 thành mô hình đã thử |
| Chương 2 | Đủ 14 đề mục | Nhập bài Hậu sau khi sửa có chọn lọc theo bảng B; bổ sung HGB và stack thực, chuyển heading/Equation | Không ghép nguyên văn kiến trúc streaming giả |
| Chương 3 | 13 đề mục | Viết khảo sát UCI, thiếu dữ liệu, công thức, phân tích từ artifact giờ; dùng bảng D | Không chạy lại Flink hoặc tạo số liệu EDA chưa trích được |
| Chương 4 | 14 đề mục | 11 feature, split theo thời gian, hai baseline và HGB; selection qua Validation, Test đóng băng; phân tích sai số từ prediction đã lưu | Không refit, tuning hoặc chọn model bằng Test; 4.13 giải thích lựa chọn trước Test dù nằm sau phần trình bày metric |
| Chương 5 | 17 đề mục | Kiến trúc SQL BATCH → file → Python → app; chức năng 3 tab, vận hành và QA có phạm vi | 5.6–5.8 cần câu phân biệt SQL grouping với DataStream KeyBy/Window/Watermark |
| Kết luận | 3 mục | Dùng mẫu E, số liệu làm tròn 4 chữ số thập phân | Không gọi MAE là accuracy; đề xuất tương lai không thành kết quả |
| Thuật ngữ | Các thuật ngữ còn dùng trong lý thuyết | Thêm HGB, Train/Validation/Test, BATCH, rolling-origin; giữ ARIMA/LSTM nếu Ch2 vẫn giới thiệu | Không coi danh mục là danh sách package đã cài |
| Caption / TOC / số trang | Heading styles, numbering và field thật | SEQ/cross-reference/update toàn bộ TOC/list khi hoàn tất; kiểm tiếp tục số Arab ở tài liệu tham khảo | Không gõ tay mục lục; giữ STYLEREF lấy số chương, không tên chương |
| Tài liệu tham khảo | 16 nguồn còn liên quan / live relationship | Bổ sung nguồn chính thức cho HGB/Flink 2.3; chuẩn hóa tác giả, tên, version, URL, ngày truy cập; kiểm link | Theo yêu cầu Thy: không `[n]` ở thân bài, giữ danh sách đánh số cuối; dẫn tên tác giả/tổ chức trong câu khi cần, không tuyên bố là IEEE đầy đủ |
| Hình mới | Hình 1.1 và hai logo nguyên byte | W01 mới đặt khung đen có caption/registry; W02 mới ảnh thật | Placeholder không là bằng chứng, chưa đủ bản nộp |

### Các câu Chương 1 cần đổi có chọn lọc

`Bxxx` là block XML trong bản trích local, không phải số trang hay dòng Word.

| Vị trí | Câu/ý hiện tại | Hướng xử lý |
| --- | --- | --- |
| 1.10, B226 | “Quy trình dự kiến là kiểm tra chất lượng bản ghi...” | Đổi riêng đoạn quy trình thành “Quy trình đã kiểm tra…” với số liệu từ Phase 1. Giữ câu huấn luyện không mặc nhiên phân tán. |
| 1.11, B230 | “Trước hết, dữ liệu sẽ được kiểm tra…” | Mô tả kiểm timestamp/thiếu/trùng đã có; đầy đủ theo 60 bản ghi, 60 phút riêng, 60 phép đo hợp lệ. Không xóa dấu thiếu trên trục giờ. |
| 1.11, B231 | “Ở nhiệm vụ phân tích, đề tài dự kiến mô tả…” | Đổi những chức năng thực có trong ba tab: phân tích giờ/ngày/tháng và đo phụ. Không tự thêm kết luận về mùa vụ/cơ chế nhân quả. |
| 1.11, B232 | “Dữ liệu sẽ được chia theo thứ tự thời gian…”; “Phương pháp dự báo cụ thể sẽ được lựa chọn…” | Nêu chia đã thực hiện, HGB được chọn bằng Validation, fit Train-only; Test chỉ đánh giá cuối. |
| 1.4, B178/B179; 1.5, B185 | “có thể…”, “cần…” về thời tiết/ngoại sinh/kiểm tra | Giữ điều kiện lý thuyết; không đổi thành đã thu thập thời tiết hoặc đã xác minh timezone/DST. |
| 1.8, B205/B213; 1.9, B221 | “đánh giá các mô hình…” | Phân biệt các hướng lý thuyết với thực nghiệm chỉ HGB + 2 baseline. Không gắn điểm Test cho RF/ARIMA/LSTM. |

## Sự thật thực nghiệm dùng để viết sau này

| Nội dung | Giá trị / quy tắc | Nguồn dự án |
| --- | --- | --- |
| Dữ liệu phút | 2.075.259 dòng, 9 cột; 16/12/2006 17:24 đến 26/11/2010 21:02; một hộ | Phase 1 full `verification.json` + UCI |
| Thiếu / trục giờ | 25.979 dòng thiếu; 34.589 khung giờ, 34.085 đầy đủ, 504 không đầy đủ; 421 giờ không có công suất hợp lệ | Cùng audit; không tính 504 giờ như đủ giờ |
| Residual | 1.050 phút âm; giữ cờ chất lượng | Không tự kết luận toàn bộ do làm tròn hoặc ép âm về 0 |
| SQL thực | `BATCH`, filesystem CSV, `GROUP BY FLOOR(event_time TO HOUR)`; parallelism 1, restart strategy none | SQL full archived, không lấy SQL smoke làm source đầy đủ |
| Feature | 5 lag + 2 rolling mean + 4 thuộc tính lịch; không impute/scale | Schema và `prepare_baselines.py` |
| Split | 70/15/15 theo **toàn trục 34.589 giờ**; sau mask hợp lệ là 22.513 / 4.727 / 4.590 | `assign_splits` + split-summary; tỷ lệ mẫu hợp lệ không đúng 70/15/15 |
| HGB / Test | Train-only, 4.590 mẫu Test; MAE 0,3220542588291146; RMSE 0,4634874854716987 kWh | Final manifest + metrics-test |
| QA app | 126/126 ở QA4 cũ; UI thay expander 75/75 + browser 7/7 ở snapshot mới | Không cộng các gate thành số kiểm độc lập hoặc tuyên bố production PASS |

Các thống kê biểu đồ phụ thuộc khoảng ngày được chọn. Ví dụ 190,54 kWh trên dashboard mặc định là điện năng ghi nhận 20–26/11/2010, không phải tổng cả dataset. Không dùng thời gian chạy oracle kiểm thử làm benchmark Flink.

## F. Kế hoạch W01 — chưa được phép bắt đầu

### File và phạm vi

Đầu vào: v3, Hậu HoanChinh trong Downloads, mẫu Mauwword, bộ đề xuất W00, nguồn code/artifact tại checkpoint và quyết định Thy duyệt.

Đầu ra đề xuất: `D:\Hoctap\bigdata\Detaituan8910\BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx`. Ngày lấy theo ngày thực hiện; nếu đã tồn tại, dùng version mới, không ghi đè. DOCX đầu ra duy nhất là bản sao mới, không sửa v3/Hậu/mẫu.

ALLOWED sau duyệt: file báo cáo mới, khung ảnh đen riêng dưới QA W01, generator/QA/preview và điều phối liên quan. FORBIDDEN: mọi nguồn DOCX, rule hiện có, app/code/dữ liệu/mô hình/PPT, ảnh app mới, I04.

### Các bước có cổng kiểm

| ID | Công việc dự kiến | Trạng thái | QA để lên VERIFIED |
| --- | --- | --- | --- |
| W01-01 | Chốt nguồn/hash và sao chép an toàn | TODO, chờ duyệt | Nguồn giữ bytes, scope/decision lưu trước khi sửa |
| W01-02 | Nội dung Mở đầu/Ch1 minimal diff/Ch2 chỉnh chọn lọc/Ch3–5/Kết luận | TODO | Read-back từng đề mục; số liệu đối chiếu artifact; không công nghệ/tính năng giả |
| W01-03 | Bảng thật, Caption/Equation/crossrefs, placeholder đen | TODO | Count bảng/hình/đơn vị/source; hình cũ nguyên byte; registry đúng từng vị trí |
| W01-04 | Style, section, TOC/list, bìa/số trang | TODO | Update field thực trong bản mới, danh mục khớp caption, không trùng numbering hoặc mất bìa |
| W01-05 | Render và rà tất cả trang, sửa layout | TODO | Không heading mồ côi, bảng tràn/mất border, Equation lỗi, ảnh/caption lệch; Lời cảm ơn 8–9 dòng thực |
| W01-06 | Bảo toàn / bàn giao / dừng | TODO | Structural + semantic + artifact verification; hash nguồn/app/model unchanged; đánh dấu còn PLACEHOLDER, không gọi bản nộp cuối |

Rủi ro: tiêu đề dài, heading trực tiếp của Hậu không nối TOC; ASCII formula khó đọc; list numbering nhập từ Hậu có thể đụng định nghĩa báo cáo; caption STYLEREF trả cả tên chương; Word save đổi footer relationship; bảng dài qua trang; ảnh đen làm nội dung đội trang. Không dùng nhiều Enter để điều chỉnh.

### Quyết định Thy/GPT Web cần duyệt

1. Duyệt bảng sửa 14 mục Hậu và các mẫu E; giữ outline năm chương, không viết lại toàn Chương 1.
2. Đề xuất đổi riêng 5.7 thành **“Xử lý dấu thời gian trong Flink SQL BATCH”**, giữ Watermark ở lý thuyết 2.11. 5.6/5.8 vẫn có số và vị trí hiện tại nhưng nội dung nói rõ GROUP BY/FLOOR, không phải job dùng KeyBy hay TUMBLE. Nếu không đổi title, phải có câu giới hạn ngay đầu 5.7. Chưa áp dụng lựa chọn nào.
3. Duyệt 8 vị trí hình mới và các bảng ở D. Có thể bỏ Hình 3.1 nếu bảng 9 cột đã đủ; không phải bắt buộc tăng số hình.
4. Các ô lịch tuần, phân công Phát và tỷ lệ đóng góp: đề xuất giữ trống đến khi Thy xác nhận. Thiếu thông tin này không ngăn viết học thuật, nhưng là phần chưa đủ để nộp.
5. Tên bản W01 và nguyên tắc W01 có placeholder / W02 ảnh thật. Chưa xác định số trang cuối; không đặt mục tiêu kéo dài báo cáo.

## Kết luận W00

W00 là hồ sơ để duyệt phương án; không là nghiệm thu học thuật toàn bộ 16 nguồn cũ hoặc bản Word cuối. Giữ riêng ba trạng thái: app ACCEPTED theo Thy; khảo sát W00 VERIFIED theo evidence; sửa Word W01 và chụp ảnh W02 TODO. Không tự chuyển giai đoạn.
