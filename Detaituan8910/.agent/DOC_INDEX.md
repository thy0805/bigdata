# Bản đồ tài liệu đồ án tuần 8–10

## Nguồn hiện hành — UI giải thích dữ liệu 10/10

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| .agent/qa/phase4-data-guide-20261010/checklist.md, review.md | Scope chỉ expander và điểm dừng | Hiện hành; G01–G04 VERIFIED, G05 chờ publication; user PENDING | Duyệt UI hoặc khôi phục task |
| .agent/qa/phase4-data-guide-20261010/technical-verification.json, browser-verification.json, screenshots/ | 75 kiểm kỹ thuật, 7 browser, 4 ảnh hai viewport | VERIFIED tại snapshot | Đối chiếu nội dung/bảo toàn/giao diện |
| .agent/scripts/verify_data_guide.py | Hồi quy75 và guard diff đúng expander | Công cụ đã chạy | Không sửa QA/verifier cũ hoặc refit |
| .agent/qa/phase4-data-guide-20261010/publication-receipt.json | HEAD/remote và read-back file phát hành | Receipt local sau push; không tracked | Kiểm trạng thái Git thực tế |

UI mới ưu tiên mô tả expander trong ảnh/hồ sơ QA4 cũ; dữ liệu, model, biểu đồ và metric giữ nguồn chuẩn cũ. I04 tiếp tục DEFERRED.

## Lịch sử — Phase4 ứng dụng trước thay UI

Lượt tiếp tục10/10: `qa/phase4-resume-20261010/{checklist.md,review.md,resume-verification.json,windows-verification.json}` là nguồn hiện trạng mới (21 kiểm); ưu tiên các tuyên bố runtime ngày09/10. QA4 cũ giữ snapshot126/126. `scripts/verify_phase4_resume.py` là công cụ kiểm tiếp tục, không thực hiện fit/fulljob/Testmetric.

`qa/phase4-app-20261009/resume-publication-1.json`: VERIFIED snapshot commit5b7f620,14/14 đọc GitHub; đọc khi đối chiếu hồ sơ lượt tiếp tục. `qa/phase4-app-20261009/remote-readback.json` là receipt local HEAD cuối, không tự suy ra nó đã tồn tại hoặc khớp nếu chưa mở.

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| .agent/decisions/20261009-phase4-app-scope.md | Scope mới I01/I02/I03/I05; I04 tạm hoãn | Hiện hành, ưu tiên approval4 cũ | Đầu phiên; không tự I04/Phase5 |
| .agent/qa/phase4-app-20261009/checklist.md, review.md | Checklist/handoff ứng dụng, giới hạn | Hiện hành; I01/I02/I03/I05 VERIFIED kỹ thuật, nghiệm thu user PENDING | Duyệt app/tiếp tục task |
| .agent/qa/phase4-app-20261009/publication.md, remote-readback-1.json | Git853974c rawread-back9/9 và vị trí sản phẩm | VERIFIED snapshot publication | GPT Web tìm evidence đúng folder |
| .agent/qa/phase4-app-20261009/remote-readback.json | Receipt HEAD Git sau checkpoint cuối | Local-only; hiện hành khi commit khớp HEAD | Kiểm publication mới; tránh vòng commit tự tham chiếu |
| .agent/qa/phase4-app-20261009/verification.json, preservation.json, package-verification.json | Gate tổng/bảo toàn/ZIP; chưa có file thì chưa VERIFIED I05 | Hiện hành sau gate | Kiểm handoff cuối |
| .agent/qa/phase4-app-20261009/technical-verification.json, integration-faults.json, browser-verification.json, screenshots/ | 67backend/17lineage-fault/11browser;8ảnh | VERIFIED riêng các phần đã kiểm | Đối chiếu KPI/inference/UI |
| .agent/qa/phase4-app-20261009/final.json, windows-runtime.json, flink-off.json, app-off.json | Recovery/ownership/cổng/LANloopback và dữ liệu đọc độc lậpcluster | VERIFIED scope dịch vụ | Vận hành/lỗi môi trường |
| .agent/qa/phase4-app-20261009/flink-recovered.json | Attempt JavaIPv6/forwarding chưa đạt | Lịch sử FAIL; final.json ưu tiên | Truy vết, không đếm vàoPASS |
| operations/services.py, operations/README.md | Start/status/stop/guard mới; foreground | VERIFIED runtime/docs qua gate126 | Thao tác từ PowerShell; không dùng cluster.py ghi QA1 |
| .agent/qa/phase4-app-20261009/REPORT_EVIDENCE_MAP.md | Bản đồ nguồn Ch3–5/đồng bộCh2 và kiến trúc thật | Hiện hành, chưa viết báo cáo | Sau phê duyệt Word/PPT riêng |
| .agent/qa/phase4-app-20261009/preflight.json, fixtures/, runtime/ | Snapshot đầy đủ/local fault copies/runtime | Nội bộ, không phát hành | Điều tra/bảo toàn; public dùng preflight-public.json |

