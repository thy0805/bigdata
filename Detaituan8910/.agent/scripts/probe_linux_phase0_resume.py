import glob
import importlib.metadata
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen

if '--http-probe' in sys.argv:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'phase0-wsl-localhost-ok')

        def log_message(self, *args):
            pass

    with HTTPServer(('127.0.0.1', 0), Handler) as server:
        server.timeout = 15
        print(json.dumps({'port': server.server_port}), flush=True)
        server.handle_request()
    sys.exit(0)

def run(args):
    try:
        value = subprocess.run(args, capture_output=True, text=True, timeout=12)
        return {'exit_code': value.returncode, 'stdout': value.stdout.strip(), 'stderr': value.stderr.strip()}
    except Exception as error:
        return {'error': str(error)}

def package(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None

def disk(path):
    usage = shutil.disk_usage(path)
    return {'total_bytes': usage.total, 'free_bytes': usage.free, 'used_bytes': usage.used}

paths = ['/mnt/d/Hoctap/bigdata/Detaituan8910', '/mnt/c/Users/thy/Downloads/individual+household+electric+power+consumption.zip']
report = {
    'platform': platform.platform(),
    'os_release': Path('/etc/os-release').read_text(),
    'identity': run(['id']),
    'python': sys.version,
    'python_executable': sys.executable,
    'modules': {name: importlib.util.find_spec(name) is not None for name in ['pip', 'venv', 'ensurepip', 'pyflink', 'pandas', 'numpy', 'sklearn', 'streamlit', 'plotly']},
    'packages': {name: package(name) for name in ['apache-flink', 'pandas', 'numpy', 'scikit-learn', 'streamlit', 'plotly']},
    'linux_packages': run(['dpkg-query', '-W', '-f=${Package} ${Version} ${Status}\n', 'openjdk*', 'python3-pip', 'python3-venv', 'python3.12-venv']),
    'java_home': os.environ.get('JAVA_HOME'),
    'java_linux_candidates': glob.glob('/usr/lib/jvm/*/bin/java') + glob.glob('/usr/bin/java') + glob.glob(str(Path.home() / '.local/*/bin/java')),
    'flink_candidates': glob.glob('/opt/*flink*') + glob.glob('/usr/local/*flink*') + glob.glob(str(Path.home() / '*flink*')) + glob.glob(str(Path.home() / '.local/*flink*')),
    'commands': {name: shutil.which(name) for name in ['java', 'flink', 'pip3', 'curl', 'wget', 'tar', 'unzip']},
    'memory': Path('/proc/meminfo').read_text().splitlines()[:8],
    'disk': {path: disk(path) for path in ['/', '/mnt/c', '/mnt/d']},
    'path_access': {path: {'exists': Path(path).exists(), 'readable': os.access(path, os.R_OK)} for path in paths},
    'listening': run(['ss', '-ltn']),
    'windows_interop': run(['/mnt/c/Windows/System32/cmd.exe', '/c', 'ver']),
}
try:
    with urlopen('https://pypi.org/pypi/apache-flink/2.3.0/json', timeout=12) as response:
        metadata = json.load(response)
        report['https_pypi'] = {'status': response.status, 'version': metadata['info']['version'], 'requires_python': metadata['info']['requires_python'], 'cp312_linux_wheels': [entry['filename'] for entry in metadata['urls'] if 'cp312' in entry['filename'] and ('manylinux' in entry['filename'] or 'linux' in entry['filename'])]}
except Exception as error:
    report['https_pypi'] = {'error': str(error)}
print(json.dumps(report, ensure_ascii=False, indent=2))
