# Lỗi đã gặp và cách xử lý

Ngày tạo: 2026-09-21 12:55:23 +07:00

Chưa ghi nhận lỗi nào trong workspace Big Data.

## 2026-10-03: mất khung bìa khi cấu trúc section thay đổi

- Bản Thy vừa lưu có 2 section và không còn pgBorders; nguồn/bản bàn giao QA trước vẫn có 3 section và khung trang đầu. Chưa xác định nguyên nhân cụ thể, không kết luận agent hay người dùng đã xóa khung chỉ từ ảnh.
- Khôi phục bằng cách chép riêng pgBorders cornerTriangles với display=firstPage vào section đầu của bản mới nhất. Không thay nội dung/section/footer bằng nguồn cũ vì có chỉnh tay cần giữ. Word kết xuất xác nhận chỉ trang 1 đổi, còn 46 trang bằng nguồn từng pixel.
- Khi sửa bìa/phân trang Word, kiểm số section, thuộc tính pgBorders, phạm vi firstPage và ảnh bìa trước–sau. Kiểm bản đã lưu thực tế, không giả định bản QA cũ vẫn là bản Thy đang sửa.

## 2026-10-03: bảng phân công và cập nhật mục lục

- Cột STT rộng 1 cm với padding ô và Times New Roman đậm 12 pt làm chữ tách thành hai dòng. Đã tăng riêng cột lên 1,3 cm và cân lại cột nội dung, giữ tổng chiều rộng theo lề; phải xem ảnh xuất thật, không chỉ kiểm có đủ chữ.
- TOC.Update tái tạo định dạng trực tiếp, làm mất lề phải 1 cm và thay ngắt dòng mục lục. Kiểm cập nhật thử trong bộ nhớ phải khôi phục lề phải trước so bố cục; so riêng nội dung/số trang và ảnh. Không lưu toàn tài liệu bằng Word cho sửa XML hẹp nếu cần giữ nguyên các phần package khác.

## 2026-10-03: namespace khi xóa ghi chú PowerPoint

- Một notesSlide dùng namespace DrawingML khai báo cục bộ trên từng phần tử thay vì ở root. Khi thay đoạn ghi chú bằng `<a:p/>`, prefix a không còn khai báo tại chỗ, gây lỗi import dù các slide không đổi. Đã thêm xmlns:a ngay trên đoạn rỗng, kiểm import và mở PowerPoint thành công. Khi sửa OOXML phải giữ namespace trong đúng phạm vi; kiểm mọi notesSlide, không chỉ slide XML. Nháp lỗi giữ trong QA, không bàn giao.

## 2026-10-03: font kế thừa trong deck người dùng đã sửa

- Finalizer dùng danh sách font của nguồn cũ bỏ sót Calibri trên dòng thành viên mới trong root PPTX. Dòng mới kế thừa major font từ theme; không có typeface Calibri trực tiếp tại run.
- Đã kiểm theme và báo cáo font của nguồn hiện hành, thêm Calibri vào chính sách reference rồi chạy receipt mới. Không đổi mặt slide chỉ để vượt kiểm tra.
- Mỗi lượt chỉnh deck cần đọc font trực tiếp và font kế thừa của bản người dùng vừa lưu; không lấy danh sách font/hash cũ làm chuẩn hiện hành.

## 2026-10-03: kiểm tiêu đề PowerPoint trong group

- Kiểm COM chỉ duyệt slide.Shapes ở cấp đầu không thấy các tiêu đề nằm trong group, gây báo title mismatch dù XML và ảnh đúng. Đã tạo công cụ QA read-only đệ quy GroupItems khi Type=6; xác minh text và bounds của title thật. Khi kiểm chữ/tiêu đề/bố cục PowerPoint, phải duyệt cả group lồng nhau trước khi kết luận thiếu chữ hoặc sửa deck.

## 2026-10-03: thời lượng và độ dài script