Các mục dưới là lịch sử trước scope ứng dụng mới. Không thay evidence các phase đã nghiệm thu.

## Nguồn ưu tiên mới — Phase4 được duyệt / GitHub

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| .agent/decisions/20261009-phase4-approval.md | Nghiệm thu3 và scope I01–I05 | Hiện hành, LOCKED quyết định | Trước tích hợp; ưu tiên pending3 cũ |
| .agent/PLAN.md | Checklist I01–I05 | Hiện hành TODO | Tiếp tục4, không suy ra done từ3 |
| ../README.md | Điểm vào GitHub cho GPT Web | Hiện hành đang verify | Tìm code/evidence/giới hạn |
| ../HANDOFF_FOR_GPT_WEB.md | Bàn giao có đường dẫn cụ thể | Hiện hành | GPT Web đọc theo thứ tự; QA3 giữ snapshot |
| ../.agent/decisions/20261009-github-publication.md | Phạm vi repo public do Thy xác nhận | Hiện hành | Trước commit/push |
| ../.agent/qa/github-publication-20261009/checklist.md | Gate phát hành/select/scan/blob/remote | Hiện hành | Publish và recovery |

QA3 và review3 giữ nguyên snapshot trước nghiệm thu. Trạng thái pending3 trong hồ sơ cũ không phủ định approval4 hiện hành.

## Nguồn ưu tiên hiện hành — Phase3

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| .agent/decisions/20261009-phase3-approval.md | Nghiệm thu2B2, duyệt dashboard3tab và phạm vi | LOCKED quyết định | Trước app/dependency/QA; ưu tiên pending3 cũ |
| .agent/qa/phase3-20261009/checklist.md, preflight.json | U00–U05 và sourcegate/guard976 file | U00–U05 VERIFIED | Recovery/kiểm/handoff |
| dashboard/README.md, app.py, data_service.py, charts.py, serve.py, style.css, .streamlit/config.toml | UI3tab, artifact/KPI/inference và launcher | VERIFIED qua67/67+browser10/10 | Chạy/kiểm UI; không standalone portable |
| .agent/qa/phase3-20261009/review.md, verification.json, technical-verification-v3.json, browser-verification.json, documents-verification.json, screenshots/ | Handoff9mục;67+10+19=96/96 | VERIFIED kỹ thuật/hồ sơ; nghiệm thu Thy PENDING | Duyệt3, ưu tiên ảnh cuối trong browser-verification |
| .agent/qa/phase3-20261009/install-report.json, install-lock.txt, pip-install-report.json | Dependency32package; pin ML cũ giữ | VERIFIED | Không pip upgrade tùy ý |
| .agent/scripts/verify_phase3.py | Decimal/KPI/cache/no-fit/inference/AppTest/guard | VERIFIED67/67 bảnv3 | QA app, không eval/train lại |
| .agent/qa/phase3-20261009/Phase3_Dashboard_Handoff_20261009_FINAL.zip, final-package-verification.json | Gói duyệt app/model/evidence/8ảnh cuối và checkpoint sau gate | Handoff hiện hành sau read-back; gói không portable | Gửi GPT Web duyệt3; không dùng ZIP trước FINAL |
| .agent/qa/phase3-20261009/attempts/handoff-a1/, technical-verification.json, technical-verification-v2.json | Lịch sử QA trước hoàn thiện UI/doc gate | Lịch sử, không evidence cuối | Chỉ truy lỗi; không sửa phase cũ |

