import argparse
import csv
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase2b2-20261009"
RUN = ROOT / "models/runs/20261009-phase2b2-a"
FINAL = ROOT / "models/final/hgb-uci-hourly-v1.0-train-only"


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("precheck", "final"), required=True)
    args = parser.parse_args()
    report_path = QA / ("documents-precheck.json" if args.stage == "precheck" else "documents-verification.json")
    if report_path.exists():
        raise FileExistsError(report_path)
    checks = []

    def check(name, passed, details=None):
        checks.append(dict(name=name, passed=bool(passed), details=details))

    files = [ROOT / name for name in ("context.md", ".agent/PLAN.md", ".agent/DOC_INDEX.md", ".agent/mistake.md", "forecasting/FINAL_EVALUATION.md")]
    files += [ROOT.parent / ".agent" / name for name in ("context.md", "PLAN.md", "DOC_INDEX.md")]
    files += sorted((ROOT / "docs/phase0-20261008").glob("*.md"))
    files += [ROOT / ".agent/decisions/20261009-phase2b2-approval.md", QA / "checklist.md", QA / "review.md", QA / "preflight-notes.md"]
    texts = {}
    for path in files:
        content = path.read_text(encoding="utf-8")
        texts[path] = content
        check("UTF8_full_read:"+str(path.relative_to(ROOT.parent)), "\ufffd" not in content and not re.search("[\u0e00-\u0e7f]", content), len(content))
    for path, content in texts.items():
        broken = []
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if target.startswith(("https://", "http://")):
                continue
            resolved = (path.parent/target.split("#")[0]).resolve()
            if not resolved.exists() and resolved != (QA / "documents-verification.json").resolve():
                broken.append(target)
        check("local_links:"+str(path.relative_to(ROOT.parent)), not broken, broken)
    review = texts[QA / "review.md"]
    check("handoff_exact_10_numbered_sections", re.findall(r"^## (\d+)\. ", review, flags=re.M) == [str(i) for i in range(1, 11)])
    qa = load(QA / "verification.json")
    testqa = load(QA / "test-verification.json")
    metrics = load(RUN / "metrics-test.json")
    validation = load(ROOT / "models/runs/20261009-phase2b1-a2/metrics-validation.json")
    final = load(FINAL / "manifest.json")
    companion = load(RUN / "verification.json")
    check("technical_QA_51_and_before_packaging_44_PASS", qa["status"] == "VERIFIED" and qa["passed"] == qa["total_checks"] == 51 and
          all(item["passed"] for item in qa["checks"]) and testqa["status"] == "VERIFIED" and testqa["passed"] == testqa["total_checks"] == 44)
    check("final_LOCKED_hash_and_QA_binding", final["status"] == "LOCKED" and final["model_sha256"] == sha256(FINAL / "model.joblib") == qa["final_model_sha256"] and
          sha256(FINAL / "manifest.json") == qa["final_manifest_sha256"] and final["test_verification_sha256"] == sha256(QA / "test-verification.json") and
          companion["status"] == "VERIFIED" and companion["qa_sha256"] == sha256(QA / "verification.json"))
    check("review_final_hash_version_size", final["model_sha256"] in review and final["version"] in review and "154.146" in review and
          (FINAL / "model.joblib").stat().st_size == 154146 and final["no_refit"] and final["fitted_rows"] == 22513)
    table_rows = review.splitlines()
    for name, label in (("hgb", "HGB"), ("naive", "Naive"), ("seasonal_naive_24", "Seasonal Naive24")):
        rows = [line for line in table_rows if line.startswith("| "+label+" |")]
        first = [value.strip() for value in rows[0].split("|")[1:-1]]
        second = [value.strip() for value in rows[1].split("|")[1:-1]]
        third = [value.strip() for value in rows[2].split("|")[1:-1]]
        check("Test_table:"+name, int(first[1]) == metrics["n"] == 4590 and all(math.isclose(float(first[index]), metrics["models"][name][kind], rel_tol=0, abs_tol=1e-14)
              for index, kind in ((2, "mae_kwh"), (3, "rmse_kwh"))))
        check("Validation_Test_compare:"+name, all(math.isclose(float(second[index]), origin["models"][name][kind], rel_tol=0, abs_tol=1e-14)
              for index, origin, kind in ((1, validation, "mae_kwh"), (2, validation, "rmse_kwh"), (3, metrics, "mae_kwh"), (4, metrics, "rmse_kwh"))))
        check("D09_table:"+name, all(math.isclose(float(third[index]), metrics["models"][name][kind], rel_tol=0, abs_tol=1e-14)
              for index, kind in ((1, "negative_raw_count"), (2, "minimum_raw_kwh"), (3, "changed_prediction_count"), (4, "d09_mae_reduction_kwh"), (5, "d09_rmse_reduction_kwh"))))
    check("scientific_limits_protocol_and_stop", all(term in review for term in ("một bước cuốn chiếu", "22.513", "4.727", "4.590", "5.189", "599", "DST", "độ trễ", "không đại diện nhiều hộ", "Phase3 chưa được phê duyệt", "Chưa tạo dashboard", "chưa sửa Word")))
    check("audit_exceptions_correct_not_cache_immutable", all(term in review for term in ("924/933", "951/951", "9 cache", "16 archive", "52 blobStorage", "3 archive", "6 blobStorage", "không phải chưa từng đọc")) and
          qa["preservation"]["matched"] == qa["preservation"]["count"] == 951 and len(qa["preservation"]["inherited_runtime_exceptions"]) == 9 and
          qa["preservation"]["historical_68"] == dict(archive=16, blobStorage=52))
    rows = [line.split("|")[1:-1] for line in texts[QA / "checklist.md"].splitlines() if re.match(r"\| T\d\d \|", line)]
    states = {values[0].strip(): values[3].strip() for values in rows}
    check("checklist_exact_states", len(states) == 6 and all(states["T"+str(i).zfill(2)] == "VERIFIED" for i in range(5)) and
          states["T05"] == ("APPLIED_UNVERIFIED" if args.stage == "precheck" else "VERIFIED"), states)
    for path in (ROOT / "context.md", ROOT / ".agent/PLAN.md", ROOT / ".agent/DOC_INDEX.md"):
        first_block = texts[path].split("## Hiện hành", 2)[1] if "## Hiện hành" in texts[path] else texts[path].split("## Nguồn ưu tiên", 2)[1]
        check("current_checkpoint_semantics:"+path.name, "Phase2B2" in first_block and "51/51" in first_block and "Phase3" in first_block and
              ("chờ docQA" in first_block if args.stage == "precheck" else "documents-verification.json" in first_block))
    for path in sorted((ROOT / "docs/phase0-20261008").glob("*.md")):
        top = texts[path].splitlines()[:8]
        check("design_sources_mark_prior_state_historical:"+path.name, "Phase2B2" in "\n".join(top) and "lịch sử" in "\n".join(top))
    check("evaluation_unchanged_after_pretest_lock", sha256(ROOT / "forecasting/evaluate_final.py") == load(QA / "selection-lock.json")["evaluation_code_sha256"])
    preservation = load(QA / "preservation-before.json")
    unchanged = []
    cache = []
    for filename, expected in preservation["files"].items():
        actual = sha256(filename) if Path(filename).is_file() else None
        if actual != expected:
            (cache if "/flink-tmp/" in filename else unchanged).append(filename)
    check("end_of_task_source_preservation", not unchanged, dict(files=preservation["count"], product_changes=unchanged, cache_exceptions=cache))
    with (RUN / "predictions-test.csv").open(newline="", encoding="utf-8") as handle:
        saved = list(csv.DictReader(handle))
    check("final_prediction_artifact_readback_count_hash", len(saved) == 4590 and len({row["target_hour"] for row in saved}) == 4590 and
          sha256(RUN / "predictions-test.csv") == final["prediction_sha256"])
    check("status_substring_regression", "APPLIED_UNVERIFIED" != "VERIFIED" and "LOCKED" != "VERIFIED")
    success = all(item["passed"] for item in checks)
    result = dict(status="VERIFIED" if success else "APPLIED_UNVERIFIED", captured_at=datetime.now(timezone.utc).isoformat(),
                  stage=args.stage, total_checks=len(checks), passed=sum(item["passed"] for item in checks), checks=checks,
                  files_sha256={str(path.relative_to(ROOT.parent)):sha256(path) for path in files},
                  technical_QA_sha256=sha256(QA / "verification.json"), source_preservation_count=preservation["count"],
                  final_model_sha256=sha256(FINAL / "model.joblib"), verifier_sha256=sha256(Path(__file__)))
    with report_path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(dict(status=result["status"], passed=result["passed"], total=len(checks), documents=len(files),
                         failed=[item["name"] for item in checks if not item["passed"]])))
    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
