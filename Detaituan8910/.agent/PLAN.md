# Kế hoạch đồ án tuần 8–10

## Hiện hành — W01.1

Canonical `qa/word-w011-20261010/checklist.md`;scope `decisions/20261010-word-w011-scope.md`. S01–S04 VERIFIED trong phạm vi Word:37/37,9/9 field,67 trang xem riêng,37 guard nguồn;18 điểm sửa. Snapshot ngoài Word INCOMPLETE1568/1571,3 link runtime không đọc được,0 changed/missing. S05 IN_PROGRESS phát hành Git. Acceptance PENDING;W02 chưa duyệt. Không sửa thêm DOCX;đẩy hồ sơ/kiểm remote rồi dừng. Các mục dưới là lịch sử.

## Lịch sử — W01 VERIFIED, chờ nghiệm thu

Canonical `qa/word-w01-20261010/checklist.md`, scope `decisions/20261010-word-w01-approval.md`. W01-01–06 VERIFIED: 67 trang đã xem riêng, 69/69 cấu trúc/ngữ nghĩa, 9/9 field probe, font khớp mẫu Mauwword; preservation1571/1571; publication486e8b3 remote50/50 khớp. Receipt local kiểm HEAD sau chốt trạng thái. W00 LOCKED, nguồn không đổi. Bản W01 có11 bảng bổ sung/7 khung đen/21 hyperlink cuối. Dừng để Thy gửi DOCX và link review cho GPT Web duyệt; W01 acceptance PENDING, W02 chưa mở, I04 DEFERRED. Không tự Word vòng mới/PPT/app/demo.

## Lịch sử — W00 khảo sát và đề xuất Word

Canonical: `qa/word-w00-20261010/checklist.md`, scope `decisions/20261010-word-w00-scope.md`. W00-01–05 VERIFIED cho hồ sơ đề xuất: 35/35 kiểm, nguồn DOCX nguyên hash, 21 chữ ký và 1.571/1.571 file bảo toàn. Preview/read-back đã kiểm; chưa sửa DOCX hoặc app.

Thy/GPT Web chấp thuận ứng dụng/UI theo yêu cầu W00 mới. W01 TODO, cần phê duyệt phạm vi và văn bản mẫu; W02 TODO, chưa tạo hình/placeholder. I04 DEFERRED; Phase4 INCOMPLETE. Dừng tại W00, không tự ghép Hậu hoặc viết các chương. Các checkpoint bên dưới là lịch sử.

## Lịch sử — UI giải thích dữ liệu 10/10

Checklist canonical: `qa/phase4-data-guide-20261010/checklist.md`. G01–G05 VERIFIED; publication-initial.json54/54/commitc9db6b8,22file đọc từ GitHub; receipt local cuối kiểm HEAD sau chốt điều phối. QA75/75, browser7/7,4ảnh;1570file bảo toàn và app.py đổi đúng expander. Chờ Thy/GPT Web nghiệm thu; I04 DEFERRED, Phase4 INCOMPLETE. Không Word/PPT/demo hoặc phase mới.

Nguồn bàn giao: `qa/phase4-data-guide-20261010/review.md`; publication receipt local sau push. Kế hoạch chỉ thay phần giới thiệu, không thay forecast/backend/model/pipeline.

## Lịch sử — Phase4 ứng dụng, I04 DEFERRED

Lượt tiếp tục10/10: checklist `qa/phase4-resume-20261010/checklist.md`. R01/R02 VERIFIED (17Linux/backend/hash +4Windows); R03 VERIFIED publication5b7f620/read-back14/14/index295file0finding. Không sửa app;1571file giữ hash. Gate126/126 bên dưới là snapshot09/10. Dừng chờ Thy/GPT Web; I04 DEFERRED. Receipt local cuối kiểm HEAD sau checkpoint điều phối.

Canonical: `qa/phase4-app-20261009/checklist.md` và `decisions/20261009-phase4-app-scope.md`, ưu tiên approval4 cũ về điểm tạm hoãn I04.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| I01 | Lineage/integration artifact | Manifests + sourcegate | VERIFIED | integration-faults17/17; technical67/67 | Không fullrerun; RESTjob cũ expired |
| I02 | Dịch vụ/ownership/recovery/faults | operations/services.py + runtime | VERIFIED trong scope |20Linux+4Windows; final.json thắng failed attempt | Coldboot NOT_TESTED/autostart chưa triển khai |
| I03 | UI/KPI/filters/inference | Code và dữ liệu khóa | VERIFIED |67backend+11browser;8ảnh đã xem | App code không thay |
| I04 | DEMO_RUNBOOK | Thy tạm hoãn | DEFERRED | Decision app scope | Không kịch bản/video/bài nói |
| I05 | QA/handoff/preservation/package/Git | Evidence4 + gate publication | VERIFIED |126/126,preservation1571/1571,ZIP47entries/46hashes;853974c remote9/9 | Chờ Thy/GPT Web, không tự Phase5 |

