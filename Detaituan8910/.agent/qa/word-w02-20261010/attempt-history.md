# Lịch sử thử W02

1. Builder dừng trước khi tạo DOCX: observed_energy_kwh của giờ không có phép đo là NULL, không chuyển được Decimal. Sửa nhánh hiển thị giữ NULL, không đổi thành 0. Không sửa nguồn CSV.
2. Word finalize bị gọi khi builder chưa tạo file, báo file không tồn tại; không mở/sửa nguồn. Các lần tiếp theo chỉ gọi khi output tồn tại.

Marker edit được chạy thành công một lần cho hai output; không lặp marker khi sửa helper.

3. Verifier lần đầu 50/52: so sánh literal relationship ID footer và yêu cầu ảnh Excel cũ tồn tại trong output dù đã được phép thay. Native Word đổi rId39→rId38 cùng footer target và dọn media không còn tham chiếu. Sửa verifier để resolve target và kiểm ảnh Excel còn trong source/QA; không sửa Word/dữ liệu để vượt kiểm. Giữ verification-attempt1.json. Lần cuối 53/53 PASS.
