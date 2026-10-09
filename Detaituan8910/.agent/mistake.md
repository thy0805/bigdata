# Lỗi cần tránh

- Streamlit fileWatcherType=none không nạp lại module charts/data_service đã import chỉ bằng browser reload. Biểu đồ tháng giữ code cũ đến khi riêng tiến trình app được restart. Chỉ dừng đúng tiến trình Streamlit do task tạo sau khi đối chiếu cmdline; không restart WSL/Windows hoặc kill dịch vụ khác. Gán type=category cho nhãnYYYY-MM để tránh Plotly vẽ trục microsecond khi chỉ một tháng.
- Kiểm UI có nhiều tab phải scope locator vào tabpanel đang hiển thị: chữ dự báo trùng với card Tổng quan ẩn làm isVisiblefalse dù kết quả đúng. Giữ lần kiểm sai trong history, dùng locator có scope và screenshot để kiểm lại; không sửa số liệu để chữa lỗi locator.

- Khi dùng audit `open` của Python trên Linux, mode có thể là `r` dù gọi `open("rb")`; không phân loại truy cập nhị phân bằng chuỗi mode. Lượt2B1 bị gate chặn trước fit lúc hash Validation. Đã chuyển hash/đọc Validation sau fit và chỉ cho Train CSV trước fit; kiểm độc lập witness X/y. Không nới gate Test để chữa lỗi hash.
- Snapshot bảo toàn không nên coi cache `flink-tmp/archivedApplicationStore-*` là artifact sản phẩm bất biến: Flink có thể tự dọn cache giữa hai task. Lượt2B1 ghi rõ68 đường dẫn tạm đã đổi/mất trước task, kiểm riêng897 file cũ còn nguyên và933 file nguồn/QA sản phẩm. Không âm thầm bỏ file nguồn drift hoặc khẳng định toàn bộ snapshot cũ còn nguyên; chỉ phân loại đúng cache runtime và giữ evidence.

- Không kiểm trạng thái bằng substring `"VERIFIED" in text`: chuỗi APPLIED_UNVERIFIED cũng khớp. Doc QA2A đã phát hiện điều kiện này và thay bằng parse đúng ô/cột + so sánh bằng tuyệt đối; có regression phân biệt hai trạng thái. Áp dụng mọi checklist/manifest trạng thái.

- Căn target/origin phải phân biệt giờ bắt đầu khoảng và thời điểm dữ liệu giờ trước đã quan sát. Với target_hour=s, E(s) thuộc[s,s+1), origin=s, lag1=E(s−1); không gán thêm một giờ khiến horizon lệch. Phase2A dùng timestamp dictionary oracle trên toàn trục và future perturbation; giữ trục giờ khi shift/rolling, không drop NULL trước tạo feature. Test schema QA khác đánh giá mô hình trên Test; không gắn metric Validation thành Test ở dashboard hoặc Word.

- Raw UCI có cả ngày D/M/YYYY và DD/MM/YYYY; sample10k tháng12/2006 không bao phủ ngày/tháng một chữ số. Full đầu đã gắn nhầm1.716.480 parse_error dù jobFINISHED. Launcher full chuẩn hóa các phần ngày bằng SPLIT_INDEX/LPAD, giữ regex1–2 chữ số và cast/roundtrip để loại ngày không tồn tại. Giữ nguyên SQL/smoke lịch sử, kiểm regression ngày nhuận/ngày sai và full oracle; không xem mẫu đầu đủ đại diện định dạng toàn bộ dữ liệu.