Artifact/QA/model các phase cũ bất biến; dashboard mới không thay Flink hoặc train. Bàn giao sau Phase3, không Phase4/Word/replay.

## Nguồn ưu tiên hiện hành — Phase2B2

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| .agent/decisions/20261009-phase2b2-approval.md | Thy nghiệm thu2B1, chọn candidate không refit và duyệt2B2 | LOCKED quyết định | Trước Test; ưu tiên mọi pending2B2 cũ |
| .agent/qa/phase2b2-20261009/checklist.md | T00–T05 và evidence gate | VERIFIED | Đầu phiên/compact/QA/handoff |
| .agent/qa/phase2b2-20261009/review.md, verification.json, test-verification.json, metric-oracle.json, documents-verification.json | Bàn giao10 mục, QA51/51, oracle độc lập và docQA62/62/17MD | VERIFIED kỹ thuật/hồ sơ; chờ nghiệm thu | Thy/GPT Web nghiệm thu2B2 |
| .agent/qa/phase2b2-20261009/selection-lock.json, pretest-verification.json, evaluation-started.json, evaluation-completed.json | Khóa trước Test và journal một lượt | LOCKED selection/VERIFIED17/17 trước Test | Không chạy lại evaluation |
| models/final/hgb-uci-hourly-v1.0-train-only/ | Model/manifest cuối; đóng gói estimator candidate không refit | LOCKED artifact sau QA | Inference khi Phase3 được duyệt |
| models/runs/20261009-phase2b2-a/ | Prediction4590/metrics/runtime/manifest và companionQA | VERIFIED51/51 | Test metric và dashboard sau duyệt |
| forecasting/evaluate_final.py, FINAL_EVALUATION.md; .agent/scripts/verify_phase2b2.py, verify_phase2b2_documents.py | Đánh giá một lần, hướng dẫn và oracle/packaging/docQA | VERIFIED | Kiểm bằng chứng; không chạy lại mặc định |

Phase0–2B1 artifact/code/QA giữ nguyên. Test đã đánh giá, final đã LOCKED sau QA; chưa Phase3/Word/dashboard. Các block bên dưới là registry và lịch sử trước duyệt2B2; source hiện hành ưu tiên block này.

## Nguồn ưu tiên hiện hành — Phase2B1

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| .agent/decisions/20261009-phase2b1-approval.md | Nghiệm thu2A, scope2B1/cấu hình HGB/D09 | LOCKED phạm vi | Trước thay đổi mô hình; ưu tiên trạng thái chờ duyệt2A cũ |
| .agent/qa/phase2b1-20261009/checklist.md, review.md, verification.json, fit-witness.json, preflight-notes.md | Task/handoff8 mục, QA và giới hạn nguồn tạm | VERIFIED37/37; chờ nghiệm thu | Recovery/duyệt2B2 |
| forecasting/train_hgb.py, predictor.py, TRAINING.md | HGB Train-only và D09 dùng chung, hướng dẫn | VERIFIED qua hai run/QA | Kiểm hoặc chạy run mới khi được giao, không Test |
| models/runs/20261009-phase2b1-a2/, 20261009-phase2b1-b/ | Model ứng viên và Validation | VERIFIED; bốn artifact giống byte | Không phải model cuối LOCKED; a2 chính, b lặp |
| .agent/scripts/verify_phase2b1.py, .agent/qa/phase2b1-20261009/preservation-before.json | Fit witness, Decimal metrics, repeat và guard933 file | VERIFIED37/37 | Kiểm2B1;68 runtime temp đã đổi trước task |
| .agent/scripts/verify_phase2b1_documents.py | Read-back/link/metric/state/provenance và bảo toàn cuối | Công cụ QA tài liệu | Kiểm B05; không chạy lại fit |

