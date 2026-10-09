import ast
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/github-publication-20261009'
GIT = ['git', '-c', 'safe.directory=' + ROOT.as_posix(), '-C', str(ROOT)]
source = (ROOT / '.agent/scripts/prepare_github_publication.py').read_text(encoding='utf-8')
tree = ast.parse(source)
patterns = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == 'patterns' for target in node.targets))
checks = []
files = []
errors = []
entries = subprocess.check_output(GIT + ['ls-files', '--stage', '-z']).decode().split('\0')
for entry in filter(None, entries):
    metadata, relative = entry.split('\t', 1)
    mode, oid, stage = metadata.split()
    blob = subprocess.check_output(GIT + ['cat-file', 'blob', oid])
    actual = (ROOT / relative).read_bytes()
    identical = blob == actual
    if not identical:
        errors.append({'path': relative, 'reason': 'index_differs_from_disk'})
    if stage != '0' or len(blob) > 8 * 1024 * 1024:
        errors.append({'path': relative, 'reason': 'stage_or_size'})
    if Path(relative).suffix.lower() in {'.docx', '.pptx', '.pdf', '.zip', '.rar', '.7z', '.log', '.pid', '.pyc'}:
        errors.append({'path': relative, 'reason': 'forbidden_extension'})
    if '/data/raw/' in relative or '/flink-tmp/' in relative or '/attempts/' in relative:
        errors.append({'path': relative, 'reason': 'forbidden_path'})
    if Path(relative).suffix.lower() not in {'.jpg', '.png', '.joblib'}:
        text = blob.decode('utf-8', errors='replace')
        for reason, pattern in patterns.items():
            for match in re.finditer(pattern, text):
                errors.append({'path': relative, 'reason': reason, 'line': text.count('\n', 0, match.start()) + 1})
    files.append({'path': relative, 'sha256': hashlib.sha256(blob).hexdigest(), 'bytes': len(blob), 'index_matches_disk': identical})
required = ['README.md', 'Detaituan8910/dashboard/app.py', 'Detaituan8910/pipeline/hourly.sql',
            'Detaituan8910/forecasting/predictor.py', 'Detaituan8910/.agent/qa/phase3-20261009/review.md',
            'Detaituan8910/models/final/hgb-uci-hourly-v1.0-train-only/model.joblib',
            'Detaituan8910/data/ml/runs/20261009-phase2a-a/holdout/test.csv']
names = {item['path'] for item in files}
checks.append({'name': 'required_code_and_evidence', 'passed': all(path in names for path in required)})
checks.append({'name': 'accepted_screenshots8', 'passed': sum(path.startswith('Detaituan8910/.agent/qa/phase3-20261009/screenshots/') for path in names) == 8})
checks.append({'name': 'all_index_blobs_equal_disk', 'passed': all(item['index_matches_disk'] for item in files)})
checks.append({'name': 'scope_size_secret_patterns', 'passed': not errors})
report = {'at': datetime.now(timezone.utc).isoformat(), 'status': 'PASS' if all(item['passed'] for item in checks) else 'FAIL',
          'count': len(files), 'bytes': sum(item['bytes'] for item in files), 'checks': checks, 'findings': errors, 'files': files,
          'source_gate': 'Separate live dashboard source_signature PASS21 checked before publication; no train/evaluation executed.',
          'phase4': 'AUTHORIZED_NOT_COMPLETED',
          'limits': 'Pattern scan is not a guarantee against every possible secret. No raw/runtime/Office files are published.'}
output = QA / sys.argv[1]
with output.open('x', encoding='utf-8') as target:
    json.dump(report, target, ensure_ascii=False, indent=2)
print(json.dumps({key: report[key] for key in ('status', 'count', 'bytes', 'checks', 'findings')}, ensure_ascii=False))
raise SystemExit(0 if report['status'] == 'PASS' else 1)
