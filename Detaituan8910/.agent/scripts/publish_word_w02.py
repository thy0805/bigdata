import ast
import hashlib
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[3]
QA = ROOT / 'Detaituan8910/.agent/qa/word-w021-20261010'
GIT = ['git', '-c', 'safe.directory=' + ROOT.as_posix(), '-C', str(ROOT)]
COORDINATION = ['.agent/context.md', '.agent/PLAN.md', '.agent/DOC_INDEX.md', 'HANDOFF_FOR_GPT_WEB.md', 'Detaituan8910/context.md', 'Detaituan8910/.agent/PLAN.md', 'Detaituan8910/.agent/DOC_INDEX.md', 'Detaituan8910/.agent/decisions/20261010-word-w02-w021-scope.md']
SCRIPTS = ['preflight_word_w02.py', 'build_word_w02.py', 'render_word_w02.py', 'verify_word_w02.py', 'build_word_w021.py', 'verify_word_w021.py', 'handoff_word_w02.py', 'publish_word_w02.py']
PUBLIC_W02 = ['checklist.md', 'changes.json', 'CHANGES.md', 'image-registry.json', 'image-registry-final.json', 'hourly-table-records.json', 'verification.json', 'verification-attempt1.json', 'attempt-history.md', 'final-verification.json', 'manifest.json', 'review.md', 'page-review.md']
PUBLIC_W021 = ['changes.json', 'verification.json', 'page-diff.json', 'page-review.md', 'renderer-diagnostic.md', 'image-registry-final.json', 'final-verification.json', 'manifest.json', 'review.md']
INDEX = 'Detaituan8910/.agent/qa/word-w021-20261010/publication-index.json'
ALLOW = COORDINATION + ['Detaituan8910/.agent/scripts/' + n for n in SCRIPTS] + ['Detaituan8910/.agent/qa/word-w02-20261010/' + n for n in PUBLIC_W02] + ['Detaituan8910/.agent/qa/word-w021-20261010/' + n for n in PUBLIC_W021] + [INDEX]
OPTIONAL = 'Detaituan8910/.agent/qa/word-w021-20261010/publication-initial.json'
if (ROOT / OPTIONAL).is_file():
    ALLOW.append(OPTIONAL)


def git(*args):
    return subprocess.check_output(GIT + list(args))


def save(name, value):
    (QA / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def check_artifacts():
    for folder in ('word-w02-20261010', 'word-w021-20261010'):
        gate = json.loads((ROOT / 'Detaituan8910/.agent/qa' / folder / 'final-verification.json').read_text(encoding='utf-8'))
        assert gate['status'] == 'VERIFIED' and hashlib.sha256(Path(gate['output']).read_bytes()).hexdigest() == gate['sha256']
        assert all(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest() == p['expected'] for p in gate['preservation'])
    assert hashlib.sha256((ROOT / '.agent/rule.md').read_bytes()).hexdigest() == 'f7ab6d5a18a4f8f2ea56360e7190476d65300399c519122adfc37866bdd848c3'


check_artifacts()
if sys.argv[1] == 'prepare':
    assert not git('diff', '--cached', '--name-only').strip(), 'Preserve unexpected existing staging'
    for path in ALLOW:
        if path != INDEX:
            subprocess.run(GIT + ['add', '-f', '--', path], check=True)
    parsed = ast.parse((ROOT / '.agent/scripts/prepare_github_publication.py').read_text(encoding='utf-8'))
    patterns = next(ast.literal_eval(n.value) for n in parsed.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'patterns' for t in n.targets))
    paths = list(filter(None, git('diff', '--cached', '--name-only', '-z').decode().split('\0')))
    findings, files = [], []
    for path in paths:
        payload = git('show', ':' + path)
        if path not in ALLOW or (ROOT / path).read_bytes() != payload or len(payload) > 8 * 1024 * 1024 or Path(path).suffix not in ('.md', '.json', '.py'):
            findings.append({'path': path, 'reason': 'scope_size_extension_or_index_mismatch'})
        content = payload.decode('utf-8')
        for reason, pattern in patterns.items():
            for match in re.finditer(pattern, content):
                findings.append({'path': path, 'reason': reason, 'line': content.count('\n', 0, match.start()) + 1})
        files.append({'path': path, 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()})
    report = {'status': 'PASS' if not findings else 'FAIL', 'at': datetime.now(timezone.utc).isoformat(), 'scope': 'W02/W02.1 evidence, helpers and coordination only; excludes dirty root rule/project mistake, Office, renders, full-text, source datasets and model', 'files': files, 'count': len(files), 'findings': findings, 'limits': 'Pattern scan is not a proof against all secrets; staged allowlist and bytes checked'}
    save('publication-index.json', report)
    assert not findings, findings
    subprocess.run(GIT + ['add', '-f', '--', INDEX], check=True)
    print(json.dumps({k: report[k] for k in ('status', 'count', 'findings')}))
elif sys.argv[1] == 'remote':
    head = git('rev-parse', 'HEAD').decode().strip()
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    assert head == remote

    def readback(path):
        with urlopen(Request('https://raw.githubusercontent.com/thy0805/bigdata/' + head + '/' + path, headers={'User-Agent': 'Word-W02-publication-check'}), timeout=30) as response:
            payload = response.read()
        return {'path': path, 'status': 'PASS' if payload == git('show', head + ':' + path) else 'FAIL', 'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)}

    with ThreadPoolExecutor(max_workers=4) as pool:
        checks = list(pool.map(readback, ALLOW))
    report = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL', 'at': datetime.now(timezone.utc).isoformat(), 'commit': head, 'remote_main': remote, 'readback_count': len(checks), 'checks': checks, 'office_published': False, 'acceptance': 'PENDING_THY_GPT_WEB'}
    save('publication-receipt.local.json', report)
    assert report['status'] == 'PASS'
    check_artifacts()
    print(json.dumps({k: report[k] for k in ('status', 'commit', 'readback_count', 'office_published')}))
else:
    raise SystemExit('Expected prepare or remote')