Phase1/2A đã LOCKED theo Thy nghiệm thu qua hồ sơ. Các block/bảng cũ bên dưới là lịch sử trạng thái. Không sửa artifact hoặc QA cũ.2B2 chưa được duyệt.

## Ưu tiên hiện hành: Phase1 LOCKED; Phase2A M01–M04 VERIFIED kỹ thuật

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| .agent/decisions/20261009-phase2a-approval.md | Phê duyệt và scope M01–M04 | Hiện hành / LOCKED scope | Trước mọi thay đổi ML; ưu tiên các trạng thái chờ Phase1 cũ |
| .agent/qa/phase2a-20261009/checklist.md, review.md, documents-verification.json | Checklist/handoff và giới hạn nghiệm thu Phase2A | Hiện hành / M01–M04/G06 VERIFIED,38/38docQA/16MD | Duyệt2A/2B/D09; không tự train |
| forecasting/requirements.txt, prepare_baselines.py, README.md | Dependency pin, tạo feature/split/baseline Validation và hướng dẫn | Hiện hành / VERIFIED qua hai run | Không có fit học máy/Testmetrics |
| data/ml/runs/20261009-phase2a-a/, 20261009-phase2a-b/ | Train/Validation/Test chuẩn bị, eligibility/schema/metadata/predictions Validation | Hiện hành / VERIFIED29/29 và30/30,9 artifact giống byte | Run a chính, b tái lập; không ghi đè; Test seal theo quy trình |
| .agent/scripts/verify_phase2a.py; .agent/qa/phase2a-20261009/preservation-before.json, install-report.json | Oracle giờ/Decimal, gap/leakage/rerun/source guards; wheel/hash | Công cụ/evidence đã chạy |965 file giữ hash; raw chỉ hash, không tổng hợp cho ML |
| .agent/scripts/verify_phase2a_documents.py | Read-back UTF8/link/range/count/metric/scope và exact trạng thái | Công cụ / VERIFIED38/38 | G06; không so trạng thái bằng substring |

Các trạng thái Phase1 chờ duyệt phía dưới được thay bằng phê duyệt trên; hồ sơ QA Phase1 giữ nguyên, Phase2B chưa được duyệt. Các bảng phía dưới là registry nguồn/historical snapshot; trạng thái hiện hành ưu tiên block này và OPEN_DECISIONS mới.

Hiện hành09/10: F05/F06 VERIFIED kỹ thuật, chờ Thy/GPT Web nghiệm thu Phase1. Nguồn canonical `.agent/qa/phase1-full-20261009/{checklist.md,review.md,handoff-verification.json}` và `.agent/decisions/20261009-flink-full-approval.md`. Launcher `pipeline/run_full.py`; oracle/regression/handoff `.agent/scripts/{verify_full_pipeline.py,verify_full_date_parser.py,collect_full_handoff.py}`. Dữ liệu sản phẩm `data/processed/runs/20261009T102201900234-full/`, rerun `20261009T102643175598-rerun/`, mỗirun verification25/25;hashgrid8b03f1e3...a8b5b2bc. Hai run đầu rejected không dùng. F04 SQL/smoke nguyênhash, parserfull sửa2biểu thức ngày không đổi phương pháp. Năm MD thiết kế được đồng bộ trạng thái, phần Phase0/lầnsmoke bên dưới là lịch sử. Word/model/dashboard/Phase2 chưa duyệt.

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| .agent/qa/phase1-smoke-20261009/checklist.md, review.md, handoff-verification.json | Scope F01–F04 và bằng chứng mẫu | Lịch sử đã LOCKED bởi Thy /82+37checks | Truy vết mẫu; không thay QA full |
| .agent/decisions/20261009-flink-phase1-approval.md | D01–D05 và giới hạn F04 ban đầu | D01–D05 LOCKED / scopeF04 lịch sử | Scopefull ưu tiên decision20261009-flink-full-approval.md |
| pipeline/README.md, pipeline/cluster.py, pipeline/flink-conf/ | Hướng dẫn/launcher foreground và config WSL/local WebUI | Hiện hành / VERIFIED trong F02 | Chạy/dừng đúng cluster; không service production |
| pipeline/hourly.sql, pipeline/run_smoke.py | FlinkSQL BATCH/parser và run guard QA-only | Hiện hành / VERIFIED trên mẫu F04 | Không full input; SQL hash trong review/README |
| data/raw/household_power_consumption.txt | Bản TXT nguyên bytes từ ZIP | Hiện hành / hash khớp | Chỉ đọc; full đã kiểm, không sửa nguồn |
| .agent/scripts/verify_phase1_smoke.py, .agent/qa/phase1-smoke-20261009/smoke-verification.json, runs/ | Đối chiếu Decimal, job/log/fixture | Công cụ /82/82VERIFIED, QA-only | Không dùng fixture làm kết quả đồ án |

