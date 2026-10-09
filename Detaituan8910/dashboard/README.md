# Dashboard điện năng UCI

## Mở ứng dụng

Địa chỉ trên Windows: [http://localhost:8501](http://localhost:8501).

Nếu ứng dụng chưa chạy, mở PowerShell và chạy:

```powershell
wsl.exe -d Ubuntu-24.04 --exec /home/cute/.local/share/uci-forecast/venv/bin/python -B /mnt/d/Hoctap/bigdata/Detaituan8910/dashboard/serve.py
```

Giữ cửa sổ chạy ứng dụng mở. Dừng bằng Ctrl+C tại cửa sổ đó. Nếu cổng 8501 đã có dịch vụ, launcher báo lỗi và không dừng dịch vụ khác. Không chạy launcher lần hai khi app đang mở được.

Server chỉ lắng nghe 127.0.0.1 trong WSL; Windows truy cập qua localhost. Không cài lại WSL/Java/Flink, mở firewall hoặc kết nối LAN. Đây là phiên phát triển foreground, chưa phải dịch vụ tự khởi động.

## Chức năng

- Tổng quan: bộ lọc ngày chung, tổng điện năng ghi nhận và độ phủ, trung bình/đỉnh trên giờ đầy đủ, biểu đồ giờ, ba nhóm đo phụ và dự báo gần nhất hợp lệ.
- Phân tích: trung bình theo giờ/ngày trong tuần, tổng ghi nhận theo tháng, nhóm đo phụ và chất lượng dữ liệu.
- Dự báo: chọn mốc hợp lệ trong Test, nạp model cuối, dùng đúng 11 feature và D09. Thực tế hiển thị sau dự báo để đối chiếu, không truyền vào model. MAE/RMSE chính thức giữ toàn bộ 4.590 mẫu, không đổi theo bộ lọc.

Ngày được chọn là ngày lịch sử 2006–2010 của một hộ tại Pháp. Không có dự báo cho hiện tại, công tơ trực tiếp hoặc dự báo nhiều bước không nhận thêm quan sát. Trục giờ nguồn chưa xác minh timezone/DST.

## Dữ liệu và bảo vệ

Đầu vào là hourly-grid của Flink, dữ liệu Phase2A và model cuối Phase2B2. Đường dẫn/schema/checksum/QA được kiểm trong `data_service.py` trước khi nạp cache. Cache dữ liệu có khóa hash artifact, cache model có hash và version. Hash hoặc metadata sai sẽ hiển thị lỗi và dừng, không tạo kết quả thay thế.

Giờ thiếu giữ NULL trên trục đầy đủ; đường biểu đồ không nối qua gap. Tổng ghi nhận chỉ cộng các phút có phép đo. Trung bình/đỉnh chỉ dùng giờ đầy đủ. Sub-metering là nhóm đo khu vực theo UCI, không phải mức tiêu thụ của từng thiết bị. Residual âm là cờ chất lượng, không bị ép về 0.

Ứng dụng không đọc ZIP/TXT phút, huấn luyện lại hoặc gọi pipeline Flink. Không cần cluster chạy để xem artifact; trạng thái Flink trong phần chi tiết lấy từ hồ sơ job lịch sử.

## Môi trường và hồ sơ

Ubuntu-24.04, Python 3.12.3; venv `/home/cute/.local/share/uci-forecast/venv`. Streamlit 1.50.0, Plotly 6.3.0. Numpy 2.2.6, Pandas 2.2.3 và scikit-learn 1.6.1 cùng các pin ML cũ giữ nguyên. Dependency mới và lock đầy đủ tại [install-report](../.agent/qa/phase3-20261009/install-report.json) và [install-lock](../.agent/qa/phase3-20261009/install-lock.txt); không chạy pip upgrade tùy ý.

[Hồ sơ Phase3](../.agent/qa/phase3-20261009/review.md) ghi kiểm kỹ thuật, ảnh trình duyệt và giới hạn. Các thư mục dữ liệu/model/QA của phase trước phải còn nguyên tại project root; sao chép riêng thư mục dashboard không tạo thành ứng dụng portable.
