# Checklist Phase2B2

Contract: ../../decisions/20261009-phase2b2-approval.md. Giữ candidate Train-only, không refit, không dashboard/Word/Phase3. Selection-lock và pretest-verification là cổng trước Test; evaluation-started chống vô tình đánh giá lại.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| T00 | Scope, bootstrap, môi trường và bảo toàn | Thy, decision2B2, checkpoint2B1 | VERIFIED | pretest-verification.json 17/17; preservation-before.json | Nguồn sản phẩm nguyên hash; 9 cache runtime ngoại lệ |
| T01 | Khóa lựa chọn, nguồn và Validation load | Candidate/2A/2B1/schema | VERIFIED | selection-lock.json + pretest-verification.json 17/17 | Validation4727 raw/final khớp tuyệt đối; Test content0/fit0 trước khóa |
| T02 | Test một lần, ba mô hình chung mask | Test cố định, selection-lock | VERIFIED | evaluation-started/completed.json; run2B2-a verification.json | 4590 timestamp; số lượt chính thức1; fit0 |
| T03 | Oracle, no-fit/leakage, save/load, tái lập | Code/output/model hiện hành | VERIFIED | test-verification.json44/44; verification.json51/51; metric-oracle.json; reproducibility-candidate/final.json | Decimal45; tiến trình riêng; nạp lại lệch0 |
| T04 | Final bundle riêng LOCKED | Candidate bất biến + QA PASS | VERIFIED | models/final/hgb-uci-hourly-v1.0-train-only/manifest.json + model.joblib | QA44/44 trước đóng gói; estimator fingerprint và dự báo giống candidate; final manifest LOCKED |
| T05 | Read-back/handoff/checkpoint/bảo toàn | Artifact cuối | VERIFIED | documents-precheck.json62/62 trên17MD; documents-verification.json kiểm snapshot cuối | Đã đọc đủ/liên kết/metric/state/guard; dừng trước Phase3 |
