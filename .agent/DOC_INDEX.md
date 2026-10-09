# Bản đồ tài liệu

Nguồn hiện hành cho thay UI10/10: `Detaituan8910/.agent/qa/phase4-data-guide-20261010/{checklist.md,review.md,technical-verification.json,browser-verification.json,screenshots/}`; scope chỉ expander, kỹ thuật VERIFIED/user PENDING. Ưu tiên nguồn này cho phần giải thích dữ liệu; QA4 cũ vẫn là lịch sử vận hành/artifact. Receipt Git local mới sau push. `HANDOFF_FOR_GPT_WEB.md` chỉ rõ thứ tự đọc.

| Tài liệu mới | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| Detaituan8910/.agent/qa/phase4-app-20261009/review.md, checklist.md | Handoff ứng dụng I01/I02/I03/I05, I04 deferred | Hiện hành | GPT Web kiểm app, ưu tiên handoff3 cũ |
| Detaituan8910/.agent/decisions/20261009-phase4-app-scope.md | Phạm vi mới và cổng dừng | Hiện hành, ưu tiên approval4 | Trước demo/Word/PPT/Phase5 |
| Detaituan8910/operations/README.md, services.py | Vận hành guarded foreground | Hiện hành | Start/status/stop/recovery |
| Detaituan8910/.agent/qa/phase4-app-20261009/REPORT_EVIDENCE_MAP.md | Nguồn báo cáo/kiến trúc/số liệu thực tế | Hiện hành | Sau khi được phép viết Word/slide |

| Tài liệu | Vai trò | Trạng thái | Đọc khi |
| --- | --- | --- | --- |
| .agent/context.md | Điều phối tương đương root context hiện có | Hiện hành/canonical | Đầu phiên bigdata; không tạo context trùng |
| README.md | Điểm vào repo GitHub/GPT Web | Hiện hành | Tìm code và hồ sơ bàn giao |
| HANDOFF_FOR_GPT_WEB.md | Thứ tự đọc/đường dẫn sản phẩm/evidence/ảnh cuối | Hiện hành | Gửi GPT Web link này trước |
| .agent/decisions/20261009-github-publication.md | Scope public push | Hiện hành | Trước Git publication |
| .agent/qa/github-publication-20261009/checklist.md | Gate phát hành và evidence | Hiện hành | Scan/blob/push/read-back |
| Detaituan8910/.agent/decisions/20261009-phase4-approval.md | Phase3 accepted / Phase4 scope | Hiện hành | Tiếp tục I01–I05; ưu tiên pending3 cũ |

Các ghi chú chờ nghiệm thu3 bên dưới là lịch sử, không dùng để khóa Phase4 mới được Thy duyệt.

Nguồn ưu tiên hiện hành Phase3: decision3, checklist/review/verification.json96/96 và final-package-verification.json/gói FINAL tại `Detaituan8910/.agent/qa/phase3-20261009/`; `Detaituan8910/dashboard/README.md` là hướng dẫn app. U00–U05 VERIFIED67+10+19,976/976nguồn/model/pipeline/QA cũ bất biến. Dashboard đã kiểm kỹ thuật, chưa Thy/GPT Web nghiệm thu giao diện. Không Phase4/Word/replay. Block hiện hành2B2/chưa3 dưới đây là lịch sử.

Nguồn ưu tiên hiện hành: `Detaituan8910/.agent/decisions/20261009-phase2b2-approval.md`, checklist/review/verification51/51 và documents-verification.json trong `Detaituan8910/.agent/qa/phase2b2-20261009/`, `forecasting/FINAL_EVALUATION.md`, run `models/runs/20261009-phase2b2-a/` và final `models/final/hgb-uci-hourly-v1.0-train-only/` đều dưới project điện năng. Test đã đánh giá một lần, no-refit; final manifest LOCKED, T05 VERIFIED/docprecheck62/62/17MD. Chưa duyệt Phase3. Block hiện hành này ưu tiên mọi pending2B2 cũ; QA cũ giữ nguyên.

