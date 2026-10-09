# Điểm vào bàn giao cho GPT Web

## Trạng thái và phạm vi

Checkpoint phát hành ngày09/10/2026: **Phase3 ACCEPTED; Phase4 AUTHORIZED, chưa hoàn tất**. Repo public được Thy chỉ định; code, hồ sơ và dữ liệu dẫn xuất được đưa lên để rà soát trực tiếp. Word vẫn gửi file riêng. Không dùng việc push GitHub làm bằng chứng nghiệm thu tích hợp Phase4.

Commit phát hành đầu: `31a7703`. [Quyết định phát hành](.agent/decisions/20261009-github-publication.md). [Checklist GitHub](.agent/qa/github-publication-20261009/checklist.md).

## Đọc theo thứ tự

1. [Checkpoint dự án hiện hành](Detaituan8910/context.md), [kế hoạch I01–I05](Detaituan8910/.agent/PLAN.md) và [phê duyệt Phase4](Detaituan8910/.agent/decisions/20261009-phase4-approval.md).
2. [Bàn giao Phase3](Detaituan8910/.agent/qa/phase3-20261009/review.md), [QA tổng96/96](Detaituan8910/.agent/qa/phase3-20261009/verification.json), [QA kỹ thuật cuối67/67](Detaituan8910/.agent/qa/phase3-20261009/technical-verification-v3.json), [QA trình duyệt10/10](Detaituan8910/.agent/qa/phase3-20261009/browser-verification.json).
3. [Ứng dụng](Detaituan8910/dashboard/app.py), [backend/artifact gate](Detaituan8910/dashboard/data_service.py), [biểu đồ](Detaituan8910/dashboard/charts.py), [launcher](Detaituan8910/dashboard/serve.py), [hướng dẫn](Detaituan8910/dashboard/README.md).
4. [Model cuối/lineage](Detaituan8910/models/final/hgb-uci-hourly-v1.0-train-only/manifest.json), [metric Test cố định](Detaituan8910/models/runs/20261009-phase2b2-a/metrics-test.json), [prediction Test](Detaituan8910/models/runs/20261009-phase2b2-a/predictions-test.csv), [bàn giao2B2](Detaituan8910/.agent/qa/phase2b2-20261009/review.md).
5. [Hourly-grid Flink](Detaituan8910/data/processed/runs/20261009T102201900234-full/hourly-grid.csv), [manifest](Detaituan8910/data/processed/runs/20261009T102201900234-full/manifest.json), [companion verification](Detaituan8910/data/processed/runs/20261009T102201900234-full/verification.json), [bàn giao full Flink](Detaituan8910/.agent/qa/phase1-full-20261009/review.md).
6. [Thiết kế và audit Phase0](Detaituan8910/docs/phase0-20261008/), [feature schema](Detaituan8910/data/ml/runs/20261009-phase2a-a/feature-schema.json), [split](Detaituan8910/data/ml/runs/20261009-phase2a-a/split-summary.json), [source ML manifest](Detaituan8910/data/ml/runs/20261009-phase2a-a/manifest.json).

## Ảnh đã nghiệm thu

| Tab | 1920×1080 | Laptop |
| --- | --- | --- |
| Tổng quan | [Ảnh](Detaituan8910/.agent/qa/phase3-20261009/screenshots/overview-1920.jpg) | [Ảnh](Detaituan8910/.agent/qa/phase3-20261009/screenshots/overview-laptop-final.jpg) |
| Phân tích | [Ảnh](Detaituan8910/.agent/qa/phase3-20261009/screenshots/analysis-1920-final-v3.jpg) | [Ảnh](Detaituan8910/.agent/qa/phase3-20261009/screenshots/analysis-laptop-final.jpg) |
| Dự báo | [Ảnh](Detaituan8910/.agent/qa/phase3-20261009/screenshots/forecast-1920-final.jpg) | [Ảnh](Detaituan8910/.agent/qa/phase3-20261009/screenshots/forecast-laptop-final.jpg) |

Hai ảnh bổ sung: [chất lượng dữ liệu](Detaituan8910/.agent/qa/phase3-20261009/screenshots/analysis-quality-1920.jpg), [mốc đầu Test](Detaituan8910/.agent/qa/phase3-20261009/screenshots/first-test-forecast.jpg).

## Quy tắc đọc bằng chứng

- JSON và review là snapshot tại thời điểm kiểm. Pending3 trong review cũ đã được phê duyệt mới thay thế, không viết lại evidence cũ.
- Manifest Flink ban đầu ghi APPLIED_UNVERIFIED; verification.json companion ghi kết quả kiểm sau đó. Không suy ra thất bại hoặc VERIFIED chỉ bằng tìm substring.
- Source gate của dashboard được chạy lại trước publication và đạt21hash. Kiểm Git so byte từng blob với file gốc; không chuyển CRLF/LF làm đổi checksum.
- Model Train-only,11feature,D09 và Test4.590 không thay đổi. Không train/refit hoặc lựa chọn mô hình bằng Test.
- Raw ZIP/TXT, bản rerun, cache Flink, bộ cài, Office/PDF và ZIP bàn giao không được phát hành. Link đến chúng trong snapshot cũ có thể không mở được trên GitHub; không khẳng định repo là toàn bộ ổ đĩa hoặc bản portable.
- localhost:8501/8081 thuộc máy của Thy. Link GitHub cho phép đọc code/evidence, không biến app localhost thành một dịch vụ trực tuyến.

## Bước tiếp theo

I01–I05 phải có QA mới và DEMO_RUNBOOK trước nghiệm thu Phase4. Sau đó đưa review/evidence mới lên repo và chỉ rõ phiên bản/đường dẫn. Chưa sửa Word, PPT, tạo video chính thức, replay hoặc mở Phase5.
