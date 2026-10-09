import importlib.metadata
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase3-20261009"
before = json.loads((QA / "preflight.json").read_text())
plan = json.loads((QA / "install-plan.json").read_text())
normalize = lambda name: name.lower().replace("_", "-")
old = {normalize(name):value for name, value in before["packages_before"].items()}
proposed = {normalize(item["metadata"]["name"]):item["metadata"]["version"] for item in plan["install"]}
assert all(name not in old or old[name] == version for name, version in proposed.items()), "Install would alter existing packages"
assert proposed["streamlit"] == "1.50.0" and proposed["plotly"] == "6.3.0"
constraints = QA / "install-lock.txt"
with constraints.open("x") as handle:
    handle.write("\n".join(name+"=="+version for name, version in sorted(proposed.items()))+"\n")
command = [sys.executable, "-B", "-m", "pip", "install", "--constraint", str(ROOT / "forecasting/requirements.txt"),
           "--constraint", str(constraints), "--requirement", str(ROOT / "dashboard/requirements.txt"),
           "--report", str(QA / "pip-install-report.json")]
result = subprocess.run(command, text=True, capture_output=True, timeout=240)
with (QA / "install.log").open("x") as handle:
    handle.write(result.stdout+"\n"+result.stderr)
assert result.returncode == 0, result.stderr
after = {d.metadata["Name"]:d.version for d in importlib.metadata.distributions()}
normal_after = {normalize(name):value for name, value in after.items()}
assert all(normal_after.get(name) == version for name, version in old.items())
assert all(importlib.metadata.version(name) == version for name, version in before["pinned_ML"].items())
compatibility = subprocess.run([sys.executable, "-B", "-m", "pip", "check"], text=True, capture_output=True)
assert compatibility.returncode == 0, compatibility.stdout+compatibility.stderr
with (QA / "install-report.json").open("x") as handle:
    json.dump(dict(status="VERIFIED", captured_at=datetime.now(timezone.utc).isoformat(), added=proposed,
                   packages_after=after, existing_packages_unchanged=True, ML_pins_unchanged=True,
                   pip_check=compatibility.stdout.strip(), command=command), handle, indent=2)
print(json.dumps(dict(status="VERIFIED", added=len(proposed), streamlit="1.50.0", plotly="6.3.0", ML_pins_unchanged=True)))
