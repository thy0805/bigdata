import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/phase4-app-20261009'
read = lambda path: json.loads(path.read_text(encoding='utf-8'))
sha = lambda value: hashlib.sha256(value).hexdigest()
verification = read(QA / 'verification.json')
preservation = read(QA / 'preservation.json')
assert verification['status'] == preservation['status'] == 'VERIFIED'
assert verification['passed'] == verification['total_checks'] == 126 and preservation['matching'] == preservation['total'] == 1571
assert 'I04 DEFERRED' in (ROOT / 'context.md').read_text()
assert '| I05 | VERIFIED' in (QA / 'review.md').read_text()
files = [path for path in QA.iterdir() if path.suffix in ('.md', '.json') and path.name not in ('preflight.json', 'package-verification.json', 'remote-readback.json')]
files.extend(QA / 'screenshots' / name for name in read(QA / 'browser-verification.json')['screenshots'])
files.extend(path for directory in ('dashboard', 'operations') for path in (ROOT / directory).rglob('*') if path.is_file() and '__pycache__' not in path.parts)
files.extend(ROOT / name for name in ('context.md', '.agent/PLAN.md', '.agent/DOC_INDEX.md', '.agent/decisions/20261009-phase4-app-scope.md'))
files.extend((ROOT / '.agent/scripts').glob('*phase4*.py'))
files.extend((ROOT / '.agent/scripts').glob('phase4_windows.ps1'))
files = sorted(set(files))
data = {path.relative_to(ROOT).as_posix():path.read_bytes() for path in files}
assert not any('/fixtures/' in name or '/runtime/' in name or name.endswith('/preflight.json') or Path(name).suffix in ('.docx', '.pptx', '.zip') for name in data)
manifest = dict(scope='Phase4 application QA only; not portable installer; I04 deferred', files={name:sha(blob) for name, blob in data.items()}, source_git_before_phase4=read(QA / 'preflight-public.json')['git_commit'])
archive = QA / 'Phase4_App_QA_20261009.zip'
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as package:
    for name, blob in data.items():
        package.writestr(name, blob)
    package.writestr('PACKAGE_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))
with zipfile.ZipFile(archive) as package:
    inner = json.loads(package.read('PACKAGE_MANIFEST.json'))
    matching = all(sha(package.read(name)) == expected for name, expected in inner['files'].items())
    names = set(package.namelist()) == set(data) | {'PACKAGE_MANIFEST.json'}
report = dict(status='VERIFIED' if matching and names else 'FAIL', archive=archive.name, bytes=archive.stat().st_size, sha256=sha(archive.read_bytes()), files=len(data), zip_entries=len(data)+1, all_hashes_match=matching, exact_entries=names, overall_phase4='INCOMPLETE', I04='DEFERRED', no_office_raw_runtime_private_preflight=True, included_hashes=inner['files'])
with (QA / 'package-verification.json').open('x', encoding='utf-8') as output:
    json.dump(report, output, ensure_ascii=False, indent=2)
print(json.dumps({key:report[key] for key in ('status','files','zip_entries','bytes','sha256')}))
sys.exit(0 if report['status'] == 'VERIFIED' else 1)
