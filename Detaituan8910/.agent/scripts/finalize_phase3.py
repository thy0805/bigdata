import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase3-20261009"
sys.path.insert(0, str(ROOT / "dashboard"))
import data_service as d

checks = []


def check(name, passed):
    checks.append(dict(name=name, passed=bool(passed)))
    print(("PASS " if passed else "FAIL ")+name, flush=True)


previous = d.read_json(QA / "verification.json")
check("combined96_unchanged", previous["status"] == "VERIFIED" and previous["passed"] == previous["total_checks"] == 96)
check("U00_U05_VERIFIED_readback", len(re.findall(r"\| U0[0-5] \|.*\| VERIFIED \|", (QA / "checklist.md").read_text(encoding="utf-8"))) == 6)
current = (ROOT / "context.md").read_text(encoding="utf-8").split("Các block dưới")[0]
check("recovery_block_and_approval_boundary", "Phase3 VERIFIED kỹ thuật" in current and "không còn trong U00–U05" in current and "Thy/GPT Web nghiệm thu3" in current and "không Phase4" in current)
review = (QA / "review.md").read_text(encoding="utf-8")
check("final_handoff_96_and_scope", "96/96" in review and "Phase3_Dashboard_Handoff_20261009_FINAL.zip" in review and "chưa LOCKED" in review)
check("source_gate_readback", dict(d.source_signature()) == previous["source_signature"])
check("app_files_unchanged_after_tests", all(d.sha256(ROOT / path) == value for path, value in previous["app_sha256"].items()))
frozen = d.read_json(QA / "preflight.json")["files"]
check("source976_after_doc_updates", len(frozen) == 976 and all(Path(path).is_file() and d.sha256(path) == value for path, value in frozen.items()))
if not all(item["passed"] for item in checks):
    raise SystemExit("Readback FAIL")
selected = [ROOT / path for path in d.read_json(QA / "bundle-manifest.json")["files"]]
selected += [ROOT / "context.md", ROOT / ".agent/PLAN.md", ROOT / ".agent/DOC_INDEX.md", ROOT / ".agent/mistake.md"]
selected += list((ROOT / "docs/phase0-20261008").glob("*.md"))
selected += [Path(__file__)]
selected = sorted(set(selected))
manifest = dict(status="VERIFIED", kind="final review bundle not portable", time=datetime.now(timezone.utc).isoformat(),
                acceptance="Thy/GPT Web PENDING", checks=checks, files={str(path.relative_to(ROOT)):d.sha256(path) for path in selected},
                promoted_screenshots=d.read_json(QA / "browser-verification.json")["screenshots"])
manifest_path = QA / "bundle-manifest-final.json"
with manifest_path.open("x", encoding="utf-8") as stream:
    json.dump(manifest, stream, ensure_ascii=False, indent=2)
archive = QA / "Phase3_Dashboard_Handoff_20261009_FINAL.zip"
with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
    for path in selected + [manifest_path]:
        bundle.write(path, str(path.relative_to(ROOT)))
with zipfile.ZipFile(archive) as bundle:
    check("zip_integrity", bundle.testzip() is None)
    check("all_packaged_entry_hashes", all(hashlib.sha256(bundle.read(path)).hexdigest() == value for path, value in manifest["files"].items()))
    check("model_packaged_expected_hash", hashlib.sha256(bundle.read(d.MODEL+"/model.joblib")).hexdigest() == d.MODEL_SHA)
report = dict(status="VERIFIED" if all(item["passed"] for item in checks) else "FAIL", passed=sum(item["passed"] for item in checks), total_checks=len(checks), checks=checks,
              archive=str(archive.relative_to(ROOT)), archive_sha256=d.sha256(archive), archive_bytes=archive.stat().st_size,
              files=len(selected)+1, source_preservation=976, app_qa=96, acceptance="PENDING", next_phase_authorized=False)
with (QA / "final-package-verification.json").open("x", encoding="utf-8") as stream:
    json.dump(report, stream, ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False), flush=True)