- Flink2.3 SQL Client có thể exit0 dù planner/job ERROR; F04 đã gặp NPE TimestampString khi CASE có nhánh NULL timestamp bị chuyển qua planner filter. Dùng TRY_CAST timestamp trực tiếp với validator riêng, giữ kiểm format/ngày. Chỉ nghiệm thu khi REST có đúng JobID FINISHED, log không ERROR và output/validation đạt; không dùng exit0 làm bằng chứng.
- Residual DOUBLE có thể âm giả rất nhỏ ở giá trị toán học0. Fixture0.018kW/sub0.1+0.2Wh đã tạo cờ âm sai; tính tử số bằng DECIMAL trước chuyển DOUBLE/chia60, kiểm zero precision và âm thật, không clamp dữ liệu âm.
- Linux venv/copy2 trên DrvFS ổD có thể lỗi metadata/ensurepip. Probe venv trênhomeLinux đã đạt; copy logging asset dùngcopyfile khôngpreserveutime. Raw/QA vẫn trênD; không chữa bằng đổi quyền Windows toàncục.
- Startcluster từWSL invocation ngắn từng làm JVM tắt khi invocation kết thúc. Dùng foregroundholder `pipeline/cluster.py serve`, kiểmREST/TM; không khẳng định có daemon/service bền vững. RESTbind127 trongWSL không truy cập đượcWindows ở probe này; bind0 trongWSLNAT, Windowslistener::1 kiểm, không thêmportproxy/firewall hoặc publicexpose.

- WSL2 chạy không đồng nghĩa Java/pip/Flink đã cài. Probe09/10 xác nhận Ubuntu chạy nhưng toolchain Linux thiếu; kiểm từng executable/package trước cài, không dùng lỗi WSL lịch sử để cài lại runtime đã hoạt động. Không coi localhost HTTP tạm đạt là Flink Web UI/job đạt.
- `df` của VHD có thể báo gần1TB trống dù ổC thật chỉ18.34GiB và VHD đang ở C. Đã kiểm registry Lxss và dung lượng Windows; luôn kiểm volume chứa VHD trước cài/tải, không tự di chuyển distro hoặc mở rộng disk ngoài phạm vi.

- `REGDB_E_CLASSNOTREG` trong `Wsl/CallMsi/Install` không tự chứng minh Windows Installer chung hỏng. Máy 09/10 có WSL glue Appx nhưng thiếu runtime MSI và class WslInstaller; WindowsInstaller.Installer chung tạo được. Đối chiếu đúng tag/mã nhánh lỗi và metadata trước repair; không đăng ký DLL hoặc sửa registry đại trà.
- Khi hypervisor/VBS đã chạy, các CPU flag ảo hóa trả false không đủ căn cứ yêu cầu sửa BIOS. Hypervisor Platform Enabled cũng không thay thế Virtual Machine Platform Disabled. Cài MSI/DISM phải giữ /norestart, suppression tương ứng và cổng Thy duyệt; không tự reboot.
- Full scan UCI thấy cả dấu `?` và ô rỗng, gap dài 7.226 phút, 504 giờ không đầy đủ. Không thay thiếu bằng 0, cộng phút còn lại thành giờ đầy đủ hoặc drop rồi shift khiến lag nối qua gap. Residual 1.050 phút âm là cờ chất lượng; chưa chứng minh mọi trường hợp chỉ do làm tròn, không tự clamp.

- Sau tiếp nhận 08/10: không dùng số lượng/đường dẫn London từ context cũ để nói dữ liệu đang có trên máy. Đã kiểm không thấy đường dẫn cũ; phải kiểm file hiện tại trước mô tả thực nghiệm.
- Dataset UCI có công suất trung bình kW theo phút, còn sub-metering là Wh từng phút; khác London kWh/nửa giờ. Phải tích phân theo thời lượng và kiểm độ phủ khi tạo kWh theo giờ, không cộng kW rồi đổi tên thành kWh.
- Bản mẫu Word có mục lục gõ tay minh họa và tiêu đề không có outline thật. Chỉ lấy bố cục/format; tạo Heading và TOC field thật, không sao chép ví dụ thành TOC hoạt động.

