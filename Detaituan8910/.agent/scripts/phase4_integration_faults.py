import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from urllib.request import urlopen
from urllib.error import HTTPError

os.environ.update(OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', MKL_NUM_THREADS='2')
ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/phase4-app-20261009'
sys.path.insert(0, str(ROOT / 'dashboard'))
import data_service as d
from streamlit.testing.v1 import AppTest

checks = []


def check(name, passed, details=None):
    checks.append(dict(name=name, passed=bool(passed), details=details))
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)


signature = d.source_signature()
preflight = d.read_json(QA / 'preflight.json')
hourly = d.read_json(ROOT / d.HOURLY / 'manifest.json')
ml = d.read_json(ROOT / d.ML / 'manifest.json')
final = d.read_json(ROOT / d.MODEL / 'manifest.json')
check('raw_txt_to_flink', d.sha256(ROOT / 'data/raw/household_power_consumption.txt') == hourly['source_sha256_before'] == hourly['source_sha256_after'])
check('zip_integrity', preflight['files']['/mnt/c/Users/thy/Downloads/individual+household+electric+power+consumption.zip'] == '9f84b46ade8a2d8e1286ec4b2b6c2987a45a755c59f263be3b3b3d10dfbda3ff')
check('flink_to_ml', ml['source']['sha256'] == d.HOURLY_SHA and ml['source']['manifest_sha256'] == d.sha256(ROOT / d.HOURLY / 'manifest.json') and ml['source']['verification_sha256'] == d.sha256(ROOT / d.HOURLY / 'verification.json'))
check('ml_to_final', final['source_phase2a_manifest_sha256'] == d.sha256(ROOT / d.ML / 'manifest.json') and final['fitted_rows'] == 22513 and final['no_refit'])
check('batch_historical_scope', hourly['mode'] == ml['source']['mode'] == 'BATCH' and hourly['minute_output_rows'] == 2075259 and ml['input_axis_hours'] == 34589 and ml['eligible_ml_hours'] == 31830)
rest = {}
for job in hourly['jobs']:
    try:
        with urlopen('http://127.0.0.1:8081/jobs/' + job['jid'], timeout=5) as response:
            rest[job['jid']] = json.load(response)
    except HTTPError as error:
        if error.code != 404:
            raise
        rest[job['jid']] = dict(live_history='EXPIRED_HTTP_404', archived_state=job['state'], archived_type=job['jobType'])
    check('archived_verified_flink_job:' + job['jid'], job['state'] == 'FINISHED' and job['jobType'] == 'BATCH' and d.read_json(ROOT / d.HOURLY / 'verification.json')['status'] == 'VERIFIED')
fixture = QA / 'fixtures/source'
fixture.mkdir(parents=True, exist_ok=False)
for name, _ in signature:
    target = fixture / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / name, target)
check('fixture_exact_chain', d.source_signature(fixture) == signature)
target = fixture / d.HOURLY / 'hourly-grid.csv'
parked = target.with_suffix('.held')
target.rename(parked)
try:
    try:
        d.source_signature(fixture)
    except FileNotFoundError:
        check('physical_missing_source_rejected', True)
    else:
        check('physical_missing_source_rejected', False)
finally:
    parked.rename(target)
target = fixture / d.MODEL / 'model.joblib'
with target.open('r+b') as stream:
    original = stream.read(1)
    stream.seek(0)
    stream.write(bytes([original[0] ^ 1]))
try:
    d.source_signature(fixture)
except d.ArtifactError as error:
    check('physical_corrupt_model_rejected_before_load', 'model.joblib' in str(error))
else:
    check('physical_corrupt_model_rejected_before_load', False)
real_signature = d.source_signature
with patch.object(d, 'source_signature', side_effect=lambda: real_signature(fixture)):
    app = AppTest.from_file(str(ROOT / 'dashboard/app.py'), default_timeout=30).run()
    check('physical_corruption_visible_error_and_stop', len(app.error) == 1 and 'Checksum' in app.error[0].value and not app.exception and len(app.tabs) == 0)
try:
    d.load_model(str(ROOT), d.MODEL_SHA, 'incorrect-version-fixture')
except d.ArtifactError:
    check('model_version_mismatch_rejected', True)
else:
    check('model_version_mismatch_rejected', False)
for service in ('app', 'flink'):
    result = subprocess.run([sys.executable, '-B', str(ROOT / 'operations/services.py'), service, 'start'], capture_output=True, text=True, timeout=10)
    check('duplicate_start_refused:' + service, result.returncode != 0 and 'start refused' in result.stderr, result.stderr.strip())
runtime = {}
for command in ([sys.executable, '-m', 'pip', 'check'], [str(Path.home() / '.local/share/uci-forecast/venv/bin/python'), '--version'], ['/usr/lib/jvm/java-17-openjdk-amd64/bin/java', '-version']):
    result = subprocess.run(command, capture_output=True, text=True, timeout=15)
    runtime[' '.join(command)] = dict(returncode=result.returncode, output=(result.stdout + result.stderr).strip())
    check('environment:' + command[-1], result.returncode == 0)
with patch.object(d.importlib.metadata, 'version', return_value='0.0.invalid'):
    try:
        d.source_signature()
    except d.ArtifactError:
        check('environment_package_mismatch_rejected', True)
    else:
        check('environment_package_mismatch_rejected', False)
report = dict(status='VERIFIED' if all(c['passed'] for c in checks) else 'FAIL', at=datetime.now(timezone.utc).isoformat(), checks=checks, passed=sum(c['passed'] for c in checks), total_checks=len(checks), source_signature=dict(signature), historical_job_rest=rest, environment=runtime, fault_scope='Only isolated source copies/mocks; real accepted artifacts untouched', full_flink_rerun=False, training=False, official_test_evaluation=False)
with (QA / 'integration-faults.json').open('x', encoding='utf-8') as output:
    json.dump(report, output, ensure_ascii=False, indent=2)
print(json.dumps(dict(status=report['status'], passed=report['passed'], total=report['total_checks'])))
sys.exit(0 if report['status'] == 'VERIFIED' else 1)