Nguồn hiện hành09/10: `Detaituan8910/.agent/decisions/20261009-phase2b1-approval.md`, checklist/review/verification37/37 trong `.agent/qa/phase2b1-20261009/`, `forecasting/TRAINING.md` và run `models/runs/20261009-phase2b1-a2/`/b. HGB Validation đã VERIFIED, chỉ đề xuất chọn; chờ nghiệm thu2B1/duyệt2B2.2A đã LOCKED. Không Test/model cuối/dashboard/Word. Các nguồn hiện hành2A/Phase1 phía dưới là lịch sử trạng thái, QA cũ vẫn bất biến.

Hiện hành09/10: Phase1 LOCKED; Phase2A M01–M04 VERIFIED kỹ thuật. Nguồn ưu tiên `Detaituan8910/context.md`, `.agent/qa/phase2a-20261009/{checklist.md,review.md}`, decision20261009-phase2a-approval.md và `forecasting/README.md`. Artifact chính `data/ml/runs/20261009-phase2a-a/`, rerunb;29/29 và30/30checks,9artifactbyteidentical. Test chuẩn bị nhưng chưađánhgiá; khôngfit ML/UI/Word. Chờ2Anghiệmthu và2B/D09duyệt. Các trạng thái cũ bên dưới là lịch sử.

Hiện hành09/10: F05/F06 VERIFIED kỹ thuật, chờ Thy/GPT Web nghiệm thu Phase1. Nguồn ưu tiên `Detaituan8910/context.md`, `Detaituan8910/.agent/qa/phase1-full-20261009/{checklist.md,review.md,handoff-verification.json}`, decisionfull, pipeline/run_full.py/README.md. Hai fullrun25/25,26/26handoff, output chínhrun20261009T102201900234-full vàrerun20261009T102643175598-rerun; hai run đầu rejected không dùng. Oracle/regression trong Detaituan8910/.agent/scripts; SQL/smoke nguyênhash. Phase2/model/UI/Word chưa duyệt; ghi chú cổngF05/F06 bên dưới là lịch sử.

Phase1 điện năng09/10 ưu tiên `Detaituan8910/context.md`, `.agent/qa/phase1-smoke-20261009/{checklist.md,review.md,smoke-verification.json}`, `.agent/decisions/20261009-flink-phase1-approval.md` và `pipeline/README.md`. D01–D05LOCKED; F01–F04VERIFIED82/82, F05/F06 chưa duyệt. Raw TXT/fixture/log dưới Detaituan8910 là dữ liệu làm việc/QA, không thay ZIP nguồn hay Word.

Ưu tiên: yêu cầu mới nhất của Thy > bản bàn giao được Thy cung cấp ngày 28/09/2026 > quy định định dạng trong mẫu > nội dung nguồn đã xác minh > đề cương cũ. `.agent/rule.md` quy định văn phong.

Đồ án điện năng ưu tiên quyết định trực tiếp của Thy ngày 08/10/2026 và `Detaituan8910/context.md`: UCI, một hộ, kWh theo giờ, dự đoán giờ tiếp theo, nhóm 3. `Mauwword` là chuẩn hình thức; khung v2 là nguồn giữ nguyên, báo cáo Flink chỉ là tham khảo lịch sử. Hash/đường dẫn nguồn trong QA cũ là checkpoint, phải kiểm file hiện tại trước sửa. Bản bàn giao 28/09 ở trên chỉ áp dụng báo cáo Flink, không ghi đè quyết định đồ án UCI.

