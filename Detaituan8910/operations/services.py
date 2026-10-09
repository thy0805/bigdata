import argparse
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.agent/qa/phase4-app-20261009/runtime'
FLINK = Path.home() / '.local/opt/flink-2.3.0'
PYTHON = Path.home() / '.local/share/uci-forecast/venv/bin/python'
JAVA = Path('/usr/lib/jvm/java-17-openjdk-amd64')
CLASSES = ('org.apache.flink.runtime.entrypoint.StandaloneSessionClusterEntrypoint', 'org.apache.flink.runtime.taskexecutor.TaskManagerRunner')


def occupied(port):
    for family, address in ((socket.AF_INET, '127.0.0.1'), (socket.AF_INET6, '::1')):
        with socket.socket(family) as probe:
            probe.settimeout(.5)
            if probe.connect_ex((address, port)) == 0:
                return True
    return False


def owned(service):
    result = []
    for proc in Path('/proc').iterdir():
        if not proc.name.isdecimal():
            continue
        try:
            args = proc.joinpath('cmdline').read_bytes().split(b'\0')
            args = [item.decode() for item in args if item]
            if proc.stat().st_uid != os.getuid():
                continue
            if service == 'app':
                valid = args[:5] == [str(PYTHON), '-B', '-m', 'streamlit', 'run'] and args[5:6] == [str(ROOT / 'dashboard/app.py')]
            else:
                configs = (str(ROOT / 'pipeline/flink-conf'), str(RUNTIME / 'conf'))
                valid = args[:1] == [str(JAVA / 'bin/java')] and any(item in args for item in CLASSES) and any(args[index:index+2] == ['--configDir', path] for path in configs for index in range(len(args)-1))
            if valid:
                result.append((int(proc.name), args))
        except (OSError, UnicodeError):
            continue
    return result


def fetch(endpoint):
    with urlopen('http://127.0.0.1:8081/' + endpoint, timeout=3) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('service', choices=['app', 'flink'])
    parser.add_argument('action', choices=['start', 'stop', 'status'])
    args = parser.parse_args()
    port = 8501 if args.service == 'app' else 8081
    processes = owned(args.service)
    if args.action == 'status':
        print(json.dumps(dict(service=args.service, occupied=occupied(port), owned_pids=[pid for pid, _ in processes], port=port)))
        return
    if args.action == 'stop':
        if not processes:
            raise SystemExit('Refusing stop: no verified project process; no unrelated process will be killed')
        if args.service == 'flink':
            if any(job['state'] not in ('FINISHED', 'FAILED', 'CANCELED') for job in fetch('jobs/overview')['jobs']):
                raise SystemExit('Refusing stop: cluster has active jobs')
        for pid, command in processes:
            if (pid, command) not in owned(args.service):
                raise SystemExit('Process ownership changed; stop refused')
            os.kill(pid, signal.SIGTERM)
        for _ in range(40):
            if not owned(args.service) and not occupied(port):
                print(json.dumps(dict(service=args.service, stopped_pids=[pid for pid, _ in processes])))
                return
            time.sleep(.5)
        raise SystemExit('Graceful stop timed out; no force kill performed')
    if occupied(port) or processes:
        raise SystemExit(f'Port {port} occupied or project process exists; start refused')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', MKL_NUM_THREADS='2')
    if args.service == 'app':
        if not PYTHON.is_file():
            raise SystemExit('Locked Python environment missing')
        raise SystemExit(subprocess.call([str(PYTHON), '-B', str(ROOT / 'dashboard/serve.py')], env=env))
    if not (FLINK / 'bin/start-cluster.sh').is_file() or not (JAVA / 'bin/java').is_file():
        raise SystemExit('Flink 2.3.0 or Java 17 missing; no automatic installation')
    conf = RUNTIME / 'conf'
    conf.mkdir(parents=True, exist_ok=True)
    for name in ('flink-logs', 'flink-pids', 'flink-tmp'):
        (RUNTIME / name).mkdir(exist_ok=True)
    for source in (ROOT / 'pipeline/flink-conf').iterdir():
        if source.is_file() and source.name != 'config.yaml':
            shutil.copyfile(source, conf / source.name)
    config = (ROOT / 'pipeline/flink-conf/config.yaml').read_text()
    config = config.replace('bind-address: 0.0.0.0', 'bind-address: 127.0.0.1').replace(str(ROOT / '.agent/qa/phase1-smoke-20261009/flink-tmp'), str(RUNTIME / 'flink-tmp'))
    (conf / 'config.yaml').write_text(config)
    env.update(JAVA_HOME=str(JAVA), JAVA_TOOL_OPTIONS='-Djava.net.preferIPv4Stack=true', FLINK_CONF_DIR=str(conf), FLINK_LOG_DIR=str(RUNTIME / 'flink-logs'), FLINK_PID_DIR=str(RUNTIME / 'flink-pids'))
    result = subprocess.run([str(FLINK / 'bin/start-cluster.sh')], env=env, capture_output=True, text=True)
    print(result.stdout + result.stderr, flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    for _ in range(50):
        try:
            info = fetch('overview')
            if info['slots-total'] == 2 and info['taskmanagers'] == 1:
                print(json.dumps(dict(status='READY', overview=info, bind='127.0.0.1')), flush=True)
                break
        except OSError:
            pass
        time.sleep(1)
    else:
        raise SystemExit('Cluster not ready; inspect runtime logs; no automatic force stop')
    while occupied(port):
        time.sleep(3)


if __name__ == '__main__':
    main()
