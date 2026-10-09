import argparse
import json
import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
QA = ROOT / '.agent/qa/phase1-smoke-20261009'
FLINK = Path.home() / '.local/opt/flink-2.3.0'

def environment():
    result = os.environ.copy()
    result.update(JAVA_HOME='/usr/lib/jvm/java-17-openjdk-amd64', FLINK_CONF_DIR=str(ROOT / 'pipeline/flink-conf'), FLINK_LOG_DIR=str(QA / 'flink-logs'), FLINK_PID_DIR=str(QA / 'flink-pids'))
    for name in ('flink-logs', 'flink-pids', 'flink-tmp'):
        (QA / name).mkdir(exist_ok=True)
    for source in (FLINK / 'conf').glob('log*.properties'):
        target = ROOT / 'pipeline/flink-conf' / source.name
        if not target.exists():
            shutil.copyfile(source, target)
    return result

def fetch(path):
    with urlopen('http://127.0.0.1:8081' + path, timeout=5) as response:
        return json.load(response)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start', 'serve', 'stop', 'status'])
    args = parser.parse_args()
    env = environment()
    if args.action in ('start', 'serve', 'stop'):
        if args.action in ('start', 'serve'):
            try:
                existing = fetch('/overview')
            except Exception:
                existing = None
            if existing:
                raise SystemExit('Port8081 already serves a cluster; verify ownership before starting')
        operation = 'start' if args.action == 'serve' else args.action
        result = subprocess.run([str(FLINK / f'bin/{operation}-cluster.sh')], env=env, capture_output=True, text=True)
        (QA / f'cluster-{args.action}.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        print(result.stdout + result.stderr, flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)
    if args.action != 'stop':
        for attempt in range(40):
            try:
                overview, managers = fetch('/overview'), fetch('/taskmanagers')
                if overview['slots-total'] == 2 and len(managers['taskmanagers']) == 1:
                    break
            except Exception:
                pass
            time.sleep(1)
        else:
            raise SystemExit('Cluster did not become ready with one TaskManager/two slots')
        result = {'captured_at': datetime.now().astimezone().isoformat(), 'overview': overview, 'taskmanagers': managers, 'environment': {k: env[k] for k in ('JAVA_HOME', 'FLINK_CONF_DIR', 'FLINK_LOG_DIR', 'FLINK_PID_DIR')}}
        (QA / 'cluster-state.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result, indent=2))
    if args.action == 'serve':
        print('Cluster holder active; stop with cluster.py stop, no WSL restart needed', flush=True)
        while True:
            time.sleep(5)
            try:
                fetch('/overview')
            except Exception:
                break
