import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/phase4-app-20261009'
GIT = ['git', '-c', 'safe.directory=' + ROOT.parent.as_posix(), '-C', str(ROOT.parent)]
head = subprocess.check_output(GIT + ['rev-parse', 'HEAD']).decode().strip()
remote = subprocess.check_output(GIT + ['ls-remote', 'origin', 'refs/heads/main']).decode().split()[0]
checks = [dict(name='remote_main_matches_HEAD', passed=head == remote, commit=head)]
paths = ['README.md', 'HANDOFF_FOR_GPT_WEB.md', 'Detaituan8910/.agent/qa/phase4-app-20261009/review.md', 'Detaituan8910/.agent/qa/phase4-app-20261009/verification.json', 'Detaituan8910/.agent/qa/phase4-app-20261009/preservation.json', 'Detaituan8910/.agent/qa/phase4-app-20261009/package-verification.json', 'Detaituan8910/operations/services.py', 'Detaituan8910/.agent/qa/phase4-app-20261009/screenshots/forecast-1920.jpg']
paths.extend(['Detaituan8910/context.md'] + ['Detaituan8910/.agent/qa/phase4-resume-20261010/' + name for name in ['review.md', 'checklist.md', 'resume-verification.json', 'windows-verification.json']])
for path in paths:
    with urlopen('https://raw.githubusercontent.com/thy0805/bigdata/' + head + '/' + path, timeout=20) as response:
        actual = response.read()
    expected = subprocess.check_output(GIT + ['show', head + ':' + path])
    checks.append(dict(name='raw_remote_readback:' + path, passed=actual == expected, sha256=hashlib.sha256(actual).hexdigest(), bytes=len(actual)))
report = dict(status='VERIFIED' if all(c['passed'] for c in checks) else 'FAIL', commit=head, remote=remote, captured_at=datetime.now(timezone.utc).isoformat(), checks=checks, passed=sum(c['passed'] for c in checks), total_checks=len(checks), overall_phase4='INCOMPLETE', I04='DEFERRED')
with (QA / sys.argv[1]).open('x', encoding='utf-8') as output:
    json.dump(report, output, ensure_ascii=False, indent=2)
print(json.dumps(dict(status=report['status'], commit=head, passed=report['passed'], total=report['total_checks'])))
sys.exit(0 if report['status'] == 'VERIFIED' else 1)