Toàn Phase4 INCOMPLETE; nghiệm thu ứng dụng Thy/GPT Web còn chờ. Gate126/126, ZIP và publication853974c đã kiểm. Checkpoint Git sau đó chỉ bổ sung receipt/điều phối; receipt cuối kiểm HEAD. Bước tiếp theo do Thy/GPT Web quyết định, không tự I04/Phase5.

## Lịch sử — Phase3 ACCEPTED; Phase4 được duyệt

Canonical scope: `decisions/20261009-phase4-approval.md`. Chưa có kết quả I01–I05. GitHub checkpoint hiện hành theo `../../.agent/qa/github-publication-20261009/checklist.md`.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| I01 | E2E/lineage | approval4 + manifests | TODO | Chưa có QA4 | Artifact chuẩn bất biến |
| I02 | Start/status/stop/recovery | approval4 + runtime thực tế | TODO | Probe có WSL/app/Flink, chưa recovery | Không kill dịch vụ khác/restart/mở LAN |
| I03 | UI/inference/filters | code/ảnh Phase3 accepted | TODO | QA3 là nguồn, không phải QA4 | Không train/tuning |
| I04 | DEMO_RUNBOOK.md | thực thi + approval4 | TODO | Chưa tạo | BATCH/historical phải rõ |
| I05 | Bằng chứng/bàn giao | test/log/hash/ảnh mới | TODO | Chưa có review4 | Dừng chờ nghiệm thu4 |

Phase3 LOCKED theo nghiệm thu mới; các dòng chờ nghiệm thu3 bên dưới là lịch sử. Không tự Phase5.

## Hiện hành — Phase3 VERIFIED, chờ nghiệm thu

Canonical `qa/phase3-20261009/checklist.md` U00–U05 VERIFIED; scope `decisions/20261009-phase3-approval.md`. Install32package/pin cũ giữ; backend/UI67/67, browser10/10,8ảnh cuối; doc/runtime19/19, tổng96/96;976/976 guard. App8501 Windows/127 Linux, foregroundsession35813. U05 đạt handoff gate/ZIP read-back. Thy đã nghiệm thu2B2 nhưng chưa nghiệm thu3. Bàn giao gói FINAL và dừng, không train/Test rerun/Word/replay/Phase4. Các pending3 cũ dưới đây là lịch sử.

## Hiện hành — Phase2B2 T00–T05 VERIFIED; chờ nghiệm thu

Canonical task: `qa/phase2b2-20261009/checklist.md`; scope `decisions/20261009-phase2b2-approval.md`. Thy nghiệm thu2B1/chọn HGB candidate, không refit Train+Validation. T00–T04 VERIFIED: pretest17/17, Test4590 một lượt, QA51/51 và final manifest LOCKED; HGB MAE0.3220542588291146/RMSE0.4634874854716987 kWh,0âm;951/951 guard nguyên hash. T05 VERIFIED qua documents-precheck.json62/62/17MD và snapshot documents-verification.json. Bàn giao `qa/phase2b2-20261009/review.md`, model `models/final/hgb-uci-hourly-v1.0-train-only/`. Chờ Thy/GPT Web nghiệm thu2B2 và duyệt Phase3; không đổi nguồn/QA cũ hoặc tự chuyển Phase3. Các mục chờ duyệt2B2 bên dưới là lịch sử.

## Hiện hành 09/10 — 2B1 VERIFIED kỹ thuật

Thy đã nghiệm thu2A và duyệt D09 cùng duy nhất cấu hình HGB trong `decisions/20261009-phase2b1-approval.md`. Canonical checklist: `qa/phase2b1-20261009/checklist.md`, handoff `review.md` cùng thư mục. B00–B04 VERIFIED37/37, HGB Validation MAE0.3694427311570533/RMSE0.5306058050415966 kWh; run a2/b bốn artifact giống byte. B05 VERIFIED47/47 docQA/18MD. Không mở Test, không khóa model cuối, không UI hoặc Word. Các trạng thái chờ duyệt2A/2B bên dưới là lịch sử;2B2 vẫn TODO/chưa duyệt.

