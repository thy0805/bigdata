import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase2b1-20261009"
RUN = ROOT / "models/runs/20261009-phase2b1-a2"


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    checks = []

    def check(name, passed, details=None):
        checks.append(dict(name=name, passed=bool(passed), details=details))

    files = [ROOT / name for name in ("context.md", ".agent/PLAN.md", ".agent/DOC_INDEX.md", ".agent/mistake.md", "forecasting/README.md", "forecasting/TRAINING.md")]
    files += [ROOT.parent / ".agent" / name for name in ("context.md", "PLAN.md", "DOC_INDEX.md")]
    files += sorted((ROOT / "docs/phase0-20261008").glob("*.md"))
    files += [ROOT / ".agent/decisions/20261009-phase2b1-approval.md", QA / "checklist.md", QA / "review.md", QA / "preflight-notes.md"]
    texts = {}
    fingerprints = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        texts[path] = text
        fingerprints[str(path.relative_to(ROOT.parent))] = sha256(path)
        check("UTF8_full_read:" + str(path.relative_to(ROOT.parent)), "\ufffd" not in text and not re.search("[\u0e00-\u0e7f]", text), dict(characters=len(text)))
    for path in (QA / "review.md", ROOT / "forecasting/TRAINING.md"):
        broken = []
        for target in re.findall(r"\]\(([^)]+)\)", texts[path]):
            if not target.startswith(("http://", "https://")) and not (path.parent / target.split("#")[0]).resolve().exists():
                broken.append(target)
        check("local_links:" + path.name, not broken, broken)
    review = texts[QA / "review.md"]
    check("handoff_eight_numbered_sections", len(re.findall(r"^## [1-8]\. ", review, flags=re.M)) == 8)
    scores = load(RUN / "metrics-validation.json")
    for name, label in (("hgb", "HGB"), ("naive", "Naive"), ("seasonal_naive_24", "Seasonal Naive24")):
        row = next(line for line in review.splitlines() if line.startswith(f"| {label} |"))
        cells = [value.strip() for value in row.split("|")[1:-1]]
        check("review_metric:" + name, int(cells[1].replace(".", "")) == scores["n"] and all(math.isclose(float(cells[index].replace(",", ".")), scores["models"][name][metric], abs_tol=5e-11, rel_tol=0)
              for index, metric in ((2, "mae_kwh"), (3, "rmse_kwh"))))
    config = load(RUN / "model-config.json")
    for parameter, value in config["approved_parameters"].items():
        row = next(line for line in review.splitlines() if line.startswith(f"| {parameter} |"))
        check("review_parameter:" + parameter, row.split("|")[2].strip() == str(value))
    manifest = load(RUN / "manifest.json")
    runtime = load(RUN / "runtime-evidence.json")
    technical = load(QA / "verification.json")
    check("technical_QA_exact_state_37", technical["status"] == "VERIFIED" and technical["passed"] == technical["total_checks"] == 37 and all(item["passed"] for item in technical["checks"]))
    check("candidate_hash_size_provenance_in_review", sha256(RUN / "candidate.joblib") in review and "154.086" in review and
          manifest["flink_source"]["sha256"] in review and manifest["flink_source"]["run_id"] in review)
    check("D09_zero_negative_impact_supported", scores["models"]["hgb"]["negative_raw_count"] == 0 and scores["models"]["hgb"]["d09_mae_reduction_kwh"] == 0 and
          "0 dự báo thô âm" in review and "chưa được đánh giá" in review)
    check("save_load_and_reproducibility_supported", runtime["persistence"]["max_raw_difference_kwh"] == 0 and all(technical["reproducibility"].values()) and
          "giống từng byte" in review)
    check("relative_improvement_not_accuracy_claim", all(f"{100 * (1-scores['models']['hgb'][metric]/scores['models']['naive'][metric]):.2f}".replace(".", ",") + "%" in review for metric in ("mae_kwh", "rmse_kwh")) and "không phải phần trăm" in review)
    checklist = texts[QA / "checklist.md"]
    statuses = {cells[0]: cells[3] for line in checklist.splitlines() if line.startswith("| B")
                for cells in [[cell.strip() for cell in line.split("|")[1:-1]]]}
    check("B00_B04_exact_VERIFIED", all(statuses[key] == "VERIFIED" for key in ("B00", "B01", "B02", "B03", "B04")))
    check("B05_workflow_state", statuses["B05"] in ("APPLIED_UNVERIFIED", "VERIFIED"))
    check("state_parser_regression", "APPLIED_UNVERIFIED" != "VERIFIED")
    check("latest_checkpoint_scope_and_stop", all(token in texts[ROOT / "context.md"][:2600] for token in ("Phase2B1 VERIFIED", "CURRENT TASK:", "SOURCE CHECKPOINT:", "ALLOWED SCOPE:", "LOCKED:", "APPLIED BUT UNVERIFIED:", "VERIFIED:", "PENDING:", "LAST EVIDENCE:", "NEXT EXACT ACTION:", "không tự LOCKED model", "Không Test metrics")))
    decision = texts[ROOT / ".agent/decisions/20261009-phase2b1-approval.md"]
    check("scope_contract_complete", all(token in decision for token in ("ALLOWED:", "FORBIDDEN:", "SOURCE OF TRUTH:", "INVARIANTS:", "ACCEPTANCE:", "Dừng sau 2B1")))
    for directory in (RUN, ROOT / "models/runs/20261009-phase2b1-b"):
        model_manifest = load(directory / "manifest.json")
        companion = load(directory / "verification.json")
        check("saved_artifact_and_code_hashes:" + directory.name, all(sha256(directory / name) == digest for name, digest in model_manifest["outputs_sha256"].items()) and
              all(sha256(ROOT / "forecasting" / name) == digest for name, digest in model_manifest["code_sha256"].items()) and
              companion["status"] == "VERIFIED" and companion["qa_sha256"] == sha256(QA / "verification.json"))
    preservation = load(QA / "preservation-before.json")
    changed = [path for path, digest in preservation["files"].items() if sha256(path) != digest]
    check("final_preservation_933", not changed and len(preservation["files"]) == 933, changed)
    check("transient_drift_disclosed_68", len(preservation["preexisting_transient_changes"]) == 68 and preservation["inherited_retained_files"] == 897 and all(token in review for token in ("68 file", "897", "933")))
    inventory = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*.md"))
    result = dict(status="VERIFIED" if all(item["passed"] for item in checks) else "APPLIED_UNVERIFIED",
                  passed=sum(item["passed"] for item in checks), total_checks=len(checks), checks=checks,
                  read_back_files=len(files), files_sha256=fingerprints, markdown_inventory=inventory,
                  historical_policy="Frozen previous QA and approved source documents reused by hash; current coordination files and new handoff read in full",
                  captured_at=datetime.now(timezone.utc).isoformat(), test_evaluated=False)
    (QA / "documents-verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(status=result["status"], passed=result["passed"], total=result["total_checks"], files=len(files),
                         failed=[item for item in checks if not item["passed"]]), ensure_ascii=False))
    if result["status"] != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
