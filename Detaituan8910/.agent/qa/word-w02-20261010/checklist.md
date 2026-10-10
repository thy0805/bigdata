# Checklist W02 → W02.1

Scope canonical: ../../decisions/20261010-word-w02-w021-scope.md. Hai lượt được Thy giao làm liên tiếp; không đồng nhất kiểm kỹ thuật với nghiệm thu cuối.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| W02-00 | Bootstrap, source và nhận diện thay đổi Thy | Disk/Git/Word nguồn | VERIFIED | preflight.json; HEAD 15bd7a2; read hash hai lần | Word nguồn đổi hash; không restore source cũ |
| W02-01 | Chốt source hiện tại và đủ 7 ảnh | Thy; image-registry + embedded images | VERIFIED | Thy yêu cầu làm tiếp; source current SHA876945c3; đã xem image3–9 | H3.2 crop đúng chart Tổng quan; H3.1 từ CSV thật, không ảnh mạng |
| W02-02 | Rà và xóa câu dẫn, giữ phân tích/dữ kiện | Thân bài source; prompt | VERIFIED | changes.json; verification.json53/53 | 14 exact diff, chỉ bỏ câu/span dẫn |
| W02-03 | Chèn/giữ/crop 7 hình đúng slot, Phát công việc | Ảnh thật được xác nhận; yêu cầu Thy | VERIFIED | 53/53;page-review.md69 trang | Đóng góp % giữ trống; CSV và screenshot nguồn nguyên hash |
| W02-04 | Field, captions, source preservation, render toàn bộ | Word thực tế + source baseline | VERIFIED | native69 trang/18bảng/5Equation/3TOC;53/53;69PNG đã xem | Ngoại lệ có sẵn trang10 glossary, ngoài scope |
| W02-05 | Bàn giao W02 và danh sách ảnh/câu xóa | W02-04 | VERIFIED | review.md;CHANGES.md;image-registry-final.json;manifest.json;final-verification.json | SHA507b2426...b20ba96;acceptance pending |
| W021-00 | Kiểm mẫu và căn cứ lịch 3 tuần | Mauwword + yêu cầu + hồ sơ công việc | VERIFIED trong phạm vi | Mẫu paragraph235 ví dụ truy cập; không có quy tắc bắt buộc | Lịch là tổ chức đầu việc đề xuất, không nhật ký lịch sử xác minh |
| W021-01 | Lịch 4 cột, Tuần 1–3, thành viên/trạng thái có căn cứ | Prompt + phân công | VERIFIED | word-w021-20261010/changes.json;verification.json48/48;page-review.md | Xóa thật cột3+grid và dòng4–10; Phát tuần2,cả nhóm tuần1/3; không gán ngày |
| W021-02 | Bỏ ngày truy cập, bảo toàn 21 nguồn/link | References source và mẫu trường | VERIFIED | changes.json21 exact deletions;verification.json | Giữ DOI/năm xuất bản/URL/hyperlink; không freshHTTPaudit |
| W021-03 | Field/render/mỗi trang/21 hyperlink/bảo toàn | Output W02.1 so W02 đã kiểm | VERIFIED | NativeWord69trang/18bảng/5Equation/3TOC;48/48;69PNG đã xem;37/37guards | 65tranggiốngpixel,đổi3/67/68/69 |
| W021-04 | Bàn giao cuối, checkpoint và điểm dừng | Các gate riêng hai pha | VERIFIED | word-w021-20261010/review.md;final-verification.json;manifest.json;context/PLAN | Nghiệm thu PENDING;dừng,không PPT/demo/app |
| PUB-01 | Chỉ phát hành hồ sơ/điều phối/helper, xác minh remote | Git allowlist, không Office/PDF/PNG/raw | IN_PROGRESS | publication-index.json và publication-receipt.local.json sau push | Không stage root rule/project mistake dirty có sẵn |

## Lịch sử preflight — ảnh trong Word nguồn trước authoring

Bảng sau là snapshot trước khi Thy yêu cầu tiếp tục; các pending ảnh đã giải quyết theo gate W02. Mapping sau Word save nằm trong image-registry-final.json. Không dùng bảng lịch sử này để mở lại tác vụ đã VERIFIED.

| Hình | Part hiện tại | Kiểm bằng mắt | Pending |
| --- | --- | --- | --- |
| 3.1 | word/media/image3.png | Bảng Excel hourly-grid, đầy đủ/không đầy đủ/NULL | Đối chiếu CSV và độ đọc khi render; quá nhiều cột trên bề ngang |
| 3.2 | word/media/image4.png | Khung đen | Cần ảnh biểu đồ thật hoặc Thy cho phép dùng crop đúng biểu đồ trong ảnh Tổng quan |
| 4.1 | word/media/image5.png | Dự báo + biểu đồ Thực tế/HGB 20–26/11/2010, baseline tắt | Crop khung biểu đồ trong Word nếu cần; không đổi ảnh thành số liệu mới |
| 5.1 | word/media/image6.png | Tổng quan 20–26/11/2010, KPI/graph | Dư nhiều lề; kiểm chữ sau crop/layout |
| 5.2 | word/media/image7.png | Dataset UCI và bảng đủ 11 đặc trưng Anh–Việt | Đúng nội dung; không tự thêm bảng 9 cột nếu yêu cầu chỉ ảnh này |
| 5.3 | word/media/image8.png | Phân tích 01/08–26/11/2010 | Kiểm đọc được khi in |
| 5.4 | word/media/image9.png | Dự báo 01/08/2010 13:00 và toàn Test/metric | Kiểm bố cục/khả năng đọc; khác mốc H4.1 là hợp lệ |

Không có ảnh mạng, không chụp mới browser, không sửa Word hoặc dữ liệu trong preflight. Ảnh nguồn được trích byte-for-byte vào source-images chỉ để QA. Đường dẫn thư mục ảnh riêng chưa được Thy cung cấp.