## Hiện hành 09/10 — Phase1 LOCKED, M01–M04 VERIFIED; chờ duyệt2B

Thy/GPT Web đã nghiệm thu F01–F06 qua hồ sơ và duyệt chỉ M01–M04. Canonical checklist `qa/phase2a-20261009/checklist.md`, scope `decisions/20261009-phase2a-approval.md`, handoff `qa/phase2a-20261009/review.md`. M01–M04/G05 VERIFIED:29/29,a;30/30,b;31830 mẫu/11feature,22513/4727/4590;9 artifact byteidentical;965 file giữ hash. Chỉ baseline Validation; không fit ML hoặc đánh giá Test. G06 VERIFIED38/38docQA/16MD. D09 và lượt B chờ duyệt. Các ghi chú chờ nghiệm thu Phase1 dưới đây là lịch sử.

## Hiện hành09/10 — F05–F06 VERIFIED, dừng chờ Phase1

Canonical checklist: qa/phase1-full-20261009/checklist.md; contract decisions/20261009-flink-full-approval.md. F01–F04 LOCKED theo Thy chấp nhận; D01–D05 giữ nguyên. F05/F06 VERIFIED: hai full jobsFINISHED,25/25QA mỗirun,34589giờ×14 và2075259phút, maxenergyerror1e-15; rerunbytehash đồng nhất,26/26handoff. SQL/smokeguard giữ nguyên; parserfull nhậnD/M/YYYY/11cases đã kiểm. G07 VERIFIED63/63docgate/16MD, review/source/resource đầy đủ. Dừng chờ Phase1, không Phase2/model/UI/Word/cài lại.

Các ghi chú F05/F06 chưa duyệt dưới đây là lịch sử.

## Hiện hành 09/10 — F01–F04 đã được Thy duyệt, đang kiểm

- Canonical: `qa/phase1-smoke-20261009/checklist.md` và `../docs/phase0-20261008/IMPLEMENTATION_PLAN.md`; decision `decisions/20261009-flink-phase1-approval.md`. D01–D05 LOCKED; chỉ F01–F04 IN_PROGRESS, F05/F06 chưa duyệt.
- F01–F04/S05 VERIFIED: Java17.0.20.1/venv-pip24.0/Flink2.3.0 SHA512 khớp; Windows8081 UI/REST mộtTM/hai slot;82/82checks,11jobs cuối,10k thật168giờ so14cột Decimal vàrerun giống byte. Handoff37/37 code/hash/read-back/liveREST đạt; F05/F06 chưa duyệt.
- Không full aggregation/model/UI/Word/Windows/restart. Các ghi chú chờ duyệt D01–D05 bên dưới là lịch sử Phase0; thiếu Java/Flink không còn là hiện trạng.

## Lịch sử 09/10 15:43 — khảo sát trước duyệt/cài

- Checklist canonical: `qa/phase0-resume-20261009/checklist.md`, R00–R05 VERIFIED khảo sát/tài liệu; evidence environment.json, dataset-verification.json13/13, documents-verification.json và review.md. Chưa duyệt thiết kế hoặc cài Flink.
- Kế hoạch triển khai canonical: `../docs/phase0-20261008/IMPLEMENTATION_PLAN.md`; quyết định chờ duyệt `OPEN_DECISIONS.md` cùng thư mục. Không tạo kế hoạch triển khai thứ hai.
- Giai đoạn 1 F01–F06 TODO, phụ thuộc Thy/GPT Web duyệt D01–D05. Đề xuất Java17 + Flink2.3.0 SQL trên WSL, bounded trước. Cần kiểm dung lượng C thật trước cài; không dùng free space ảo Linux làm bằng chứng đủ chỗ.
- WSL2 đã VERIFIED; thiếu Java/pip/Flink là toolchain chưa cài, không phải lỗi đăng ký WSL còn tồn tại. Không cài lại WSL, Docker, sửa Word, chạy job/train/dashboard hoặc restart trong lượt này.
- Năm MD đã đọc lại; hash nguồn giữ nguyên. Bước tiếp theo là nhận duyệt, không tự chuyển giai đoạn. Các bảng Pxx/timer bên dưới là lịch sử trước khôi phục WSL, không dùng làm task hiện tại.

## Lịch sử checkpoint 09/10 01:48

