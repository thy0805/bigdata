# Khảo sát dữ liệu UCI

## Hiện hành — Phase3

[Hồ sơ3](../../.agent/qa/phase3-20261009/review.md) và [oracle67/67](../../.agent/qa/phase3-20261009/technical-verification-v3.json) xác nhận dashboard đọc hourly artifact, không quét/tổng hợp dữ liệu phút. KPI toàn chuỗi/biên/default và nhóm đo khớp Decimal; gap/coverage/NULL giữ đúng.976/976file nguồn trước3 giữ hash; không đánh giá Test lại. Khảo sát/split/metric2B2 giữ nguyên; trạng thái chưa có UI bên dưới là lịch sử.

## Hiện hành — Phase2B2

[Bàn giao2B2](../../.agent/qa/phase2b2-20261009/review.md) và [QA51/51](../../.agent/qa/phase2b2-20261009/verification.json) ưu tiên trạng thái cũ. Test4590 đã đánh giá một lần; HGB không refit, MAE0.3220542588291146/RMSE0.4634874854716987kWh,0âm. Dataset/Flink/ML/split/mask giữ nguyên;951/951 guard khớp. Ngoại lệ audit trước duyệt9 cache mất,68 ngoại lệ cũ=16archive+52blobStorage. Final manifest LOCKED; chưa Phase3/Word/UI. Nội dung khảo sát và trạng thái bên dưới là lịch sử, không ghi đè nguồn hiện hành.

## Cập nhật hiện hành Phase2B1 ngày09/10

Phase1 và Phase2A LOCKED qua nghiệm thu hồ sơ. [Bàn giao2B1](../../.agent/qa/phase2b1-20261009/review.md) HGB VERIFIED37/37, chỉ Train/Validation; [schema](../../data/ml/runs/20261009-phase2a-a/feature-schema.json) bất biến. Nguồn Flink34589 giờ/34085đủ/504NULL giữ nguyên;31830 mẫu đủ11feature+nhãn, Train22513/Validation4727/Test4590. Loại2759 mẫu có lý do; không nội suy hoặc dùng observed của giờ thiếu làm target. D09 chỉ xử lý dự báo, không sửa năng lượng đo/residual/nhãn. Test chưa đánh giá, chưa dashboard/Word. Các câu chờ nghiệm thu Phase1 hoặc chưa tính mẫu ML bên dưới thuộc khảo sát lịch sử.

Ngày đối chiếu: 09/10/2026. D03/D04 LOCKED. Full `20261009T102201900234-full` và rerun `20261009T102643175598-rerun` VERIFIED25/25 mỗirun: 34.589 giờ×14cột/484.246 trường, toàn bộ2.075.259 phút, NULL/residual và hash nguồn khớp; maxenergyerror1e-15kWh; grid và Flinkparts giốngbyte. Evidence `.agent/qa/phase1-full-20261009/{review.md,handoff-verification.json,runs/<run_id>/verification.json}`. Chờ người dùng nghiệm thu Phase1; không tập huấn luyện/model/dashboard; fixture chỉ QA. TXT giữ SHA2564259c9d7ece5dbee9ab8d53682baac68d791c864f0f64a52b4043cb3b90894b7.

## 1. Nguồn và tính toàn vẹn

- Dataset: UCI Individual Household Electric Power Consumption, một hộ gia đình tại Sceaux, Pháp.
- ZIP gốc: `C:\Users\thy\Downloads\individual+household+electric+power+consumption.zip`.
- Thành viên: `household_power_consumption.txt`, 132.960.755 byte, CRC32 `969f48c7`.
- SHA-256 ZIP: `9f84b46ade8a2d8e1286ec4b2b6c2987a45a755c59f263be3b3b3d10dfbda3ff`.
- [Metadata, đơn vị và mô tả nhóm đo phụ của UCI](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption).

Evidence: [audit toàn bộ](../../.agent/qa/phase0-20261008/dataset-audit.json), [đối chiếu ngày 09/10](../../.agent/qa/phase0-resume-20261009/dataset-verification.json), [công cụ full audit](../../.agent/scripts/audit_phase0_uci.py).