| Tài liệu | Vai trò | Trạng thái | Đọc khi / phụ thuộc |
| --- | --- | --- | --- |
| `Detaituan8910/docs/phase0-20261008/` | Năm tài liệu DATA_AUDIT, TECHNICAL_ARCHITECTURE, APP_UI_SPEC, IMPLEMENTATION_PLAN, OPEN_DECISIONS | Hiện hành / khảo sát VERIFIED, thiết kế PROPOSED | Sau WSL2 chạy; kế hoạch và D01–D05 chờ duyệt trước Giai đoạn1 |
| `Detaituan8910/.agent/qa/phase0-resume-20261009/` | Checklist R00–R05, probe WSL2,13 kiểm dữ liệu/hash và kiểm năm tài liệu | Hiện hành / VERIFIED khảo sát, không job/app/model | Đầu phiên đọc project context; source mới ưu tiên snapshot WSL cũ |
| `Detaituan8910/.agent/qa/phase0-20261008/checklist.md`, `dataset-audit.json`, `environment-wsl-20261009.json`, `WSL_DIAGNOSIS.md` | Full audit dataset vẫn dùng; checklist/môi trường trước khôi phục WSL | Audit hiện hành; WSL/checklist là lịch sử | Tái sử dụng full audit theo hash/mẫu QA mới; không coi WSL hiện vẫn lỗi |
| `.agent/context.md` | Context hiện có của workspace; dùng thay context ở root để tránh trùng | Hiện hành | Đầu phiên; đọc thêm PLAN để biết công việc mới |
| `Detaituan8910/context.md`, `Detaituan8910/.agent/PLAN.md`, `Detaituan8910/.agent/DOC_INDEX.md` | Context và nguồn khung năm chương của đồ án cuối môn tuần 8–10 | Hiện hành | Khi làm đồ án điện năng; không gộp với báo cáo Flink tuần 5–7 |
| `Detaituan8910/BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx` | Bản 37 trang QA caption/MAE/bìa, bỏ marker trong bài giữ nguồn/footer | Hiện hành / VERIFIED QA, chưa LOCKED hoặc đủ nộp | Nguồn sửa tiếp khi Thy giao; không dựng lại từ khung cũ |
| `Detaituan8910/BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v2_20261008.docx` | Bước caption/MAE trước scope bìa/marker | Lịch sử / nguồn giữ hash | Truy vết; không ghi đè tài liệu đang mở |
| `Detaituan8910/BaoCao_PhanTich_DuDoan_DienNang_UCI_20261008.docx` | Bản ghép ban đầu 37 trang, nguồn v2/v3 | Lịch sử / nguồn giữ hash | Truy vết; v3 hiện hành ưu tiên |
| `Detaituan8910/.agent/qa/word-uci-cover-citations-20261008/`, `Detaituan8910/.agent/qa/word-uci-caption-math-20261008/` | QA v3: 31 checks/37 trang; QA v2 làm evidence nguồn caption/math | Hiện hành v3 / lịch sử v2, nội bộ | Đọc checklist/review/verification; không gửi QA kèm Word |
| `C:/Users/thy/Downloads/individual+household+electric+power+consumption.zip` | UCI gốc do Thy chỉ rõ, 9 cột/2.075.259 dòng | Hiện hành / đọc đủ CRC và cấu trúc | Làm Ch3 khi được giao; giữ ZIP, chưa giải nén/huấn luyện |
| `Detaituan8910/.agent/qa/word-uci-20261008/` | QA ghép ban đầu, đọc ZIP và đối chiếu PDF | Lịch sử ghép / dataset-inspection vẫn là evidence ban đầu | Truy vết; QA v3 ưu tiên khi kiểm Word mới |
| `BaoCao_PhanTich_DuDoan_DienNang_Khung_v2.docx` | Khung 21 trang, một bìa, 77 mục, TOC tự động; MSSV Phát 2001230640 đã sửa đúng hai vị trí | Lịch sử / nguồn giữ nguyên | Đối chiếu hoặc phục hồi; bản UCI mới ưu tiên |
| `BaoCao_PhanTich_DuDoan_DienNang_Khung.docx` | Khung trước xác nhận MSSV, nguồn tạo v2 giữ nguyên | Lịch sử / nguồn chỉ đọc | Đối chiếu hoặc phục hồi; v2 ưu tiên |
| `Detaituan8910/.agent/qa/diennang-mssv-20261006/` | Scope, manifest, phép đảo XML, Word và đủ 21 ảnh v2; chỉ trang 1–2 đổi MSSV | Hiện hành / QA | Bằng chứng sửa MSSV, không gửi kèm DOCX |
| `Detaituan8910/.agent/qa/diennang-khung-20261006/` | Format contract, checklist, audit nguồn, native Word/field tests và 21 ảnh kết xuất | Hiện hành / QA | Kiểm/truy vết khung điện năng; không gửi tài liệu nội bộ kèm DOCX |
| `.agent/PLAN.md` | Kế hoạch báo cáo tổng hợp | Hiện hành | Tiếp tục công việc |
| `.agent/rule.md` | Quy tắc văn phong | Hiện hành | Trước khi viết báo cáo |
| `Script_ApacheFlink.md` | Script đủ 14 slide, heading khớp deck; có nhãn người nói Thy thêm, không có mốc tập | Hiện hành / nguồn lời nói | Dùng gắn Notes; chỉ lấy lời nói, không đưa nhãn/heading vào Notes; không rewrite khi chưa yêu cầu |
| `.agent/mistake.md` | Lỗi cần tránh | Hiện hành | Trước khi xử lý Word và thuật ngữ |
| `Mauwword/Mau bao cao_Do an_Khoa luan_2025.docx` | Mẫu bìa và chuẩn định dạng; hai trang cuối là quy định | Hiện hành | Khi định dạng; không ghi đè mẫu |
| `ApacheFlink_Khoituan.docx` | Đề cương chương 1–2, tên file không khớp nội dung | Tham khảo | Kiểm phạm vi cũ |
| `ApacheFlink_LyVuNhanHau.docx` | Đề cương chương 3–4, tên file không khớp nội dung | Tham khảo | Kiểm phạm vi cũ |
| `TỔNG QUAN VỀ APACHE FLINK.docx` | Bản thành viên chương 1–2 | Tham khảo | Giữ nội dung đúng làm nguồn cho bản tổng hợp |
| `ApacheFlink_LyVuNhanHau_HoanChinh.docx` | Bản thành viên chương 3–4 | Tham khảo | Sửa các điểm kỹ thuật, nguồn và văn phong |
| `BanNop/BoTrichDan/ApacheFlink.docx` | Bản 47 trang bỏ số trích dẫn trong nội dung, giữ 25 nguồn cuối có liên kết bấm được và khung bìa | Hiện hành / bàn giao | Tiếp tục sửa hoặc nộp; ưu tiên hơn bản KhoiPhucBia |
| `.agent/qa/flink-references-20261003/`, `.agent/scripts/clean_flink_references.py`, `verify_flink_references.ps1` | Kiểm 25 URL, xóa trích dẫn số, hyperlink native, cache TOC, bảo toàn nội dung và ảnh đủ 47 trang | Hiện hành / công cụ | Truy vết bản BoTrichDan; builder không ghi đè output, fields chỉ sửa candidate do agent tạo |
| `BanNop/KhoiPhucBia/ApacheFlink.docx` | Nguồn 47 trang khôi phục khung bìa 1, có chỉnh sửa tên/bảng mới nhất trước khi bỏ số trích dẫn | Lịch sử / nguồn giữ nguyên | Đối chiếu khung và chỉnh tay; bản BoTrichDan ưu tiên |
| `BanNop/ApacheFlink.docx` | Nguồn Thy lưu lúc 12:11:46 ngày 03/10, đã điền bảng và sửa bìa; thiếu khung trang đầu trước khôi phục | Nguồn / giữ nguyên | Đối chiếu phần chỉnh tay; bản KhoiPhucBia ưu tiên, không chạy lại builder phân công trống |
| `.agent/qa/flink-cover-recovery-20261003/`, `.agent/scripts/restore_flink_cover.py`, `verify_flink_cover.ps1` | Snapshot bản Thy vừa sửa, khôi phục border-only, kiểm ZIP/XML và kết xuất Word đủ 47 trang | Hiện hành / công cụ | Truy vết khung bìa; chỉ trang đầu khác ảnh, đầu ra mới không ghi đè nguồn |
| `ApacheFlink.docx` | Mẫu 47 trang khi dựng khung, checkpoint hash efac5e...662d3 ngày 06/10; hash là lịch sử, phải kiểm lại trước dùng | Nguồn chỉ đọc | Đối chiếu bìa/styles/lề/bảng; không dùng hash hoặc nội dung QA cũ để ghi đè |
| `.agent/archive/ApacheFlink_TruocPhanCong_20261003.docx` | Bản sao nguồn root trước thêm bảng, hash đã kiểm | Lịch sử / sao lưu | Phục hồi hoặc đối chiếu phạm vi sửa |
| `.agent/qa/flink-assignment-20261003/`, `.agent/scripts/add_flink_assignment.py`, `verify_flink_assignment.ps1` | Quy cách, package patch, Word chỉ đọc, ảnh đủ 47 trang và kiểm bảo toàn | Hiện hành / công cụ | Truy vết bản BanNop; builder không ghi đè đầu ra đã tồn tại |
| `BaoCao_ApacheFlink_CoDieuHuong_20261001.docx` | Tên cũ của bản Word 46 trang hiện mang tên ApacheFlink.docx | Lịch sử / tên cũ | Truy vết QA; file tên cũ không còn ở root lúc kiểm ngày 03/10 |
| `.agent/qa/flink-script-20261003/script-clean.md`, `counts-clean.json` | Bản QA trước bỏ mốc tập và đồng bộ heading; kiểm lượng chữ trong lời nói | Tham khảo / lịch sử | Truy vết; Script_ApacheFlink.md và yêu cầu mới nhất của Thy ưu tiên |
| `.agent/qa/flink-script-20261003/script-draft.md`, `verification.md` | Nháp trước có phân người và bản kiểm đối chiếu Word/14 slide | Lịch sử / tham khảo | Truy vết; bản sạch và yêu cầu mới nhất của Thy có ưu tiên |
| `.agent/qa/flink-navigation/`, `.agent/scripts/add_flink_navigation.py`, `verify_flink_navigation.ps1`, `check_flink_navigation_preservation.py` | Kiểm outline trong Word, TOC cập nhật thử và bảo toàn 46 trang | Hiện hành / công cụ | Khi kiểm hoặc sửa điều hướng của bản CoDieuHuong |
| `BaoCao_ApacheFlink_BoSungHinhBang_20261001.docx` | Nguồn 46 trang trước bổ sung điều hướng, 5 hình kỹ thuật + 5 bảng nội dung | Lịch sử | So sánh/phục hồi; CoDieuHuong hiện hành ưu tiên |
| `BaoCao_ApacheFlink_TheoMau.docx` | Nguồn Thy sửa tay, 42 trang tại 22:07 ngày 01/10; được giữ nguyên để đối chiếu | Lịch sử | Phục hồi hoặc so sánh trước bổ sung hình/bảng; không dùng builder cũ ghi đè |
| `C:/Users/thy/.codex/attachments/32ad4146-b345-42e5-b14a-df34747072b2/Văn bản đã dán.txt` | Bản bàn giao GPT web do Thy gửi; chỉ dẫn hiệu chỉnh nội dung | Hiện hành | Đối chiếu phạm vi và điều kiện kỹ thuật; yêu cầu trực tiếp của Thy có ưu tiên cao hơn |
| `.agent/qa/flink-visuals/artifact.md`, `verification.json`, `qa-summary.md`, `diagrams/` | Quy cách, kiểm bảo toàn, rà 46 trang và nguồn SVG/PNG của bốn hình mới | Hiện hành | Khi kiểm hoặc sửa bản Word BoSungHinhBang |
| `.agent/scripts/add_flink_visuals.py`, `draw_flink_diagrams.py`, `rasterize_flink_diagrams.cjs`, `finalize_flink_visuals.py`, `verify_flink_visuals.py` | Công cụ bổ sung trên bản sao, kết xuất sơ đồ, kiểm bảo toàn và finalize không ghi đè | Công cụ | Dựng lại khi được yêu cầu; nguồn hiện hành có thể đã được Thy sửa tay, cần kiểm trước |
| `.agent/qa/flink-report/artifact.md` | Quy cách dựng tài liệu ban đầu đã đối chiếu mẫu | Tham khảo | Khi cần truy vết format; bản QA flink-visuals và file hiện hành ưu tiên |
| `.agent/qa/flink-report/sources.json` | 24 URL, nhánh phiên bản và ngày mở kiểm chứng | Hiện hành | Khi kiểm chứng hoặc cập nhật phát biểu kỹ thuật |
| `.agent/qa/flink-report/verification.json` và `qa-summary.md` | Kiểm tra bản 38 trang trước bổ sung London | Lịch sử | Đối chiếu các trang và nguồn ban đầu |
| `.agent/qa/flink-lcl/verification.json`, `qa-summary.md`, `source-25.json` | Kiểm tra bản 43 trang ngày 28/09 và nguồn London Datastore | Lịch sử / tham khảo | Truy vết 4.5–4.7 và dataset; QA flink-visuals mới hơn cho bản Word hiện hành |
| `Detaituan8910/Partitioned LCL Data/Small LCL Data` | Đường dẫn London lịch sử của mô hình minh họa Flink; không thấy tại đường dẫn cũ khi kiểm 08/10 | Lịch sử / tham khảo bài Flink | Chỉ truy vết; không dùng làm dataset đồ án UCI hiện hành |
| `.agent/archive/BaoCao_ApacheFlink_TruocBoSungLCL_20260928.docx` | Bản báo cáo 38 trang trước bổ sung | Lịch sử | Phục hồi hoặc đối chiếu nội dung gốc |
| `.agent/scripts/build_flink_report.py` | Dựng báo cáo theo phạm vi cũ, để trống 4.5–4.7 | Công cụ lịch sử | Không chạy lên bản hiện hành; sẽ ghi đè nội dung mới |
| `.agent/scripts/append_lcl_sections.py` | Ghép 4.5–4.7 từ bản sao trước sửa, thêm sơ đồ và nguồn | Công cụ | Chạy lại sẽ bỏ các sửa tay sau lượt này; lưu bản hiện hành trước khi dùng |
| `.agent/scripts/inspect_lcl_sample.py`, `verify_lcl_report.py` | Khảo sát ba CSV và kiểm tra bảo toàn/phân trang | Công cụ | Kiểm tra dataset hoặc bản Word sau bổ sung |
| `.agent/scripts/word_pdf.ps1`, `finalize_flink_report.py` | Cập nhật trường, xuất PDF, hiệu chỉnh mục lục và metadata | Công cụ | Finalize sau lần lưu Word cuối, xuất PDF chỉ đọc và kiểm tra lại |
| `C:/Users/thy/Downloads/Báo cáo Apache Flink.pptx` | Deck Gamma gốc 13 slide, chuẩn thiết kế | Tham khảo | Khi cần đối chiếu; không ghi đè |
| `Slides/Slide_ApacheFlink_DaChot_20261001.pptx` | Deck trước bốn chỉnh nhỏ cuối, giữ để đối chiếu | Lịch sử | Phục hồi và so sánh; bản ChotCuoi ưu tiên hơn |
| `Slides/ApacheFlink_CoScriptNotes_20261003.pptx` | Bản riêng 14 slide gắn đúng lời nói vào từng Notes; giữ nguyên mặt slide nguồn Thy sửa mới nhất | Hiện hành / tập đọc | Dùng khi muốn đọc script trong Notes; không thay bản không Notes |
| `.agent/qa/flink-script-notes-20261003/`, `.agent/scripts/add_flink_script_notes.mjs`, `verify_flink_script_notes.ps1` | Mapping script/slide/Notes, package patch tối thiểu, native PowerPoint xác nhận 14 Notes, so pixel 14 trang | Hiện hành / công cụ | Truy vết bản có script; xem manifest, verification-final và receipt v2; không rerun lên output đã tồn tại |
| `Slides/ApacheFlink_14Slide_KhongGhiChu_20261003.pptx` | Đường dẫn cũ của bản không Notes; không còn tại tên này, Thy đã đổi tên/sửa tiếp | Lịch sử / tên cũ | Chỉ truy vết QA; dùng root ApacheFlink.pptx hiện có cho chỉnh tiếp |
| `.agent/qa/flink-notes-20261003/`, `.agent/scripts/clear_flink_notes.mjs`, `inspect_flink_notes.ps1` | Kiểm xóa Notes có mục tiêu, bảo toàn mọi slide, PowerPoint xác nhận Notes rỗng, so pixel 14 trang | Hiện hành / công cụ | Truy vết bản Không Ghi Chú; nguồn và edit-manifest giữ ghi chú cũ để khôi phục |
| `Slides/ApacheFlink_14Slide_MocChuong_20261003.pptx` | Nguồn trước xóa Notes; bốn tiêu đề mở phần khớp mục lục, slide 4 chỉ Apache Flink, footer x/14 | Lịch sử / nguồn | Phục hồi ghi chú hoặc so sánh; bản Không Ghi Chú ưu tiên |
| `.agent/qa/flink-titles-20261003/`, `.agent/scripts/fix_flink_titles.mjs`, `inspect_flink_title_bounds.ps1` | Nguồn kiểm, build/finalizer, bảo toàn năm title-only changes, render PowerPoint, so pixel và COM group text bounds | Hiện hành / công cụ | Kiểm hoặc truy vết deck Mốc Chương; finalizer không ghi đè output/receipt |
| `Slides/ApacheFlink_14Slide_20261002.pptx` | Nguồn 14 slide trước đồng bộ tiêu đề mở phần ngày 03/10; giữ nguyên để đối chiếu | Lịch sử / nguồn | Phục hồi/so sánh; bản Mốc Chương ưu tiên |
| `ApacheFlink.pptx` | Deck root Thy sửa tay, lưu lúc 12:56:06 ngày 03/10, 14 slide; SHA-256 ac372699b9b63db3ab8104f9e64787cd82cba2252a86b564856a6c6d3f19c679 | Hiện hành / nguồn mặt slide | Ưu tiên khi sửa tiếp; kiểm lại file/hash trước task, không ghi đè bằng nguồn cũ 13 slide |
| `Slides/ApacheFlink.pptx` | Deck 14 slide Thy lưu trước root lúc 11:35:06 ngày 03/10, SHA-256 2439f34353d1e1bc6775f1ca4eea3402c37800a1a0ba06fde24fa3900d6db650 | Lịch sử / nguồn giữ nguyên | So sánh hoặc khôi phục; root lưu sau ưu tiên |
| `.agent/qa/flink-14slides-20261002/artifact.md`, `validation-final.json`, `verification-final.json`, `qa-summary.md`, `final-render-v2/` | Quy cách, package/layout/font/import, kiểm bảo toàn nguồn và ảnh PowerPoint 14 slide | Hiện hành | Xác minh bản 14 slide; các nháp trong build và render trước đó không phải bản bàn giao |
| `.agent/scripts/inspect_flink_14.mjs`, `build_flink_14.mjs`, `finalize_flink_14.mjs`, `render_flink_14.ps1`, `verify_flink_14.mjs` | Công cụ kiểm nguồn, dựng slide native, finalize và kiểm PowerPoint/bảo toàn | Công cụ | Chạy lại chỉ khi được yêu cầu; builder kiểm hash nguồn; output/receipt finalizer cần đường dẫn chưa tồn tại |
| `.agent/qa/gamma-final/`, `.agent/scripts/final_touches_gamma.py` | Bằng chứng và công cụ sửa đúng bốn chi tiết, bảo toàn các phần còn lại | Hiện hành | Kiểm bản ChotCuoi; script tạo candidate, finalizer cần tên đầu ra mới |
| `.agent/qa/gamma-fix/` | Inventory, hash, kiểm package/layout/import, kiểm nội dung và ảnh QA PowerPoint | Hiện hành | Xác minh deck ngày 01/10 |
| `.agent/scripts/fix_gamma_deck.py`, `finalize_gamma.mjs`, `verify_gamma.py`, `render_deck.ps1` | Sửa trên bản sao nguồn, kiểm và xuất slide | Công cụ | Dựng lại khi được yêu cầu; finalizer không ghi đè output, cần tên phiên bản mới |