Ưu tiên yêu cầu mới nhất của Thy: nhóm3/UCI/một hộ/kWh giờ/giờ kế tiếp vàD01–D05 LOCKED; F01–F04 được chấp nhận, F05/F06 VERIFIED kỹ thuật, chờ nghiệm thu Phase1. QAfull ưu tiên snapshotPhase0/mẫu. Model/UI/Word/Phase2 chưa duyệt. Không Docker/restart. PDF áp dụng trừ nhóm2/danh sách gợi ý; Mauwword chuẩn hình thức, Wordv3 giữ nguyên. Snapshot lỗiWSL/timer cũ là lịch sử.

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| docs/phase0-20261008/DATA_AUDIT.md | Full audit UCI, hash, đơn vị và giới hạn kiểm độc lập | Hiện hành / VERIFIED khảo sát | Trước pipeline/EDA; phân biệt observed và giờ đầy đủ |
| docs/phase0-20261008/TECHNICAL_ARCHITECTURE.md | Runtime và kiến trúc dữ liệu | Hiện hành / F01–F06VERIFIED kỹ thuật; ML/UI PROPOSED | QAfull ưu tiên snapshot trước cài |
| docs/phase0-20261008/APP_UI_SPEC.md | Minimal ba tab, KPI/history/model states | Hiện hành / PROPOSED triển khai | Giai đoạn3 sau duyệt, không phải app đã có |
| docs/phase0-20261008/IMPLEMENTATION_PLAN.md | Kế hoạch canonical và cổng kiểm từng giai đoạn | Hiện hành / F01–F06VERIFIED kỹ thuật | Chờ Thy/GPT Web nghiệm thu Phase1 trước Phase2 |
| docs/phase0-20261008/OPEN_DECISIONS.md | D01–D05LOCKED; D06–D10pha sau chưa duyệt | Hiện hành | Không áp dụng quyết định model/UI sớm |
| .agent/qa/phase0-resume-20261009/ | Checklist R00–R05, môi trường,13 kiểm dữ liệu/hash, verifier tài liệu và review | Hiện hành / VERIFIED trong phạm vi khảo sát | Recovery và bằng chứng; không job/model/renderer Word |
| .agent/scripts/probe_linux_phase0_resume.py, verify_phase0_resume.py, verify_phase0_documents.py | Probe chỉ đọc, HTTP tạm tự kết thúc, kiểm metadata/mẫu/hash/tài liệu | Công cụ / đã chạy QA | Không cài hoặc tạo pipeline; chỉ ghi QA hỗ trợ |
| .agent/qa/power-timer-20261009/checklist.md, status.json, display-before.txt, sleep-before.txt | Scope, kiểm timer và backup power setting | Lịch sử; timer kết thúc theo probe10:32 | Truy vết; không chạy lại timer hoặc dùng AC120 cũ thay setting mới |
| .agent/scripts/shutdown_30min_20261009.ps1, Huy_hen_tat_may_20261009.cmd | Helper độc lập quota và launcher hủy | Công cụ theo yêu cầu Thy; launcher hủy chưa chạy thử | Chỉ hủy trước deadline khi cần; không force/reboot |
| .agent/qa/phase0-20261008/antigravity-api-legacy-v2-20261009.json, antigravity-api-ide-extra-20261009.json | Đọc 287 chat/50.831 step, count khớp và 0 lỗi | Hiện hành / VERIFIED độ phủ văn bản, chưa tìm chuỗi sửa | Tra lịch sử sandbox/WSL; không chạy lệnh cũ; ảnh chưa OCR |
| .agent/scripts/search_antigravity_wsl_history.ps1 | Bộ đọc RPC gốc Hub/IDE, phân trang và lọc liên quan | Công cụ chỉ đọc | Không in token hoặc nội dung chat ngoài phạm vi |
| .agent/qa/phase0-20261008/antigravity-wsl-history-20261009.md | Bối cảnh sandbox/WSL 14/5, giới hạn tra lịch sử và DISM 00:58 | Hiện hành / VERIFIED phần đã đọc; chưa tìm chuỗi sửa | Tiếp tục khi Antigravity mở; không chạy lại lệnh lịch sử hoặc kết luận WSL2 đã chạy |
| .agent/qa/phase0-20261008/dism-progress-20261009-0028.md | Snapshot DISM/CBS cũ; selection console và lỗi profile Conda riêng | Lịch sử snapshot / VERIFIED tại 00:28 | Truy vết; ảnh mới đã hết Select và vẫn đứng, không dùng snapshot làm bằng chứng nguyên nhân hiện tại |
| .agent/qa/phase0-20261008/checklist.md | Scope/checklist trước khôi phục WSL | Lịch sử / ưu tiên R00–R05 mới | Truy vết, không dùng Pxx làm task hiện tại |
| .agent/qa/phase0-20261008/dataset-audit.json | Full scan UCI: missing/timestamp/hour/residual/hash | Hiện hành / tái sử dụng full audit, mẫu/hash đã đối chiếu trong QA mới | Trước pipeline; kiểm độc lập mới chỉ10.000 dòng/hai giờ, không metric |
| .agent/qa/phase0-20261008/environment-wsl-20261009.json, WSL_DIAGNOSIS.md | Chẩn đoán lỗi WSL trước khôi phục | Lịch sử / snapshot đã kiểm thời điểm cũ | Truy vết; runtime hiện đã chạy theo QA mới, không repair từ ghi chú cũ |
| .agent/scripts/audit_phase0_uci.py, audit_wsl_readonly.ps1 | Công cụ audit read-only; chỉ tạo QA mới | Công cụ | Không coi là pipeline; không gọi Install/khởi động lại |
| BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx | Bản tiếp tục 37 trang: caption/MAE, bìa theo mẫu và bỏ 29 marker trong bài | Hiện hành / VERIFIED QA, chưa LOCKED hoặc đủ nộp | Mọi lượt sửa sau; giữ số nguồn/hyperlink/footer và nguồn gốc |
| BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v2_20261008.docx | Bước sửa caption/MAE trước scope bìa và marker | Lịch sử / nguồn giữ hash | Truy vết minimal diff; không ưu tiên hơn v3 hoặc ghi đè file đang mở |
| BaoCao_PhanTich_DuDoan_DienNang_UCI_20261008.docx | Bản ghép ban đầu 37 trang: Ch1 và khung Ch2–5 | Lịch sử / nguồn giữ hash | Đối chiếu; v3 là nguồn tiếp tục |
| .agent/qa/word-uci-cover-citations-20261008/ | Scope/checklist, review, 31 kiểm, Word field probes và 37 PNG cuối | Hiện hành / QA nội bộ | Recovery và kiểm v3; không gửi QA kèm DOCX |
| .agent/qa/word-uci-caption-math-20261008/ | Bước caption/MAE: 29 kiểm cấu trúc, probe và render v2 | Lịch sử / QA nguồn | V2 mới xem riêng trang 1–20; final visual gate là đủ 37 trang v3 |
| .agent/scripts/fix_uci_cover_citations.py, inspect_uci_cover_citations.py, verify_uci_cover_citations.py, finalize_uci_caption_math.ps1, probe_uci_captions.ps1 | Minimal patch và QA v3/caption; native Word chỉ tác động bản mới hoặc probe không lưu | Công cụ | Builder không chạy lại đè output; verifier đọc artifact và ghi QA |
| C:/Users/thy/Downloads/individual+household+electric+power+consumption.zip | Dataset UCI gốc do Thy chỉ rõ; TXT 9 cột/2.075.259 bản ghi | Hiện hành / chỉ đọc, full scan Phase0; hash 9f84b4…a3ff | Audit/thiết kế Phase0; chưa tạo dataset triển khai hoặc huấn luyện |
| .agent/qa/word-uci-20261008/checklist.md, artifact.md, review.md, final-verification.json, final-field-tests.json, final-word.json, final-render/, dataset-inspection.json, reference-links.json | QA ghép ban đầu, đọc ZIP và đối chiếu PDF/phần thiếu | Lịch sử ghép / dataset-inspection vẫn là evidence khảo sát ban đầu | Truy vết; QA v3 ưu tiên khi kiểm Word mới |
| .agent/scripts/build_uci_report.py, refine_uci_report.py, finish_uci_word.ps1, verify_uci_report.py, inspect_uci_zip.py, check_uci_reference_links.py | Công cụ ghép DOCX, refine, native field/QA và đọc ZIP | Công cụ | Chỉ chạy đúng scope; builder không ghi đè output; Word normalize field có thể thành fldSimple |
| Ke hoach Do an mon hoc Nhap mon Big data.pdf | Yêu cầu, hồ sơ nộp, cấu trúc báo cáo và rubric | Hiện hành / nguồn giảng viên, đã đọc 08/10 | Cho phép Flink; nhóm 2/danh sách gợi ý không áp dụng theo Thy; review.md ghi chưa hoàn thành thực nghiệm |
| KhoiTuan Tong Quan Bai Toan Chuong 1.docx | Chương 1 gốc 15 trang/4 bảng/1 hình; giữ hash | Nguồn thành viên chỉ đọc / đã ghép và sửa trọng điểm ở bản mới | Truy vết nội dung; bản gốc thiếu 1.3 và Heading, không sửa nguồn |
| ../Mauwword/Mau bao cao_Do an_Khoa luan_2025.docx | Mẫu bìa, TOC, danh mục và quy định format trang 17–18 | Hiện hành / nguồn format do Thy chỉ định 08/10 | Trước chỉnh Word; mẫu không có TOC field thật, phải tạo field mới |
| .agent/qa/intake-20261008/review.md, checklist.md, sources.json, *-text.txt, *-word.json, *-render/ | Rà nguồn và hiện trạng trước chỉnh Word | Lịch sử / QA nội bộ | Truy vết trước ghép; QA word-uci hiện hành ưu tiên |
| C:/Users/thy/.codex/attachments/bd161909-e22c-4a51-8864-7217c2190c7d/Văn bản đã dán.txt | Đề xuất các pha UCI/chỉnh Word/triển khai | Tham khảo / phần Word được Thy giao, ứng dụng chưa giao | Không mở rộng scope từ prompt dán; output trong Detaituan8910 |
| context.md | Trạng thái, phạm vi, phân công và toàn bộ khung năm chương | Hiện hành | Đầu phiên, viết nội dung hoặc xuất đề cương |
| .agent/PLAN.md | Kế hoạch và tiêu chí nghiệm thu | Hiện hành | Tiếp tục công việc |
| ../.agent/rule.md | Quy tắc văn phong được kế thừa từ workspace Big Data | Hiện hành | Trước khi viết báo cáo |
| .agent/mistake.md | Cảnh báo dữ liệu và phạm vi | Hiện hành | Xử lý dữ liệu hoặc mô tả triển khai |
| ../BaoCao_PhanTich_DuDoan_DienNang_Khung_v2.docx | Khung 21 trang/MSSV Phát đã xác nhận; nguồn dựng Word UCI | Lịch sử / nguồn giữ nguyên hash | Phục hồi/đối chiếu; bản UCI mới là nguồn sửa tiếp |
| ../BaoCao_PhanTich_DuDoan_DienNang_Khung.docx | Khung báo cáo 21 trang trước xác nhận MSSV; nguồn sửa v2, giữ nguyên | Lịch sử / nguồn chỉ đọc | Đối chiếu hoặc phục hồi; không ưu tiên hơn v2 |
| ../ApacheFlink.docx | Mẫu ở lượt dựng khung cũ, không dùng lý thuyết cho đồ án mới | Lịch sử / tham khảo chỉ đọc | Không ưu tiên hơn Mauwword về format; không sửa ở đồ án UCI |
| .agent/qa/diennang-mssv-20261006/, .agent/scripts/fix_skeleton_mssv.py, verify_skeleton_mssv.py | Scope, phép đảo sửa XML, kiểm nguồn khung/part/Word và 21 ảnh v2 | Hiện hành / QA và công cụ | Evidence sửa đúng hai MSSV; không chạy builder lại khi chỉ cần mở v2 |
| KhoiTuan_Chuong1_TongQuanBaiToan.docx | Đề cương sạch Chương 1, 11 mục; khác bản Chương 1 có nội dung mới | Tham khảo / đề cương cũ | Đối chiếu mục 1.3 và cấu trúc; không coi đây là bài thành viên đã viết |
| HAULYVUNHAN_Chuong2_CoSoLyThuyet.docx | Đề cương sạch Chương 2, 14 mục; đổi tên từ Chuong2_CoSoLyThuyet.docx, bytes không đổi | Hiện hành | Gửi thành viên viết Chương 2 |
| .agent/qa/diennang-khung-20261006/checklist.md, artifact.md, outline.json | Scope contract, format distillation và outline mới nhất | Hiện hành / QA | Trước sửa khung; không dùng tên mục lịch sử ghi đè |
| .agent/qa/diennang-khung-20261006/verification.json, final-word.json, final-field-tests.json, final-render/ | Kiểm đủ outline/TOC, nguồn, numbering, fields và 21 trang thực tế | Hiện hành / QA | Bằng chứng bàn giao; không gửi kèm Word |
| .agent/scripts/build_word_skeleton.py, finalize_word_skeleton.py, render_skeleton_word.ps1, render_skeleton_pdf.py, verify_skeleton_word.ps1, verify_word_skeleton.py | Dựng bản copy, sửa package, kết xuất Word/PDFium và kiểm 3 lớp | Công cụ | Chỉ dùng khi được yêu cầu; output đã tồn tại không ghi đè tùy ý |
| Partitioned LCL Data/Small LCL Data | Đường dẫn dữ liệu London ở checkpoint 01/10 | Lịch sử / không tồn tại ở đường dẫn đã kiểm 08/10 | Chỉ truy vết; xác minh đường dẫn mới trước khảo sát, không suy ra file đang có |
| ../.agent/qa/flink-lcl/verification.json | Khảo sát ba CSV từ bài trước | Tham khảo | Hiểu dữ liệu; không xem là khảo sát toàn bộ |
| .agent/scripts/build_chapter_outlines.py | Xuất hai DOCX trực tiếp từ khung trong context.md | Công cụ | Dựng lại khi được yêu cầu; chỉ ghi đè bản do script tạo nếu SHA-256 vẫn khớp lần kiểm trước |
| .agent/scripts/verify_outline_render.py | Kết xuất PDF Word sang PNG và kiểm nguyên văn/metadata/hash | Công cụ | QA sau sửa DOCX |
| .agent/qa/chapter-outlines/ | PDF/PNG và kết quả kiểm tra riêng | QA nội bộ | Kiểm tra trước bàn giao; không gửi kèm DOCX |
