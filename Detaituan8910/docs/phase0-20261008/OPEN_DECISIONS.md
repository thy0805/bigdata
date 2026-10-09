# Quyết định đã chốt và đề xuất chờ duyệt

## Hiện hành — Phase3

[Decision3](../../.agent/decisions/20261009-phase3-approval.md) xác nhận2B2 đã nghiệm thu, Streamlit/Plotly và đúng3tab được duyệt. Model Train-only/schema11/D09/maskTest giữ LOCKED; dashboard [đã kiểm](../../.agent/qa/phase3-20261009/review.md) nhưng nghiệm thu giao diện3 còn PENDING. Không hỏi lại quyết định cũ hoặc coi Phase4 đã được duyệt. Những pending2B2/3 trước phê duyệt bên dưới thuộc lịch sử.

## Hiện hành — Phase2B2

[Decision2B2](../../.agent/decisions/20261009-phase2b2-approval.md) ưu tiên các pending cũ: Thy nghiệm thu2B1/chọn HGB Train-only, cấm refit Train+Validation. [Bàn giao2B2](../../.agent/qa/phase2b2-20261009/review.md) VERIFIED51/51; Test4590 một lần/final manifest LOCKED. D09/split/eligibility/schema không đổi. Chỉ còn chờ nghiệm thu2B2 và duyệt Phase3; không hỏi lại dataset/nhóm/cấu hình đã khóa. Các trạng thái quyết định bên dưới là lịch sử trước duyệt2B2; không sửa ngược QA cũ.

Ngày cập nhật: 09/10/2026. Không hỏi lại những quyết định đã LOCKED; chỉ xin duyệt các điểm kỹ thuật còn mở.

## 1. LOCKED theo Thy

- Tên đề tài: PHÂN TÍCH DỮ LIỆU TIÊU THỤ ĐIỆN NĂNG VÀ DỰ ĐOÁN NHU CẦU SỬ DỤNG ĐIỆN THEO THỜI GIAN.
- UCI Individual Household Electric Power Consumption, một hộ, phút đầu vào, kWh theo giờ, dự báo giờ kế tiếp. Không London, không nhiều hộ.
- WSL2 + Apache Flink trực tiếp; không Docker Desktop, không tự restart. WSL2 đã chạy qua probe ngày 09/10.
- Flink thực hiện xử lý dữ liệu thật; ML tách riêng; không dùng số liệu giả.
- Minimal sáng/xanh dương nhẹ, ba tab Tổng quan/Phân tích/Dự báo; ưu tiên Streamlit+Plotly, không tự chuyển frontend phức tạp.
- Có cổng duyệt từng giai đoạn; Phase1 và Phase2A đã LOCKED theo nghiệm thu hồ sơ. Thy đã duyệt2B1 và D09 qua attachment9e335786; HGB Train-only/Validation VERIFIED37/37. Chờ nghiệm thu2B1 và duyệt2B2; chưa Test metrics/model cuối/UI/Word.
- Ba sinh viên chính thức trong Word giữ nguyên theo xác nhận; Thy/Codex/GPT Web là ba vai trò phối hợp, không thay danh sách bìa.

## 2. D01–D05 và Phase1 LOCKED

| ID | Đề xuất | Lý do / đánh đổi | Trạng thái |
| --- | --- | --- | --- |
| D01 | Flink 2.3.0 + Java17 Linux, pipeline Flink SQL; chưa cài PyFlink | SQL có filesystem/CSV sẵn, giữ Flink thật và giảm dependency Python | LOCKED |
| D02 | Cài openjdk-17-jdk-headless, python3.12-venv; runtime trong home Linux, raw/output trên D | Không thay Python/Java Windows/WSL; disk kiểm thực trước/sau cài | LOCKED |
| D03 | Giữ tất cả giờ, energy_kwh NULL nếu không đủ60; vòng đầu không nội suy | Bảo toàn trục thời gian và loại nhãn mục tiêu sai; giảm mẫu huấn luyện quanh gap | LOCKED |
| D04 | Giữ residual âm và flag, không clamp hoặc gọi phần âm là “Khác” | Nguyên nhân chưa được chứng minh cho mọi dòng; UI phải trình bày giới hạn | LOCKED |
| D05 | Vòng đầu bounded BATCH; streaming replay xem xét riêng sau | Kiểm số liệu trước demo nâng cao; không mô tả watermark/checkpoint đã nghiệm thu từ group-by batch | LOCKED |

D01–D05 được Thy duyệt qua attachment45ccd38f ngày09/10; decision `.agent/decisions/20261009-flink-phase1-approval.md`. Java/Flink đã cài, không dùng/lưu mật khẩu hoặc đổi quyền Windows. Scope mới nhất [decision2B1](../../.agent/decisions/20261009-phase2b1-approval.md) nghiệm thu2A và mở chỉ2B1.2B2 chưa duyệt.

## 3. Các quyết định cho Giai đoạn 2–3

| ID | Đề xuất | Cần xác nhận khi |
| --- | --- | --- |
| D06 | ML dùng venv Python3.12 WSL riêng, dependency pin | LOCKED cho2A; cài/import/pip check VERIFIED; UI chưa cài |
| D07 | Naive + SeasonalNaive24, split70/15/15 theo target axis | LOCKED baseline/split; HGB được duyệt2B1 đúng một cấu hình, fit Train/Validation VERIFIED; chưa khóa model cuối |
| D08 | Target và11 feature đầy đủ, timestamp lag chính xác/rolling đủ giờ; common mask | LOCKED cho2A;31830 mẫu, Validation4727. Lag168 tra đúng timestamp, không yêu cầu168 giờ trung gian đều đủ |
| D09 | final=max(0,raw), giữ cả raw/final; metric chính thức trên final | LOCKED qua duyệt2B1;0 dự báo âm Validation; Test/inference sau này phải dùng cùng predictor |
| D10 | Timezone giữ lịch nguồn naive; không khẳng định UTC/DST | LOCKED cho2A; cần nguồn/quyết định riêng nếu đổi timezone |

Không cần chốt ngay mô hình tốt nhất hoặc mức sai số; chỉ kết luận sau train/validation/test thật. Đường dẫn dữ liệu gốc đã tìm và hash đã kiểm, không còn quyết định “đổi dataset” hoặc “tìm Partitioned UCI Data”.

## 4. Evidence và điểm tiếp tục

[DATA_AUDIT](DATA_AUDIT.md), [TECHNICAL_ARCHITECTURE](TECHNICAL_ARCHITECTURE.md), [APP_UI_SPEC](APP_UI_SPEC.md), [IMPLEMENTATION_PLAN](IMPLEMENTATION_PLAN.md). Hash/probe và kiểm đọc lại ở `.agent/qa/phase0-resume-20261009/`.

NEXT EXACT ACTION: Thy/GPT Web nghiệm thu [Phase2B1](../../.agent/qa/phase2b1-20261009/review.md), duyệt lựa chọn HGB/config trước2B2. HGB Validation MAE0.3694427311570533/RMSE0.5306058050415966 kWh,0âm; đề xuất giữ cấu hình200iter/early_stopping=False. Không tự mở Test, refit Train+Validation hoặc khóa model cuối.