- Nhận xét GPT web từng cộng dãy mốc 720 giây thành 820 giây. Kiểm lại bằng mã cho thấy cả ba lịch phân bổ đều là 720 giây. Luôn cộng tự động trước khi báo tổng, phân biệt thời lượng thiết kế với lần đọc đã bấm giờ.
- Khi kiểm độ dài lời nói tiếng Việt, đếm theo khoảng trắng chỉ là đơn vị chữ/âm tiết hỗn hợp, không phải số từ đã phân đoạn. Bỏ tiêu đề và mốc thời gian, ghi rõ tiêu chí vì thứ hạng theo ký tự có thể khác thứ hạng theo lượng chữ cần đọc.

## 2026-09-21 13:11:43 +07:00

- Lỗi: bản mục lục nháp từng đặt DataSet API ngang hàng với DataStream API như một nội dung API hiện hành.
- Cách xử lý: thay bằng “DataStream API và Table API/SQL”; DataSet API chỉ nhắc ngắn gọn là API đã bị loại bỏ từ Flink 2.0.

## 2026-09-21 13:41:13 +07:00

- Lỗi: môi trường đang thiếu LibreOffice nên không thể dựng DOCX thành ảnh để kiểm tra trực quan tự động.
- Cách xử lý: đã kiểm tra cấu trúc, font, màu chữ, khổ giấy, lề, nội dung và metadata bằng DOCX; trước khi nộp báo cáo chính thức cần mở lại trong Word để kiểm tra trực quan lần cuối.

## 2026-09-28: kiểm tra Word và nguồn nội dung

- Hai tên file đề cương không phản ánh đúng chương bên trong. Kiểm nội dung thực tế trước khi gán vai trò: `ApacheFlink_Khoituan.docx` chứa chương 1–2, `ApacheFlink_LyVuNhanHau.docx` chứa chương 3–4.
- LibreOffice vẫn không có trong môi trường. Đã dùng phiên Microsoft Word COM riêng, vô hình, để cập nhật trường và xuất PDF, rồi PDFium kết xuất PNG. Đã kiểm tra 38 trang bản mới; trạng thái chưa kiểm tra trực quan ngày 21/09 chỉ áp dụng các file cũ.
- Word chuẩn hóa tên style và kế thừa font/cỡ chữ, thêm tên người dùng Office vào `lastModifiedBy`, loại media không còn được tham chiếu. Kiểm font hiệu lực qua chuỗi style và defaults; xóa metadata cá nhân sau lần lưu cuối. Không đánh đồng việc thiếu font trực tiếp trên style với sai font.
- Mục lục dài có thể đẩy riêng số trang sang dòng mới. Đã đặt lề phải phần mục lục 1 cm sau cập nhật trường để dòng chữ xuống hàng trước số trang; kết xuất lại và kiểm tra.
- Các phát biểu về nguồn hữu hạn, ngưỡng watermark, checkpoint/savepoint và exactly-once phải kèm điều kiện. Không dùng độ trễ cố định hoặc kết luận hiệu năng tuyệt đối khi không có phép đo.

## 2026-09-28: London Smart Meter và trường Word

- Không coi thứ tự các CSV London là thứ tự Event Time toàn cục. Ba tệp đã khảo sát có thời gian quay về mốc cũ khi đổi hộ; MAC000036 nối qua tệp 0 và 1. Phát lại phải tổ chức thứ tự hoặc điều phối sự kiện, không chọn tùy tiện watermark sai thứ tự ngắn rồi coi các bản ghi còn lại là đến trễ. Dùng LCLid làm khóa, không dùng số tệp.
- Giá trị KWH/hh là điện năng kWh của khoảng nửa giờ, không phải công suất kW. SumKWh là tổng phép đo hợp lệ; AvgKWh/MaxKWh là thống kê các phép đo, không tự chuyển thành công suất. Theo dõi khoảng đo thiếu; không mặc định Null bằng 0.
- Sau Word cập nhật SEQ, `python-docx` Paragraph.text có thể không gồm chữ trong fldSimple. Đối chiếu w:t cùng PDF trước khi kết luận số caption bị mất; không sửa caption đúng chỉ vì kết quả trích xuất thiếu.

## 2026-10-01: deck Gamma và PowerPoint

