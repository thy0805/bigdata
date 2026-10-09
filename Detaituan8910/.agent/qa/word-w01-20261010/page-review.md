# Kiểm hình thức toàn bộ W01

Artifact SHA-256: 4a47523a0bfe9c2a035df66c9fedff2e33a776dcb8c2ec01b50be8dd0d33f591

Main agent đã xem riêng từng PNG cuối cùng 1–67 ở độ phân giải gốc 1191×1684; không suy ra từ contact sheet. Render bằng native Word và PDFium sau khi cập nhật trường. LibreOffice bundled không khả dụng ở môi trường này; hai lần thử có lỗi được giữ trong QA cục bộ, không xem đó là render thành công.

| Trang vật lý | Nội dung | Kết quả |
| --- | --- | --- |
| 1–2 | Hai bìa, khung, logo, tên/MSSV/giảng viên | PASS, bảo toàn nguồn |
| 3–4 | Lịch tuần và phân công | PASS, ô chưa xác nhận giữ trống |
| 5 | Lời cảm ơn | PASS, 9 dòng thực tế |
| 6–8 | Mục lục tự động | PASS, tên dài xuống dòng và số trang rõ |
| 9–10 | Thuật ngữ | PASS, header bảng lặp; thêm HGB/Train/Validation/Test |
| 11–12 | Danh mục hình/bảng | PASS, 8 hình/15 bảng và số theo chương |
| 13 | Mở đầu, bắt đầu trang Arab 1 | PASS |
| 14–27 | Chương 1 và Hình 1.1 gốc | PASS, MAE/RMSE trang 21 rõ; hình gốc trang 27 giữ nguyên |
| 28–41 | Chương 2, 14 mục Hậu | PASS, công thức trang 35–36 rõ, lý thuyết tách triển khai BATCH |
| 42–48 | Chương 3 | PASS, bảng không cắt chữ, 2 khung đen đúng chỗ |
| 49–54 | Chương 4 | PASS, feature/split/metric rõ, 4.14 không tạo trang gần trống riêng |
| 55–63 | Chương 5 | PASS, 4 khung đen, H5.2 trước H5.3; B5.3 có REF thật |
| 64 | Kết luận | PASS |
| 65–67 | Tài liệu tham khảo | PASS, số Arab tiếp tục; hyperlink dài xuống dòng đọc được |

Không phát hiện trang trắng thừa, chữ bị cắt, overlap hoặc ký tự công thức hỏng. Một số tên tiếng Anh dài xuống dòng trong ô bảng; không tràn khỏi ô. Giữ bảng nguyên khối có thể để khoảng trắng cuối trang, không phải trang trắng bất thường. Bảy khung đen là placeholder có chủ ý, không phải hình thực nghiệm hoàn tất.
