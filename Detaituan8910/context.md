# Đồ án Big Data tuần 8–10

## Hiện hành — giải thích dữ liệu trên dashboard, 10/10/2026

CURRENT TASK: bàn giao thay đổi riêng expander giới thiệu dữ liệu; chờ Thy/GPT Web duyệt giao diện.
SOURCE CHECKPOINT: Git2da758a; .agent/qa/phase4-data-guide-20261010/checklist.md; DATA_AUDIT và feature-schema khóa.
ALLOWED SCOPE: expander cuối dashboard/app.py, QA/ảnh mới và điều phối/GitHub. Không Word/PPT/I04/video/replay.
LOCKED: raw/Flink hourly/ML/schema11/split/HGB Train22513/D09/Test4590/metric; backend và charts/KPI/forecast không đổi.
APPLIED BUT UNVERIFIED: publication đang chờ kiểm index/push/read-back; receipt riêng sau push. Nghiệm thu Thy/GPT Web PENDING.
VERIFIED: QA75/75; browser7/7 và4ảnh ở1366×768/1920×1080, không tràn;1570/1570 file được bảo vệ khớp snapshot QA4, chỉ app.py được phép đổi. Hai bảng9cột gốc/11feature, source link, không metadata kỹ thuật trên UI; checksum backend giữ nguyên. Prefix/footer app nguyên văn so Git2da758a.
PENDING: nghiệm thu giao diện; I04 DEFERRED, toànPhase4 INCOMPLETE. Coldboot/autostart chưa kiểm/triển khai như trước.
LAST EVIDENCE: .agent/qa/phase4-data-guide-20261010/{technical-verification.json,browser-verification.json,review.md,screenshots/}; hai browser attempt giữ lịch sử, viewport reset. App restart riêng, không dừng Flink hoặc fit/rerun/Testeval.
NEXT EXACT ACTION: hoàn tất publication gate rồi dừng để Thy/GPT Web mở expander cuối localhost8501; đọc review mới, không tự mở phase khác.

Các block phía dưới là lịch sử; scope UI mới chỉ cho phép thay expander, không mở lại artifact đã khóa.

## Lịch sử — Phase4 ứng dụng; I04 tạm hoãn

CURRENT TASK: bàn giao I01/I02/I03/I05; chờ Thy/GPT Web kiểm app. ToànPhase4 INCOMPLETE vì I04 DEFERRED.
SOURCE CHECKPOINT: .agent/decisions/20261009-phase4-app-scope.md; QA4 .agent/qa/phase4-app-20261009/checklist.md; Git base0e442f6.
ALLOWED SCOPE: QA ứng dụng/integration artifact/vận hành và GitHub; không Word/Ch2Hậu/PPT/runbook/speech/video/replay/Phase5.
LOCKED: raw/Flhourly/ML/Test4590/HGB Train22513/11feature/D09 và toànQA1–3; không train/refit/tuning/metricTest mới.
APPLIED BUT UNVERIFIED: không có thay đổi code/artifact chưa kiểm. Hồ sơ tiếp tục đã push5b7f620/read-back14/14; receipt local cuối kiểm HEAD sau chốt điều phối. Nghiệm thu Thy/GPT Web vẫn PENDING.
VERIFIED: I01 chain17/17; backend/AppTest67/67; runtime20/20 Linux +4/4 Windows; browser11/11,8ảnh đã đọc. Gate cuối126/126 và preservation1571/1571. App giữ nguyên code. Launcher operations/services.py mới kiểm ownership/start-stop/foreign-port; JavaIPv4Stack+REST127 khắc phục Windows8081 loopback. App có inference/tab khi Flink tắt. I05 hồ sơ qua gate, ZIP/Git có evidence riêng.
PENDING: chỉ chờ Thy/GPT Web kiểm ứng dụng; I04 DEFERRED; coldboot WSL/Windows NOT_TESTED, autostart chưa triển khai. Không xem được jobfull cũ trong REST do expiry; dùng archivedevidence, không fullrerun mới.
LAST EVIDENCE: 10/10 qa/phase4-resume-20261010/resume-verification.json17/17/windows-verification.json4/4;1571/1571/source21/ZIP khớp. QA4/resume-publication-1.json:5b7f620 remote14/14; index295file0finding. WSL2 ban đầu Stopped, đã mở và khởi động app/Flink bằng launcher, holder session9762/80208; foreground. QA4 gate126/126/8ảnh là snapshot09/10, không chạy lại. Receipt local QA4/remote-readback.json kiểm HEAD sau checkpoint cuối.
NEXT EXACT ACTION: dừng; Thy/GPT Web đọc .agent/qa/phase4-resume-20261010/review.md và mở app localhost8501 để duyệt. Không tự I04/Word/PPT/Phase5 hoặc chạy lại mô hình; kiểm dịch vụ/receipt khi quay lại.

Các block sau là lịch sử; decision app scope và checklist QA4 có ưu tiên.

## Lịch sử — Phase3 ACCEPTED; Phase4 được phép triển khai; GitHub checkpoint

CURRENT TASK: checkpoint code/tài liệu đã phát hành lên repo public thy0805/bigdata; Phase4 I01–I05 là bước tiếp theo đã được duyệt.
SOURCE CHECKPOINT: .agent/decisions/20261009-phase4-approval.md; nguồn QA3 đã nghiệm thu; ../.agent/decisions/20261009-github-publication.md.
ALLOWED SCOPE: Phase4 kiểm tích hợp/runbook/launcher/QA mới và GitHub; không thay artifact đã khóa.
LOCKED: Phase3 đã ACCEPTED qua hồ sơ/8ảnh/54hash và QA96/96; model cuối,11feature,D09,Train-only và metricTest4590 giữ nguyên.
APPLIED BUT UNVERIFIED: không có code Phase4 mới; tài liệu bổ sung bàn giao được kiểm ở verify-index-2.json trước commit tiếp.
VERIFIED: push ban đầu commit31a7703; remote main khớp HEAD; đọc lại README/app/review3/metrics trên GitHub PASS5/5. Git244blob bằng disk/0secretpattern; app source_signature PASS21. WSL2 running, dashboard127.0.0.1:8501, Windowslistener8501loopback; Flink có JVM8081, Windowslistener::1. Đây chỉ là probe, chưa phải QA4.
PENDING: I01–I05 chưa hoàn tất; không Phase5/Word/PPT/video/replay. LinuxFlink8081 wildcard là cấu hình cũ; cần đánh giá khi làm I02, chưa sửa.
LAST EVIDENCE: ../.agent/qa/github-publication-20261009/{verify-index-1.json,remote-readback-1.json}; GitHub get_repo/probe ss/proc/Windowslistener09/10; hồ sơ QA3 giữ nguyên. Điểm vào GPT Web: ../HANDOFF_FOR_GPT_WEB.md.
NEXT EXACT ACTION: thực hiện I01 lineage rồi I02 recovery theo decisionPhase4; tạo QA/checklistPhase4 mới, giữ artifact cũ. Không coi push là nghiệm thu4 hoặc tự sửa Word/Phase5.

Các checkpoint dưới là lịch sử; decisionPhase4 và block này có ưu tiên về phạm vi phê duyệt.

## Hiện hành — Phase3 VERIFIED kỹ thuật; chờ nghiệm thu giao diện

CURRENT TASK: bàn giao dashboard Streamlit+Plotly theo attachment0ece5ac5, chỉ Phase3; U00–U05 VERIFIED.
SOURCE CHECKPOINT: .agent/decisions/20261009-phase3-approval.md; .agent/qa/phase3-20261009/checklist.md; APP_UI_SPEC; final2B2.
ALLOWED SCOPE: dashboard/launcher mới, UI dependencies với constraints ML, QA/screenshots và Markdown điều phối.
LOCKED: final SHAf4c33c54...67d8749c, schema11/D09/Train-only, artifact các phase cũ/metricTest4590. Không train/Test rerun/pipeline/Word/replay/Phase4.
APPLIED BUT UNVERIFIED: không còn trong U00–U05; nghiệm thu của Thy/GPT Web tách khỏi QA kỹ thuật.
VERIFIED: U00–U05; Streamlit1.50.0/Plotly6.3.0,32package mới/pin cũ giữ. technical67/67; browser10/10,8ảnh cuối; doc/runtime19/19; tổngverification96/96.976/976 file cũ nguyênhash; model thật/no-fit. Windowslocalhost8501 health200, Linuxbind127.0.0.1; ZIP45file hash/read-back đạt trước final checkpoint.
PENDING: Thy/GPT Web nghiệm thu3; không Phase4/Word/replay/video.
LAST EVIDENCE: .agent/qa/phase3-20261009/{verification.json,technical-verification-v3.json,browser-verification.json,documents-verification.json,review.md,runtime-evidence.json}; runtime foreground session35813, không autostart. Gói cuối Phase3_Dashboard_Handoff_20261009_FINAL.zip/final-package-verification.json sau read-back checkpoint.
NEXT EXACT ACTION: Thy mở http://localhost:8501, gửi gói FINAL trong .agent/qa/phase3-20261009 cho GPT Web duyệt3. Nếu app tắt, dùng dashboard/README.md và kiểm cổng trước; không fit/rerun/reinstall hoặc tự Phase4.

