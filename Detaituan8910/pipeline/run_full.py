import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

from cluster import environment, fetch, FLINK, ROOT
from run_smoke import generate, HOUR_COLUMNS

QA_FULL = ROOT / '.agent/qa/phase1-full-20261009'
SOURCE = ROOT / 'data/raw/household_power_consumption.txt'
SQL_HASH = '424b084c2c776b1d253ca272527c61734a7e64f6be9df6e2dd2a55f96e3966f3'

def generate_full(source, output, name):
    sql = generate(source, output, name)
    old_stamp = "CONCAT(SUBSTRING(d, 7, 4), '-', SUBSTRING(d, 4, 2), '-', SUBSTRING(d, 1, 2), ' ', t)"
    new_stamp = "CONCAT(SPLIT_INDEX(d, '/', 2), '-', LPAD(SPLIT_INDEX(d, '/', 1), 2, '0'), '-', LPAD(SPLIT_INDEX(d, '/', 0), 2, '0'), ' ', t)"
    old_regex = "REGEXP(d, '^[0-9]{2}/[0-9]{2}/[0-9]{4}$')"
    new_regex = "REGEXP(d, '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$')"
    assert sql.count(old_stamp) == sql.count(old_regex) == 1
    return sql.replace(old_stamp, new_stamp).replace(old_regex, new_regex)

def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()

def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

def parts(path):
    for item in sorted(path.glob('part-*')):
        if item.is_file():
            with item.open(encoding='utf-8', newline='') as stream:
                yield from csv.reader(stream)

def resources():
    memory = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        key, value = line.split(':', 1)
        if key in ('MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree'):
            memory[key + '_bytes'] = int(value.strip().split()[0]) * 1024
    processes = []
    for path in Path('/proc').glob('[0-9]*'):
        try:
            name = (path / 'comm').read_text().strip()
            if name not in ('java', 'python3', 'python'):
                continue
            match = re.search(r'^VmRSS:\s+(\d+) kB', (path / 'status').read_text(), re.M)
            processes.append({'pid': int(path.name), 'name': name, 'rss_bytes': int(match[1]) * 1024 if match else 0})
        except (OSError, ProcessLookupError):
            pass
    disk = {}
    for drive in ('c', 'd'):
        usage = os.statvfs('/mnt/' + drive)
        disk[drive.upper() + '_free_bytes'] = usage.f_bavail * usage.f_frsize
    return {'at': datetime.now().astimezone().isoformat(), **memory, **disk, 'processes': processes, 'java_rss_sum_bytes': sum(p['rss_bytes'] for p in processes if p['name'] == 'java')}

