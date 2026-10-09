# Nguồn đối chiếu W00

Các URL dưới đây đã mở bằng công cụ web ngày10/10/2026, trừ nơi ghi hạn chế. Chỉ nguồn chính thức/ấn phẩm của tác giả; không tạo DOI hoặc lấy bài blog thay tài liệu phiên bản. Đây là registry nguồn để duyệt, chưa nhập vào danh sách tham khảo của DOCX.

| ID | Nguồn / URL | Vị trí cần dùng trong báo cáo |
| --- | --- | --- |
| S01 | [UCI: Individual Household Electric Power Consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption), Hebrail & Berard; DOI chính thức10.24432/C58K54 | 3.1–3.2: đối tượng, thuộc tính, đơn vị, giai đoạn. Metadata UCI bảng Variables hiện ghi no-missing từng cột nhưng mô tả có missing; dùng scan file thực để kết luận thiếu. Tệp thật có`?`/rỗng; không lấy UI metadata mâu thuẫn làm bằng chứng không thiếu. |
| S02 | [scikit-learn1.6.1: StandardScaler](https://scikit-learn.org/1.6/modules/generated/sklearn.preprocessing.StandardScaler.html) | 2.4: chuẩn hóa trung bình/phương sai, không bảo đảm biến phân phối thành Gaussian. Project không triển khai scaler. |
| S03 | [scikit-learn1.6.1: HistGradientBoostingRegressor](https://scikit-learn.org/1.6/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html) | 2.7,4.7–4.8: hồi quy boosting dùng histogram, tham số. Không dùng defaultearly_stopping='auto' thay cấu hình actualFalse. |
| S04 | [scikit-learn1.6.1: Lagged features for time series forecasting](https://scikit-learn.org/1.6/auto_examples/applications/plot_time_series_lagged_features.html) | 2.5–2.6: minh họa feature quá khứ/chia dữ liệu theo thời gian. Ví dụ này không là code hoặc kết quả của project. |
| S05 | [Hyndman & Athanasopoulos: FPP3, Time series components](https://otexts.com/fpp3/components.html) | 2.2: xu hướng, mùa vụ, chu kỳ; không tự kết luận chuỗi UCI đã có đủ mọi thành phần. |
| S06 | [FPP3: Stationarity and differencing](https://otexts.com/fpp3/stationarity.html) | 2.2,2.4: khái niệm dừng và sai phân, tránh khẳng định sai phân luôn làm dừng. |
| S07 | [FPP3: Some simple forecasting methods](https://otexts.com/fpp3/simple-methods.html) | 2.7,4.6: Naive và SeasonalNaive; chu kỳ thực nghiệm24giờ. |
| S08 | [FPP3: Evaluating point forecast accuracy](https://otexts.com/fpp3/accuracy.html) | 2.8: MAE/RMSE, hạn chế percentage errors; không lấy metric sách làm số liệu Test của nhóm. |
| S09 | [ApacheFlink2.3: Execution Mode (Batch/Streaming)](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/execution_mode/) | 2.9,2.11,2.13: mode thực thi bounded, khác recovery/checkpoints. Lý thuyếtDataStream không thay bằng chứng SQLđã chạy. |
| S10 | [ApacheFlink2.3: Flink Architecture](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/concepts/flink-architecture/) | 2.10: JM/TM/slot, không cô lậpCPU theo slot. |
| S11 | [ApacheFlink2.3: Windows](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/operators/windows/) | 2.11–2.12: tumbling/sliding/session, trigger/late data. Đây là cơ chếDataStream, không pipelineproject. |
| S12 | [ApacheFlink2.3: DataStream Operators](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/operators/overview/) | 2.12: keyBy phân vùng logic theo khóa, không aggregate hoặc cam kếtcùngslot. |
| S13 | [ApacheFlink2.3: Checkpointing](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/fault-tolerance/checkpointing/) | 2.13: cần bật/cấu hình, nguồn replay và lưu trạng thái; không coi hashartifact là checkpoint. |
| S14 | [ApacheFlink2.3: Group Aggregation](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/group-agg/) | 5.6–5.8: SQL GROUPBY thực. Đường dẫn cũ `/docs/dev/table/sql/queries/group-agg/` lỗi khi mở; đã theo link chính thức sang đường dẫn mới, không giữ link lỗi trong nguồn đề xuất. |

Không copy các đoạn dài từ tài liệu vào báo cáo; viết giải thích riêng và dẫn đúng tên tổ chức/tác giả, version. Nguồn S01 đã có trong16nguồn cuốiWord nên không tạo mục trùng. Các trang FPP3 có thể dẫn chung đầu sách đã có và thêm vị trí chương/mục; không tăng tài liệu tham khảo chỉ để tăng số lượng.

## Căn cứ dự án đọc trực tiếp

Đường dẫn bên dưới tính từ `D:\Hoctap\bigdata\Detaituan8910`:

- `.agent/qa/phase4-app-20261009/REPORT_EVIDENCE_MAP.md`: bản đồreport; cần đối chiếuartifact/code khi có mâu thuẫn.
- `.agent/qa/phase1-full-20261009/runs/20261009T102201900234-full/job.sql`: SQL full đã chạy, parseDate + GROUPBYFLOOR, BATCH/filesystem.
- `data/processed/runs/20261009T102201900234-full/verification.json`, `manifest.json`, `hourly-grid.csv`: auditfull, lineage/output.
- `data/ml/runs/20261009-phase2a-a/feature-schema.json`, `split-summary.json`, `manifest.json`: feature11 vàsplit thực.
- `models/runs/20261009-phase2b1-a2/model-config.json`, `metrics-validation.json`; `.agent/qa/phase2b1-20261009/fit-witness.json`: cấu hình,selectionValidation,Train-only.
- `models/final/hgb-uci-hourly-v1.0-train-only/manifest.json`, `model.joblib`: model khóa và lineage.
- `models/runs/20261009-phase2b2-a/metrics-test.json`, `predictions-test.csv`, `verification.json`: kết quả Test cuối; W00 chỉđọc, khôngtínhmetric/chọnmodel lại.
- `forecasting/prepare_baselines.py`: reindex đúng timestamp, giữtrụcgiờ, rollingpast/eligibility/cắtsplit.
- `forecasting/train_hgb.py`, `forecasting/predictor.py`: fitTrain vàD09/inference.
- `dashboard/app.py`, `data_service.py`, `charts.py`, `requirements.txt`; `operations/services.py`: chức năngapp, đơn vị, lỗi nguồn vàvậnhành.
- `.agent/qa/phase4-app-20261009/verification.json`; `.agent/qa/phase4-data-guide-20261010/technical-verification.json`, `browser-verification.json`: scopedQA theo snapshot, không claimcoldboot/production.

Các hash nguồn đang dùng và bất biến sẽ được read-back vào verification.json của W00; không chạy lại dữ liệu hoặc mô hình.

## Phần tham khảo cũ còn cần kiểm ở W01

16hyperlink trongDOCX đã có relationshipđúng; **W00 không tuyên bố vừa kiểm độ sống và nội dung của cả16trang cũ**. Các DOI và metadata nghiên cứuCh1 phải được rà trực tiếp trước bảnWordcuối nếu thay nội dung tương ứng. Trìnhbày đúng ngàytruycập thực; không đổi ngày08/10sang10/10khi chưa truycập lại.

Giữ yêu cầuThy: `[1]…[n]` chỉdanhmục cuối; thân bài dùng tên tácgiả/tổchức hoặc lời nguồn cạnh bảng, không thêm marker. Cách này không làcitationIEEEđầyđủ; nếu giảngviên yêu cầuIEEE phải xinThy quyết định riêng thay vì tự thêm lại `[n]`.
