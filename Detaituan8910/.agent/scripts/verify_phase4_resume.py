import ast
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

os.environ.update(OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', MKL_NUM_THREADS='2')
ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/phase4-app-20261009'
OUT = ROOT / '.agent/qa/phase4-resume-20261010/resume-verification.json'
if OUT.exists():
    raise SystemExit('Existing receipt must not be overwritten')
sys.path.insert(0, str(ROOT / 'dashboard'))
import data_service as d
from streamlit.testing.v1 import AppTest

checks = []


def check(name, passed, details=None):
    checks.append(dict(name=name, passed=bool(passed), details=details))
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)


before = d.read_json(QA / 'preflight.json')['files']
changed = []
missing = []
for path, expected in before.items():
    if not Path(path).is_file():
        missing.append(path)
    elif d.sha256(path) != expected:
        changed.append(path)
check('frozen_1571_files', len(before) == 1571 and not changed and not missing,
      dict(total=len(before), matching=len(before)-len(changed)-len(missing), changed=changed, missing=missing))
previous = d.read_json(QA / 'verification.json')
check('previous_gate_structure', previous['status'] == 'VERIFIED' and previous['passed'] == previous['total_checks'] == 126
      and all(c['passed'] for c in previous['checks']), dict(snapshot=previous['at'], passed=previous['passed']))
drift = [name for name, sha in previous['selected_evidence'].items() if d.sha256(QA / name) != sha]
check('previous_selected_evidence_unchanged', not drift, drift)
shot_drift = [name for name, item in previous['screenshots'].items() if d.sha256(QA / 'screenshots' / name) != item['sha256']]
check('previous_eight_screenshots_unchanged', len(previous['screenshots']) == 8 and not shot_drift, shot_drift)
package = d.read_json(QA / 'package-verification.json')
archive = QA / package['archive']
check('handoff_archive_unchanged', package['status'] == 'VERIFIED' and archive.stat().st_size == package['bytes']
      and d.sha256(archive) == package['sha256'], dict(bytes=archive.stat().st_size, sha256=d.sha256(archive)))
signature = d.source_signature()
check('locked_source_gate21', len(signature) == 21, dict(count=len(signature), model_sha256=d.MODEL_SHA))
data = d.load_data(str(ROOT), signature)
hourly, test = data['hourly'], data['test']
check('hourly_and_test_structure', len(hourly) == 34589 and int(hourly['energy_kwh'].isna().sum()) == 504
      and len(test) == len(data['saved']) == 4590, dict(hourly=len(hourly), null_hours=int(hourly['energy_kwh'].isna().sum()), test=len(test)))
bundle = d.load_model(str(ROOT), d.MODEL_SHA, data['final']['version'])
for index in (0, len(test)-1):
    stamp = test.iloc[index]['target_hour']
    actual = d.forecast(bundle, test, stamp)
    saved = data['saved'].iloc[index]
    same = math.isclose(actual['prediction_final_kwh'], float(saved['hgb_final_kwh']), rel_tol=0, abs_tol=1e-12)
    check('locked_sample_inference_' + str(index), same and len(actual['feature_columns']) == 11
          and actual['prediction_final_kwh'] == max(0, actual['prediction_raw_kwh']),
          dict(target_hour=str(stamp), prediction=actual['prediction_final_kwh'], saved=float(saved['hgb_final_kwh'])))
empty = d.select_range(hourly, '2007-04-29', '2007-04-29')
stats = d.summarize(empty)
check('all_missing_day_no_false_zero', len(empty) == 24 and stats['complete_hours'] == 0 and stats['observed_kwh'] is None
      and stats['average_full_kwh'] is None and stats['peak_kwh'] is None, stats)
check('reverse_date_range_empty', d.select_range(hourly, '2010-11-26', '2010-11-20').empty)
app = AppTest.from_file(str(ROOT / 'dashboard/app.py'), default_timeout=60).run()
labels = [tab.label for tab in app.tabs]
check('current_app_render_three_tabs', not app.exception and not app.error and labels == ['Tổng quan', 'Phân tích', 'Dự báo'],
      dict(tabs=labels, exceptions=[str(item.value) for item in app.exception], errors=[str(item.value) for item in app.error]))
services = {}
for name in ('app', 'flink'):
    services[name] = json.loads(subprocess.check_output([sys.executable, '-B', str(ROOT / 'operations/services.py'), name, 'status']))
    check(name + '_owned_and_listening', services[name]['occupied'] and len(services[name]['owned_pids']) == (1 if name == 'app' else 2), services[name])
with urlopen('http://127.0.0.1:8501/_stcore/health', timeout=5) as response:
    check('linux_streamlit_health', response.status == 200 and response.read() == b'ok')
with urlopen('http://127.0.0.1:8081/overview', timeout=5) as response:
    overview = json.load(response)
check('linux_flink_ready_without_new_job', overview['taskmanagers'] == 1 and overview['slots-total'] == 2 and overview['jobs-running'] == 0, overview)
trees = [ast.parse((ROOT / folder / name).read_text(encoding='utf-8')) for folder, name in
         [('dashboard', 'app.py'), ('dashboard', 'data_service.py'), ('operations', 'services.py')]]
check('application_operations_no_fit_calls', not any(isinstance(node, ast.Attribute) and node.attr in ('fit', 'fit_transform', 'partial_fit')
      for tree in trees for node in ast.walk(tree)))
report = dict(status='VERIFIED' if all(c['passed'] for c in checks) else 'FAIL', captured_at=datetime.now(timezone.utc).isoformat(),
              source_checkpoint='853974cbf3d858efc2d4209c1ba1e60ffc1c650a', passed=sum(c['passed'] for c in checks), total_checks=len(checks),
              checks=checks, previous_gate_snapshot='126/126 on 2026-10-09; not rerun in full', overall_phase4='INCOMPLETE', I04='DEFERRED',
              acceptance='PENDING Thy/GPT Web', source_gate=signature, services=services,
              limits=['No new browser visual QA; previous eight images hash-verified', 'No full Flink rerun, training or Test metric evaluation',
                      'No Windows/WSL shutdown or restart; initially stopped distro started normally', 'No autostart', 'Windows HTTP checked separately'])
with OUT.open('x', encoding='utf-8') as stream:
    json.dump(report, stream, ensure_ascii=False, indent=2, default=str)
print(json.dumps(dict(status=report['status'], passed=report['passed'], total=report['total_checks'])))
raise SystemExit(0 if report['status'] == 'VERIFIED' else 1)
