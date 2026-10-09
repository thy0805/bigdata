# Phạm vi phát hành GitHub

## Nguồn yêu cầu

Thy yêu cầu push trong phạm vi `D:\Hoctap\bigdata`, để GPT Web đọc code và tài liệu không cần ZIP; Word vẫn gửi trực tiếp. Repo đích do Thy xác nhận: `https://github.com/thy0805/bigdata`. Đã kiểm metadata repo public, trống và tài khoản có quyền push.

ALLOWED: khởi tạo Git tại bigdata; README, chính sách ignore/giữ byte; code dự án, Markdown, evidence JSON, tám ảnh dashboard cuối, output giờ/ML chính và model cuối; checkpoint điều phối; commit và push thông thường.

FORBIDDEN: force push, ghi đè lịch sử remote, thay model/dataset/QA đã nghiệm thu; đưa mật khẩu/token, dataset thô, bộ cài, cache/runtime, Office/PDF/ZIP lên repo; cài công cụ hoặc thay cấu hình Git toàn cục.

SOURCE OF TRUTH: file hiện hành trên đĩa, manifest/hash đã khóa, quyết định Phase3/Phase4 và remote GitHub do Thy chọn.

INVARIANTS: giữ nguyên byte artifact đã nghiệm thu; .gitattributes tắt chuyển dòng tự động để checksum trên GitHub khớp file gốc. GitHub chỉ là bản phát hành có chọn lọc, không thay nguồn dữ liệu gốc.

ACCEPTANCE: scan đúng danh sách phát hành trước commit; không có secret phát hiện; kiểm blob Git bằng SHA-256 so file gốc; push không force; HEAD local = main remote; đọc lại file từ remote.

Checkpoint phát hành ban đầu là Phase3 accepted / Phase4 authorized chưa hoàn tất. Kết quả Phase4 chỉ được cập nhật khi có bằng chứng mới; không tạo hồ sơ PASS thay thế kiểm tích hợp.
