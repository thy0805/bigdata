import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "forecasting"))
import prepare_baselines as product


def main():
    qa = ROOT / ".agent/qa/phase2a-20261009"
    run = ROOT / "data/ml/runs/20261009-phase2a-a"
    rerun = ROOT / "data/ml/runs/20261009-phase2a-b"
    manifest = json.loads((run / "manifest.json").read_text())
    summary = json.loads((run / "split-summary.json").read_text())
    metrics = json.loads((run / "metrics-validation.json").read_text())
    review = (qa / "review.md").read_text(encoding="utf-8")
    checks = []

    def check(name, passed, details=None):
        checks.append({"name": name, "passed": bool(passed), "details": details})

    files = [ROOT / "context.md", ROOT / ".agent/PLAN.md", ROOT / ".agent/DOC_INDEX.md", ROOT / ".agent/mistake.md"]
    files += [ROOT.parent / ".agent" / name for name in ("context.md", "PLAN.md", "DOC_INDEX.md")]
    files += list((ROOT / "docs/phase0-20261008").glob("*.md"))
    files += [ROOT / ".agent/decisions/20261009-phase2a-approval.md", qa / "checklist.md", qa / "review.md", ROOT / "forecasting/README.md"]
    hashes = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        hashes[str(path.relative_to(ROOT.parent))] = product.sha256(path)
        check(f"UTF8_full_read:{path.name}:{path.parent.name}", "\ufffd" not in text and not re.search("[\u0e00-\u0e7f]", text), {"characters": len(text)})
    for path in (qa / "review.md", ROOT / "forecasting/README.md"):
        broken = []
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://")):
                continue
            if not (path.parent / target.split("#")[0]).resolve().exists():
                broken.append(target)
        check(f"deliverable_local_links:{path.name}", not broken, broken)
    check("review_source_checksum", manifest["source"]["sha256"] in review and manifest["source"]["run_id"] in review)
    check("review_counts_from_manifest", all(f"{manifest[key]:,}".replace(",", ".") in review for key in ("input_axis_hours", "input_complete_hours", "input_null_hours", "eligible_ml_hours", "excluded_ml_hours")))
    for split, label in (("train", "Train"), ("validation", "Validation"), ("test", "Test")):
        row = next(line for line in review.splitlines() if line.startswith(f"| {label} |"))
        parts = [part.strip() for part in row.split("|")[1:-1]]
        values = summary[split]
        check(f"review_split_counts:{split}", [int(p.replace(".", "")) for p in parts[2:]] == [values["axis_hours"], values["eligible_hours"], values["excluded_hours"]])
        import datetime
        endpoints = [datetime.datetime.fromisoformat(values[k]).strftime("%d/%m/%Y %H:%M") for k in ("axis_start", "axis_end")]
        check(f"review_split_range:{split}", all(value in parts[1] for value in endpoints))
    for model, label in (("naive", "Naive"), ("seasonal_naive_24", "Seasonal Naive24")):
        row = next(line for line in review.splitlines() if line.startswith(f"| {label} |"))
        check(f"review_metrics:{model}", all(f"{metrics['models'][model][metric]:.10f}".replace(".", ",") in row for metric in ("mae_kwh", "rmse_kwh")) and "4.727" in row)
    primary = {}
    for split in summary.values():
        for key, value in split["exclusion_primary"].items():
            primary[key] = primary.get(key, 0) + value
    check("review_exclusion_reconciliation", sum(primary.values()) == manifest["excluded_ml_hours"] and primary == {"missing_target": 504, "insufficient_history": 166, "missing_lag_1": 67, "missing_lag_2": 67, "missing_lag_3": 67, "missing_lag_24": 209, "missing_lag_168": 501, "missing_rolling_24": 1178})
    for folder, expected in ((run, 29), (rerun, 30)):
        result = json.loads((folder / "verification.json").read_text())
        check(f"QA_report_final:{folder.name}", result["status"] == "VERIFIED" and result["passed"] == result["total_checks"] == expected)
    check("rerun_hash_manifest", manifest["outputs_sha256"] == json.loads((rerun / "manifest.json").read_text())["outputs_sha256"])
    check("review_gap_and_mask_limits_explicit", all(token in review for token in ("7.226", "121 giờ", "Lag 168", "không nén trục", "Rolling 3/24", "4.727 timestamp", "không phải mã hóa")))
    check("review_HGB_and_D09_pending", "cấu hình khởi đầu chưa fit" in review and "phê duyệt Phase2B và chính sách D09" in review and "early_stopping=False" in review)
    checklist = (qa / "checklist.md").read_text(encoding="utf-8")
    def status_of(row):
        return row.split("|")[4].strip()

    check("state_parser_rejects_APPLIED_UNVERIFIED_as_VERIFIED", status_of("| G06 | item | source | APPLIED_UNVERIFIED | evidence | note |") != "VERIFIED")
    check("M01_M04_verified_with_evidence", all(status_of(next(line for line in checklist.splitlines() if line.startswith(f"| {task} |"))) == "VERIFIED" for task in ("G00", "M01", "M02", "M03", "M04", "G05")))
    check("G06_workflow_state_exact", status_of(next(line for line in checklist.splitlines() if line.startswith("| G06 |"))) in ("APPLIED_UNVERIFIED", "VERIFIED"))
    check("latest_context_gate", "Phase2A VERIFIED" in (ROOT / "context.md").read_text(encoding="utf-8")[:200] and "chờ" in (ROOT / "context.md").read_text(encoding="utf-8")[:500])
    result = {"status": "VERIFIED" if all(c["passed"] for c in checks) else "APPLIED_UNVERIFIED", "passed": sum(c["passed"] for c in checks), "total_checks": len(checks), "read_back_files": len(files), "files_sha256": hashes, "checks": checks}
    product.write_json(qa / "documents-verification.json", result)
    print(json.dumps({"status": result["status"], "passed": result["passed"], "total": result["total_checks"], "files": len(files), "failed": [c for c in checks if not c["passed"]]}, ensure_ascii=False))
    if result["status"] != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
