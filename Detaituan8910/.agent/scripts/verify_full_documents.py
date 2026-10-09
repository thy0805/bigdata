import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'pipeline'))
from run_full import digest, save

QA = ROOT / '.agent/qa/phase1-full-20261009'
handoff = json.loads((QA / 'handoff-verification.json').read_text())
checks = []
def check(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})
check('handoff_all_checks_pass', handoff['status'] == 'VERIFIED' and all(c['passed'] for c in handoff['checks']))
for path, expected in handoff['support_sha256'].items():
    check('support_hash_preserved:' + path, digest(ROOT / path) == expected)
files = [ROOT / 'context.md', ROOT / '.agent/PLAN.md', ROOT / '.agent/DOC_INDEX.md', ROOT / '.agent/mistake.md', ROOT / 'pipeline/README.md', QA / 'checklist.md', QA / 'review.md', ROOT / '.agent/decisions/20261009-flink-full-approval.md', *sorted((ROOT / 'docs/phase0-20261008').glob('*.md')), *[ROOT.parent / '.agent' / name for name in ('context.md', 'PLAN.md', 'DOC_INDEX.md')]]
read_back = []
for path in files:
    content = path.read_text(encoding='utf-8')
    check('markdown_utf8:' + str(path.relative_to(ROOT.parent)), '\ufffd' not in content and content.startswith('#'))
    read_back.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    for link in re.findall(r'\]\(([^)]+)\)', content):
        if not re.match(r'^(https?://|#|[A-Za-z]:)', link):
            target = link.split('#')[0]
            if target:
                check('local_link:' + path.name + ':' + link, (path.parent / target).exists())
review = (QA / 'review.md').read_text()
for run, checksum in zip(handoff['run_ids'], handoff['hourly_grid_sha256']):
    manifest = json.loads((QA / 'runs' / run / 'manifest.json').read_text())
    verification = json.loads((QA / 'runs' / run / 'verification.json').read_text())
    check('review_has_real_run_and_job:' + run, run in review and manifest['jobs'][0]['jid'] in review)
    check('final_csv_hash_and_schema:' + run, checksum in review and digest(ROOT / 'data/processed/runs' / run / 'hourly-grid.csv') == checksum)
    check('oracle_coverage_semantics:' + run, verification['audit']['rows'] == manifest['metrics']['data_rows'] and verification['audit']['hours'] == manifest['hourly_grid_rows'] and verification['status'] == 'VERIFIED')
check('review_preserves_acceptance_gate', 'Giai đoạn 2 chưa được duyệt' in review and 'PENDING' in review)
check('no_missing_pending_labeled_complete', 'Giới hạn chưa kiểm' in review and 'checkpoint recovery' in review and 'không phải service' in review)
result = {'captured_at': datetime.now().astimezone().isoformat(), 'status': 'VERIFIED' if all(c['passed'] for c in checks) else 'APPLIED_UNVERIFIED', 'passed': sum(c['passed'] for c in checks), 'total_checks': len(checks), 'read_back': read_back, 'checks': checks, 'scope': 'Read-back all16 current/relevant Markdown; historical QA kept unchanged. Source artifacts separately verified in both full-run verification reports. No Word/render/model/UI performed.'}
save(QA / 'documents-verification.json', result)
print(json.dumps({'status': result['status'], 'passed': result['passed'], 'total_checks': result['total_checks'], 'failed': [c for c in checks if not c['passed']]}, indent=2), flush=True)
raise SystemExit(0 if result['status'] == 'VERIFIED' else 2)