Audit Phase0 đọc đủ2.075.259 bản ghi ZIP; kiểm khôi phục Phase0 chỉ đọc10k mẫu và13 kiểm. F06 ngày09/10 đã đọc raw full độc lập bằng Decimal, đối chiếu100% giờ và phút đầu ra Flink, đủ giờ/phút liên tục/không trùng, checksum8 nguồn DOCX/PDF/ZIP giữ nguyên. Kết quả mới nằm ở QA full, không dùng mô tả độ phủ mẫu Phase0 để đại diện F06.

## 2. Cấu trúc và đơn vị

TXT dùng dấu phân cách `;`, có một dòng tên cột. Tất cả bản ghi trong audit có 9 trường.

| Trường | Nội dung | Đơn vị / cách đọc |
| --- | --- | --- |
| Date | Ngày quan sát | `D/M/YYYY` hoặc `DD/MM/YYYY`; ngày/tháng có1–2 chữ số |
| Time | Giờ quan sát | `HH:mm:ss` |
| Global_active_power | Công suất tác dụng trung bình từng phút | kW |
| Global_reactive_power | Công suất phản kháng trung bình từng phút | UCI ghi kilowatt; không tự đổi nhãn thành kVAr khi chưa giải quyết khác biệt mô tả |
| Voltage | Điện áp trung bình từng phút | V |
| Global_intensity | Cường độ dòng điện trung bình từng phút | A |
| Sub_metering_1 | Nhóm đo phụ khu vực bếp | Wh từng phút |
| Sub_metering_2 | Nhóm đo phụ khu vực giặt giũ | Wh từng phút |
| Sub_metering_3 | Nhóm bình nước nóng và điều hòa | Wh từng phút |

Ba nhóm đo phụ không phải ba hộ hoặc phép đo riêng từng thiết bị. Biến mục tiêu chỉ được tính từ Global_active_power; chưa chọn công suất phản kháng làm đặc trưng mô hình.

## 3. Kết quả full audit được tái sử dụng

| Chỉ tiêu | Kết quả |
| --- | ---: |
| Bản ghi theo phút | 2.075.259 |
| Cột | 9 |
| Bản ghi đủ cả 7 phép đo số | 2.049.280 |
| Bản ghi thiếu cả 7 phép đo | 25.979 |
| Ô thiếu biểu diễn bằng `?` | 155.874 |
| Ô thiếu rỗng | 25.979 |
| Timestamp sai / trùng / không đúng phút | 0 / 0 / 0 |
| Bước thời gian khác 60 giây | 0 |
| Khoảng giờ có bản ghi | 34.589 |
| Giờ đủ 60 bản ghi và 60 công suất hợp lệ | 34.085 |
| Giờ không đầy đủ | 504 |
| Giờ không có công suất hợp lệ | 421 |
| Giờ ở giữa chuỗi thiếu một phần phép đo | 81 |
| Giờ đầu/cuối chỉ có một phần khoảng quan sát | 2 |
| Chuỗi phút liên tiếp thiếu công suất | 71 |
| Khoảng thiếu dài nhất | 7.226 phút |
| Bản ghi có phần điện năng còn lại âm | 1.050 |

Khoảng quan sát: 16/12/2006 17:24 đến 26/11/2010 21:02. Timestamp liên tục không đồng nghĩa phép đo liên tục: vẫn tồn tại dòng thời gian với giá trị đo thiếu. Khoảng thiếu dài nhất từ 17/08/2010 21:02 đến 22/08/2010 21:27.

Không có giá trị số sai định dạng, không hữu hạn hoặc âm trong bảy cột đo ở audit này. Các cực trị thống kê chưa được chứng minh là lỗi cảm biến.

## 4. Quy tắc điện năng theo giờ đề xuất

Đối với mỗi phút có công suất trung bình hợp lệ:

`minute_energy_kwh = Global_active_power / 60`.

Đối với khoảng giờ đủ 60 phút khác nhau:

`energy_kwh = SUM(Global_active_power) / 60`.

