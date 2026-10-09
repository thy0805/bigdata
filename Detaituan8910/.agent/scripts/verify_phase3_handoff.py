import ast
import importlib.metadata
import json
import re
import subprocess
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase3-20261009"
sys.path.insert(0, str(ROOT / "dashboard"))
import data_service as d

checks = []


def check(name, passed, detail=None):
    checks.append(dict(name=name, passed=bool(passed), details=detail))
    print(("PASS " if passed else "FAIL ")+name, flush=True)


technical = d.read_json(QA / "technical-verification-v3.json")
browser = d.read_json(QA / "browser-verification.json")
installed = d.read_json(QA / "install-report.json")
check("technical67_and_browser10", technical["status"] == browser["status"] == "VERIFIED" and technical["passed"] == technical["total_checks"] == 67 and len(browser["checks"]) == 10 and all(row["passed"] for row in browser["checks"]))
check("UI_versions_and_ML_pins", installed["status"] == "VERIFIED" and len(installed["added"]) == 32 and all(importlib.metadata.version(name) == version for name, version in installed["added"].items()))
pip = subprocess.run([sys.executable, "-m", "pip", "check"], capture_output=True, text=True)
check("pip_check_final", pip.returncode == 0, pip.stdout.strip())
gate = d.source_signature()
check("source_gate_final", len(gate) == 21)
health = urllib.request.urlopen("http://127.0.0.1:8501/_stcore/health", timeout=5)
check("linux_health", health.status == 200 and health.read().decode() == "ok")
windows = subprocess.run(["powershell.exe", "-NoProfile", "-Command", "Invoke-WebRequest -Uri http://localhost:8501/_stcore/health -UseBasicParsing -TimeoutSec 8 | Select-Object StatusCode,Content | ConvertTo-Json -Compress"], capture_output=True, text=True, timeout=15)
windows_health = json.loads(windows.stdout.strip()) if windows.returncode == 0 else {}
check("windows_localhost_health", windows_health.get("StatusCode") == 200 and windows_health.get("Content") == "ok", windows_health)
listeners = subprocess.run(["ss", "-ltnp", "sport", "=", ":8501"], capture_output=True, text=True)
check("loopback_only_bind", "127.0.0.1:8501" in listeners.stdout and "0.0.0.0:8501" not in listeners.stdout and "[::]:8501" not in listeners.stdout, listeners.stdout.strip())
collision = subprocess.run([sys.executable, "-B", str(ROOT / "dashboard/serve.py")], capture_output=True, text=True, timeout=5)
check("launcher_refuses_busy_port", collision.returncode != 0 and "already in use" in collision.stderr+collision.stdout)

selected_screens = browser["screenshots"]
check("eight_promoted_screenshots", len(selected_screens) == len(set(selected_screens)) == 8)
dimensions = {}
for name in selected_screens:
    path = QA / "screenshots" / name
    with Image.open(path) as shot:
        dimensions[name] = shot.size
        shot.verify()
check("screenshots_dimensions", all(width >= 1200 and height >= 650 for width, height in dimensions.values()), dimensions)
check("1920_screens_present", dimensions["overview-1920.jpg"] == dimensions["analysis-1920-final-v3.jpg"] == dimensions["forecast-1920-final.jpg"] == (1920, 1080))

docs = [ROOT / "dashboard/README.md", QA / "review.md", QA / "checklist.md", QA / "BUNDLE_README.md",
        ROOT / "context.md", ROOT / ".agent/PLAN.md", ROOT / ".agent/DOC_INDEX.md", ROOT / ".agent/mistake.md"]
docs.extend((ROOT / "docs/phase0-20261008").glob("*.md"))
missing_links = []
for doc in docs:
    content = doc.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)]+)\)", content):
        if "://" not in target and not target.startswith("#"):
            destination = (doc.parent / target.split("#")[0]).resolve()
            if not destination.exists():
                missing_links.append(dict(doc=str(doc), target=target))
check("local_doc_links", not missing_links, missing_links)
review = (QA / "review.md").read_text(encoding="utf-8")
check("nine_handoff_sections", len(re.findall(r"^## [1-9]\. ", review, re.M)) == 9)
check("review_metric_exact_artifacts", all(str(value) in review for model in d.read_json(ROOT / d.RUN / "metrics-test.json")["models"].values() for key, value in model.items() if key in ("mae_kwh", "rmse_kwh")))
check("review_counts_and_limits", all(value in review for value in ("67/67", "10/10", "976/976", "4.590", "không fit", "chưa LOCKED", "Không bắt đầu Phase4")))
current_context = (ROOT / "context.md").read_text(encoding="utf-8").split("Các block dưới")[0]
check("current_context_phase3", "Phase3" in current_context and "không Phase4" in current_context)
check("canonical_checklist_statuses", len(re.findall(r"\| U0[0-4] \|.*\| VERIFIED \|", (QA / "checklist.md").read_text(encoding="utf-8"))) == 5)
for source in (ROOT / "dashboard").glob("*.py"):
    ast.parse(source.read_text(encoding="utf-8"))
