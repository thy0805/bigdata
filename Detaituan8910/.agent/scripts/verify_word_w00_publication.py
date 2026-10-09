import hashlib
import json
import re
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = ROOT / 'Detaituan8910/.agent/qa/word-w00-20261010'


def git(*args):
    return subprocess.check_output(['git', '-c', 'safe.directory=D:/Hoctap/bigdata', *args], cwd=ROOT)


def sha(value):
    return hashlib.sha256(value).hexdigest()


files = [
    '.agent/context.md', '.agent/PLAN.md', '.agent/DOC_INDEX.md',
    'Detaituan8910/context.md', 'Detaituan8910/.agent/PLAN.md',
    'Detaituan8910/.agent/DOC_INDEX.md', 'HANDOFF_FOR_GPT_WEB.md',
    'Detaituan8910/.agent/decisions/20261010-word-w00-scope.md',
]
files += ['Detaituan8910/.agent/scripts/' + name for name in [
    'inspect_word_w00.py', 'preview_word_w00.ps1', 'contact_word_w00.py',
    'verify_word_w00.py', 'verify_word_w00_publication.py',
]]
files += ['Detaituan8910/.agent/qa/word-w00-20261010/' + name for name in [
    'checklist.md', 'W00_REVIEW.md', 'CHAPTER2_REVIEW.md', 'TABLE_FIGURE_PLAN.md',
    'DRAFTS_FOR_APPROVAL.md', 'SOURCES.md', 'evidence-map.json', 'verification.json',
]]
mode = 'remote' if __import__('sys').argv[1:] == ['remote'] else 'staged'
head = git('rev-parse', 'HEAD').decode().strip()
results = []
findings = []
for path in files:
    local = (ROOT / path).read_bytes()
    text = local.decode('utf-8-sig')
    patterns = [r'gh[pousr]_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{30,}',
                r'sk-[A-Za-z0-9_-]{30,}', r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----']
    if any(re.search(pattern, text) for pattern in patterns):
        findings.append(path)
    if mode == 'remote':
        url = f'https://raw.githubusercontent.com/thy0805/bigdata/{head}/{path}'
        request = urllib.request.Request(url, headers={'User-Agent': 'Word-W00-Readback'})
        with urllib.request.urlopen(request, timeout=30) as response:
            actual = response.read()
    else:
        actual = git('show', ':' + path)
    results.append(dict(path=path, sha256=sha(local), bytes=len(local), matched=sha(local) == sha(actual)))
checks = dict(all_blobs_match=all(item['matched'] for item in results), no_secret_patterns=not findings,
              existing_user_rule_unchanged=sha((ROOT / '.agent/rule.md').read_bytes()) == 'f7ab6d5a18a4f8f2ea56360e7190476d65300399c519122adfc37866bdd848c3')
if mode == 'staged':
    staged = git('diff', '--cached', '--name-only', '-z').decode().strip('\0').split('\0')
    checks['exact_publication_scope'] = set(staged) == set(files)
else:
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    checks['remote_head_matches'] = remote == head
report = dict(status='VERIFIED' if all(checks.values()) else 'APPLIED_UNVERIFIED',
              captured_at=datetime.now(timezone.utc).isoformat(), mode=mode, commit=head,
              files=results, checks=checks, findings=findings,
              excluded=['source DOCX', 'PDF/PNG previews', 'source dumps', 'user rule edit', 'raw dataset', 'credentials'])
name = 'publication-receipt.local.json' if mode == 'remote' else 'publication-staged.local.json'
(QA / name).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(status=report['status'], mode=mode, files=len(results), checks=checks, findings=findings)))
if not all(checks.values()):
    raise SystemExit(1)
