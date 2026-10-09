# Quy tắc văn phong báo cáo

Khi viết báo cáo, tài liệu học thuật, mô tả hệ thống hoặc nội dung bàn giao, phải sử dụng văn phong học thuật trực tiếp, trung tính và có căn cứ.

## 1. Nguyên tắc chung

- Viết trực tiếp vào đối tượng đang mô tả: hệ thống, dữ liệu, nghiệp vụ, kiến trúc, thuật toán, giao diện hoặc kết quả kiểm thử.
- Ưu tiên câu rõ nghĩa, có chủ thể và hành động cụ thể.
- Không dùng văn phong quảng cáo, cảm tính hoặc tự đánh giá chất lượng.
- Không viết để “đủ chữ”, không kéo dài câu bằng nội dung hiển nhiên.
- Không diễn giải lại tên bảng, class, API hoặc method nếu phần diễn giải không bổ sung thông tin.
- Thuật ngữ phải nhất quán trong toàn bộ tài liệu.

## 2. Không kể quá trình làm báo cáo

Không viết các câu mô tả quá trình soạn tài liệu như:

- “Trong phần tiếp theo sẽ trình bày...”
- “Ở phần trên đã đề cập...”
- “Để phù hợp với trang A4...”
- “Theo yêu cầu của giảng viên...”
- “Nhóm đã tiến hành chỉnh sửa...”
- “Sau khi nghiên cứu, nhóm quyết định...”

Thay vào đó, trình bày trực tiếp nội dung cần mô tả.

Ví dụ:

Sai:
“Trong phần tiếp theo, nhóm sẽ trình bày kiến trúc của hệ thống.”

Đúng:
“Hệ thống được tổ chức theo kiến trúc ba tầng gồm giao diện, dịch vụ nghiệp vụ và tầng dữ liệu.”

## 3. Không tự đánh giá

Không sử dụng các câu như:

- “Hệ thống đã được tối ưu.”
- “Thiết kế hoàn toàn chính xác.”
- “Giải pháp đáp ứng tốt yêu cầu.”
- “Cơ sở dữ liệu được thiết kế khoa học.”
- “Giao diện thân thiện và chuyên nghiệp.”

Chỉ nêu đặc điểm hoặc bằng chứng có thể kiểm tra.

Ví dụ:

Sai:
“API được thiết kế tối ưu và bảo mật cao.”

Đúng:
“API sử dụng xác thực theo phiên, kiểm tra quyền tại Backend và giới hạn phạm vi dữ liệu theo vai trò người dùng.”

## 4. Phân biệt trạng thái thực tế

Phải phân biệt rõ:

- đã triển khai;
- đã kiểm thử;
- chỉ có mã nguồn;
- mới ở mức thiết kế;
- dự kiến triển khai;
- quy tắc do ứng dụng kiểm tra;
- ràng buộc do cơ sở dữ liệu trực tiếp thực thi.

Không được mô tả một chức năng là đã hoạt động nếu chỉ mới có thiết kế hoặc mã chưa được kiểm chứng.

Ví dụ:

Sai:
“PostgreSQL bảo đảm người lập phiếu không được tự duyệt.”

Nếu DB không có constraint tương ứng, phải viết:

“Ứng dụng kiểm tra người duyệt phải khác người lập trước khi thực hiện thao tác duyệt.”

## 5. Mọi phát biểu kỹ thuật phải có nguồn thật

Trước khi viết một phát biểu về:

- cấu trúc bảng;
- khóa ngoại;
- constraint;
- API;
- phân quyền;
- luồng nghiệp vụ;
- trạng thái;
- công thức;
- giao diện;
- kết quả kiểm thử;

phải đối chiếu nguồn hiện hành như:

- mã nguồn;
- schema SQL;
- cơ sở dữ liệu;
- sơ đồ;
- đặc tả;
- test;
- log;
- tài liệu nguồn đã được xác nhận.

Không suy đoán từ trí nhớ nếu có nguồn thật để kiểm tra.

Nếu các nguồn mâu thuẫn, không tự chọn một nguồn để viết tiếp. Phải xác định nguồn hiện hành hoặc ghi nhận mâu thuẫn trước.

## 6. Cách viết mô tả kỹ thuật

Một đoạn kỹ thuật nên ưu tiên cấu trúc:

1. Đối tượng hoặc chức năng là gì.
2. Dữ liệu hoặc thành phần nào tham gia.
3. Quy tắc xử lý chính.
4. Điều kiện hoặc giới hạn quan trọng.
5. Kết quả được lưu hoặc trả về.

Không bắt buộc đủ cả năm ý nếu không cần thiết.

Ví dụ:

“Phiếu nhập được lập cho một nhà cung cấp và một kho nhận hàng. Người lập khai báo lô, số lượng và đơn giá nhập cho từng vật tư. Sau khi phiếu được gửi duyệt, nội dung nghiệp vụ không còn được chỉnh sửa. Khi người có quyền duyệt xác nhận phiếu, hệ thống cập nhật tồn kho và ghi nhận biến động kho trong cùng giao dịch.”

## 7. Tránh văn phong AI

Không sử dụng quá nhiều các cấu trúc:

- “không chỉ... mà còn...”
- “đóng vai trò quan trọng...”
- “mang lại nhiều lợi ích...”
- “góp phần nâng cao...”
- “một cách hiệu quả...”
- “toàn diện và tối ưu...”
- “đảm bảo tính chính xác, linh hoạt và hiệu quả...”

Chỉ dùng khi nội dung thực sự cần và có căn cứ.

Không lặp lại cùng một ý bằng nhiều câu với từ khác nhau.

## 8. Không thêm nội dung ngoài phạm vi

Không tự bổ sung:

- actor;
- role;
- bảng;
- chức năng;
- công nghệ;
- quy trình;
- kết quả kiểm thử;

chỉ để đoạn văn có vẻ đầy đủ hơn.

Nếu tài liệu nguồn không hỗ trợ một thông tin, phải bỏ qua hoặc ghi rõ đó là đề xuất/dự kiến.

## 9. Quy tắc sau khi viết

Sau khi hoàn thành một đoạn hoặc mục báo cáo, phải đọc lại toàn bộ đoạn để kiểm tra:

- có mâu thuẫn với nguồn thật hay không;
- có lặp ý hay không;
- có câu tự đánh giá hay không;
- có nhầm giữa thiết kế và triển khai hay không;
- có nhầm giữa constraint DB và kiểm tra ở tầng ứng dụng hay không;
- thuật ngữ có nhất quán hay không;
- câu văn có nghe như văn AI hoặc văn quảng cáo hay không.

Nếu có, sửa trước khi coi nội dung là hoàn tất.