Các block dưới là lịch sử trước phê duyệt Phase3; ưu tiên decision3 và checklist mới.

## Hiện hành — Phase2B2 VERIFIED kỹ thuật; chờ nghiệm thu và duyệt Phase3

CURRENT TASK: bàn giao2B2 theo attachment764156e8; kỹ thuật PASS51/51, không refit; T00–T05 VERIFIED.
SOURCE CHECKPOINT: `.agent/decisions/20261009-phase2b2-approval.md`; `.agent/qa/phase2b2-20261009/checklist.md`; model2B1-a2 và Phase2A-a.
ALLOWED SCOPE: evaluation code mới, output Test/final model/QA mới; Markdown điều phối.
LOCKED: candidate SHA94ed8c4e...98a95c38; Train22513/11feature/cấu hình2B1/D09; không refit Train+Validation; Test4590/hashf9785b91...bd3574.
APPLIED BUT UNVERIFIED: không còn trong scope T00–T05.
VERIFIED: pretest17/17 trước Test; Test4590 HGB MAE0.3220542588291146/RMSE0.4634874854716987kWh;51/51QA/44/44 trước đóng gói, fit0. Ba model chungmask, Decimal45; candidate/final cold-load dự báo lệch0.951/951 guard nguyên hash; snapshot trước duyệt924/933,9 cache mất;68 ngoại lệ lịch sử=16archive+52blobStorage.
PENDING: Thy/GPT Web nghiệm thu2B2 và duyệt Phase3. Không dashboard/Word/replay/cài mới.
LAST EVIDENCE: .agent/qa/phase2b2-20261009/{verification.json,review.md,selection-lock.json,documents-precheck.json,documents-verification.json}; docprecheck62/62 trên17MD; models/runs/20261009-phase2b2-a/verification.json; final models/final/hgb-uci-hourly-v1.0-train-only/manifest.json LOCKED, model SHA f4c33c54b026a3c81312dff9c9623c7dad33a3f9df4986ecd8693b7267d8749c.
NEXT EXACT ACTION: bàn giao review/evidence cho Thy/GPT Web và dừng chờ duyệt Phase3. Test đã đánh giá, không chạy evaluate/train lại hoặc tự mở UI.

Các block dưới là lịch sử trước phê duyệt2B2; ưu tiên decision2B2 và checklist mới.

## Hiện hành 09/10 — Phase2A LOCKED; Phase2B1 VERIFIED

CURRENT TASK: Phase2B1 VERIFIED kỹ thuật; bàn giao, chờ Thy/GPT Web nghiệm thu và duyệt2B2.
SOURCE CHECKPOINT: `.agent/decisions/20261009-phase2b1-approval.md`; `.agent/qa/phase2b1-20261009/checklist.md`; Phase2A run `20261009-phase2a-a` VERIFIED 29/29.
ALLOWED SCOPE: mã HGB/D09 mới, model ứng viên/run Validation mới, QA và Markdown điều phối.
LOCKED: Phase1 và Phase2A đã nghiệm thu qua hồ sơ; 11 feature, 22513/4727/4590 và split/eligibility. D09=max(0,raw). Nguồn/code/QA cũ không sửa.
APPLIED BUT UNVERIFIED: không còn trong B00–B05. Manifest là snapshot trước QA, companion verification xác nhận kỹ thuật; nghiệm thu của Thy vẫn riêng.
VERIFIED: 37/37 QA mô hình; HGB fit đúng22513 Train/11 feature, Validation4727 MAE0.3694427311570533/RMSE0.5306058050415966 kWh.0 dự báo âm; raw=final. Save/load lệch0; run a2/b model/predictions/metrics/config giống byte. Fit witness nhận đúng Train; không Test.933 file giữ hash;68 cache runtime đã đổi trước task được ghi rõ, không sửa nguồn.
PENDING: nghiệm thu2B1/chọn model để duyệt2B2. Đề xuất HGB, không tự LOCKED model. Không Test metrics, refit Train+Validation, dashboard hoặc Word.
LAST EVIDENCE: `.agent/qa/phase2b1-20261009/{verification.json,fit-witness.json,review.md,preservation-before.json,documents-verification.json}`;37/37 mô hình và47/47 docQA/18MD; run a2/b verification. Run a bị gate chặn trước fit, giữ thư mục, không promote.
NEXT EXACT ACTION: Thy/GPT Web đọc review8 mục, duyệt model/config cho2B2; chỉ sau đó kiểm seal/hash và đánh giá Test một lần. Không chạy lại2A/Flink hoặc tự mở Test khi quay lại.

Các block “hiện hành” phía dưới là lịch sử trước duyệt2B1. Scope mới nhất ưu tiên block này và decision2B1, không sửa hồ sơ QA cũ.

## Hiện hành 09/10/2026 — Phase1 LOCKED, Phase2A VERIFIED kỹ thuật

CURRENT TASK: M01–M04/G05/G06 VERIFIED kỹ thuật; bàn giao và dừng chờ Thy/GPT Web nghiệm thu2A và duyệt2B/D09.
SOURCE CHECKPOINT: .agent/decisions/20261009-phase2a-approval.md; .agent/qa/phase2a-20261009/checklist.md; Flink run20261009T102201900234-full.
ALLOWED SCOPE: forecasting mới, ML outputs/QA và venv ML riêng; tài liệu điều phối liên quan.
LOCKED: F01–F06 đã nghiệm thu qua hồ sơ; pipeline và Phase1 giữ nguyên. UCI/một hộ/kWh giờ/giờ kế tiếp; D01–D05, D06/D08/D10 và baseline/split của D07.
APPLIED BUT UNVERIFIED: không còn trong scope M01–M04/G05/G06; manifest ML giữ snapshot trước QA, verification.json xác nhận QA cuối.
VERIFIED: Python3.12.3 venv ML riêng, dependency pin/pip check; sourcegate Flink SHA8b03f1e3...a8b5b2bc/VERIFIED.31830 mẫu/11features;22513Train/4727Validation/4590Test. Naive Validation MAE0.45927228686270355/RMSE0.6828109073989009kWh; Seasonal24 MAE0.6597176503772654/RMSE0.9503385628415242kWh. Run a29/29,b30/30;9 artifact byteidentical,965 file nguồn/pipeline/Phase1/Word/PDF/ZIP/raw giữ hash. Target/origin/gap/future/testperturbation đạt.
PENDING: Thy/GPT Web nghiệm thu2A, duyệt2B/HGB/D09. Chưa fit học máy/Testmetrics/dashboard/Word; Test chỉ QA chuẩn bị dữ liệu, seal theo quy trình không mã hóa.
LAST EVIDENCE: .agent/qa/phase2a-20261009/review.md vàdocuments-verification.json38/38/16MD; data/ml/runs/20261009-phase2a-a và20261009-phase2a-b/verification.json; C27642818560bytes/D242049794048bytes sau QA. Venv /home/cute/.local/share/uci-forecast/venv,357785166bytes logic.
NEXT EXACT ACTION: Thy/GPT Web đọc review.md, nghiệm thu2A và duyệt2B/D09. Không train hoặc mở metric Test tự động khi quay lại; bảo toàn run a/b và Phase1.

Các checkpoint chờ nghiệm thu Phase1 bên dưới là lịch sử.

## Hiện hành 09/10/2026 — F05–F06 đã kiểm, chờ nghiệm thu Phase1