- Timer/màn hình: checklist canonical `qa/power-timer-20261009/checklist.md`. Timer RUNNING PID21884, shutdown không force lúc 02:16:44+07 ngày 09/10; không restart. Chưa kiểm shutdown thực tế hoặc chạy launcher hủy. Không chạy timer lần nữa sau quay lại.
- P02c VERIFIED phạm vi đọc văn bản/tool output 287 chat/50.831 step, 0 lỗi và count mismatch; nguồn `antigravity-api-legacy-v2-20261009.json` + `antigravity-api-ide-extra-20261009.json`. Không tìm chuỗi sửa Ubuntu thành công; ảnh lịch sử chưa OCR. Bối cảnh sandbox 14/5 đã xác nhận. Các ghi chú app chưa mở phía dưới là checkpoint cũ.
- P02b vẫn IN_PROGRESS: 01:47 không thấy Dism/DismHost, TiWorker/TrustedInstaller còn; log chưa success. Bước tiếp theo kiểm VMP/kết quả terminal sau Thy quay lại; không tự repair/restart hoặc cài Flink.

## Lịch sử — Giai đoạn 0 trước khi khôi phục WSL 09/10/2026

Checklist canonical: `qa/phase0-20261008/checklist.md`. Thy cho phép hỗ trợ cài môi trường, nhưng yêu cầu chẩn đoán WSL trước, WSL2 + Flink trực tiếp/no Docker, Administrator/restart phải hướng dẫn và chờ Thy. Không tự chuyển giai đoạn.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Bước tiếp theo |
| --- | --- | --- | --- | --- | --- |
| P00 | Bootstrap/scope | Thy + context/PLAN/index/rule | VERIFIED | Checklist Phase0 | Giữ Word và nguồn dữ liệu |
| P01 | Audit dữ liệu toàn bộ + kiểm độc lập | ZIP UCI | IN_PROGRESS | dataset-audit.json, full scan 2.075.259 dòng | Đối chiếu độc lập, không tạo tập huấn luyện |
| P02a | Chẩn đoán WSL/môi trường | CIM/metadata/COM read-only + Microsoft 2.7.3 | VERIFIED | environment-wsl-20261009.json; WSL_DIAGNOSIS.md | Runtime MSI/installer-class thiếu; VMP Disabled |
| P02b | Khôi phục WSL2 và môi trường Flink | Quyết định Thy + installer chính thức | IN_PROGRESS | antigravity-wsl-history-20261009.md: CBS 00:58 vẫn 50/100, DISM còn chạy, ảnh đã hết Select | Chưa xác minh VMP/WSL2; không tự hủy/restart/cài Flink; cổng thao tác Windows vẫn do Thy quyết định |
| P02c | Tra lịch sử sửa WSL/Antigravity | Yêu cầu Thy + log USER_EXPLICIT | VERIFIED | antigravity-wsl-history-20261009.md; ba chat 14/5 có lỗi sandbox và yêu cầu dùng WSL | Chỉ VERIFIED đoạn đã đọc; chưa tìm chuỗi sửa thành công. Cần Antigravity mở để truy lịch sử gốc; không coi lời MODEL là runtime evidence |
| P03 | Kiến trúc và nguồn kỹ thuật | P01/P02 + nguồn chính thức | IN_PROGRESS | Đã kiểm nguồn UCI/Apache/Microsoft; chưa có artifact kiến trúc | Hoàn thiện sau hiện trạng WSL, không job/app |
| P04 | Năm Markdown thiết kế | Yêu cầu Giai đoạn 0 | TODO | Chưa có docs/phase0-20261008/ | DATA_AUDIT, TECHNICAL_ARCHITECTURE, APP_UI_SPEC, IMPLEMENTATION_PLAN, OPEN_DECISIONS |
| P05 | Verify/read-back/handoff Phase0 | Artifact/log/hash + nguồn | TODO | Hash ZIP và Word v3 khớp; chưa có 5 tài liệu | Không báo Giai đoạn 0 xong; chờ duyệt trước Giai đoạn 1 |

Phần chẩn đoán đã kiểm không đồng nghĩa WSL2 hoặc Flink đang chạy. Python Miniconda 3.13.13, Java8 trên PATH/JBR21 của Android Studio giữ nguyên; không cài lại Python mù hoặc sửa global PATH/JAVA_HOME.

## Checkpoint Word — QA v3 Word UCI 08/10/2026

