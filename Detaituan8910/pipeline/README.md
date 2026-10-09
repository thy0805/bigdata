# Pipeline Flink — F01–F06

## Full UCI — F05–F06 được Thy duyệt ngày09/10

Kết quả ngày09/10: hai fullrun VERIFIED25/25 mỗirun, rerun byteidentical; handoff26/26 và đọc lại16MD/63kiểm. Bàn giao `.agent/qa/phase1-full-20261009/review.md`; đang chờ Thy/GPT Web nghiệm thu Phase1. Các lệnh dưới đây để tái lập khi được yêu cầu, không tự mở Phase2.

Launcher full riêng giữ file SQL/smoke F04 nguyên hash. Dữ liệu UCI có cả D/M/YYYY và DD/MM/YYYY; launcher chuẩn hóa các phần ngày bằng SPLIT_INDEX/LPAD và kiểm cast/roundtrip. Chỉ hai biểu thức đọc ngày khác bản mẫu; công thức tổng hợp, NULL, residual, strictschema giữ nguyên. Tài liệu hàm: [Apache Flink2.3](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/functions/built-in-functions/).

Kiểm cluster bằng lệnh status dưới đây. Nếu chưa chạy, giữ một terminal serve. Khi không có job khác đang chạy, từ PowerShell:

```powershell
wsl -d Ubuntu-24.04 -u cute -- python3 /mnt/d/Hoctap/bigdata/Detaituan8910/pipeline/run_full.py --label full
```

Mỗi lần tạo run_id mới trong `data/processed/runs/`, CSV parts do Flink tạo. `hourly-grid.csv` có14 cột, Python chỉ sắp xếp/bổ sung bucket trống, không tính năng lượng thay Flink. Manifest chỉ APPLIED_UNVERIFIED đến khi oracle độc lập đạt. Log, SQL thực thi, REST/job/version, RAM/actualC/D mỗi3giây và manifest ở `.agent/qa/phase1-full-20261009/runs/<run_id>/`. Không sửa thư mục run cũ hoặc append/trộn dữ liệu.

Sau khi launcher kết thúc thành công và có manifest, thay `<run_id>` bằng giá trị vừa in:

```powershell
wsl -d Ubuntu-24.04 -u cute -- python3 /mnt/d/Hoctap/bigdata/Detaituan8910/.agent/scripts/verify_full_pipeline.py <run_id>
```

Oracle đọc raw độc lập, so toàn bộ giờ×14 trường và toàn bộ phút/residual, nguồn/hash/NULL. Năng lượng tolerance1e-8kWh, count/time/NULL exact. Kết quả ở verification.json, không dùng oracle làm dữ liệu sản phẩm. Chạy lại pipeline với `--label rerun` rồi kiểm run_id mới, so hash hourly-grid.csv. Không chạy hai launcher full đồng thời trên cụm này.

QA ngày hợp lệ/ngày sai riêng: `.agent/scripts/verify_full_date_parser.py`; fixture chỉ là test. Hai run đầu ngày09/10 bị parser cũ gắn nhầm1.716.480 lỗi ngày; không có hourly-grid.csv và không được dùng làm dữ liệu sản phẩm. Không bỏ guard/parservalidation để ép nghiệm thu.

F05/F06 không cho phép train, dashboard, sửa Word hoặc tự chuyển Giai đoạn2. Bàn giao hiện hành trong `.agent/qa/phase1-full-20261009/`.

## Lịch sử / hướng dẫn chạy mẫu F01–F04

Môi trường đã kiểm: Ubuntu-24.04 WSL2, Java17, Flink2.3.0 SQL BATCH, mộtTaskManager/hai slot. Chỉ chạy mẫu QA, chưa chạy toàn bộ UCI hoặc tạo dữ liệu sản phẩm.

Chạy từ PowerShell Windows, không cần sudo hay mật khẩu. Cluster hiện có thể còn chạy; kiểm trạng thái trước khi start.

```powershell
wsl -d Ubuntu-24.04 -- python3 /mnt/d/Hoctap/bigdata/Detaituan8910/pipeline/cluster.py status
```

Nếu chưa có cluster, mở một terminal riêng và giữ lệnh này chạy:

```powershell
wsl -d Ubuntu-24.04 -- python3 /mnt/d/Hoctap/bigdata/Detaituan8910/pipeline/cluster.py serve
```

Xem [Flink Web UI](http://localhost:8081). `serve` không tạo service tự khởi động. Khi đóng holder/WSL, phải kiểm lại cluster thay vì giả định vẫn chạy.

Từ terminal khác chạy mẫu thật10.000 dòng:

```powershell
wsl -d Ubuntu-24.04 -- python3 /mnt/d/Hoctap/bigdata/Detaituan8910/pipeline/run_smoke.py /mnt/d/Hoctap/bigdata/Detaituan8910/.agent/qa/phase1-smoke-20261009/inputs/real-10000.txt --label real-manual
```

Mỗi lần tạo run_id mới dưới `.agent/qa/phase1-smoke-20261009/runs/`; SQL, JobID/REST, log, source/template hash và CSV part có trong đó. `hourly-grid.csv` chỉ được tạo khi jobFINISHED và kiểm dữ liệu đạt. Python chỉ bổ sung bucket giờ trống, không tính thay các tổng điện năng của Flink. Source số lỗi/ngày lỗi có quarantine giữ raw strings; CSV sai số cột khiến jobFAILED; không silent-ignore.

Chạy lại toàn bộ bộ kiểm nhỏ, không phải full UCI:

```powershell
wsl -d Ubuntu-24.04 -- python3 /mnt/d/Hoctap/bigdata/Detaituan8910/.agent/scripts/verify_phase1_smoke.py
```

Dừng cluster riêng của project:

```powershell
wsl -d Ubuntu-24.04 -- python3 /mnt/d/Hoctap/bigdata/Detaituan8910/pipeline/cluster.py stop
```

Không đổi input sang raw full. Wrapper chặn input ngoàiQA/inputs và hơn25k dòng. F05/F06 phải được Thy duyệt trước. Fixtures chỉ là kiểm thử, không đưa lên dashboard/báo cáo làm số liệu thực nghiệm.

Evidence nghiệm thu: `.agent/qa/phase1-smoke-20261009/smoke-verification.json`82/82, `environment-final.json`, `runtime-install.json`, `inputs-manifest.json`, `review.md`. Bản SQL cuối SHA256424b084c2c776b1d253ca272527c61734a7e64f6be9df6e2dd2a55f96e3966f3.
