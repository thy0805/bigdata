# Ghi nhận trước khi khóa Test

Kiểm cú pháp đầu tiên phát hiện thiếu dấu đóng ngoặc ở mã mới `load_frame`. Python dừng trước thực thi; chưa đọc Test, chưa dự báo hoặc tính metric, chưa tạo selection-lock. Đã sửa dấu ngoặc trước khi khóa mã. Không thay candidate, cấu hình, feature hoặc dữ liệu.