- Khoảng cách ký tự trên nhãn tiếng Việt dùng IBM Plex Mono khiến chữ nhìn tách rời. Đổi riêng ba nhãn 3V sang Montserrat Bold có sẵn của deck, spc=0 và chữ Unicode NFC; kiểm qua ảnh PowerPoint, không chỉ XML.
- PowerPoint COM cần đường dẫn Windows có dấu gạch ngược khi mở file; đường dẫn slash gây lỗi file not found dù file tồn tại.
- Finalizer runtime gọi hardlink bị EISDIR trên Windows. Wrapper cục bộ dùng copyFile với COPYFILE_EXCL chỉ khi đúng lỗi này, giữ kiểm SHA-256 và receipt của finalizer; không sửa runtime hoặc ghi đè đầu ra. RUNTIME_NODE_MODULES phải được truyền cho kiểm import.
- Trong slide 10 nguồn, đường nối đi qua chữ Checkpoint/Savepoint. Dời hai nhóm chữ ra ngoài đường nối trước khi bàn giao. Card ứng dụng dùng từng ý một textbox để các dòng xuống hàng không bị cách đoạn quá xa.

## 2026-10-01: hình kỹ thuật trong báo cáo Word

- Caption và danh mục hình không chứng minh có hình thực tế. Bản nguồn có Hình 2.1/2.2 nhưng chỉ chứa đoạn trống với line height cố định. Khi bổ sung phải thay placeholder, xóa giãn dòng exact để không cắt ảnh, kiểm `wp:inline` ngay trước từng caption và xem bản Word kết xuất.
- Context cũ ghi bìa trống và 43 trang, nhưng Thy đã sửa file thành 42 trang và điền bìa. Luôn kiểm bản hiện tại, giữ chỉnh tay, lưu đầu ra mới và so sánh bìa bằng ảnh; không chạy builder nguồn cũ.
- Bảng ngắn bị tách giữa trang dù hàng không tách. Với ba bảng mới có thể vừa một trang, đặt keep-with-next trong các ô để giữ cùng caption/nguồn; kiểm lại khoảng trắng và phân trang sau cập nhật mục lục.

## 2026-10-01: khung điều hướng và mục lục Word

- Tiêu đề lớn chưa chắc hiện trong khung Headings nếu style không có outline level. Thêm cấp đề mục cho FrontTitle/FrontTitleNoTOC, không chỉ tăng font/bold.
- Khi thêm outline cho MỤC LỤC, TOC dùng lựa chọn mọi cấp đề mục có thể tự liệt kê chính nó. Bản CoDieuHuong dùng field TOC ánh xạ style rõ ràng (FrontTitle, Heading 11/21/31), loại FrontTitleNoTOC; kiểm cập nhật thật trong Word trước bàn giao.

## 2026-10-02: thêm slide và kiểm hình hiển thị

- Không lấy rId slide mới bằng số slide hoặc số quan hệ slide: presentation còn quan hệ master/font/notes. Tính ID lớn nhất trong toàn bộ presentation.xml.rels rồi cấp ID chưa dùng; kiểm package và mở PowerPoint thật.
- XML/COM có chữ 11/14 nhưng font IBM Plex Mono Bold của nguồn xuất hình nhìn thành 14/14. Chưa kết luận nguyên nhân bên trong font; đã đổi riêng footer mới sang Open Sans Bold có sẵn và kết xuất lại, đúng 11/14. Phải kiểm số trang trên ảnh thực tế, không chỉ kiểm chuỗi trong XML.
- Native bullet đúng marL/indent vẫn có thể nhìn dính vào chữ. Với slide mới, tăng hanging indent và thêm tab stop rõ ràng; kiểm PowerPoint đã có khoảng cách, không gõ ký tự bullet giả vào nội dung.
- Finalizer không ghi đè cả output lẫn receipt. Nếu một lần finalize đã tạo output nhưng dừng vì receipt tồn tại, xác minh hash của output do agent vừa tạo, giữ bản đó trong QA rồi dùng receipt mới; không di chuyển file của Thy hoặc ghi đè âm thầm.
# Git ownership khi ổ D giữ SID từ Windows cũ

Git tại bigdata báo dubious ownership do owner SID cũ khác SID hiện tại. Không đổi quyền sở hữu thư mục hoặc thêm safe.directory wildcard/global. Dùng `git -c safe.directory=D:/Hoctap/bigdata ...` đúng repo theo từng lệnh; vẫn scan/index/remote gate trước push.