- Không coi ví dụ đối tượng/độ phân giải/horizon là quyết định nếu chưa được Thy xác nhận. Riêng 08/10 đã LOCKED UCI/một hộ/kWh theo giờ/dự đoán giờ tiếp theo; không hỏi lại hoặc dùng London cũ ghi đè.
- Không gọi CSV lịch sử hoặc dữ liệu phát lại là hệ thống công tơ thời gian thực đã triển khai.
- Không đổi kWh của khoảng nửa giờ thành kW, hoặc tự thay Null bằng 0.
- Không dựa trên số tệp làm khóa hộ hoặc giả định Event Time tăng toàn cục; khảo sát mẫu trước đã có hộ đi qua ranh giới tệp.
- Không mô tả số liệu phân tích, metric, pipeline hoặc mô hình là đã chạy nếu chưa có bằng chứng thực nghiệm.
- Style Title của DOCX mặc định có thể kế thừa đường viền xanh dưới tiêu đề dù font đã đen. Đã loại pBdr khỏi styles và kết xuất lại. Kiểm ảnh thực tế, không chỉ kiểm màu chữ.

- Word lưu lại có thể đổi thứ tự tên footer1.xml/footer2.xml/footer3.xml. Khôi phục part chỉ theo tên file từng làm số trang hiện trên bìa. Đã sửa bằng mapping section → relationship → target, giữ footer bìa rỗng và hai footer nguồn đúng vai trò. Sau Word save phải kiểm lại section refs và trang bìa thực tế.
- Numbering mới có thể bị Word chuẩn hóa thành nhãn rỗng dù styles/XML ban đầu có numPr. Đã dùng definition multilevel đủ 9 cấp, numPr rõ trên heading hiện có và style link để thêm mục sau. Kiểm ListString của mọi mục và thử chèn/xóa qua Word, không chỉ kiểm XML có numId.
- PDFium ở scale 1.25 có thể làm mất đường bảng mảnh do pha pixel; scale 2 hiển thị đủ đường như PDF. Kiểm bản kết xuất độ phân giải cao trước kết luận DOCX mất border; final QA dùng scale 2.

- Caption STYLEREF chỉ dùng `\n` có thể trả cả nhãn “CHƯƠNG 1.”; bản ghép từng dùng `\s` và native Word hiển thị đúng nhưng GPT web báo đọc ra tiêu đề chương. Lượt QA đã thay bằng `STYLEREF "ChapterTitle" \n \t`, lấy paragraph number và bỏ chữ nhãn, giữ SEQ. Kiểm Word update/read-back và probe thêm/xóa bảng/hình/danh mục, không chỉ tin cache. Chưa kiểm renderer GPT web nên không khẳng định đã tái hiện hoặc sửa tận gốc lỗi riêng của renderer đó.
- MAE dùng dấu `|` rời trong OMML bị báo lỗi ở renderer ngoài dù Word native hiển thị đúng. Đã chuyển sang cặp delimiter OMML `m:d` begin/end `|`, giữ residual và giới hạn tổng; render lại bằng Word/PDFium, RMSE và E = P × Δt phải giữ XML nguồn.
- Bìa lấy mẫu nhưng tự nén khoảng cách, giảm tiêu đề xuống 18 pt/ngành 14 pt và căn giữa từng dòng tên sẽ lệch mẫu trường. QA v3 khôi phục vai trò font 20/16/14 pt, căn trái khối sinh viên, chỉnh spacing để chứa tên đề tài dài; giữ logo/khung và metadata. Phải xem cả hai bìa thực tế, không chỉ kiểm font chung Times New Roman.
- Bỏ [n] phải giới hạn trước heading Tài liệu tham khảo, kể cả marker trong ô bảng; giữ số nguồn [1]–[16], hyperlink và số trang footer. Kiểm lại nguyên văn ngoài các span đã bỏ, không xóa mọi số trong tài liệu hoặc gọi đó là chuẩn IEEE đầy đủ.
- Word save có thể chuẩn hóa `instrText` thành `fldSimple`, chuyển font/cỡ chữ vào docDefaults và bỏ thuộc tính decimal mặc định. QA cần đọc cả hai kiểu field và resolve style/default, không coi “không có thuộc tính trực tiếp” là lỗi. Probe danh mục dùng đúng TablesOfContents object, không duyệt collection Fields đang thay đổi rồi kết luận danh mục hỏng.
- Right indent TOC 1–1,4 cm vẫn để mục dài sát số trang. Lượt UCI dùng 2,5 cm và render lại, giữ Heading nguyên văn; không chỉ kiểm chuỗi tab tồn tại rồi nói mục lục dễ đọc.