- Artifact VERIFIED: `../BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx`, 37 trang; 31/31 checks, đủ 37 PNG đã xem riêng. Sửa caption/MAE, bỏ 29 marker trong bài, chỉnh hai bìa theo Mauwword; giữ 16 nguồn/hyperlink và footer tăng. Nguồn gốc/v2/mẫu giữ hash.
- Checklist canonical: `qa/word-uci-cover-citations-20261008/checklist.md`, C01–C05 VERIFIED; đã đọc lại project/root context/PLAN/index, mistake và review; verifier cuối 31/31 PASS, hash giữ nguyên. Caption/math checklist v2 dùng truy vết, không phải bản bàn giao mới nhất.
- Thy xác nhận chính thức Phát/Hậu/Khôi và MSSV; giữ Nguyễn Thành Ngô. Không viết thêm học thuật, Chương 2–5, lịch/đóng góp hoặc ứng dụng. V3 chưa LOCKED và chưa là báo cáo hoàn chỉnh để nộp.
- Bước tiếp theo: bàn giao v3; chờ Thy duyệt hoặc giao task mới. Các checkpoint dưới đây là lịch sử.

## Checkpoint ghép ban đầu — chỉnh Word UCI 08/10/2026 — lịch sử

Nguồn chốt: Thy đã giao thực hiện; nhóm 3, dataset UCI, một hộ/kWh theo giờ/dự đoán giờ tiếp theo. Không còn chờ các quyết định này. Checklist canonical cho lượt chỉnh Word: `qa/word-uci-20261008/checklist.md` (W01–W06); contract `artifact.md` cùng thư mục. Dựng báo cáo mới trong Detaituan8910, dùng khung v2 ở thư mục cha và format Mauwword, giữ các nguồn.

- W01 VERIFIED: ZIP trong Downloads, đọc đủ 2.075.259 bản ghi; evidence `dataset-inspection.json`. Chưa giải nén, làm sạch, huấn luyện hoặc triển khai.
- W02 VERIFIED: distill và áp dụng mẫu trường, giữ khung v2/nguồn hash; artifact.md và final-verification.json.
- W03–W05 VERIFIED: Word mới 37 trang, ghép 55 đoạn/4 bảng/1 hình Chương 1, thêm 1.3, ba công thức OMML/16 nguồn; Ch2 giữ outline, 3–5 đồng bộ UCI. 41/41 checks, thử chèn/xóa heading/caption qua Word; đã xem đủ 37 PNG cuối.
- W06 VERIFIED: đã đọc lại context/PLAN/DOC_INDEX/mistake/review/checklist của project và context/PLAN/DOC_INDEX ở root; các nguồn hiện hành thống nhất UCI/Word mới, checkpoint 06/10 và London được đánh dấu lịch sử. Kiểm cuối `verify_uci_report.py` vẫn 41/41 PASS, hash artifact giữ nguyên; chờ Thy duyệt, không tự LOCKED.
- Toàn bộ quyết định pending về nhóm/dataset/phạm vi trong phần lịch sử bên dưới đã được thay thế. Artifact hiện hành là BaoCao_PhanTich_DuDoan_DienNang_UCI_20261008.docx, chưa LOCKED bởi Thy và chưa đủ báo cáo nộp.
- TODO sau duyệt: nội dung Ch2 thật; khảo sát sâu/tiền xử lý, mô hình và ứng dụng Ch3–5; lời cảm ơn/Mở đầu/Kết luận; điền lịch tuần, phần việc Phát và contribution có căn cứ. Không tự bắt đầu ứng dụng/huấn luyện ở lượt này.

## Lịch sử tiếp nhận 08/10/2026 — trước giao chỉnh Word

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| I01 | Đọc bản dán, PDF giảng viên, Chương 1–2 và mẫu | Thy + file hiện tại | VERIFIED | .agent/qa/intake-20261008/checklist.md và review.md | Chỉ kiểm hiện trạng, không coi đủ paper đã xác minh |
| I02 | Kiểm dữ liệu/mã địa phương và bảo toàn nguồn | Inventory + SHA-256 | VERIFIED | sources.json; 5 nguồn hash không đổi; 3 đường dẫn dataset không tồn tại | Chưa tải hoặc chạy dữ liệu |
| I03 | Chốt phạm vi chỉnh Word và hướng UCI | Thy | TODO | Đã hỏi lựa chọn, chưa nhận trả lời | Bản dán đề xuất một hộ, giờ, horizon 1 giờ; không tự triển khai toàn bộ prompt |
| I04 | Sửa/ghép Word mới trong Detaituan8910 | Phạm vi được Thy duyệt + PDF + Mauwword | TODO | | Không ghi đè nguồn; thêm 1.3/Heading, lịch tuần/mức đóng góp nếu được yêu cầu; Chương 2 chưa có nội dung |
| I05 | Rà đầy đủ nghiên cứu/liên kết tham khảo | Nguồn chính thức và paper | TODO | Chỉ UCI metadata đã đối chiếu | Không gọi toàn Chương 1 VERIFIED học thuật |
| I06 | Khảo sát dữ liệu và triển khai Chương 3–5 | Dataset/code thật + kế hoạch được duyệt | TODO | | Chờ đúng đường dẫn; không tạo metric hoặc kết quả giả |

