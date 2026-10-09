import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(r'D:\Hoctap\bigdata\Detaituan8910')
QA = ROOT / '.agent/qa/phase1-smoke-20261009'

def linux(args):
    result = subprocess.run(['wsl', '-d', 'Ubuntu-24.04', '--', *args], capture_output=True, timeout=60)
    return {'command': args, 'exit_code': result.returncode, 'stdout': result.stdout.decode('utf-8', errors='replace'), 'stderr': result.stderr.decode('utf-8', errors='replace')}

commands = [linux(['java', '-version']), linux(['python3', '--version']), linux(['dpkg-query', '-W', 'openjdk-17-jdk-headless', 'python3.12-venv']), linux(['/home/cute/.local/opt/flink-2.3.0/bin/flink', '--version'])]
venv = '/home/cute/.local/share/uci-flink-qa/venv'
commands.append(linux(['python3', '-m', 'venv', venv]))
commands.append(linux([venv + '/bin/python', '-m', 'pip', '--version']))
with urlopen('http://localhost:8081/', timeout=10) as response:
    html = response.read().decode('utf-8')
    ui_status = response.status
(QA / 'windows-web-ui.html').write_text(html, encoding='utf-8')
with urlopen('http://localhost:8081/overview', timeout=10) as response:
    overview = json.load(response)
with urlopen('http://localhost:8081/taskmanagers', timeout=10) as response:
    managers = json.load(response)
result = {'captured_at': datetime.now().astimezone().isoformat(), 'commands': commands, 'venv_on_linux_fs': venv, 'ui_http_status': ui_status, 'html_has_flink': 'Apache Flink' in html, 'overview_windows': overview, 'taskmanagers_windows': managers, 'disk_preinstall_bytes_free': {'C': 30785843200, 'D': 225280733184}, 'disk_now': {drive: shutil.disk_usage(drive + ':/')._asdict() for drive in ('C', 'D')}, 'source_preservation': {}, 'notes': ['Linux venv on D had ensurepip error; final probe uses Linux filesystem', 'Observed Windows volume delta also includes background Windows activity', 'REST listens inside WSL NAT on 0.0.0.0; no Windows portproxy/firewall changes']}
manifest = json.loads((QA / 'inputs-manifest.json').read_text(encoding='utf-8'))
for path, expected in manifest['source_hashes_before'].items():
    with Path(path).open('rb') as stream:
        value = hashlib.file_digest(stream, 'sha256').hexdigest()
    result['source_preservation'][path] = value == expected
if 'disk_before' in manifest:
    manifest['disk_after_preparation'] = manifest.pop('disk_before')
    (QA / 'inputs-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
result['passed'] = all(item['exit_code'] == 0 for item in commands) and ui_status == 200 and result['html_has_flink'] and overview['flink-version'] == '2.3.0' and overview['slots-total'] == 2 and len(managers['taskmanagers']) == 1 and all(result['source_preservation'].values())
(QA / 'environment-final.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result['passed'] else 1)
