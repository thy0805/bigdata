# Phê duyệt Giai đoạn 2B1

Nguồn: yêu cầu Thy đính kèm `9e335786-f484-4aa6-bcfd-d33f3c4f6ab2/Văn bản đã dán.txt`, ngày 09/10/2026. M01–M04 được nghiệm thu dựa trên hồ sơ bàn giao; không mô tả GPT Web đã chạy lại kiểm thử.

## Scope contract

ALLOWED: thêm mã huấn luyện HGB và hàm dự báo D09 trong `forecasting/`; model ứng viên và dự báo Validation trong thư mục run mới; QA, log và Markdown điều phối liên quan.

FORBIDDEN: sửa artifact/code/QA Phase1 hoặc Phase2A; đọc Test để huấn luyện, chọn tham số hoặc đánh giá; thay feature, split, eligibility hoặc target; huấn luyện dashboard, sửa Word, cài lại môi trường, tự chuyển 2B2.

SOURCE OF TRUTH: Phase2A run `20261009-phase2a-a` và `verification.json` VERIFIED 29/29; Flink run `20261009T102201900234-full`; cấu hình và D09 được Thy duyệt trong attachment.

INVARIANTS: 11 feature, 22.513 Train, 4.727 Validation, 4.590 Test. Chỉ fit Train. Timestamp và đơn vị kWh giữ nguyên. D09 là `max(0, prediction_raw)`; lưu cả raw/final, metric chính thức trên final, không sửa target. Chính sách phải dùng chung khi đánh giá Test và inference sau này.

ACCEPTANCE: source/hash/schema/count đúng; fit không nhận Validation hoặc Test; cùng 4.727 timestamp để so ba mô hình; MAE/RMSE độc lập; D09, save/load và tái lập đạt; artifact có manifest/provenance; bảo toàn toàn bộ nguồn cũ. Hoàn thành kỹ thuật không đồng nghĩa Thy nghiệm thu hoặc model cuối LOCKED.

## Cấu hình duy nhất được duyệt

`loss=squared_error`, `learning_rate=0.05`, `max_iter=200`, `max_leaf_nodes=15`, `min_samples_leaf=30`, `l2_regularization=1.0`, `max_bins=255`, `early_stopping=False`, `random_state=42`.

Tái huấn luyện cùng dữ liệu/cấu hình để kiểm tái lập được phép; không phải thử cấu hình thứ hai. Không hyperparameter search. D09 LOCKED. Cấu hình được phép thử không phải model cuối đã khóa.

## Điểm dừng

Dừng sau 2B1. Chờ Thy/GPT Web duyệt lựa chọn trên Validation trước 2B2: đánh giá Test một lần và lưu model chính thức. Chưa dashboard hoặc Word.