Scope contract, chi tiết lỗi và recovery checkpoint nằm ở QA intake và context.md. Các mốc dưới đây là lịch sử dựng khung, không chứng minh dataset/code hiện tồn tại.

## Sửa MSSV sau khi Thy xác nhận 06/10/2026

- VERIFIED: ../BaoCao_PhanTich_DuDoan_DienNang_Khung_v2.docx; MSSV Phát 2001230640 trên bìa và bảng. Bản khung gốc giữ nguyên; không đổi format/outline/TOC hoặc nội dung.
- Scope/checklist: .agent/qa/diennang-mssv-20261006/checklist.md. Evidence verification.json và manifest.json: đảo sửa khôi phục XML nguồn; mọi part khác giữ bytes; Word mở 21 trang, headings/TOC/sections giữ nguyên; xem đủ 21 ảnh, chỉ trang 1–2 khác pixel đúng vị trí MSSV.
- Tiếp theo: Thy dùng bản v2 để điền sau. Không còn chờ xác nhận MSSV; chưa viết nội dung hoặc làm thực nghiệm, ba thông số dự đoán vẫn cần quyết định.

## Lượt 06/10/2026 — dựng khung Word, chưa viết nội dung

- VERIFIED: `../BaoCao_PhanTich_DuDoan_DienNang_Khung.docx`, 21 trang; chỉ khung, không nội dung. Theo format `../ApacheFlink.docx` hiện tại; nguồn, hai đề cương, slide/script và dataset không sửa.
- Checklist và scope contract: `.agent/qa/diennang-khung-20261006/checklist.md`; template contract: `artifact.md` cùng thư mục.
- Outline mới nhất dùng 3.4 “Kiểm tra chất lượng dữ liệu”, 5.10 “Tích hợp mô hình dự đoán”; 77 mục cấp 2. Không tạo nội dung, kết quả hoặc hình/bảng học thuật.
- Evidence: `verification.json`, `final-word.json`, `final-field-tests.json` và đủ 21 ảnh trong QA. Đã kiểm cấu trúc, nguyên văn/numbering/số trang, cập nhật field và chèn/xóa mục trong bộ nhớ, kết xuất và xem toàn bộ. Khung/logo/lề/font/styles giữ theo mẫu; có một bìa không số, front Roman và body Arabic.
- Bản khung ban đầu được giữ làm nguồn/lịch sử; bản v2 phía trên ưu tiên sau xác nhận MSSV. Chỉ tiếp tục nội dung hoặc dữ liệu khi Thy yêu cầu. Đối tượng, độ phân giải, horizon vẫn chưa chốt.

- Đã chốt khung năm chương trong context.md; Chương 1 có 11 mục, Chương 2 có 14 mục, Chương 3 có 13 mục, Chương 4 có 14 mục, Chương 5 có 17 mục.
- Hai đề cương một trang hiện mang tên KhoiTuan_Chuong1_TongQuanBaiToan.docx và HAULYVUNHAN_Chuong2_CoSoLyThuyet.docx. Ngày 06/10 đã đối chiếu nguyên văn và SHA-256 khớp QA 01/10; tên cũ trong QA chỉ dùng truy vết.
- Chưa làm: nội dung báo cáo, mã pipeline, mô hình dự đoán, dashboard và thực nghiệm. Thy nhận Chương 3–5.
- Cần quyết định trước thực nghiệm: đối tượng dự đoán, độ phân giải và khoảng dự đoán. Ví dụ một giờ chưa phải quyết định.
- Tiêu chí bàn giao đề cương: đúng nguyên văn các mục đã chốt; Times New Roman, chữ đen; không tên người, hướng dẫn hoặc mã mẫu; kết xuất và xem toàn bộ trang.
