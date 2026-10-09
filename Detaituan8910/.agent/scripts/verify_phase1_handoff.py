import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(r'D:\Hoctap\bigdata\Detaituan8910')
QA = ROOT / '.agent/qa/phase1-smoke-20261009'
checks = []

def check(name, passed, evidence):
    checks.append({'name': name, 'passed': bool(passed), 'evidence': evidence})

def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

smoke = json.loads((QA / 'smoke-verification.json').read_text(encoding='utf-8'))
environment = json.loads((QA / 'environment-final.json').read_text(encoding='utf-8'))
install = json.loads((QA / 'runtime-install.json').read_text(encoding='utf-8'))
inputs = json.loads((QA / 'inputs-manifest.json').read_text(encoding='utf-8'))
check('runtime-and-independent-checks', smoke['passed'] == smoke['total'] == 82 and all(item['passed'] for item in smoke['checks']), smoke['status'])
check('installation-and-linux-venv', environment['passed'] and install['checksum_match'] and all(item['exit_code'] == 0 for item in environment['commands']), 'Java17/venv/Flink2.3 SHA512')
sql_hash = digest(ROOT / 'pipeline/hourly.sql')
check('all-final-runs-same-current-template', len(smoke['runs']) == 11 and all(item['template_sha256'] == sql_hash for item in smoke['runs']), sql_hash)
for item in smoke['runs']:
    mapped = ROOT / Path(item['run_dir']).relative_to('/mnt/d/Hoctap/bigdata/Detaituan8910')
    check('run-evidence/' + item['label'], (mapped / 'manifest.json').exists() and (mapped / 'sql-client.log').exists() and all((mapped / ('job-' + job['jid'] + '-details.json')).exists() for job in item['jobs']), item['run_dir'])
for source, expected in inputs['source_hashes_before'].items():
    check('unchanged/' + Path(source).name, digest(source) == expected, expected)
check('raw-still-exact', digest(ROOT / 'data/raw/household_power_consumption.txt') == inputs['raw_sha256'], inputs['raw_sha256'])
for path in [ROOT / 'pipeline/cluster.py', ROOT / 'pipeline/run_smoke.py', ROOT / '.agent/scripts/verify_phase1_smoke.py', ROOT / '.agent/scripts/check_phase1_environment.py']:
    compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    check('syntax/' + path.name, True, digest(path))
documents = ['context.md', '.agent/PLAN.md', '.agent/DOC_INDEX.md', '.agent/qa/phase1-smoke-20261009/checklist.md', '.agent/qa/phase1-smoke-20261009/review.md', 'pipeline/README.md', 'docs/phase0-20261008/IMPLEMENTATION_PLAN.md', 'docs/phase0-20261008/OPEN_DECISIONS.md']
for name in documents:
    text = (ROOT / name).read_text(encoding='utf-8')
    check('readback/' + name, bool(text.strip()) and 'F05' in text, digest(ROOT / name))
decisions = (ROOT / 'docs/phase0-20261008/OPEN_DECISIONS.md').read_text(encoding='utf-8')
decision_rows = [line for line in decisions.splitlines() if any(line.startswith('| D0' + str(index) + ' |') for index in range(1, 6))]
check('D01-D05-locked-and-next-gate-kept', len(decision_rows) == 5 and all('LOCKED' in line for line in decision_rows) and 'F05/F06' in decisions, decision_rows)
with urlopen('http://localhost:8081/overview', timeout=10) as response:
    state = json.load(response)
check('cluster-live-at-handoff', state['taskmanagers'] == 1 and state['slots-total'] == 2 and state['jobs-running'] == 0 and state['flink-version'] == '2.3.0', state)
result = {'captured_at': datetime.now().astimezone().isoformat(), 'passed': sum(item['passed'] for item in checks), 'total': len(checks), 'checks': checks, 'disk_now': {drive: shutil.disk_usage(drive + ':/')._asdict() for drive in ('C', 'D')}, 'scope': 'F01-F04 only; F05/F06 await approval', 'source_preservation_verified': True}
(QA / 'handoff-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({key: result[key] for key in ('captured_at', 'passed', 'total', 'disk_now')}, indent=2))
raise SystemExit(0 if result['passed'] == result['total'] else 1)
