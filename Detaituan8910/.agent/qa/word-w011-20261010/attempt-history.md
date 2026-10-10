# Lịch sử kiểm W01.1

Lượt authoring đầu bị guard chặn tại đoạn5.11: paragraph có6 text node do chứa REF hình thật, không phải một text node prose. Chưa ghi output. Lệnh finalize tiếp theo không tìm thấy output và dừng; không có nguồn bị sửa. Đã sửa patch chỉ nhánh prose sau REF, giữ field/numbering nguyên, không nới whitelist.

Lượt verification đầu 30/33 giữ trong verification-attempt1.json. Hai FAIL bookmark/field là so raw ID tự sinh của TOC; Word cập nhật thay114ID. Không chỉnh DOCX để ép ID cũ. Kiểm cuối ánh xạ114ID một-một, stable bookmarks, vị trí và field instructions chính xác;PAGEREF đích tồn tại. Lỗi kiểm false positive đã sửa trong verifier, không xóa lịch sử.

Ngoại lệ còn tồn tại: preservation-attempt1 và preservation cuối đều1568/1571;3 python links của venv-probe Phase1 là reparse points Windows, WSL báo No such device. Không coi là1571/1571, không sửa môi trường. Raw verification hiện37PASS/38,1INCOMPLETE,0FAIL; gate Word VERIFIED sau9/9 field probe và67 trang xem riêng.
