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
QA = ROOT / 'Detaituan8910/.agent/qa/word-w011-20261010'
GIT = ['git', '-c', 'safe.directory=' + ROOT.as_posix(), '-C', str(ROOT)]
OUTPUT = ROOT / 'Detaituan8910/BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx'
EXPECTED = 'fafe4d7485601ba667a468990c1c80e188bf0e7126dd3edaf51059dfca3e2006'
PUBLIC = ['artifact.md', 'checklist.md', 'attempt-history.md', 'preflight.json', 'applied.json',
          'changes.json', 'CHANGES.md', 'field-probe.json', 'final-verification.json', 'font-audit.json',
          'manifest.json', 'page-review.md', 'page-diff.json', 'preservation.json', 'review.md',
          'verification-attempt1.json', 'preservation-attempt1.json', 'verification.json',
          'visual-verification.json', 'word-summary.json']
COORDINATION = ['.agent/context.md', '.agent/PLAN.md', '.agent/DOC_INDEX.md', 'HANDOFF_FOR_GPT_WEB.md',
                'Detaituan8910/context.md', 'Detaituan8910/.agent/PLAN.md',
                'Detaituan8910/.agent/DOC_INDEX.md', 'Detaituan8910/.agent/mistake.md',
                'Detaituan8910/.agent/decisions/20261010-word-w011-scope.md']
SCRIPTS = ['edit_word_w011.py', 'verify_word_w011.py', 'handoff_word_w011.py', 'publish_word_w011.py']
ALLOW = COORDINATION + ['Detaituan8910/.agent/scripts/' + name for name in SCRIPTS]
ALLOW += ['Detaituan8910/.agent/qa/word-w011-20261010/' + name for name in PUBLIC]
INDEX_PATH = 'Detaituan8910/.agent/qa/word-w011-20261010/publication-index.json'
ALLOW.append(INDEX_PATH)


def git(*args):
    return subprocess.check_output(GIT + list(args))


def save(name, value):
    (QA / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


assert hashlib.sha256(OUTPUT.read_bytes()).hexdigest() == EXPECTED
assert hashlib.sha256((ROOT / '.agent/rule.md').read_bytes()).hexdigest() == 'f7ab6d5a18a4f8f2ea56360e7190476d65300399c519122adfc37866bdd848c3'
mode = sys.argv[1]
if mode == 'prepare':
    existing = [p for p in git('diff', '--cached', '--name-only', '-z').decode().split('\0') if p]
    assert not existing, f'Unexpected staged paths: {existing}'
    for path in ALLOW:
        if path != INDEX_PATH:
            subprocess.run(GIT + ['add', '-f', '--', path], check=True)
    source = (ROOT / '.agent/scripts/prepare_github_publication.py').read_text(encoding='utf-8')
    parsed = ast.parse(source)
    patterns = next(ast.literal_eval(node.value) for node in parsed.body if isinstance(node, ast.Assign)
                    and any(isinstance(target, ast.Name) and target.id == 'patterns' for target in node.targets))
    paths = [p for p in git('diff', '--cached', '--name-only', '-z').decode().split('\0') if p]
    findings = []
    files = []
    for path in paths:
        payload = git('show', ':' + path)
        if path not in ALLOW or (ROOT / path).read_bytes() != payload or len(payload) > 8 * 1024 * 1024:
            findings.append({'path': path, 'reason': 'scope_size_or_index_mismatch'})
        if Path(path).suffix.lower() not in ('.md', '.json', '.py', '.ps1'):
            findings.append({'path': path, 'reason': 'forbidden_extension'})
        content = payload.decode('utf-8')
        for reason, pattern in patterns.items():
            for match in re.finditer(pattern, content):
                findings.append({'path': path, 'reason': reason, 'line': content.count('\n', 0, match.start()) + 1})
        files.append({'path': path, 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()})
    report = {'status': 'PASS' if not findings else 'FAIL', 'at': datetime.now(timezone.utc).isoformat(),
              'scope': 'Only new W01.1 evidence/helpers and current coordination. Dirty root rule excluded.',
              'files': files, 'count': len(files), 'findings': findings,
              'limits': 'Pattern scan is not a guarantee against every secret. Office/render/fulltext/probe copies excluded.'}
    save('publication-index.json', report)
    assert not findings, findings
    subprocess.run(GIT + ['add', '-f', '--', INDEX_PATH], check=True)
    print(json.dumps({key: report[key] for key in ('status', 'count', 'findings')}, ensure_ascii=False))
elif mode == 'remote':
    head = git('rev-parse', 'HEAD').decode().strip()
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    assert head == remote
    paths = [p for p in ALLOW if subprocess.run(GIT + ['cat-file', '-e', head + ':' + p], capture_output=True).returncode == 0]

    def check(path):
        request = Request('https://raw.githubusercontent.com/thy0805/bigdata/' + head + '/' + path,
                          headers={'User-Agent': 'W011-publication-check'})
        with urlopen(request, timeout=25) as response:
            payload = response.read()
        expected = git('show', head + ':' + path)
        return {'path': path, 'status': 'PASS' if payload == expected else 'FAIL',
                'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)}

    with ThreadPoolExecutor(max_workers=4) as pool:
        checks = list(pool.map(check, paths))
    report = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
              'at': datetime.now(timezone.utc).isoformat(), 'commit': head, 'remote_main': remote,
              'checks': checks, 'readback_count': len(checks), 'output_sha256': EXPECTED,
              'office_published': False, 'acceptance': 'PENDING_THY_GPT_WEB'}
    save('publication-receipt.local.json', report)
    assert report['status'] == 'PASS'
    assert hashlib.sha256(OUTPUT.read_bytes()).hexdigest() == EXPECTED
    print(json.dumps({key: report[key] for key in ('status', 'commit', 'readback_count', 'office_published')}, ensure_ascii=False))
else:
    raise SystemExit('Expected prepare or remote')