def run(label):
    expected = json.loads((ROOT / '.agent/qa/phase1-smoke-20261009/inputs-manifest.json').read_text())
    source_hash = digest(SOURCE)
    assert source_hash == expected['raw_sha256'], 'Raw source hash changed'
    assert digest(ROOT / 'pipeline/hourly.sql') == SQL_HASH, 'Frozen SQL changed'
    config = fetch('/config')
    assert config['flink-version'] == '2.3.0', 'Unexpected runtime version'
    overview = fetch('/overview')
    assert overview['taskmanagers'] == 1 and overview['slots-total'] == 2
    assert not any(j['state'] in ('RUNNING', 'CREATED', 'RESTARTING') for j in fetch('/jobs/overview')['jobs']), 'Another job is active'
    initial = resources()
    assert initial['C_free_bytes'] > 5 * 1024**3 and initial['D_free_bytes'] > 3 * 1024**3, 'Insufficient actual disk space'
    run_id = datetime.now().strftime('%Y%m%dT%H%M%S%f') + '-' + label
    support = QA_FULL / 'runs' / run_id
    product = ROOT / 'data/processed/runs' / run_id
    support.mkdir(parents=True, exist_ok=False)
    product.mkdir(parents=True, exist_ok=False)
    output = product / 'flink-parts'
    sql = support / 'job.sql'
    sql.write_text(generate_full(SOURCE, output, 'uci-full-' + run_id), encoding='utf-8')
    before = {j['jid'] for j in fetch('/jobs/overview')['jobs']}
    started = time.monotonic()
    snapshots = [initial]
    print(json.dumps({'run_id': run_id, 'support': str(support), 'product': str(product)}, indent=2), flush=True)
    with (support / 'resources.jsonl').open('w') as monitoring, (support / 'sql-client.log').open('w', encoding='utf-8') as log:
        process = subprocess.Popen([str(FLINK / 'bin/sql-client.sh'), '-f', str(sql)], env=environment(), stdout=log, stderr=subprocess.STDOUT)
        while True:
            sample = resources()
            jobs = [j for j in fetch('/jobs/overview')['jobs'] if j['jid'] not in before]
            sample['jobs'] = jobs
            snapshots.append(sample)
            monitoring.write(json.dumps(sample) + '\n')
            monitoring.flush()
            if process.poll() is not None:
                break
            if time.monotonic() - started > 900 or sample['C_free_bytes'] < 1024**3 or sample['D_free_bytes'] < 1024**3:
                for job in jobs:
                    if job['state'] == 'RUNNING':
                        subprocess.run([str(FLINK / 'bin/flink'), 'cancel', job['jid']], env=environment(), timeout=30, stdout=log, stderr=subprocess.STDOUT)
                process.terminate()
                process.wait(timeout=30)
                save(support / 'failure.json', {'reason': 'time/disk safety limit', 'last_sample': sample})
                raise RuntimeError('Full job safety limit; output not promoted')
            time.sleep(3)
    duration = time.monotonic() - started
    jobs = [j for j in fetch('/jobs/overview')['jobs'] if j['jid'] not in before]
    for job in jobs:
        for endpoint in ('', '/plan', '/exceptions', '/config'):
            save(support / ('job-' + job['jid'] + (endpoint.replace('/', '-') or '-details') + '.json'), fetch('/jobs/' + job['jid'] + endpoint))
    log_text = (support / 'sql-client.log').read_text()
    assert process.returncode == 0 and len(jobs) == 1 and jobs[0]['state'] == 'FINISHED' and '[ERROR]' not in log_text, 'Full SQL job failed; no promotion'
    metric_rows = list(parts(output / 'metrics'))
    assert len(metric_rows) == 1 and len(metric_rows[0]) == 5
    metrics = dict(zip(['total_input_rows', 'header_rows', 'data_rows', 'parse_error_rows', 'missing_cells'], map(int, metric_rows[0])))
    if metrics['parse_error_rows'] != 0 or metrics['header_rows'] != 1:
        save(support / 'failure.json', {'status': 'APPLIED_UNVERIFIED', 'reason': 'input semantic validation failed; no hourly promotion', 'metrics': metrics, 'jobs': jobs})
        raise ValueError('Input semantic validation failed; output not promoted')
    minute_count = 0
    for row in parts(output / 'minutes'):
        assert len(row) == 17 and row[3] == 'false'
        minute_count += 1
    assert minute_count == metrics['data_rows']
    duplicate_groups = sum(1 for _ in parts(output / 'duplicates'))
    assert duplicate_groups == 0
    keyed = {}
    for row in parts(output / 'hourly'):
        assert len(row) == len(HOUR_COLUMNS)
        stamp = datetime.fromisoformat(row[0])
        assert stamp not in keyed, 'Duplicate hourly key'
        keyed[stamp] = row
    assert keyed, 'No hourly output'
    count = 0
    with (product / 'hourly-grid.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(HOUR_COLUMNS)
        stamp = min(keyed)
        while stamp <= max(keyed):
            writer.writerow(keyed.get(stamp, [str(stamp), '0', '0', '0', 'NULL', 'false', 'NULL', '0', '0', '0', 'NULL', 'NULL', 'NULL', '0']))
            count += 1
            stamp += timedelta(hours=1)
    assert digest(SOURCE) == source_hash and digest(ROOT / 'pipeline/hourly.sql') == SQL_HASH
    final = resources()
    snapshots.append(final)
    summary = {'sampling_interval_seconds': 3, 'samples': len(snapshots), 'before': initial, 'after': final, 'peak_observed_java_rss_bytes': max(s['java_rss_sum_bytes'] for s in snapshots), 'min_observed_mem_available_bytes': min(s['MemAvailable_bytes'] for s in snapshots), 'min_C_free_bytes': min(s['C_free_bytes'] for s in snapshots), 'min_D_free_bytes': min(s['D_free_bytes'] for s in snapshots), 'limitations': 'Observed Linux process RSS sums can count shared pages. Not Windows whole-machine peak; sampled every3s, not continuous. C/D statvfs is mounted physical volume, not VHD virtual capacity.'}
    save(support / 'resource-summary.json', summary)
    manifest = {'status': 'APPLIED_UNVERIFIED', 'scope': 'F05 full Flink; pending independent F06 oracle', 'captured_at': datetime.now().astimezone().isoformat(), 'run_id': run_id, 'run_dir': str(product), 'support_dir': str(support), 'source': str(SOURCE), 'source_sha256_before': source_hash, 'source_sha256_after': digest(SOURCE), 'template_sha256': SQL_HASH, 'sql_sha256': digest(sql), 'launcher_sha256': digest(Path(__file__)), 'parser_revision': 'F05-D/M/YYYY-and-DD/MM/YYYY; date parts padded before validated TRY_CAST; aggregation unchanged', 'runtime': config, 'mode': 'BATCH', 'timezone_policy': 'naive source calendar; no UTC/DST inference', 'client_exit_code': process.returncode, 'client_wall_seconds': duration, 'jobs': jobs, 'metrics': metrics, 'minute_output_rows': minute_count, 'duplicate_groups': duplicate_groups, 'flink_hourly_rows': len(keyed), 'hourly_grid_rows': count, 'reindex_only_python': True, 'resources': summary}
    manifest['artifacts'] = [{'path': str(path.relative_to(product)), 'bytes': path.stat().st_size, 'sha256': digest(path)} for path in sorted(product.rglob('*')) if path.is_file()]
    manifest['product_bytes'] = sum(a['bytes'] for a in manifest['artifacts'])
    save(support / 'manifest.json', manifest)
    save(product / 'manifest.json', manifest)
    print(json.dumps(manifest, indent=2), flush=True)
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True, choices=('full', 'rerun'))
    args = parser.parse_args()
    run(args.label)
