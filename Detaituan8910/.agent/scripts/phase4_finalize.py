import ast
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/phase4-app-20261009'
sys.path.insert(0, str(ROOT / 'dashboard'))
import data_service as d

names = ['technical-verification.json', 'integration-faults.json', 'stop-app.json', 'app-off.json', 'app-recovered.json', 'stop-flink.json', 'flink-off.json', 'final.json', 'windows-runtime.json', 'browser-verification.json']
checks = []
reports = {name: d.read_json(QA / name) for name in names}
for name, report in reports.items():
    if report['status'] != 'VERIFIED' or report['passed'] != report['total_checks']:
        raise SystemExit('Unverified source: ' + name)
    checks.extend(dict(item, evidence=name) for item in report['checks'])


def check(name, passed, details=None):
    checks.append(dict(name=name, passed=bool(passed), evidence='handoff gate', details=details))
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)


preflight = d.read_json(QA / 'preflight.json')
changed, missing = [], []
for path, expected in preflight['files'].items():
    if not Path(path).is_file():
        missing.append(path)
    elif d.sha256(path) != expected:
        changed.append(path)
preservation = dict(status='VERIFIED' if not changed and not missing else 'FAIL', total=len(preflight['files']), matching=len(preflight['files'])-len(changed)-len(missing), changed=changed, missing=missing, excluded=preflight['excluded'], mutable_coordinators=preflight['mutable_coordinators'], scope='Raw ZIP/TXT, prior project source/artifacts/QA and Office/PDF; runtime cache/log/PID and permitted coordinators excluded')
check('final_1571_frozen_files', not changed and not missing and preservation['total'] == 1571, preservation)
shots = {}
for name in reports['browser-verification.json']['screenshots']:
    with Image.open(QA / 'screenshots' / name) as picture:
        expected = (1366, 768) if 'laptop' in name else (1920, 1080)
        shots[name] = dict(size=list(picture.size), sha256=d.sha256(QA / 'screenshots' / name), expected=list(expected))
check('eight_screenshots_dimensions_and_visual_readback', len(shots) == 8 and all(item['size'] == item['expected'] for item in shots.values()), shots)
future = {QA / name for name in ['verification.json', 'preservation.json', 'package-verification.json']}
bad_links = []
docs = [QA / 'review.md', ROOT / 'operations/README.md', ROOT.parent / 'README.md', ROOT.parent / 'HANDOFF_FOR_GPT_WEB.md']
for path in docs:
    text = path.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)', text):
        if not target.startswith(('https:', 'http:', '#')):
            resolved = (path.parent / target.split('#')[0]).resolve()
            if not resolved.exists() and resolved not in future:
                bad_links.append(dict(document=str(path), target=target))
check('new_handoff_links_resolve', not bad_links, bad_links)
full = d.read_json(ROOT / d.HOURLY / 'manifest.json')
full_support = ROOT / '.agent/qa/phase1-full-20261009/runs/20261009T102201900234-full'
job = d.read_json(full_support / ('job-' + full['jobs'][0]['jid'] + '-details.json'))
check('archived_job_and_actual_full_sql', d.sha256(full_support / 'job.sql') == full['sql_sha256'] and job['state'] == 'FINISHED', dict(job=job['jid'], mode=full['mode'], sql_sha256=full['sql_sha256']))
check('final_locked_sourcegate_21', len(d.source_signature()) == 21)
trees = [ast.parse(path.read_text(encoding='utf-8')) for path in (ROOT / 'operations').glob('*.py')]
check('new_operations_syntax_no_training', all(not any(isinstance(node, ast.Attribute) and node.attr in ('fit', 'fit_transform', 'partial_fit') for node in ast.walk(tree)) for tree in trees))
scope = (ROOT / '.agent/decisions/20261009-phase4-app-scope.md').read_text()
check('I04_deferred_no_runbook_created', 'I04 DEFERRED' in scope and not any('demo_runbook' in str(path).lower() for path in QA.rglob('*')))
public_preflight = dict(at=preflight['at'], frozen_count=preflight['frozen_count'], git_commit=preflight['git_commit'], flink_before=preflight['flink_before']['overview'], excluded=preflight['excluded'], cold_wsl_boot=preflight['cold_wsl_boot'], I04='DEFERRED', private_preflight='Full host process/network inventory retained locally; not included')
for name, value in [('preflight-public.json', public_preflight), ('preservation.json', preservation)]:
    with (QA / name).open('x', encoding='utf-8') as output:
        json.dump(value, output, ensure_ascii=False, indent=2)
report = dict(status='VERIFIED' if all(c['passed'] for c in checks) else 'FAIL', overall_phase4='INCOMPLETE', I04='DEFERRED', acceptance='PENDING Thy/GPT Web', at=datetime.now(timezone.utc).isoformat(), scope='I01 artifact integration; I02 service restart only; I03 application; I05 handoff gate; no full pipeline rerun/training/Test evaluation', passed=sum(c['passed'] for c in checks), total_checks=len(checks), functional_assertions=sum(r['total_checks'] for r in reports.values()), checks=checks, selected_evidence={name:d.sha256(QA/name) for name in names}, screenshots=shots, excluded_failed_attempt='flink-recovered.json retained as history; superseded by final.json and windows-runtime.json', limits=['Cold WSL/Windows boot not tested','No autostart','Archived Flink job history expired in live REST','No full end-to-end reexecution this turn','No streaming/direct meter/Word/PPT/I04'], no_fit_witness=reports['technical-verification.json']['witness'])
with (QA / 'verification.json').open('x', encoding='utf-8') as output:
    json.dump(report, output, ensure_ascii=False, indent=2)
print(json.dumps(dict(status=report['status'], passed=report['passed'], total=report['total_checks'], functional=report['functional_assertions'])))
sys.exit(0 if report['status'] == 'VERIFIED' else 1)
