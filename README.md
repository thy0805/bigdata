# Big Data — Phân tích và dự báo điện năng

Tên đề tài: **Phân tích dữ liệu tiêu thụ điện năng và dự đoán nhu cầu sử dụng điện theo thời gian**.

## Trạng thái hiện hành

Phase 0–2B2 đã nghiệm thu. Dashboard Phase 3 đã được Thy và GPT Web nghiệm thu qua hồ sơ và ảnh. Phase 4 được phép triển khai nhưng **chưa hoàn tất**. Không coi bằng chứng Phase 3 là kết quả kiểm tích hợp Phase 4.

Checkpoint dự án: [context.md](Detaituan8910/context.md). Kế hoạch và nguồn ưu tiên: [PLAN](Detaituan8910/.agent/PLAN.md), [DOC_INDEX](Detaituan8910/.agent/DOC_INDEX.md).

## Đường dẫn dành cho người rà soát

| Thành phần | Nguồn |
| --- | --- |
| Dashboard 3 tab | [Mã và hướng dẫn](Detaituan8910/dashboard/README.md) |
| Kiểm dữ liệu, KPI và inference | [data_service.py](Detaituan8910/dashboard/data_service.py) |
| Apache Flink SQL BATCH | [Pipeline](Detaituan8910/pipeline/README.md) |
| Đặc trưng, baseline, huấn luyện và D09 | [forecasting](Detaituan8910/forecasting/) |
| Model cuối Train-only | [Manifest](Detaituan8910/models/final/hgb-uci-hourly-v1.0-train-only/manifest.json) |
| Test cố định 4.590 mẫu | [Metric chính thức](Detaituan8910/models/runs/20261009-phase2b2-a/metrics-test.json) |
| Bàn giao dashboard | [review.md](Detaituan8910/.agent/qa/phase3-20261009/review.md) |
| QA dashboard | [verification.json](Detaituan8910/.agent/qa/phase3-20261009/verification.json) |
| Ảnh ứng dụng thật | [screenshots](Detaituan8910/.agent/qa/phase3-20261009/screenshots/) |
| Khảo sát và kiến trúc | [docs](Detaituan8910/docs/) |

Các review/manifest cũ là snapshot tại thời điểm tạo. Quyết định mới nhất và context hiện hành có ưu tiên về phạm vi phê duyệt; không sửa ngược hồ sơ đã nghiệm thu.

## Dữ liệu và giới hạn

Nguồn: [UCI Individual Household Electric Power Consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption), Georges Hebrail và Alice Berard, DOI [10.24432/C58K54](https://doi.org/10.24432/C58K54), giấy phép CC BY 4.0. Dữ liệu lịch sử của một hộ tại Pháp, theo phút trong giai đoạn 2006–2010.

Flink trực tiếp tổng hợp dữ liệu theo giờ. Điện năng giờ đầy đủ tính bằng tổng công suất trung bình từng phút (kW) chia 60; giờ thiếu giữ NULL. Model HGB dự báo một bước theo giờ, với lịch sử đã quan sát; không dự báo công tơ trực tiếp hoặc điện năng hiện tại năm 2026. Test không dùng để chọn lại mô hình.

Repo chứa code, tài liệu Markdown, evidence JSON, ảnh cuối đã duyệt, dữ liệu giờ/ML và model cuối phục vụ kiểm chứng. Không chứa ZIP/TXT thô, bộ cài, cache/log runtime, tài liệu Office hoặc PDF. **Word phải được gửi trực tiếp**, không lấy một file nháp cũ trong repo làm báo cáo chính.

Không chạy lại script huấn luyện, đánh giá Test hoặc full pipeline chỉ để xem giao diện. Môi trường đã khóa: WSL2 Ubuntu-24.04, Java 17, Flink 2.3.0, Python 3.12.3, scikit-learn 1.6.1, Streamlit 1.50.0, Plotly 6.3.0. Xem hướng dẫn thành phần trước khi chạy; clone repo không tự cài WSL, Java hoặc Flink.

Một số kiểm toán lịch sử dẫn tới file thô/runtime hoặc bản rerun không được phát hành. Đây là các nguồn được cố ý loại khỏi GitHub, không phải tuyên bố repo là bản sao toàn bộ ổ đĩa.
