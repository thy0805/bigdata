import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/phase4-app-20261009'
mutable = {'context.md', '.agent/PLAN.md', '.agent/DOC_INDEX.md', '.agent/mistake.md'}
excluded_parts = {'flink-tmp', 'flink-logs', 'flink-pids', '__pycache__'}

def sha(path):
    value = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()

files = {}
for path in ROOT.rglob('*'):
    if not path.is_file() or QA in path.parents or excluded_parts.intersection(path.parts):
        continue
    relative = path.relative_to(ROOT).as_posix()
    if relative not in mutable and path.suffix not in {'.log', '.pid', '.pyc'}:
        files[str(path)] = sha(path)
for path in ROOT.parent.rglob('*'):
    if path.is_file() and path.suffix.lower() in {'.docx', '.pptx', '.pdf'} and not path.name.startswith('~$'):
        files[str(path)] = sha(path)
zip_path = Path('/mnt/c/Users/thy/Downloads/individual+household+electric+power+consumption.zip')
files[str(zip_path)] = sha(zip_path)
rest = {}
for endpoint in ('overview', 'jobs/overview', 'taskmanagers'):
    try:
        with urlopen('http://127.0.0.1:8081/' + endpoint, timeout=5) as response:
            rest[endpoint] = json.load(response)
    except Exception as error:
        rest[endpoint] = {'error': str(error)}
report = {'at': datetime.now(timezone.utc).isoformat(), 'files': files, 'frozen_count': len(files),
          'git_commit': subprocess.check_output(['git', '-c', 'safe.directory=/mnt/d/Hoctap/bigdata', '-C', str(ROOT.parent), 'rev-parse', 'HEAD']).decode().strip(),
          'flink_before': rest, 'processes': subprocess.check_output(['ps', '-eo', 'pid,ppid,args']).decode(),
          'listeners': subprocess.check_output(['ss', '-ltnp']).decode(), 'ram': Path('/proc/meminfo').read_text(),
          'excluded': sorted(excluded_parts), 'mutable_coordinators': sorted(mutable),
          'cold_wsl_boot': 'NOT_TESTED: no shutdown/reboot authorized', 'I04': 'DEFERRED'}
with (QA / 'preflight.json').open('x', encoding='utf-8') as output:
    json.dump(report, output, ensure_ascii=False, indent=2)
print(json.dumps({'frozen_count': len(files), 'git_commit': report['git_commit'], 'flink_before': rest['overview']}, ensure_ascii=False))
