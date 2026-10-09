import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/github-publication-20261009'
GIT = ['git', '-c', 'safe.directory=' + ROOT.as_posix(), '-C', str(ROOT)]
patterns = {
    'github_token': r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})',
    'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'aws_key': r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    'openai_key': r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{25,}\b',
    'url_password': r'https?://[^\s/:]+:[^\s/@]+@',
    'literal_credential': r'''(?i)\b(?:password|passwd|api_key|access_token|secret_key)\s*[:=]\s*["'][A-Za-z0-9_+/.=-]{8,}["']''',
    'bare_password': r'(?im)^\s*(?:pass(?:word)?|mật khẩu)\s*[:=]\s*[A-Za-z0-9@!#$%_+-]*\d[A-Za-z0-9@!#$%_+-]{5,}\s*$',
}
paths = subprocess.check_output(GIT + ['ls-files', '--others', '--exclude-standard', '-z']).decode().split('\0')
inventory = []
findings = []
for relative in sorted(filter(None, paths)):
    path = ROOT / relative
    content = path.read_bytes()
    if len(content) > 8 * 1024 * 1024:
        findings.append({'path': relative, 'reason': 'oversize'})
    if path.suffix.lower() in {'.docx', '.pptx', '.pdf', '.zip', '.rar', '.7z', '.log', '.pid', '.pyc'}:
        findings.append({'path': relative, 'reason': 'forbidden_extension'})
    if path.suffix.lower() not in {'.jpg', '.png', '.joblib'}:
        text = content.decode('utf-8', errors='replace')
        for reason, pattern in patterns.items():
            for match in re.finditer(pattern, text):
                findings.append({'path': relative, 'reason': reason, 'line': text.count('\n', 0, match.start()) + 1})
    inventory.append({'path': relative, 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()})
report = {'at': datetime.now(timezone.utc).isoformat(), 'status': 'PASS' if not findings else 'FAIL',
          'repository': 'https://github.com/thy0805/bigdata', 'files': inventory,
          'count': len(inventory), 'bytes': sum(row['bytes'] for row in inventory), 'findings': findings,
          'limits': 'Pattern scan cannot prove absence of all secrets; publication uses an allowlist and excludes runtime/personal archives.'}
QA.mkdir(parents=True, exist_ok=True)
with (QA / 'inventory.json').open('x', encoding='utf-8') as target:
    json.dump(report, target, ensure_ascii=False, indent=2)
print(json.dumps({key: report[key] for key in ('status', 'count', 'bytes', 'findings')}, ensure_ascii=False))
raise SystemExit(0 if not findings else 1)
