import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/phase4-data-guide-20261010'
GIT = ['git', '-c', 'safe.directory=' + ROOT.parent.as_posix(), '-C', str(ROOT.parent)]
checks = []


def check(name, passed, details=None):
    checks.append(dict(name=name, passed=bool(passed), details=details))


def digest(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


technical = json.loads((QA / 'technical-verification.json').read_text(encoding='utf-8'))
browser = json.loads((QA / 'browser-verification.json').read_text(encoding='utf-8'))
check('technical_75', technical['status'] == 'VERIFIED' and technical['passed'] == technical['total_checks'] == 75)
check('browser_7', browser['status'] == 'VERIFIED' and browser['passed'] == browser['total_checks'] == 7)
frozen = json.loads((ROOT / '.agent/qa/phase4-app-20261009/preflight.json').read_text(encoding='utf-8'))['files'].copy()
frozen.pop(str(ROOT / 'dashboard/app.py'))
changed = [path for path, expected in frozen.items() if not Path(path).is_file() or digest(Path(path)) != expected]
check('protected_snapshot_1570', len(frozen) == 1570 and not changed, dict(total=len(frozen), changed=changed))
for relative, expected in technical['source_signature'].items():
    check('source:' + relative, digest(ROOT / relative) == expected)
for shot in browser['screenshots']:
    check('screenshot:' + shot['path'], digest(QA / shot['path']) == shot['sha256'])
old_app = subprocess.check_output(GIT + ['show', '2da758a:Detaituan8910/dashboard/app.py']).decode('utf-8')
new_app = (ROOT / 'dashboard/app.py').read_text(encoding='utf-8')
check('expander_only_diff', old_app.split('with st.expander("Nguồn dữ liệu, model và giới hạn"):')[0] == new_app.split('with st.expander("Tìm hiểu bộ dữ liệu và cách AI dự báo", expanded=False):')[0] and old_app.split('st.markdown(\'<div class="footer-note">')[1] == new_app.split('st.markdown(\'<div class="footer-note">')[1])
for name in ('checklist.md', 'review.md'):
    content = (QA / name).read_text(encoding='utf-8')
    check('readback:' + name, '\ufffd' not in content and 'DEFERRED' in content)
report = dict(status='VERIFIED' if all(c['passed'] for c in checks) else 'FAIL', at=datetime.now(timezone.utc).isoformat(), checks=checks, passed=sum(c['passed'] for c in checks), total_checks=len(checks), overall_phase4='INCOMPLETE', user_acceptance='PENDING', I04='DEFERRED')
if len(sys.argv) > 1 and sys.argv[1] == 'remote':
    head = subprocess.check_output(GIT + ['rev-parse', 'HEAD']).decode().strip()
    remote = subprocess.check_output(GIT + ['ls-remote', 'origin', 'refs/heads/main']).decode().split()[0]
    check('remote_main_matches_HEAD', head == remote, head)
    paths = subprocess.check_output(GIT + ['diff', '--name-only', '2da758a', head]).decode().splitlines()
    for path in paths:
        with urlopen('https://raw.githubusercontent.com/thy0805/bigdata/' + head + '/' + path, timeout=30) as response:
            actual = response.read()
        expected = subprocess.check_output(GIT + ['show', head + ':' + path])
        check('remote_readback:' + path, actual == expected, dict(sha256=hashlib.sha256(actual).hexdigest(), bytes=len(actual)))
    report.update(status='VERIFIED' if all(c['passed'] for c in checks) else 'FAIL', passed=sum(c['passed'] for c in checks), total_checks=len(checks), commit=head, remote=remote)
    output = QA / 'publication-receipt.json'
else:
    output = QA / 'handoff-verification.json'
with output.open('x', encoding='utf-8') as stream:
    json.dump(report, stream, ensure_ascii=False, indent=2)
print(json.dumps({key: report[key] for key in ('status', 'passed', 'total_checks')}, ensure_ascii=False))
raise SystemExit(0 if report['status'] == 'VERIFIED' else 1)