Không dùng SUM(kW) trực tiếp làm kWh. Các giá trị công suất hiện có tối đa ba chữ số thập phân; có thể cộng bằng DECIMAL hoặc tổng số nguyên milli-kW rồi chia 60.000 để hạn chế sai số số học. Không làm tròn từng phút trước tổng hợp.

| Giờ mẫu | Phút hợp lệ | Điện năng ghi nhận (kWh) | Có thể dùng làm mục tiêu một giờ? |
| --- | ---: | ---: | --- |
| 16/12/2006 17:00 | 36 | 2,5337333333 | Không; chỉ quan sát một phần giờ |
| 16/12/2006 18:00 | 60 | 3,6322 | Có |

Hợp đồng đầu ra đề xuất:

- `hour_start`: đầu khoảng `[hour_start, hour_start + 1 giờ)`; timestamp lịch nguồn, không tự gắn UTC.
- `record_count`, `distinct_minute_count`, `valid_power_count`: số bản ghi, số phút khác nhau, số công suất hợp lệ.
- `observed_energy_kwh`: tổng năng lượng từ các phép đo có thật; NULL nếu không có phép đo, không thay bằng 0.
- `is_complete`: đủ 60 phút khác nhau và 60 công suất hợp lệ; duplicate/parse error phải được xử lý ở cổng kiểm dữ liệu.
- `energy_kwh`: bằng observed_energy_kwh khi is_complete; NULL cho giờ không đầy đủ.
- `sub1/2/3_observed_kwh`, `sub1/2/3_valid_count`: tổng Wh/1.000 và độ phủ riêng từng nhóm.
- `negative_residual_count`: số phút có sai khác âm, giữ nguyên dấu và raw value để tra cứu.

Giữ trục đủ 34.589 giờ, kể cả giờ thiếu. Đề xuất vòng đầu không nội suy; chỉ dùng target và những giá trị quá khứ bắt buộc đầy đủ khi tạo mẫu mô hình. Số mẫu huấn luyện sẽ ít hơn 34.085 do lag và khoảng thiếu; chưa tính số này trong Giai đoạn 0.

## 5. Sai khác đo đếm và giới hạn

`residual_wh = Global_active_power * 1000 / 60 - (Sub_metering_1 + Sub_metering_2 + Sub_metering_3)`.

Audit có 1.050 phút residual âm, nhỏ nhất -2,4 Wh. Không đủ căn cứ kết luận mọi trường hợp chỉ do làm tròn; không tự ép thành 0 hoặc gọi là điện năng của một thiết bị khác. Dashboard phải hiển thị cờ sai khác và không dùng biểu đồ tỷ trọng đòi hỏi các thành phần không âm trong những khoảng này.

Tổng điện năng trên các phút hợp lệ là 37.283,7477 kWh; riêng giờ đầy đủ là 37.164,9650333333 kWh. Hai số đều là tổng phạm vi quan sát tương ứng, không phải mức tiêu thụ thực đầy đủ của toàn giai đoạn có mất phép đo.

TXT không cung cấp timezone/DST rõ ràng. Giữ lịch nguồn bằng timestamp không timezone; không tự chuyển sang UTC hoặc tính một ngày DST như dữ liệu đã xác minh múi giờ. Dữ liệu lịch sử kết thúc năm 2010; dự báo giờ tiếp theo phải gắn với mốc lịch sử, không phải ngày hiện tại.

## 6. Cổng nghiệm thu dữ liệu Giai đoạn 1

Flink phải đọc và tổng hợp raw TXT thật. Đối chiếu tổng số dòng, giờ, giờ đầy đủ, điện năng mẫu và các cờ thiếu với audit. Python chỉ được dùng làm phép tính tham chiếu độc lập trong kiểm thử hoặc làm EDA/đặc trưng sau đầu ra Flink; không thay Flink tổng hợp cho sản phẩm.

Chi tiết kiểm thử ở [kế hoạch triển khai](IMPLEMENTATION_PLAN.md). D03/D04 và Phase1 đã LOCKED; Phase2A có QA29/29 vàrerun30/30. Dừng chờ nghiệm thu2A, duyệt2B/D09; không thay các kết quả audit lịch sử.
