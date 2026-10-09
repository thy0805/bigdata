import argparse
import importlib.util
import json
import os
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

os.environ.update(OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', MKL_NUM_THREADS='2')
ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/phase4-app-20261009'
spec = importlib.util.spec_from_file_location('services', ROOT / 'operations/services.py')
services = importlib.util.module_from_spec(spec)
spec.loader.exec_module(services)
parser = argparse.ArgumentParser()
parser.add_argument('step', choices=['stop-app', 'app-off', 'app-recovered', 'stop-flink', 'flink-off', 'flink-recovered', 'final'])
args = parser.parse_args()
checks = []


def check(name, passed, details=None):
    checks.append(dict(name=name, passed=bool(passed), details=details))
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)


def command(service, action):
    result = subprocess.run([sys.executable, '-B', str(ROOT / 'operations/services.py'), service, action], capture_output=True, text=True, timeout=35)
    return dict(returncode=result.returncode, stdout=result.stdout.strip(), stderr=result.stderr.strip())


if args.step.startswith('stop-'):
    service = args.step[5:]
    result = command(service, 'stop')
    check('graceful_stop_owned:' + service, result['returncode'] == 0, result)
elif args.step.endswith('-off'):
    service = args.step[:-4]
    port = 8501 if service == 'app' else 8081
    check('port_released:' + service, not services.occupied(port) and not services.owned(service))
    with socket.socket() as dummy:
        dummy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        dummy.bind(('127.0.0.1', port))
        dummy.listen(5)
        result = command(service, 'start')
        check('foreign_port_start_refused:' + service, result['returncode'] != 0 and 'start refused' in result['stderr'], result)
        result = command(service, 'stop')
        check('foreign_process_stop_refused:' + service, result['returncode'] != 0 and 'no verified project process' in result['stderr'] and dummy.fileno() >= 0, result)
    check('fixture_socket_released:' + service, not services.occupied(port))
    if service == 'flink':
        with urlopen('http://127.0.0.1:8501/_stcore/health', timeout=5) as response:
            check('dashboard_health_without_flink', response.status == 200)
        sys.path.insert(0, str(ROOT / 'dashboard'))
        import data_service as d
        from streamlit.testing.v1 import AppTest
        data = d.load_data(str(ROOT), d.source_signature())
        bundle = d.load_model(str(ROOT), d.MODEL_SHA, data['final']['version'])
        prediction = d.forecast(bundle, data['test'], data['test'].target_hour.iloc[-1])
        check('locked_inference_without_flink', abs(prediction['prediction_final_kwh'] - data['saved'].hgb_final_kwh.iloc[-1]) < 1e-12)
        app = AppTest.from_file(str(ROOT / 'dashboard/app.py'), default_timeout=30).run()
        check('all_tabs_without_flink', not app.error and not app.exception and len(app.tabs) == 3)
elif args.step == 'app-recovered':
    with urlopen('http://127.0.0.1:8501/_stcore/health', timeout=5) as response:
        check('app_health_after_restart', response.status == 200)
    check('app_ownership_after_restart', len(services.owned('app')) == 1)
elif args.step in ('flink-recovered', 'final'):
    info = services.fetch('overview')
    check('flink_recovery_one_tm_two_slots', info['taskmanagers'] == 1 and info['slots-total'] == info['slots-available'] == 2, info)
    check('flink_owned_two_jvms', len(services.owned('flink')) == 2)
    listeners = subprocess.check_output(['ss', '-ltnp']).decode()
    relevant = [line for line in listeners.splitlines() if ':8081 ' in line or ':8501 ' in line]
    check('rest_and_app_linux_loopback', all('127.0.0.1:' in line or '[::1]:' in line for line in relevant) and len(relevant) == 2, relevant)
    if args.step == 'final':
        check('app_owned_live', len(services.owned('app')) == 1)
        with urlopen('http://127.0.0.1:8501/_stcore/health', timeout=5) as response:
            check('app_final_health', response.status == 200)
report = dict(step=args.step, at=datetime.now(timezone.utc).isoformat(), status='VERIFIED' if all(c['passed'] for c in checks) else 'FAIL', checks=checks, passed=sum(c['passed'] for c in checks), total_checks=len(checks), cold_wsl_boot='NOT_TESTED', scope='Project service restart only; no WSL/Windows reboot; no jobs submitted')
with (QA / (args.step + '.json')).open('x', encoding='utf-8') as output:
    json.dump(report, output, ensure_ascii=False, indent=2)
sys.exit(0 if report['status'] == 'VERIFIED' else 1)
