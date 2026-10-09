import hashlib
import importlib.metadata
import json
import platform
import socket
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase3-20261009"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    final = ROOT / "models/final/hgb-uci-hourly-v1.0-train-only"
    fm = read(final / "manifest.json")
    qa2 = read(ROOT / ".agent/qa/phase2b2-20261009/verification.json")
    assert fm["status"] == "LOCKED" and qa2["status"] == "VERIFIED" and qa2["passed"] == qa2["total_checks"] == 51
    assert sha(final / "model.joblib") == fm["model_sha256"] == "f4c33c54b026a3c81312dff9c9623c7dad33a3f9df4986ecd8693b7267d8749c"
    assert sha(final / "manifest.json") == qa2["final_manifest_sha256"]
    ml = ROOT / "data/ml/runs/20261009-phase2a-a"
    assert sha(ml / "manifest.json") == fm["source_phase2a_manifest_sha256"]
    assert all(sha(ml / p) == value for p, value in fm["source_phase2a_outputs"].items())
    hourly = ROOT / fm["flink_source"]["path"]
    assert sha(hourly) == fm["flink_source"]["sha256"]
    assert read(hourly.parent / "verification.json")["status"] == "VERIFIED"
    assert len(fm["feature_columns"]) == 11 and fm["test_metrics"]["n"] == 4590
    assert all(importlib.metadata.version(p) == v for p, v in fm["packages"].items())
    with socket.socket() as sock:
        assert sock.connect_ex(("127.0.0.1", 8501)) != 0
    previous = read(ROOT / ".agent/qa/phase2b2-20261009/preservation-before.json")
    frozen = {}
    missing_runtime = []
    for p, expected in previous["files"].items():
        path = Path(p)
        actual = sha(path) if path.is_file() else None
        if actual != expected:
            if "/flink-tmp/" not in p:
                raise ValueError("Source drift: " + p)
            missing_runtime.append(p)
        else:
            frozen[p] = expected
    for folder in ("models/final", "models/runs/20261009-phase2b2-a", ".agent/qa/phase2b2-20261009", "forecasting"):
        for p in (ROOT / folder).rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts:
                frozen[str(p)] = sha(p)
    record = dict(status="VERIFIED", captured_at=datetime.now(timezone.utc).isoformat(), files=frozen, count=len(frozen),
                  packages_before={d.metadata["Name"]:d.version for d in importlib.metadata.distributions()},
                  pinned_ML=fm["packages"], python=platform.python_version(), port8501_available=True,
                  source_gate=True, runtime_exceptions=missing_runtime, inherited_9_runtime=previous["current_runtime_exceptions"])
    with (QA / "preflight.json").open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(dict(status="VERIFIED", frozen_files=len(frozen), python=record["python"], source_gate=True, port8501_available=True)))


if __name__ == "__main__":
    main()