CURRENT TASK: F05/F06 VERIFIED kỹ thuật; hoàn tất read-back/handoff, dừng chờ Thy/GPT Web nghiệm thu Phase1.
SOURCE CHECKPOINT: .agent/decisions/20261009-flink-full-approval.md; .agent/qa/phase1-full-20261009/checklist.md; F04 SQL/hash và raw UCI.
ALLOWED SCOPE: launcher full riêng, output từng run, oracle/log/resource/handoff và Markdown liên quan.
LOCKED: F01–F04 đã được Thy chấp nhận; SQL/smoke guard và D01–D05 giữ nguyên. Không Word/model/dashboard/reinstall/Windows/restart.
APPLIED BUT UNVERIFIED: không còn trong phạm vi F05/F06/G07. Manifest là snapshot APPLIED_UNVERIFIED; verification.json của từng run xác nhận QA cuối VERIFIED. Người dùng nghiệm thu Phase1 vẫn PENDING, không tự LOCKED.
VERIFIED: full9307ab8abf4d8286245019045ed694ac168015ms và rerun170801766af83f1b80107c86d91cedfd138444ms FINISHED; mỗi run25/25QA,2075259phút/34589giờ×14=484246 trường,34085đủ/504thiếu/421khôngpower/1050âm, NULLcount2188; maxenergyerror1e-15kWh;11/11parserdatecases. Rerungrid và partcategories giốngbyte; hash8nguồn/raw/SQL/smoke giữ nguyên.
PENDING: Thy/GPT Web nghiệm thu Phase1; D06–D10/Phase2/train/dashboard/Word chưa duyệt. Không tự làm tiếp.
LAST EVIDENCE: .agent/qa/phase1-full-20261009/review.md, handoff-verification.json26/26 lúc17:32, runs/*/verification.json. WindowsREST mộtTM/hai slot/0running; C27956445184bytes/D242080260096bytes. Hai output lỗi parserD/M/YYYY giữ rejected.json, khôngpromote; SQL/smoke gốc nguyênhash, launcherfull sửa2 biểu thức đọc ngày, không đổi aggregation/NULL/residual.
NEXT EXACT ACTION: bàn giao review.md và hourly-grid.csv của run20261009T102201900234-full; chờ Thy/GPT Web. G07 documents-verification.json63/63/16MD đạt; không rerun/cài/restart hoặc Phase2 tự động sau quay lại khi chưa có yêu cầu mới.

Các checkpoint F05/F06 chưa duyệt bên dưới là lịch sử trước yêu cầu mới này.

## Lịch sử 09/10/2026 — F01–F04 đã kiểm, trước duyệt F05/F06

Thy đã duyệt D01–D05 và chỉ F01–F04 qua attachment `45ccd38f-dc6e-4fd8-9ed8-a0e40483f6ff/Văn bản đã dán.txt`. Ghi chú chờ duyệt Phase0 bên dưới là lịch sử. Thy yêu cầu agent cài Java17/python3.12-venv giúp; apt thực hiện qua root WSL có phạm vi, không dùng hay lưu mật khẩu, không đổi quyền Windows.

CURRENT TASK: F01–F04 và S05 VERIFIED; bàn giao, dừng chờ Thy/GPT Web trước F05/F06.
SOURCE CHECKPOINT: .agent/decisions/20261009-flink-phase1-approval.md; .agent/qa/phase1-smoke-20261009/checklist.md; ZIP/audit UCI và tài liệu Apache2.3.
ALLOWED SCOPE: Java17/venv/Flink2.3 trong WSL; pipeline SQL và QA mẫu; TXT trên D; tài liệu điều phối. Không Word/model/dashboard/full aggregation.
LOCKED: D01–D05; BATCH SQL, một hộ lịch sử; giờ thiếu NULL, không nội suy/clamp; không Docker/reinstall/restart.
APPLIED BUT UNVERIFIED: không còn thay đổi chưa kiểm trong scope. Giới hạn: visual UI khung bên hẹp chỉ thấy sidebar, không kiểm mọi màn hình; không có fullhourlydata/model/app.
VERIFIED: apt ba bước exit0; Java17.0.20.1/Python3.12.3/Linuxvenvpip24.0; Flink2.3.0 c0f8d1a SHA512 khớp; runtime653947269bytes. ZIP/TXT nguyên bytes; tám nguồn giữ hash. Windows8081UI/REST200 mộtTM/hai slot; browserDOM có jobFINISHED. SQL cuối so mẫu10k/168giờ14cột Decimal;11jobs cuối9FINISHED+2FAILED có chủ ý,82/82checks; rerungridgiốngbyte. Precisionresidual không gắn cờâmgiả.
PENDING: Thy/GPT Web duyệt F05/F06 trước fullaggregation; D06–D10/ML/UI chưa duyệt; Word giữ nguyên.
LAST EVIDENCE: QA smoke-verification.json82/82 lúc16:32; handoff-verification.json37/37, liveREST mộtTM/hai slot/0running, disk16:38 C27823206400bytes/D224378388480bytes; runtime-install/environment-final/inputs-manifest.json, review.md và checklist.md. Job thật012e738558e523488383da8e5456fe5d; rerun3aa29bb5c6fee8b17a7e33504b9e1d35.
NEXT EXACT ACTION: bàn giao review.md và chờ duyệt F05/F06. Sau duyệt đọc checklist/review/README trước thiết kế full launcher; không bỏ F04QA-onlyguard. Cluster foregroundserve session30934, kiểmREST trước dùng; chưaautostart/service, khôngreinstallWSL.

Disk snapshot trước cài: C30785843200bytes (~28.67GiB), D225280733184bytes. Sau cài ~16:15 C28459868160bytes (~26.50GiB). VHD trên C; tải archive/raw/log/output QA trên D. Không quy toàn bộ biến thiên C cho Flink vì Windows còn chạy tác vụ khác.

## Lịch sử 09/10/2026 15:43 — Giai đoạn 0 trước duyệt/cài

- VERIFIED khảo sát/tài liệu, chưa duyệt thiết kế triển khai: năm Markdown trong `docs/phase0-20261008/`; checklist canonical `.agent/qa/phase0-resume-20261009/checklist.md` R00–R05. Các snapshot WSL/DISM/timer bên dưới là lịch sử, không dùng làm hiện trạng.
- Probe trực tiếp 15:43: WSL 2.7.14.0, Ubuntu-24.04 chạy VERSION2, Ubuntu24.04.5, user cute; Python Linux3.12.3. Chưa có Java/JAVA_HOME, pip/ensurepip/python3.12-venv package, Flink/PyFlink ở các vị trí/package đã kiểm. Python/Java Windows giữ nguyên. WSL2 đã chạy, không tiếp tục repair WSL cũ.
- Windows đọc dịch vụ HTTP tạm trong WSL qua localhost thành công, server đã kết thúc; Linux đọc ổ D/Downloads và gọi Windows thành công. Đây không phải kiểm Flink Web UI. C còn khoảng18.34GiB và VHD Ubuntu nằm trên C; dung lượng ảo Linux khoảng1TB không phải dung lượng vật lý còn trống.
- Tái sử dụng full audit UCI: 2.075.259 dòng, 25.979 dòng thiếu, 34.589 giờ/34.085 giờ đủ60 đo hợp lệ. Kiểm độc lập10.000 dòng/hai giờ bằng Decimal, metadata/invariants và tám hash nguồn:13/13. Không quét lại toàn bộ độc lập; chưa tạo dữ liệu theo giờ triển khai.
- Đề xuất chờ duyệt: Flink2.3.0 standalone SQL Client + Java17 trong WSL, bounded BATCH trước; Python3.12 venv cho các giai đoạn sau. Không cần PyFlink cho phương án SQL. Giữ giờ thiếu/energy_kwh NULL, không nối lag qua gap hoặc clamp residual âm. UI Minimal ba tab và dự báo một hộ giờ tiếp theo giữ nguyên.
- Lượt này chỉ tạo tài liệu và QA/script kiểm tra; không cài package, job/pipeline/model/dashboard, không sửa Word hoặc ZIP, không thay Windows/VMware/power/restart. Hash Word QA v3 và nguồn được bảo toàn.

CURRENT TASK: Giai đoạn 0 VERIFIED khảo sát/tài liệu; dừng chờ Thy và GPT Web duyệt.
SOURCE CHECKPOINT: yêu cầu tiếp tục09/10; full audit cũ + probe/hash/mẫu độc lập hiện tại; năm MD và nguồn chính thức.
ALLOWED SCOPE: Markdown điều phối/thiết kế và QA chỉ đọc của lượt này.
LOCKED: UCI một hộ, phút → kWh giờ, dự báo giờ kế tiếp; không Docker; UI ba tab; từng giai đoạn cần phê duyệt.
APPLIED BUT UNVERIFIED: phiên bản/kiến trúc Flink mới chỉ đề xuất, chưa cài hoặc chạy thử; không có pipeline hay model.
VERIFIED: WSL2/runtime/network/path;13 kiểm dữ liệu/hash; năm MD read-back và verifier tài liệu; nguồn Word/ZIP/PDF không đổi.
PENDING: D01–D05 trong OPEN_DECISIONS.md; Giai đoạn 1 TODO, không tự triển khai.
LAST EVIDENCE: .agent/qa/phase0-resume-20261009/{environment.json,environment-extra.md,dataset-verification.json,documents-verification.json,review.md}.
NEXT EXACT ACTION: sau phê duyệt D01–D05, kiểm lại dung lượng C rồi làm F01 chuẩn bị Java17/Flink/venv; chạy smoke job mẫu trước full dataset và đối chiếu độc lập, theo IMPLEMENTATION_PLAN.md.

## Power setting mới nhất — Thy yêu cầu bỏ tự tắt màn hình 09/10/2026

- VERIFIED: đã đổi monitor-timeout-ac về 0 (Never) bằng powercfg và đọc lại VIDEOIDLE AC=0, DC=0. Màn hình không tự tắt khi cắm sạc do timeout này nữa; setting được lưu trên power plan hiện hành. Không thay sleep, không đặt timer shutdown mới. Ghi chú AC120 giây bên dưới là lịch sử đã được yêu cầu này thay thế.

## Lịch sử live check 09/10/2026 10:32 — timer đã kết thúc

- Read-back status.json: SHUTDOWN_REQUESTED, ShutdownExitCode=0, deadline02:16:44 đã qua; không tạo hẹn mới. Windows LastBootUpTime=10:20:56 ngày09/10. Đây chứng minh lệnh shutdown được nhận và máy hiện đã có phiên boot mới, không chứng minh chính xác thời điểm tắt vật lý.
- Không thấy Dism/DismHost; TiWorker/TrustedInstaller hiện chạy với PID mới và CBS có log10:31. Chưa có kết quả thành công bật VMP trong DISM log đã đọc; không suy ra Windows đang treo chỉ từ service tồn tại.
- Chưa có C:/Program Files/WSL/wsl.exe hoặc WslService/LxssManager trong probe. Chưa gọi CLI WSL tránh tự kích hoạt repair; chưa xác minh WSL2 chạy. Lịch sử Antigravity chưa có phát hiện mới ngoài audit287 chat bên dưới.
- NEXT EXACT ACTION: tiếp tục kiểm trạng thái VMP và thiếu runtime WSL theo read-only; nếu cần quyền admin thì hướng dẫn Thy. Timer cũ đã kết thúc, không chạy lại.

## Lịch sử 09/10/2026 01:48 — timer và lịch sử Antigravity

- Thy yêu cầu ưu tiên màn hình tắt/máy vẫn chạy và hẹn shutdown 30 phút độc lập quota. VERIFIED powercfg: AC display 120 giây, DC giữ 0; sleep AC/DC giữ 0. Helper PID21884 bắt đầu 01:46:44+07, deadline **02:16:44+07 ngày 09/10/2026**; status RUNNING cập nhật. Không force-close, không reboot. Chưa thử shutdown thực tế, app chưa lưu có thể chặn. Hủy trước deadline bằng `.agent/scripts/Huy_hen_tat_may_20261009.cmd`; launcher chưa chạy thử vì phải giữ timer. QA `.agent/qa/power-timer-20261009/checklist.md`, status.json và backup trước đổi.
- Thy đã mở Hub và Antigravity IDE. Đọc RPC gốc đủ 287 chat riêng biệt/50.831 step: legacy-v2 126 chat/25.877 step, IDE-extra 161 chat/24.954 step, cả hai 0 lỗi và ReadSteps=ExpectedSteps toàn bộ. Không gửi message hoặc chạy lệnh lịch sử. Đúng bối cảnh lỗi sandbox ngày 14/5 được xác nhận; **chưa tìm được chuỗi cài/sửa Ubuntu/WSL thành công** trong văn bản/tool output đã quét. Các match mới chỉ extension remote-wsl, cảnh báo TensorFlow và nhắc WSL không liên quan sửa. Giới hạn: không OCR ảnh lịch sử; không suy ra chưa từng sửa hoặc WSL chưa từng hoạt động.
- 01:47 không còn Dism/DismHost trong process snapshot; TiWorker/TrustedInstaller còn. DISM log cuối vẫn 00:19:35, chưa có success/exit code. Không kết luận VMP đã bật; agent không hủy tiến trình. Các snapshot bên dưới là lịch sử, không phải trạng thái hiện tại.

CURRENT TASK: Giai đoạn 0 IN_PROGRESS; timer độc lập đang chạy; tra lịch sử hoàn tất phạm vi văn bản/tool output hiện có.
SOURCE CHECKPOINT: Thy cho phép shutdown 30 phút tại lượt này; audit JSON legacy-v2 và IDE-extra, powercfg/status read-back.
ALLOWED SCOPE: màn hình AC/timer theo Thy, QA/context/PLAN/index và khảo sát chỉ đọc; không chạy lại cách sửa từ chat cũ.
LOCKED: UCI/một hộ/kWh giờ/giờ tiếp theo; không Docker; không sửa Word; không tự restart. Ngoại lệ mới duy nhất: shutdown đã được Thy yêu cầu lúc 02:16:44 ngày 09/10, không force.
APPLIED BUT UNVERIFIED: launcher hủy chưa chạy; shutdown thực tế chưa kiểm; năm Markdown Phase0 chưa tạo.
VERIFIED: timer process/status tiến triển; AC display120 và sleep0; 287 chat/50.831 step đọc đủ, 0 lỗi/count mismatch.
PENDING: xác minh kết quả DISM/VMP và WSL2 sau khi Thy bật máy lại; Phase0 chưa được duyệt; không app/job/train.
LAST EVIDENCE: .agent/qa/power-timer-20261009/status.json và checklist.md; .agent/qa/phase0-20261008/antigravity-api-legacy-v2-20261009.json và antigravity-api-ide-extra-20261009.json.
NEXT EXACT ACTION: khi quay lại kiểm giờ/status timer trước, không khởi động timer cũ lần nữa; kiểm VMP bằng read-only có quyền phù hợp, hỏi kết quả terminal DISM của Thy nếu cần. Không coi DISM đã xong chỉ vì process mất.

## Checkpoint trước 01:06 — lịch sử Giai đoạn 0 và chẩn đoán WSL

- Thy giao khảo sát/thiết kế Giai đoạn 0, năm tài liệu Markdown; không xây app, chạy job Flink, train model hoặc sửa Word. Quy trình triển khai từng giai đoạn chỉ chuyển sau Thy duyệt. Thy cho phép hỗ trợ cài công cụ, nhưng chốt WSL2 + Apache Flink trực tiếp, không Docker Desktop; chẩn đoán WSL trước, gặp Administrator/restart phải hướng dẫn và chờ xác nhận, không tự restart. Chỉ cài Flink sau WSL2 hoạt động.
- ZIP trong Downloads đã quét toàn bộ bằng `.agent/scripts/audit_phase0_uci.py`; evidence `.agent/qa/phase0-20261008/dataset-audit.json`: 2.075.259 dòng, 9 cột, timestamp liên tiếp từng phút, không trùng/sai, 25.979 dòng thiếu, 34.589 giờ có dữ liệu/34.085 giờ đủ 60 đo hợp lệ. Thiếu gồm dấu `?` và ô rỗng; có gap dài 7.226 phút và 1.050 residual đo phụ âm cần giữ cờ. Chưa tạo dữ liệu triển khai, chưa kiểm độc lập đầy đủ.
- VERIFIED chẩn đoán môi trường 09/10: Windows 11 Home 25H2 26200.9457; VMP Disabled, Hypervisor Platform Enabled, WSL optional component cũ Disabled. HypervisorPresent true/VBS đang chạy; không kết luận BIOS tắt từ các CPU flag false. Appx WSL 2.7.3.0 là gói glue, runtime MSI/registry MSI/installer service-class đều thiếu. Đối chiếu đúng mã Microsoft tag 2.7.3 giải thích trực tiếp lỗi `CallMsi/Install/REGDB_E_CLASSNOTREG`; chưa biết sự kiện lịch sử làm thiếu. Windows Installer COM chung tạo được, không được gọi là MSI toàn hệ thống hỏng.
- Phiên không Administrator. Không cài hoặc sửa hệ thống; không chạy WSL trong probe cuối vì CLI có thể tự vào nhánh repair. Python đã có Miniconda 3.13.13; Java PATH 8u401 và Android Studio JBR 21.0.8 giữ nguyên, chưa tạo môi trường riêng/JDK17/Flink. Hash ZIP và Word QA v3 khớp nguồn.
- Nguồn hiện hành: `.agent/qa/phase0-20261008/checklist.md`, `environment-wsl-20261009.json`, `WSL_DIAGNOSIS.md`; script `audit_wsl_readonly.ps1`. Năm tài liệu `docs/phase0-20261008/` chưa tạo và Phase0 chưa hoàn tất. Các mốc Word bên dưới là checkpoint artifact, không phải nhiệm vụ hiện tại.
- 09/10 00:28–00:29: Thy đã chạy DISM bật VMP bằng Administrator; ảnh ở 37.8%, cửa sổ `Select`. VERIFIED snapshot: bốn tiến trình DISM/CBS còn tồn tại, CBS.log tăng 672 byte/5 giây nhưng DownloadProgress lặp 50/100 — đang chờ Windows Update, chưa chứng minh tải có tiến triển hoặc feature đã bật. Hướng dẫn Esc bỏ Select, không Ctrl+C/đóng/restart/chạy lại. Lỗi đỏ riêng do profile gọi hook Miniconda cũ ở ProgramData, hook thật nằm trong Users; chỉ chẩn đoán, chưa sửa profile. Evidence `dism-progress-20261009-0028.md`.

- 09/10 khoảng 00:58–01:06: Thy giao tra lịch sử Antigravity, xác nhận trước đây cài WSL để sửa lỗi sandbox khi làm đồ án rồi sau đó xóa. VERIFIED tìm đúng bối cảnh chiều 14/5 tại ba chat `ff1e3079...`, `64d6a1a8...`, `b5a8f5cf...`: agent báo `sandboxing is not supported on Windows`, Thy yêu cầu dùng WSL và nói đã cài. Chưa tìm được chuỗi cài/sửa thành công; archive nhị phân chưa đọc hết, Antigravity không chạy và API metadata báo thiếu địa chỉ LS. Không chạy lại lệnh lịch sử. Evidence `antigravity-wsl-history-20261009.md`.
- DISM 00:58 vẫn còn các tiến trình từ 00:19:33, CBS lặp DownloadProgress 50/100. Ảnh Thy mới đã hết Select; không quy cho selection nữa. Snapshot cũ 00:28 chỉ dùng truy vết. Chưa hủy lệnh, sửa Windows, cài thêm hoặc restart.

CURRENT TASK: Giai đoạn 0 IN_PROGRESS; tra lịch sử Antigravity đã tìm đúng bối cảnh nhưng chưa tìm quy trình sửa; DISM bật VMP chưa có kết quả cuối.
SOURCE CHECKPOINT: Thy chọn WSL2 trực tiếp; ZIP/Word v3 giữ hash; metadata máy 09/10 và mã Microsoft tag 2.7.3.
ALLOWED SCOPE: khảo sát chỉ đọc, QA/context/PLAN/index và tài liệu thiết kế; hỗ trợ cài môi trường theo cổng Thy đã chốt.
LOCKED: UCI/một hộ/kWh theo giờ/giờ tiếp theo; UI Minimal ba tab; không Docker; không tự restart, thay dataset hoặc sửa Word; từng giai đoạn phải được duyệt.
APPLIED BUT UNVERIFIED: năm Markdown chưa tạo; quét dữ liệu hoàn tất nhưng phép đối chiếu độc lập còn thiếu.
VERIFIED: audit read-only môi trường chạy; trạng thái package/class/service/features và native versions; đối chiếu nhánh lỗi Microsoft; ZIP và Word v3 không đổi hash.
PENDING: mở Antigravity để đọc lịch sử gốc và tìm chuỗi sửa sau bối cảnh 14/5; kết thúc DISM và xác minh VMP qua cổng Thy thao tác, không tự hủy/restart; cài MSI chính thức nếu phù hợp; chứng minh WSL2 chạy; hoàn thiện Phase0 và nhận duyệt trước job/app/model. Chờ tải CBS chưa xác định nguyên nhân sâu.
LAST EVIDENCE: .agent/qa/phase0-20261008/antigravity-wsl-history-20261009.md (history và CBS 00:58); environment-wsl-20261009.json, WSL_DIAGNOSIS.md và dataset-audit.json. dism-progress-20261009-0028.md là snapshot cũ.
NEXT EXACT ACTION: đề nghị Thy mở Antigravity để tiếp cận lịch sử đầy đủ; tìm đoạn cài/sửa WSL sau các thử nghiệm 14/5. Không chạy lại lệnh từ chat cũ hoặc cài Flink; DISM đang chạy không tự hủy/restart.

## Checkpoint Word 08/10/2026 — QA v3 caption, công thức, bìa và trích dẫn

- Bản tiếp tục: `BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx`, 37 trang, SHA-256 `efc3acdfec05bc264eb3320f2df363241cab29818830a7159cc88aabdb77bdd1`. VERIFIED artifact: 31/31 checks và xem riêng đủ 37 PNG cuối; chưa LOCKED bởi Thy.
- Sửa 5 caption thành field lấy số chương bằng `STYLEREF "ChapterTitle" \n \t`, giữ SEQ và cho ra Bảng 1.1–1.4, Hình 1.1. MAE dùng cặp dấu trị tuyệt đối OMML native; RMSE và E = P × Δt giữ nguyên. Thử thêm/xóa caption, heading, cập nhật TOC và danh mục trong Word đều đạt, không lưu probe vào nguồn.
- Theo yêu cầu bổ sung của Thy: bỏ đúng 29 marker [n] trong nội dung trước Tài liệu tham khảo; giữ [1]–[16] ở danh sách nguồn và 16 hyperlink, giữ footer Roman i–x và Arabic 1–25. Không gọi bản không có in-text citation là chuẩn IEEE đầy đủ.
- Hai bìa được đối chiếu lại Mauwword: tiêu đề 20 pt, ngành 16 pt, tên/MSSV 14 pt căn trái cùng khối; sửa khoảng cách/vị trí, giữ Times New Roman đen, logo và khung. Thy đã xác nhận danh sách chính thức: Nguyễn Đức Thành Phát 2001230640, Lý Vũ Nhân Hậu 2001230227, Nguyễn Tuấn Khôi 2001230418; giảng viên Nguyễn Thành Ngô giữ nguyên.
- Nguồn gốc và QA v2 không đổi hash, không ghi đè file đang mở. Styles, numbering, footer/header, ảnh và geometry bảng giữ nguyên. Các trang 3–13 và 27–37 bằng v2 từng pixel; Chương 2–5, phần trống và Tài liệu tham khảo không bị viết lại. Không đọc/chạy dataset hoặc triển khai ứng dụng ở lượt QA.
- Giới hạn: lỗi caption/MAE được GPT web báo chưa tái hiện ở Word native của bản nguồn; đã sửa cấu trúc field/Equation và kiểm Word/PDFium. Chưa kiểm được renderer của GPT web. Renderer đóng gói thiếu LibreOffice; không cài phần mềm thay thế.
- QA canonical: `.agent/qa/word-uci-cover-citations-20261008/` (checklist, review, verification, final-word, caption/heading-probes, final-render). QA caption/math v2 là bước nguồn; bản ghép ban đầu dưới đây là lịch sử.

CURRENT TASK: VERIFIED QA v3 và đồng bộ tài liệu điều phối; sẵn bàn giao, chờ Thy duyệt.
SOURCE CHECKPOINT: Thy 08/10 mở rộng scope bỏ marker và sửa bìa; QA v2 hash a69a0a...2f6f5, mẫu trường 25ce34...ec35, nguồn ghép 51edbc...582fe2.
ALLOWED SCOPE: bản mới v3, caption/MAE, marker trong bài, hai bìa theo mẫu, field/QA và tài liệu liên quan.
LOCKED: UCI/một hộ/kWh theo giờ/giờ tiếp theo; 3 thành viên và MSSV đã xác nhận; giữ nguồn, khung/logo, hình/bảng, Chương 2–5 và dữ liệu/ứng dụng.
APPLIED BUT UNVERIFIED: không còn sửa artifact hoặc tài liệu điều phối chưa kiểm trong lượt QA.
VERIFIED: 31/31 structural/semantic/runtime checks; 37 trang đã xem riêng; Word probe caption/heading/TOC đạt; 29 marker bỏ, 16 nguồn/hyperlink giữ; 5 caption đúng, 3 Equation; source hash giữ.
PENDING: Thy duyệt v3; nội dung Ch2 thật, Ch3–5 và thực nghiệm; lời cảm ơn/Mở đầu/Kết luận, lịch tuần, phần việc Phát và đóng góp chưa xác nhận. Không tự triển khai.
LAST EVIDENCE: .agent/qa/word-uci-cover-citations-20261008/verification.json, final-word.json, final-pdf.json, caption-probes.json, heading-probes.json, final-render/page-1.png đến page-37.png, review.md.
NEXT EXACT ACTION: bàn giao v3 và nhận phản hồi Thy; không tự sửa tiếp nội dung hoặc triển khai ứng dụng.

## Checkpoint ghép ban đầu 08/10/2026 — lịch sử

- Thy đã giao thực hiện chỉnh Word mới trong thư mục này; không còn chờ xác nhận nhóm/dataset/phạm vi. LOCKED: nhóm 3 người, UCI Individual Household Electric Power Consumption, một hộ, điện năng kWh theo giờ, dự đoán giờ tiếp theo. Mauwword là chuẩn hình thức; khung v2 ở thư mục cha là nguồn báo cáo, không sửa nguồn.
- Dataset do Thy chỉ rõ: `C:/Users/thy/Downloads/individual+household+electric+power+consumption.zip`. VERIFIED đọc hết thành viên ZIP `household_power_consumption.txt`: 9 cột phân cách `;`, 2.075.259 bản ghi, 25.979 giá trị thiếu ở mỗi cột số; đầu/cuối 16/12/2006 17:24:00 và 26/11/2010 21:02:00. Chưa kiểm sâu trùng thời gian/ngoại lệ hoặc xử lý dữ liệu. Không giải nén/di chuyển ZIP. `Partitioned UCI Data` không tồn tại trong cây thư mục đã tìm.
- Nhiệm vụ: ghép Chương 1 Khôi, bổ sung 1.3 và sửa trọng điểm; Chương 2 Hậu chỉ có 14 heading nên giữ trống; đồng bộ đề mục 3–5 theo UCI. Thêm form lịch tuần và phân công, không bịa lịch sử hoặc tỷ lệ đóng góp. Chưa triển khai ứng dụng/huấn luyện.
- VERIFIED: `BaoCao_PhanTich_DuDoan_DienNang_UCI_20261008.docx`, 37 trang, SHA-256 `51edbc9ba1f27e2d2c194eabca31f8f7fcd15568b5edc5ea1a8cdb9097582fe2`. Hai bìa theo mẫu trường, khung cover1 và logo giữ; bìa không số, front i–x, nội dung 1–25. Ghép Chương 1 đủ 11 mục, 4 bảng/1 hình giữ từ Khôi, thêm 1.3 và 3 công thức OMML; 16 nguồn hyperlink. Heading/TOC/Caption/PAGE thật, 77 H2 và 91 TOC entry; đã thử chèn/xóa heading/caption trong Word và xem đủ 37 trang cuối. Chỉ VERIFIED phần ghép và khung, chưa phải báo cáo nộp hoàn chỉnh hoặc được Thy LOCKED.
- Chương 2 vẫn đúng 14 heading từ Hậu; Chương 3–5 chỉ đề cương 13/14/17 mục đã đồng bộ UCI/hour-ahead, không có kết quả giả. Lời cảm ơn, Mở đầu và Kết luận còn trống. Lịch 10 tuần, mức đóng góp và phần việc của Nguyễn Đức Thành Phát để trống vì chưa có thông tin chắc chắn. Khôi Ch1/Hậu Ch2 được ghi theo nguồn thực tế. Không tự đồng nhất Phát với Thy.
- Scope/checklist: `.agent/qa/word-uci-20261008/checklist.md`; contract: `artifact.md`; evidence: `final-verification.json`, `final-field-tests.json`, `final-word.json`, `final-render/`, `dataset-inspection.json`; `review.md` đối chiếu PDF/phần thiếu. Nguồn DOCX/PDF/ZIP giữ hash. Các checkpoint tiếp nhận/dựng khung dưới đây là lịch sử, không được ghi đè quyết định hiện hành.

CURRENT TASK: VERIFIED ghép Chương 1 và hoàn thiện Word khung UCI; chờ Thy duyệt bản mới.
SOURCE CHECKPOINT: Thy 08/10; khung v2 e44e1a...5a58, Khôi d7d62c...3b15, Mauwword 25ce34...ec35; ZIP 9f84b4...a3ff.
ALLOWED SCOPE: bản Word mới, sửa trọng điểm Chương 1, front matter, đề mục 3–5, QA và tài liệu điều phối; đọc ZIP.
LOCKED: 3 người; UCI/một hộ/giờ tiếp theo; tên/MSSV từ nguồn; giữ nguồn PDF/DOCX/ZIP, bài Flink cũ, slide/script.
APPLIED BUT UNVERIFIED: không còn sửa artifact hoặc tài liệu điều phối chưa kiểm; đã đọc lại các file liên quan ở root và project.
VERIFIED: 41/41 structural/semantic/runtime checks; 37 trang đã xem; TOC/numbering/list caption chèn/xóa cập nhật đúng; 4 bảng và bytes hình nguồn giữ; 4 DOCX/PDF/ZIP không đổi hash; ZIP đọc đủ 2.075.259 dòng.
PENDING: Thy duyệt Word; nội dung Chương 2 thật; Chương 3–5 và thực nghiệm/code/demo; lời cảm ơn/Mở đầu/Kết luận; lịch tuần/phân công Phát/tỷ lệ đóng góp thật. Không hỏi lại dataset, nhóm hoặc horizon đã chốt.
LAST EVIDENCE: .agent/qa/word-uci-20261008/final-verification.json, final-field-tests.json, final-word.json, final-render/page-1.png đến page-37.png, review.md.
NEXT EXACT ACTION: nhận phản hồi về bản Word mới. Nếu Thy giao Chương 3, lập scope khảo sát/tiền xử lý riêng từ ZIP hiện tại và chỉ viết kết quả sau chạy thật; không tự bắt đầu ứng dụng trong lượt Word này.

## Lịch sử tiếp nhận 08/10/2026 — trước khi được giao chỉnh Word

- Thư mục triển khai do Thy chỉ định là `D:\Hoctap\bigdata\Detaituan8910`; `../Mauwword` chỉ dùng tham khảo định dạng. Đã đọc bản dán mới đủ 468 dòng, PDF giảng viên đủ 5 trang, bài Chương 1 đủ 15 trang và mẫu Word đủ 18 trang.
- Bản dán đề xuất chuyển London sang UCI Individual Household Electric Power Consumption: một hộ, kWh theo giờ, dự đoán một giờ tiếp theo; Flink là lớp xử lý, ML là thành phần riêng. Đã đối chiếu metadata/đơn vị trên trang UCI chính thức, chưa có dữ liệu địa phương để kiểm. Hướng này đã được tiếp nhận, chưa tự khóa hoặc sửa outline vì lượt trực tiếp yêu cầu đọc; đã hỏi Thy chọn chỉ rà soát hay thực hiện chỉnh Word, chưa có trả lời.
- Nguồn Chương 1 có nội dung là `KhoiTuan Tong Quan Bai Toan Chuong 1.docx`, khác với đề cương một trang cũ. Thiếu 1.3, không có Heading thật; có 4 bảng và Hình 1.1 thật. Cần chỉnh bảng 1.4 tách trang, trình bày công thức và rà nguồn; không cần bỏ toàn bộ nội dung. Chương 2 hiện chỉ là đề cương 14 mục.
- PDF cho phép Flink, không bắt buộc Spark/HDFS; yêu cầu thêm lịch làm việc theo tuần và mức đóng góp. PDF ghi nhóm 2, hồ sơ hiện có 3; không tự xóa người. Mốc tuần trong PDF chưa nhất quán nên không suy ra deadline.
- Mẫu Word quy định A4, Times New Roman, lề trái 3,5 cm/các lề khác 2,5 cm, thân bài 13 pt/Multiple 1,3; caption và các danh mục tự động. Mẫu có hai bìa, khung cũ một bìa theo yêu cầu lúc dựng; không tự thay cấu trúc bìa trước xác định phạm vi.
- VERIFIED cho hiện trạng nguồn: cả 5 PDF/DOCX giữ nguyên SHA-256. Chưa sửa Word, triển khai code, tải dữ liệu, huấn luyện hoặc tạo kết quả. Chưa kiểm đủ paper/17 nguồn trong Chương 1.
- Không thấy `Partitioned UCI Data` tại root hoặc trong thư mục này, cũng không thấy `Partitioned LCL Data` tại đường dẫn cũ. Không có CSV/notebook/mã ứng dụng ngoài `.agent` theo inventory hiện tại của thư mục này; không suy rộng sang toàn ổ D:.
- Bằng chứng và nội dung rà soát: `.agent/qa/intake-20261008/review.md`, `checklist.md`, `sources.json`, văn bản trích xuất và ảnh Word/PDF.

## Recovery checkpoint tiếp nhận 08/10/2026 — lịch sử

CURRENT TASK: tiếp nhận và đối chiếu tài liệu mới; VERIFIED cho việc đọc/kiểm hiện trạng, chưa chỉnh báo cáo.
SOURCE CHECKPOINT: yêu cầu trực tiếp của Thy; PDF giảng viên; Chương 1 có nội dung; bản dán là đề xuất; Mauwword là nguồn format. Hash 5 nguồn giữ nguyên theo sources.json.
ALLOWED SCOPE: đọc/audit nguồn, QA và tài liệu điều phối trong Detaituan8910. Chỉ sửa Word sau khi làm rõ yêu cầu thực hiện bản dán.
LOCKED: giữ nguyên các PDF/DOCX nguồn, khung v2, tài liệu Flink tuần 5–7, slide/script và tên/MSSV đã xác nhận.
APPLIED BUT UNVERIFIED: không có thay đổi artifact; ghi chú điều phối đã đọc lại, không còn cập nhật chưa kiểm trong lượt tiếp nhận.
VERIFIED: PDF 5 trang, Chương 1 15 trang, mẫu 18 trang đã xem; Chương 2 chỉ outline; các lỗi cấu trúc/bố cục ghi trong review.md; UCI metadata/đơn vị đã đối chiếu; file nguồn không đổi.
PENDING: lựa chọn chỉ rà soát hay chỉnh Word; xác nhận hướng UCI/nhóm/số bìa khi cần; đường dẫn dataset/code; kiểm đầy đủ nguồn học thuật; toàn bộ thực nghiệm.
LAST EVIDENCE: .agent/qa/intake-20261008/review.md, checklist.md, sources.json, chapter1-word.json, teacher-render/, chapter1-render/, template-render/; hash read-back khớp cả 5 nguồn.
NEXT EXACT ACTION: nhận phản hồi Thy; nếu chỉnh Word, lập scope riêng và tạo bản mới trong Detaituan8910, không chạy ứng dụng hoặc ghi kết quả khi chưa có dữ liệu thật.

## Checkpoint dựng khung 06/10/2026 — lịch sử

- Tên đề tài: Phân tích dữ liệu tiêu thụ điện năng và dự đoán nhu cầu sử dụng điện theo thời gian.
- Phạm vi riêng với báo cáo Apache Flink tuần 5–7; không sửa hoặc gộp báo cáo/slide của bài trước.
- Khung năm chương chốt ngày 01/10/2026; prompt ngày 06/10/2026 ưu tiên tên 3.4 “Kiểm tra chất lượng dữ liệu” và 5.10 “Tích hợp mô hình dự đoán”. Các tên dài hơn trước đó chỉ còn là lịch sử.
- Thy nhận Chương 3, 4 và 5. Chưa chỉ định người nhận Chương 1–2 trong lượt này.
- Hai đề cương hiện mang tên KhoiTuan_Chuong1_TongQuanBaiToan.docx (11 mục) và HAULYVUNHAN_Chuong2_CoSoLyThuyet.docx (14 mục). Ngày 06/10 đã đọc lại nguyên văn và kiểm SHA-256: cùng bytes bản một trang được kiểm ngày 01/10; không nhập nội dung các file này vào báo cáo mới.
- VERIFIED hiện hành ngày 06/10: ../BaoCao_PhanTich_DuDoan_DienNang_Khung_v2.docx, 21 trang, một bìa, 8 phần chính và 77 mục cấp 2; có đầy đủ bảng phân công, lời cảm ơn, TOC, danh mục thuật ngữ/hình/bảng. Chỉ là khung; toàn bộ nội dung, công việc phân công, thuật ngữ, hình/bảng và tài liệu tham khảo còn trống. Bản khung không hậu tố được giữ nguyên làm nguồn/lịch sử.
- Mẫu định dạng tại lượt dựng khung: ../ApacheFlink.docx, 47 trang, SHA-256 khi dựng efac5eade11afeff8b17f458b183edcb5f1ca600ebdfbb86e167d895d08662d3; không có bản Flink trong thư mục đồ án mới. Giữ A4, lề, Times New Roman đen, styles, logo và khung cornerTriangles; dùng một bìa theo prompt. Bìa không số, phần đầu i–viii, Mở đầu bắt đầu 1. Hash mẫu là checkpoint lịch sử, phải đọc lại trước lượt dùng mẫu mới; lượt sửa MSSV chỉ dùng bản khung d2199f...acdd, không sửa mẫu Flink đang mở.
- TOC có 90 mục và hyperlink nội bộ; numbering chương/mục tự động, style cấp 3 sẵn dùng. Word đã thử chèn/xóa mục, cập nhật TOC và thêm caption trong bộ nhớ rồi đóng không lưu; các danh mục nhận đúng. Đã kết xuất và xem đủ 21 trang ở 144 dpi. SHA-256 đầu ra d2199f0a30ba74234778622d14f4757736faea2eeddfd0d560d162c4f4deacdd; evidence .agent/qa/diennang-khung-20261006/verification.json.
- Bìa dùng tên giảng viên Nguyễn Thành Ngô và danh sách sinh viên từ nguồn Word. Thy đã xác nhận MSSV Nguyễn Đức Thành Phát là 2001230640; bản v2 sửa đúng hai chỗ trên bìa và bảng phân công, không đổi tên hoặc thông tin khác. SHA-256 v2 e44e1a3d2e81a1c8d4240c24fffc429b6439600cce42e8b3af62e31b128d5a58; evidence .agent/qa/diennang-mssv-20261006/verification.json: đảo sửa XML, nguồn khung giữ hash, mọi part khác giữ bytes, 21 trang đã xem; chỉ hai trang đầu thay đúng MSSV, trang 3–21 giống từng pixel.
- Checkpoint 06/10: ba thông số chưa được xác nhận. Bản dán 08/10 đề xuất rõ một hộ UCI, theo giờ, một giờ tiếp theo; trạng thái tiếp nhận hiện tại và phần cần xác nhận nằm ở đầu file, không dùng ví dụ London cũ để ghi đè.
- Chưa viết nội dung, khảo sát dataset, triển khai pipeline, huấn luyện mô hình hoặc tạo kết quả trong lượt dựng/sửa khung. Tiếp theo: Thy kiểm bản v2; chỉ bắt đầu Chương 3 khi được yêu cầu, chốt ba thông số trước thiết kế thực nghiệm.
- Nguồn quy tắc văn phong: ../.agent/rule.md. Kế hoạch và bản đồ tài liệu: .agent/PLAN.md, .agent/DOC_INDEX.md.

## Recovery checkpoint 06/10/2026

CURRENT TASK: sửa riêng MSSV Phát trong khung v2, trạng thái VERIFIED; chờ Thy duyệt khung.
SOURCE CHECKPOINT: Thy xác nhận 2001230640; ../BaoCao_PhanTich_DuDoan_DienNang_Khung.docx hash d2199f...acdd là nguồn sửa, giữ nguyên. Format/outline từ lượt dựng khung giữ nguyên.
ALLOWED SCOPE: bản v2 chỉ MSSV trên bìa và bảng phân công; công cụ/QA/context/PLAN/index liên quan. Không nghiên cứu hoặc xử lý dataset.
LOCKED: outline năm chương, styles/TOC/khung/logo/footer và toàn bộ nội dung khác không đổi; không chỉnh nguồn Flink, hai DOCX thành viên, slides/script hoặc dữ liệu.
APPLIED BUT UNVERIFIED: không còn sửa định dạng chưa kiểm.
VERIFIED: 2001230640 xuất hiện đúng hai vị trí; đảo sửa khôi phục XML nguồn; chỉ document.xml đổi; 21 trang, headings/TOC/sections giữ nguyên; xem đủ ảnh, trang 3–21 pixel-identical; nguồn khung không đổi hash.
PENDING: Thy duyệt khung; đối tượng dự đoán, độ phân giải và horizon chưa chốt; nội dung và thực nghiệm chưa làm.
LAST EVIDENCE: .agent/qa/diennang-mssv-20261006/manifest.json, verification.json, final-word.json, final-render/page-1.png đến page-21.png; bộ QA dựng khung ban đầu giữ để truy vết.
NEXT EXACT ACTION: dùng bản v2 hiện hành và nhận phản hồi về khung; không tự viết Chương 1–5 hay chạy dữ liệu.

## Dữ liệu và ranh giới nội dung — checkpoint London lịch sử

- Checkpoint lịch sử 01/10: Partitioned LCL Data/Small LCL Data từng được đếm 168 CSV, có LCLid, stdorToU, DateTime, KWH/hh (per half hour). Ngày 08/10 không thấy thư mục tại đường dẫn cũ; không coi ghi chú này là bằng chứng dữ liệu đang có trên máy.
- Nguồn dataset: https://data.london.gov.uk/dataset/smartmeter-energy-consumption-data-in-london-households-vqm0d
- Dữ liệu lịch sử; lượng điện năng kWh theo khoảng nửa giờ, không phải công suất kW. Phát lại mô phỏng luồng không đồng nghĩa hệ thống công tơ thời gian thực.
- Các khảo sát mẫu trước đây nằm ở ../.agent/qa/flink-lcl/verification.json; chưa khảo sát toàn bộ dữ liệu. Không mặc định Null bằng 0; không coi thứ tự CSV là thứ tự Event Time toàn cục.
- Chương 1 đặt bối cảnh; Chương 2 trình bày lý thuyết. Chương 3 mô tả dữ liệu và kết quả phân tích; Chương 4 trình bày thực nghiệm dự đoán; Chương 5 mô tả cách hệ thống triển khai và tích hợp. Không lặp nội dung giữa các chương.
- Nguồn chính thức làm căn cứ cho phương pháp/công nghệ; kiến trúc, biểu đồ, metric và kết quả chạy thử phải dựa vào sản phẩm và thực nghiệm của nhóm.
- Chia dữ liệu theo thời gian, tránh rò rỉ dữ liệu; chỉ học tham số tiền xử lý trên tập huấn luyện. Lựa chọn mô hình qua tập kiểm định, dùng tập kiểm thử cho đánh giá cuối.

## Khung báo cáo hiện hành

### MỞ ĐẦU

1. Lý do chọn đề tài
2. Mục tiêu nghiên cứu
3. Đối tượng và phạm vi nghiên cứu
4. Phương pháp thực hiện
5. Bố cục báo cáo

### CHƯƠNG 1. TỔNG QUAN VỀ BÀI TOÁN PHÂN TÍCH VÀ DỰ ĐOÁN TIÊU THỤ ĐIỆN NĂNG

1.1. Bối cảnh và nhu cầu phân tích dữ liệu tiêu thụ điện năng
1.2. Tổng quan về dữ liệu tiêu thụ điện năng
1.3. Dữ liệu công tơ thông minh
1.4. Đặc điểm của dữ liệu tiêu thụ điện năng theo thời gian
1.5. Những thách thức trong xử lý dữ liệu tiêu thụ điện năng
1.6. Bài toán phân tích dữ liệu tiêu thụ điện năng
1.7. Bài toán dự đoán nhu cầu sử dụng điện
1.8. Các hướng tiếp cận dự đoán tiêu thụ điện năng
1.9. Tổng quan một số nghiên cứu liên quan
1.10. Vai trò của Big Data trong phân tích dữ liệu điện năng
1.11. Định hướng tiếp cận của đề tài

### CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG

2.1. Tổng quan về dữ liệu chuỗi thời gian
2.2. Các thành phần và đặc điểm của chuỗi thời gian
2.3. Bài toán dự báo chuỗi thời gian và Forecasting Horizon
2.4. Tiền xử lý dữ liệu chuỗi thời gian
2.5. Kỹ thuật xây dựng đặc trưng cho bài toán dự đoán
2.6. Phương pháp phân chia dữ liệu chuỗi thời gian
2.7. Các phương pháp và mô hình dự đoán
2.8. Các chỉ số đánh giá mô hình
2.9. Tổng quan về Apache Flink
2.10. Mô hình xử lý dữ liệu trong Apache Flink
2.11. Event Time và Watermark
2.12. KeyBy và Window
2.13. State và Checkpoint
2.14. Các công nghệ và thư viện sử dụng

### CHƯƠNG 3. KHẢO SÁT, TIỀN XỬ LÝ VÀ PHÂN TÍCH DỮ LIỆU TIÊU THỤ ĐIỆN NĂNG

3.1. Giới thiệu bộ dữ liệu UCI Individual Household Electric Power Consumption
3.2. Cấu trúc và các thuộc tính của dữ liệu
3.3. Khảo sát dữ liệu ban đầu
3.4. Kiểm tra chất lượng dữ liệu
3.5. Xử lý dữ liệu thiếu và dữ liệu không hợp lệ
3.6. Chuẩn hóa dữ liệu thời gian
3.7. Tổng hợp dữ liệu tiêu thụ điện năng theo thời gian
3.8. Phân tích thống kê dữ liệu tiêu thụ điện năng
3.9. Phân tích mức tiêu thụ theo thời gian
3.10. Phân tích các nhóm đo phụ trong một hộ sử dụng điện
3.11. Trực quan hóa dữ liệu
3.12. Xây dựng tập dữ liệu sau tiền xử lý
3.13. Nhận xét kết quả phân tích

### CHƯƠNG 4. XÂY DỰNG VÀ ĐÁNH GIÁ MÔ HÌNH DỰ ĐOÁN NHU CẦU SỬ DỤNG ĐIỆN

4.1. Xác định bài toán dự đoán điện năng của hộ trong giờ tiếp theo
4.2. Xác định biến mục tiêu điện năng theo giờ (kWh)
4.3. Lựa chọn dữ liệu đầu vào
4.4. Xây dựng đặc trưng cho mô hình
4.5. Phân chia tập dữ liệu huấn luyện, kiểm định và kiểm thử
4.6. Xây dựng mô hình dự đoán cơ sở
4.7. Xây dựng các mô hình dự đoán
4.8. Huấn luyện mô hình
4.9. Đánh giá kết quả dự đoán
4.10. So sánh các mô hình
4.11. Phân tích sai số dự đoán
4.12. Trực quan hóa kết quả dự đoán
4.13. Lựa chọn mô hình phù hợp
4.14. Lưu và sử dụng mô hình dự đoán

### CHƯƠNG 5. XÂY DỰNG HỆ THỐNG XỬ LÝ DỮ LIỆU VÀ ỨNG DỤNG MINH HỌA

5.1. Yêu cầu của hệ thống
5.2. Kiến trúc tổng thể của hệ thống
5.3. Thiết kế luồng xử lý dữ liệu
5.4. Đọc và tiếp nhận dữ liệu bằng Apache Flink
5.5. Tiền xử lý dữ liệu trong Flink
5.6. Phân vùng dữ liệu theo khóa
5.7. Xử lý dữ liệu theo Event Time và Watermark
5.8. Xử lý dữ liệu theo cửa sổ thời gian một giờ
5.9. Tổng hợp và xuất dữ liệu sau xử lý
5.10. Tích hợp mô hình đã huấn luyện để thực hiện dự đoán
5.11. Thiết kế ứng dụng trực quan hóa
5.12. Chức năng phân tích dữ liệu tiêu thụ điện năng
5.13. Chức năng dự đoán nhu cầu sử dụng điện
5.14. Hiển thị kết quả dự đoán và các chỉ số đánh giá
5.15. Kết quả chạy thử hệ thống
5.16. Đánh giá hệ thống
5.17. Hạn chế và hướng phát triển

### KẾT LUẬN

1. Kết quả đạt được
2. Hạn chế của đề tài
3. Hướng phát triển

### TÀI LIỆU THAM KHẢO
