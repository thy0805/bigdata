import argparse
import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from cluster import environment, fetch, FLINK, QA, ROOT

NUMBERS = [('p', 'power_kw'), ('r', 'reactive'), ('v', 'voltage'), ('a', 'intensity'), ('s1', 'sub1_wh'), ('s2', 'sub2_wh'), ('s3', 'sub3_wh')]
HOUR_COLUMNS = ['hour_start', 'record_count', 'distinct_minute_count', 'valid_power_count', 'observed_energy_kwh', 'is_complete', 'energy_kwh', 'sub1_valid_count', 'sub2_valid_count', 'sub3_valid_count', 'sub1_observed_kwh', 'sub2_observed_kwh', 'sub3_observed_kwh', 'negative_residual_count']

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_parts(directory):
    result = []
    for path in sorted(directory.glob('part-*')):
        if path.is_file():
            with path.open(encoding='utf-8', newline='') as stream:
                result.extend(csv.reader(stream))
    return result

def generate(source, output, job_name):
    sql = (ROOT / 'pipeline/hourly.sql').read_text(encoding='utf-8')
    clean = [f"CASE WHEN {field} IS NULL OR TRIM({field}) IN ('', '?') THEN CAST(NULL AS STRING) ELSE TRIM({field}) END AS {name}_text" for field, name in NUMBERS]
    parsed = [f"CASE WHEN REGEXP({name}_text, '^[+]?[0-9]+([.][0-9]{{1,6}})?$') THEN TRY_CAST({name}_text AS DECIMAL(18,6)) ELSE CAST(NULL AS DECIMAL(18,6)) END AS {name}" for field, name in NUMBERS]
    errors = [f'({name}_text IS NOT NULL AND {name} IS NULL)' for field, name in NUMBERS]
    missing = [f'CASE WHEN {name}_text IS NULL THEN 1 ELSE 0 END' for field, name in NUMBERS]
    mapping = {'SOURCE': source.as_uri(), 'OUTPUT': output.as_uri(), 'JOB_NAME': job_name, 'CLEAN_COLUMNS': ',\n  '.join(clean), 'PARSE_COLUMNS': ',\n  '.join(parsed), 'ERROR_COLUMNS': ' OR '.join(errors), 'MISSING_COLUMNS': ' + '.join(missing)}
    for key, value in mapping.items():
        sql = sql.replace('{{' + key + '}}', value)
    assert '{{' not in sql
    return sql

def run(source, label):
    source = source.resolve()
    allowed = (QA / 'inputs').resolve()
    if not source.is_relative_to(allowed):
        raise ValueError('F04 restricted to QA sample/fixture input; full dataset needs F05 approval')
    with source.open(encoding='utf-8') as stream:
        for index, line in enumerate(stream):
            if index > 25000:
                raise ValueError('F04 max25000 sample rows; full run is not approved')
    stamp = datetime.now().strftime('%Y%m%dT%H%M%S%f')
    run_dir = QA / 'runs' / (stamp + '-' + label)
    run_dir.mkdir(parents=True)
    sql_path = run_dir / 'job.sql'
    output = run_dir / 'output'
    sql_path.write_text(generate(source, output, 'uci-smoke-' + label), encoding='utf-8')
    before = {item['jid'] for item in fetch('/jobs/overview')['jobs']}
    with (run_dir / 'sql-client.log').open('w', encoding='utf-8') as log:
        result = subprocess.run([str(FLINK / 'bin/sql-client.sh'), '-f', str(sql_path)], env=environment(), stdout=log, stderr=subprocess.STDOUT, timeout=180)
    content = (run_dir / 'sql-client.log').read_text(encoding='utf-8')
    jobs = [item for item in fetch('/jobs/overview')['jobs'] if item['jid'] not in before]
    for item in jobs:
        for endpoint in ('', '/plan', '/exceptions', '/config'):
            try:
                info = fetch('/jobs/' + item['jid'] + endpoint)
                (run_dir / ('job-' + item['jid'] + (endpoint.replace('/', '-') or '-details') + '.json')).write_text(json.dumps(info, indent=2), encoding='utf-8')
            except Exception as error:
                (run_dir / ('rest-error' + endpoint.replace('/', '-') + '.txt')).write_text(str(error), encoding='utf-8')
    good = len(jobs) == 1 and jobs[0]['state'] == 'FINISHED' and '[ERROR]' not in content
    metrics, minutes, duplicates, hours = {}, [], [], []
    if good:
        entries = read_parts(output / 'metrics')
        if len(entries) != 1:
            good = False
        else:
            metrics = dict(zip(['total_input_rows', 'header_rows', 'data_rows', 'parse_error_rows', 'missing_cells'], map(int, entries[0])))
        minutes = read_parts(output / 'minutes')
        duplicates = read_parts(output / 'duplicates')
        hours = read_parts(output / 'hourly')
    accepted = good and metrics.get('parse_error_rows') == 0 and not duplicates and metrics.get('data_rows') == len(minutes)
    if accepted and hours:
        keyed = {datetime.fromisoformat(item[0]): item for item in hours}
        if len(keyed) != len(hours):
            raise ValueError('Nonunique hourly output')
        current = min(keyed)
        grid = []
        while current <= max(keyed):
            grid.append(keyed.get(current, [str(current), '0', '0', '0', 'NULL', 'false', 'NULL', '0', '0', '0', 'NULL', 'NULL', 'NULL', '0']))
            current += timedelta(hours=1)
        with (run_dir / 'hourly-grid.csv').open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(HOUR_COLUMNS)
            writer.writerows(grid)
    if metrics and metrics.get('parse_error_rows'):
        with (run_dir / 'quarantine.csv').open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['date_raw', 'time_raw', 'event_time', 'parse_error', 'missing_cells', 'power_kw', 'sub1_wh', 'sub2_wh', 'sub3_wh', 'residual_wh', 'power_raw', 'reactive_raw', 'voltage_raw', 'intensity_raw', 'sub1_raw', 'sub2_raw', 'sub3_raw'])
            writer.writerows(item for item in minutes if item[3] == 'true')
    manifest = {'captured_at': datetime.now().astimezone().isoformat(), 'source': str(source), 'source_sha256': digest(source), 'template_sha256': digest(ROOT / 'pipeline/hourly.sql'), 'sql_sha256': digest(sql_path), 'flink_version': '2.3.0', 'java_home': environment()['JAVA_HOME'], 'mode': 'BATCH', 'label': label, 'client_exit_code': result.returncode, 'jobs': jobs, 'runtime_finished': good, 'validation_accepted': accepted, 'metrics': metrics, 'minute_output_rows': len(minutes), 'duplicate_groups': len(duplicates), 'hourly_flink_rows': len(hours), 'run_dir': str(run_dir), 'scope': 'F04 QA sample/fixture only; not product or full data'}
    (run_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2), flush=True)
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', args.label):
        raise ValueError('Invalid label')
    manifest = run(Path(args.input), args.label)
    raise SystemExit(0 if manifest['validation_accepted'] else 2)