check("app_source_parse_final", True)
frozen = d.read_json(QA / "preflight.json")["files"]
drift = [path for path, value in frozen.items() if not Path(path).is_file() or d.sha256(path) != value]
check("final_frozen976_preservation", len(frozen) == 976 and not drift, drift)

runtime = dict(captured_at=datetime.now(timezone.utc).isoformat(), windows_health=windows_health,
               linux_bind=listeners.stdout.strip(), url="http://localhost:8501", launch_session=35813,
               foreground_not_service=True, historical_flink_not_live=True, launcher_collision_refused=True)
with (QA / "runtime-evidence.json").open("x", encoding="utf-8") as stream:
    json.dump(runtime, stream, ensure_ascii=False, indent=2)
new_sources = {str(path.relative_to(ROOT)):d.sha256(path) for path in (ROOT / "dashboard").rglob("*") if path.is_file()}
doc_report = dict(status="VERIFIED" if all(row["passed"] for row in checks) else "FAIL",
                  passed=sum(row["passed"] for row in checks), total_checks=len(checks), checks=checks,
                  app_sha256=new_sources, documents_read=[str(path.relative_to(ROOT)) for path in docs])
with (QA / "documents-verification.json").open("x", encoding="utf-8") as stream:
    json.dump(doc_report, stream, ensure_ascii=False, indent=2)
combined = [dict(row, phase="technical") for row in technical["checks"]]
combined += [dict(row, phase="browser") for row in browser["checks"]]
combined += [dict(row, phase="handoff") for row in checks]
report = dict(status="VERIFIED" if all(row["passed"] for row in combined) else "FAIL",
              captured_at=runtime["captured_at"], total_checks=len(combined), passed=sum(row["passed"] for row in combined),
              checks=combined, technical_checks=67, browser_checks=10, handoff_checks=len(checks),
              model_sha256=d.MODEL_SHA, source_signature=dict(gate), app_sha256=new_sources,
              preservation=dict(total=976, matching=976-len(drift), drift=drift), screenshots=dimensions,
              fit_calls=technical["witness"]["fit_calls"], acceptance="Thy/GPT Web PENDING", next_phase_authorized=False)
with (QA / "verification.json").open("x", encoding="utf-8") as stream:
    json.dump(report, stream, ensure_ascii=False, indent=2)
if report["status"] != "VERIFIED":
    raise SystemExit("Handoff FAIL; do not package")

paths = [ROOT / relative for relative in new_sources]
paths += [QA / name for name in ("review.md", "BUNDLE_README.md", "checklist.md", "preflight.json", "install-report.json", "install-lock.txt", "pip-install-report.json", "technical-verification-v3.json", "browser-verification.json", "runtime-evidence.json", "documents-verification.json", "verification.json")]
paths += [QA / "screenshots" / name for name in selected_screens]
paths += [ROOT / d.MODEL / name for name in ("model.joblib", "manifest.json")]
paths += [ROOT / d.HOURLY / name for name in ("hourly-grid.csv", "manifest.json", "verification.json")]
paths += [ROOT / d.ML / name for name in ("feature-schema.json", "holdout/test.csv")]
paths += [ROOT / d.RUN / name for name in ("predictions-test.csv", "metrics-test.json", "manifest.json", "verification.json")]
paths += [ROOT / "forecasting" / name for name in ("predictor.py", "requirements.txt")]
paths += [Path(__file__), ROOT / ".agent/scripts/verify_phase3.py", ROOT / ".agent/decisions/20261009-phase3-approval.md"]
bundle_manifest = dict(kind="review bundle not standalone app", status="VERIFIED", files={str(path.relative_to(ROOT)):d.sha256(path) for path in paths})
with (QA / "bundle-manifest.json").open("x", encoding="utf-8") as stream:
    json.dump(bundle_manifest, stream, ensure_ascii=False, indent=2)
archive = QA / "Phase3_Dashboard_Handoff_20261009.zip"
with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle_zip:
    for path in paths + [QA / "bundle-manifest.json"]:
        bundle_zip.write(path, str(path.relative_to(ROOT)))
with zipfile.ZipFile(archive) as bundle_zip:
    assert bundle_zip.testzip() is None
    import hashlib
    assert all(hashlib.sha256(bundle_zip.read(name)).hexdigest() == value for name, value in bundle_manifest["files"].items())
package_report = dict(status="VERIFIED", archive=str(archive.relative_to(ROOT)), archive_sha256=d.sha256(archive), files=len(paths)+1, all_entry_hashes_match=True)
with (QA / "package-verification.json").open("x", encoding="utf-8") as stream:
    json.dump(package_report, stream, ensure_ascii=False, indent=2)
print(json.dumps(dict(status=report["status"], passed=report["passed"], total=report["total_checks"], package=package_report)), flush=True)
