# Phê duyệt Phase2B2 và khóa lựa chọn trước Test

Nguồn: yêu cầu Thy trong `C:/Users/thy/.codex/attachments/764156e8-7c2f-4dfe-a281-8991e64ac306/Văn bản đã dán.txt`, đã đọc đầy đủ. Thy/GPT Web nghiệm thu 2B1 qua hồ sơ và audit Codex; không mô tả GPT Web đã chạy kiểm độc lập tại máy.

ALLOWED: mã đánh giá không fit mới trong forecasting; output Test/run mới; final artifact riêng đóng gói candidate; QA/script/log mới; Markdown điều phối liên quan.

FORBIDDEN: sửa artifact/code/QA các phase cũ; fit/refit Train+Validation; chọn lại model/feature/hyperparameter/seed/split/mask theo Test; dashboard, cài Streamlit/Plotly, Word, Flink rerun/replay, thay hệ thống hoặc tự chuyển Phase3.

SOURCE OF TRUTH: Phase2B1 run `20261009-phase2b1-a2`, candidate SHA256 `94ed8c4e493025ae363a3cc6fb1b0639ef2368264966b5bda190303e98a95c38`; Phase2A run a và verification; quyết định Thy trong attachment.

LOCKED: chọn HistGradientBoostingRegressor đã fit 22.513 Train; không refit. 11 feature đúng thứ tự, cấu hình 2B1, D09=max(0,raw), môi trường sklearn1.6.1/Python3.12.3. Test 4.590 mẫu, SHA256 `f9785b91f46c43bbb22c08c98294cd32739f75e5df0218e355baa53d5fbd3574`. Target E(s) trong [s,s+1), origin=s, dữ liệu thực quá khứ tới s−1, one-step rolling origin, lịch nguồn naive.

ACCEPTANCE: checksum/lineage đúng; selection-lock và pretest QA lưu trước đọc Test; load/Validation exact; đánh giá Test chính thức một lần; HGB và hai baseline chung mask, raw/final/MAE/RMSE/âm/D09; Decimal độc lập; save/load và tái lập dự báo cố định không fit/tuning; bảo toàn nguồn; final bundle riêng LOCKED sau PASS; bàn giao 10 mục và dừng.

Ngoại lệ lịch sử: audit trước duyệt 924/933 file khớp, 9 cache Flink mất; 68 ngoại lệ trước 2B1 gồm16 archive/52 blobStorage. Kiểm lại hiện trạng và ghi riêng ngoại lệ runtime, không phục hồi/sửa ngược hồ sơ cũ. Test đã chuẩn bị và QA cấu trúc ở2A; không tuyên bố chưa từng đọc. Bằng chứng trước2B2 không ghi nhận Test fit/tuning/metric.
