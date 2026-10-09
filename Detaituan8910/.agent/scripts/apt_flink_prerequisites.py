import json
import subprocess
from datetime import datetime
from pathlib import Path

QA = Path('/mnt/d/Hoctap/bigdata/Detaituan8910/.agent/qa/phase1-smoke-20261009')
commands = [
    ['apt-get', 'update'],
    ['apt-get', '-s', 'install', '--no-install-recommends', 'openjdk-17-jdk-headless', 'python3.12-venv'],
    ['apt-get', 'install', '-y', '--no-install-recommends', 'openjdk-17-jdk-headless', 'python3.12-venv'],
]
history = []
for index, command in enumerate(commands):
    log = QA / f'apt-{index}.log'
    print(f'Executing package stage {index}', flush=True)
    with log.open('w', encoding='utf-8') as output:
        process = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT, env={'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'DEBIAN_FRONTEND': 'noninteractive', 'NEEDRESTART_MODE': 'l'})
    history.append({'command': command, 'exit_code': process.returncode, 'log': str(log)})
    (QA / 'apt-install.json').write_text(json.dumps({'captured_at': datetime.now().astimezone().isoformat(), 'commands': history}, indent=2), encoding='utf-8')
    print(log.read_text(encoding='utf-8')[-1800:], flush=True)
    if process.returncode:
        raise SystemExit(process.returncode)
