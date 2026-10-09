# Tiếp tục Phase4 sau gián đoạn

SOURCE CHECKPOINT: Git local/remote 853974cbf3d858efc2d4209c1ba1e60ffc1c650a; QA phase4-app-20261009.

ALLOWED: kiểm hiện trạng WSL/dịch vụ, khởi động app và cluster bằng operations/services.py; kiểm nguồn/QA/hash và suy luận mẫu; hoàn tất điều phối/receipt còn dang dở, commit/push thông thường.

FORBIDDEN: sửa Word/PPT/nội dung học thuật; I04; train/refit/tuning/đánh giá lại Test; chạy lại full Flink; thay artifact đã khóa hoặc sửa lịch sử QA.

INVARIANTS: 11 feature, HGB Train-only, D09, Test4590; 1571 file trong snapshot bảo toàn; dữ liệu lịch sử UCI/Flink BATCH.

ACCEPTANCE: kiểm cấu trúc hồ sơ, hash nguồn và suy luận mẫu, app/cluster thực tế từ Linux và Windows; remote khớp commit cuối. Các gate126/126 ngày09/10 là snapshot, không phải 126 kiểm mới ngày10/10.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| R01 | Khôi phục Git/QA/môi trường | Context, QA4, Git, WSL | VERIFIED | HEAD/remote853974c; Ubuntu-24.04 WSL2, Python3.12.3/Java17/Flink có trên đĩa | Hai dịch vụ ban đầu tắt |
| R02 | Kiểm runtime/nguồn/inference và bảo toàn | App, model khóa, preflight QA4 | VERIFIED | resume-verification.json17/17; windows-verification.json4/4;1571/1571 hash | Không fullQA/fullpipeline/fit |
| R03 | Hoàn tất checkpoint và phát hành | Diff, index gate, remote receipt | VERIFIED | Commit5b7f620; ../phase4-app-20261009/resume-publication-1.json14/14; index295file/0finding | Receipt cuối local kiểm HEAD sau chốt điều phối; ZIP/QA cũ giữ |
| R04 | Nghiệm thu ứng dụng | Thy/GPT Web | TODO | Chưa có quyết định nghiệm thu mới | I04 DEFERRED; Phase4 INCOMPLETE |
