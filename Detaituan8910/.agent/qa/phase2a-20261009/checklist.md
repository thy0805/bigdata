# Checklist Giai đoạn 2A

Contract: ../../decisions/20261009-phase2a-approval.md. Không huấn luyện ML/đánh giá Test/dashboard/Word.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| G00 | Bootstrap, phạm vi và môi trường riêng | Thy, context, decision | VERIFIED | Python3.12.3, install-report.json, pip check đạt; C trước27951398912 bytes | Venv ML riêng, không reinstall |
| M01 | Source gate/schema/NULL/fullgrid | Flink hourly-grid + verification | VERIFIED | Run a verification29/29; checksum đúng;34589 giờ,504 NULL | Raw chỉ hash bảo toàn, không tính ML |
| M02 | Feature/target theo timestamp | Decision và nguồn giờ | VERIFIED | Oracle tất cả34589 giờ ×11feature và origin/target;31830 eligible | Không fill NULL |
| M03 | Split thời gian và holdout | Trục mục tiêu 70/15/15 | VERIFIED | split-summary.json;22513/4727/4590;holdout seal | Test chỉ QA chuẩn bị, không metric |
| M04 | Hai baseline Validation cùng mask | Lag1/24 từ nguồn | VERIFIED | metrics-validation.json; Decimal kiểm toàn4727 mẫu | MAE/RMSE kWh |
| G05 | Oracle, regression, rerun, preservation | Source và output thực tế | VERIFIED | Run b30/30;9 artifact byteidentical;965 file giữ hash | Ba lớp kiểm |
| G06 | Read-back/handoff/checkpoint | Artifact cuối | VERIFIED | documents-verification.json38/38,16 tài liệu đọc lại; link/range/metric/count/scope đúng | Dừng chờ 2B |
