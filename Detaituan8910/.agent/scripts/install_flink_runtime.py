import hashlib
import json
import os
import re
import shutil
import subprocess
import tarfile
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

ROOT = Path('/mnt/d/Hoctap/bigdata/Detaituan8910')
QA = ROOT / '.agent/qa/phase1-smoke-20261009'
TARGET = Path.home() / '.local/opt/flink-2.3.0'
BASE = 'https://downloads.apache.org/flink/flink-2.3.0/'
NAME = 'flink-2.3.0-bin-scala_2.12.tgz'
DOWNLOAD = QA / 'downloads'
DOWNLOAD.mkdir(parents=True, exist_ok=True)

def digest(path):
    result = hashlib.sha512()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            result.update(block)
    return result.hexdigest()

def fetch(url, path):
    if path.exists():
        return
    with urlopen(url, timeout=90) as response, path.open('xb') as output:
        shutil.copyfileobj(response, output, 1048576)

fetch(BASE + NAME + '.sha512', DOWNLOAD / (NAME + '.sha512'))
expected = re.search(r'\b[0-9a-fA-F]{128}\b', (DOWNLOAD / (NAME + '.sha512')).read_text()).group(0).lower()
fetch(BASE + NAME, DOWNLOAD / NAME)
actual = digest(DOWNLOAD / NAME)
assert actual == expected, 'Flink SHA512 mismatch'
if not TARGET.exists():
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(DOWNLOAD / NAME) as archive:
        members = archive.getmembers()
        for member in members:
            resolved = (TARGET.parent / member.name).resolve()
            assert resolved.is_relative_to(TARGET.resolve()), member.name
        archive.extractall(TARGET.parent, filter='data')
assert (TARGET / 'bin/sql-client.sh').is_file()
manifest = {
    'captured_at': datetime.now().astimezone().isoformat(),
    'source_url': BASE + NAME,
    'checksum_url': BASE + NAME + '.sha512',
    'sha512_expected': expected,
    'sha512_actual': actual,
    'checksum_match': actual == expected,
    'archive_bytes': (DOWNLOAD / NAME).stat().st_size,
    'runtime_path': str(TARGET),
    'runtime_file_bytes': sum(p.stat().st_size for p in TARGET.rglob('*') if p.is_file()),
    'uid': os.getuid(),
    'java': subprocess.run(['java', '-version'], capture_output=True, text=True).stderr if shutil.which('java') else None,
    'flink_installed_without_root': os.getuid() != 0,
}
(QA / 'runtime-install.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2), flush=True)
