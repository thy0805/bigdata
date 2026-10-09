import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
GIT = ['git', '-c', 'safe.directory=' + ROOT.as_posix(), '-C', str(ROOT)]
head = subprocess.check_output(GIT + ['rev-parse', 'HEAD']).decode().strip()
remote = subprocess.check_output(GIT + ['ls-remote', 'origin', 'refs/heads/main']).decode().split()[0]
paths = ['README.md', 'Detaituan8910/dashboard/app.py',
         'Detaituan8910/.agent/qa/phase3-20261009/review.md',
         'Detaituan8910/models/runs/20261009-phase2b2-a/metrics-test.json']
if (ROOT / 'HANDOFF_FOR_GPT_WEB.md').exists() and subprocess.run(GIT + ['cat-file', '-e', head + ':HANDOFF_FOR_GPT_WEB.md'], capture_output=True).returncode == 0:
    paths.append('HANDOFF_FOR_GPT_WEB.md')
checks = [{'name': 'remote_main_equals_local_HEAD', 'passed': head == remote}]
for relative in paths:
    request = Request('https://raw.githubusercontent.com/thy0805/bigdata/' + head + '/' + relative,
                      headers={'User-Agent': 'BigData-publication-verifier'})
    with urlopen(request, timeout=30) as response:
        payload = response.read()
    expected = subprocess.check_output(GIT + ['cat-file', 'blob', head + ':' + relative])
    checks.append({'name': 'remote_readback:' + relative, 'passed': payload == expected,
                   'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)})
report = {'at': datetime.now(timezone.utc).isoformat(), 'status': 'PASS' if all(row['passed'] for row in checks) else 'FAIL',
          'repository': 'https://github.com/thy0805/bigdata', 'commit': head, 'remote_main': remote, 'checks': checks}
with (ROOT / '.agent/qa/github-publication-20261009' / sys.argv[1]).open('x', encoding='utf-8') as target:
    json.dump(report, target, ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['status'] == 'PASS' else 1)
