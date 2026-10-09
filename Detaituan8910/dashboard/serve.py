import json
import os
import socket
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
with socket.socket() as probe:
    if probe.connect_ex(("127.0.0.1", 8501)) == 0:
        raise SystemExit("Port8501 already in use; do not kill the other service")
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2", MKL_NUM_THREADS="2")
command = [sys.executable, "-B", "-m", "streamlit", "run", str(ROOT / "dashboard/app.py"),
           "--server.address=127.0.0.1", "--server.port=8501", "--server.headless=true", "--browser.gatherUsageStats=false"]
print(json.dumps(dict(url="http://localhost:8501", bind="127.0.0.1", command=command)), flush=True)
raise SystemExit(subprocess.call(command, cwd=ROOT / "dashboard", env=env))
