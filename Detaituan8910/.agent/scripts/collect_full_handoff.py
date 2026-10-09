import ast
import csv
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'pipeline'))
from run_full import digest, generate_full, save
from run_smoke import generate

QA = ROOT / '.agent/qa/phase1-full-20261009'

def collect(run_ids):
    reports = [json.loads((QA / 'runs' / run / 'verification.json').read_text()) for run in run_ids]
    manifests = [json.loads((QA / 'runs' / run / 'manifest.json').read_text()) for run in run_ids]
    products = [ROOT / 'data/processed/runs' / run for run in run_ids]
    checks = []
    def check(name, passed, detail=None):
        checks.append({'name': name, 'passed': bool(passed), 'detail': detail})
    check('two_independent_full_runs_verified', len(reports) == 2 and all(r['status'] == 'VERIFIED' for r in reports))
    check('different_run_dirs_and_jobids', run_ids[0] != run_ids[1] and manifests[0]['jobs'][0]['jid'] != manifests[1]['jobs'][0]['jid'])
    hashes = [digest(p / 'hourly-grid.csv') for p in products]
    check('rerun_hourly_grid_identical_bytes', hashes[0] == hashes[1], hashes)
    for run, manifest in zip(run_ids, manifests):
        check('runtime_source_' + run, manifest['source_sha256_before'] == manifest['source_sha256_after'] == '4259c9d7ece5dbee9ab8d53682baac68d791c864f0f64a52b4043cb3b90894b7')
        check('full_input_and_coverage_' + run, manifest['metrics']['data_rows'] == 2075259 and manifest['hourly_grid_rows'] == 34589)
        check('resource_evidence_' + run, manifest['resources']['samples'] > 1 and manifest['resources']['min_C_free_bytes'] > 1024**3 and manifest['resources']['min_D_free_bytes'] > 1024**3)
        expected_sql = generate_full(ROOT / 'data/raw/household_power_consumption.txt', ROOT / 'data/processed/runs' / run / 'flink-parts', 'uci-full-' + run)
        check('executed_SQL_matches_full_generator_' + run, (QA / 'runs' / run / 'job.sql').read_text() == expected_sql)
    for category in ('hourly', 'minutes', 'metrics'):
        category_hashes = [sorted(a['sha256'] for a in m['artifacts'] if a['path'].startswith('flink-parts/' + category + '/')) for m in manifests]
        check('rerun_Flink_parts_content_' + category, bool(category_hashes[0]) and category_hashes[0] == category_hashes[1])
    parser = json.loads((QA / 'date-parser-verification.json').read_text())
    check('valid_and_invalid_date_regression', parser['passed'])
    sql = ROOT / 'pipeline/hourly.sql'
    smoke = ROOT / 'pipeline/run_smoke.py'
    check('frozen_F04_SQL', digest(sql) == '424b084c2c776b1d253ca272527c61734a7e64f6be9df6e2dd2a55f96e3966f3')
    check('frozen_F04_smoke_with_guard', digest(smoke) == '35713f95b960b876efa7a8a4fc0a90c9ce69ffd7e34330f46e06b00c8f98b4e9')
    for path in (ROOT / 'pipeline/run_full.py', ROOT / '.agent/scripts/verify_full_pipeline.py', ROOT / '.agent/scripts/verify_full_date_parser.py'):
        ast.parse(path.read_text())
        check('syntax_' + path.name, True)
    check('smoke_guard_outside_QA_still_rejects', "if not source.is_relative_to(allowed):" in smoke.read_text() and 'if index > 25000:' in smoke.read_text())
    original = generate(ROOT / 'data/raw/household_power_consumption.txt', QA / 'compare-only', 'compare-only')
    patched = generate_full(ROOT / 'data/raw/household_power_consumption.txt', QA / 'compare-only', 'compare-only')
    reversed_patch = patched.replace("CONCAT(SPLIT_INDEX(d, '/', 2), '-', LPAD(SPLIT_INDEX(d, '/', 1), 2, '0'), '-', LPAD(SPLIT_INDEX(d, '/', 0), 2, '0'), ' ', t)", "CONCAT(SUBSTRING(d, 7, 4), '-', SUBSTRING(d, 4, 2), '-', SUBSTRING(d, 1, 2), ' ', t)").replace("REGEXP(d, '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$')", "REGEXP(d, '^[0-9]{2}/[0-9]{2}/[0-9]{4}$')")
    check('only_two_date_parser_expressions_changed', reversed_patch == original and patched != original)
    rejected = []
    for run in ('20261009T101221593425-full', '20261009T101440768187-rerun'):
        support = QA / 'runs' / run
        product = ROOT / 'data/processed/runs' / run
        metrics_file = next((product / 'flink-parts/metrics').glob('part-*'))
        with metrics_file.open() as stream:
            metrics = next(csv.reader(stream))
        record = {'status': 'REJECTED', 'run_id': run, 'reason': 'old parser expected zero-padded date; valid D/M/YYYY flagged', 'metrics': metrics, 'hourly_promoted': (product / 'hourly-grid.csv').exists(), 'detail_files': [p.name for p in support.glob('job-*-details.json')]}
        save(support / 'rejected.json', record)
        rejected.append(record)
        check('invalid_output_not_promoted_' + run, not record['hourly_promoted'] and int(metrics[3]) == 1716480)
    ps = ['powershell.exe', '-NoProfile', '-Command', "Get-PSDrive -Name C,D | Select-Object Name,Free,Used | ConvertTo-Json -Compress"]
    disk_probe = subprocess.run(ps, capture_output=True, text=True, timeout=30)
    check('Windows_actual_C_D_probe', disk_probe.returncode == 0)
    windows_disk = json.loads(disk_probe.stdout) if disk_probe.returncode == 0 else {'error': disk_probe.stderr}
    rest_probe = subprocess.run(['powershell.exe', '-NoProfile', '-Command', "Invoke-RestMethod 'http://localhost:8081/overview' | ConvertTo-Json -Compress"], capture_output=True, text=True, timeout=30)
    rest = json.loads(rest_probe.stdout) if rest_probe.returncode == 0 else {}
    check('Windows_live_REST', rest.get('flink-version') == '2.3.0' and rest.get('taskmanagers') == 1 and rest.get('slots-total') == 2 and rest.get('jobs-running') == 0, rest)
    data = {'captured_at': datetime.now().astimezone().isoformat(), 'status': 'VERIFIED' if all(c['passed'] for c in checks) else 'APPLIED_UNVERIFIED', 'phase1_user_acceptance': 'PENDING; Phase2 not approved', 'passed': sum(c['passed'] for c in checks), 'total_checks': len(checks), 'run_ids': run_ids, 'hourly_grid_sha256': hashes, 'Windows_disk': windows_disk, 'live_REST': rest, 'rejected_runs': rejected, 'checks': checks, 'support_sha256': {str(p.relative_to(ROOT)): digest(p) for p in [ROOT / 'pipeline/run_full.py', ROOT / '.agent/scripts/verify_full_pipeline.py', ROOT / '.agent/scripts/verify_full_date_parser.py', ROOT / '.agent/scripts/collect_full_handoff.py', *[QA / 'runs' / run / file for run in run_ids for file in ('job.sql', 'sql-client.log', 'manifest.json', 'verification.json', 'resources.jsonl', 'resource-summary.json')]]}, 'verified_run_summaries': [{'run_id': m['run_id'], 'job': m['jobs'][0], 'metrics': m['metrics'], 'product_bytes': m['product_bytes'], 'resources': m['resources'], 'oracle': r['audit'], 'hourly_comparison': next(c['details'] for c in r['checks'] if c['name'] == '100_percent_hourly_cells')} for m, r in zip(manifests, reports)]}
    save(QA / 'handoff-verification.json', data)
    print(json.dumps(data, ensure_ascii=False, indent=2), flush=True)
    return data

if __name__ == '__main__':
    data = collect(sys.argv[1:])
    raise SystemExit(0 if data['status'] == 'VERIFIED' else 2)
