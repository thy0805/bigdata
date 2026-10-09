# F05–F06: full UCI

Contract: ../../decisions/20261009-flink-full-approval.md. Không model/dashboard/Word. SQL và smoke launcher giữ nguyên.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| G00 | Scope/runtime/disk/source guard | Thy + manifest + REST | VERIFIED | handoff-verification.json;26/26 trước docread-back, nguồn/hash/runtime/disk | Không cài lại |
| F05 | Launcher riêng/full Flink | SQL F04 + raw | VERIFIED | Jobs9307ab8abf4d8286245019045ed694ac/170801766af83f1b80107c86d91cedfd FINISHED;2075259rows/0parseerror; verification25/25 mỗi run | Parserfull nhậnD/M/YYYY, SQL/smoke gốc giữ hash |
| F06a | Oracle full14 cột, phút/residual | Raw độc lập + audit | VERIFIED | Mỗi run34589giờ×14=484246 trường;2075259phút;25/25, maxenergyerror1e-15kWh | NULL2188/count/time exact; residualerror6.67e-15Wh |
| F06b | Rerun riêng/hash equivalence | Full pipeline | VERIFIED | handoff-verification.json;grid8b03f1e3...a8b5b2bc và tất cả Flink partcategories giống byte | 11/11datecases; hai output lỗi không promote |
| G07 | Source/runtime/resource/read-back/handoff | Manifest/log/hash | VERIFIED | documents-verification.json63/63,16MD UTF8/link/read-back + supporthash, handoff26/26; review.md đã đọc toàn bộ | Dừng chờ Phase1; Phase2 chưa duyệt |
