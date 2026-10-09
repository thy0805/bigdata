import csv
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'pipeline'))
from run_smoke import HOUR_COLUMNS, digest, read_parts, run
from cluster import QA

HEADER = ['Date', 'Time', 'Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
CHECKS = []

def check(name, passed, evidence):
    CHECKS.append({'name': name, 'passed': bool(passed), 'evidence': evidence})
    print(name + ': ' + ('PASS' if passed else 'FAIL'), flush=True)

def equal(expected, actual):
    if expected is None:
        return actual == 'NULL'
    if isinstance(expected, bool):
        return str(expected).lower() == actual
    if isinstance(expected, int):
        return str(expected) == actual
    if isinstance(expected, Decimal):
        return math.isclose(float(expected), float(actual), abs_tol=1e-10, rel_tol=1e-10)
    return str(expected) == actual

def reference(path):
    groups = defaultdict(list)
    stamps = Counter()
    metrics = dict(total_input_rows=0, header_rows=0, data_rows=0, parse_error_rows=0, missing_cells=0)
    with path.open(newline='', encoding='utf-8') as stream:
        for row in csv.reader(stream, delimiter=';'):
            metrics['total_input_rows'] += 1
            if len(row) != 9:
                raise ValueError('Exactly nine columns required')
            if row == HEADER:
                metrics['header_rows'] += 1
                continue
            metrics['data_rows'] += 1
            parsed, error = [], False
            for raw in row[2:]:
                value = raw.strip()
                if value in ('', '?'):
                    parsed.append(None)
                    metrics['missing_cells'] += 1
                elif re.fullmatch(r'[+]?[0-9]+([.][0-9]{1,6})?', value) and Decimal(value) < Decimal('1000000000000'):
                    parsed.append(Decimal(value))
                else:
                    error = True
                    parsed.append(None)
            try:
                stamp = datetime.strptime(row[0] + ' ' + row[1], '%d/%m/%Y %H:%M:%S')
                if stamp.strftime('%d/%m/%Y %H:%M:%S') != row[0] + ' ' + row[1] or stamp.second:
                    raise ValueError('Timestamp must be exact minute')
            except ValueError:
                error = True
            if error:
                metrics['parse_error_rows'] += 1
                continue
            stamps[stamp] += 1
            groups[stamp.replace(minute=0)].append((stamp, parsed))
    hours = {}
    if groups:
        current, stop = min(groups), max(groups)
        while current <= stop:
            rows = groups.get(current, [])
            values = [[item[1][index] for item in rows if item[1][index] is not None] for index in range(7)]
            observed = sum(values[0], Decimal(0)) / 60 if values[0] else None
            complete = len(rows) == len({item[0] for item in rows}) == len(values[0]) == 60
            negative = sum(1 for stamp, item in rows if all(item[index] is not None for index in (0, 4, 5, 6)) and item[0] * 1000 / 60 - sum(item[4:], Decimal(0)) < 0)
            hours[str(current)] = [str(current), len(rows), len({item[0] for item in rows}), len(values[0]), observed, complete, observed if complete else None, *[len(values[index]) for index in (4, 5, 6)], *[sum(values[index], Decimal(0)) / 1000 if values[index] else None for index in (4, 5, 6)], negative]
            current += timedelta(hours=1)
    return metrics, hours, sum(count > 1 for count in stamps.values())

def verify(label, source, manifest, expected_accepted):
    expected_metrics, expected_hours, expected_duplicates = reference(source)
    check(label + '/real-job-finished', manifest['runtime_finished'], manifest['jobs'])
    check(label + '/metrics', manifest['metrics'] == expected_metrics, {'expected': expected_metrics, 'actual': manifest['metrics']})
    check(label + '/validation', manifest['validation_accepted'] == expected_accepted, manifest['validation_accepted'])
    check(label + '/duplicates', manifest['duplicate_groups'] == expected_duplicates, expected_duplicates)
    check(label + '/source-template-hash', manifest['source_sha256'] == digest(source) and manifest['template_sha256'] == digest(ROOT / 'pipeline/hourly.sql'), manifest['template_sha256'])
    if expected_accepted:
        with (Path(manifest['run_dir']) / 'hourly-grid.csv').open(newline='', encoding='utf-8') as stream:
            reader = csv.reader(stream)
            check(label + '/hour-columns', next(reader) == HOUR_COLUMNS, HOUR_COLUMNS)
            actual = {row[0]: row for row in reader}
        matches = actual.keys() == expected_hours.keys() and all(all(equal(value, row[index]) for index, value in enumerate(expected_hours[key])) for key, row in actual.items())
        check(label + '/all-hour-values-independent-decimal', matches, {'compared_hours': len(expected_hours), 'tolerance': '1e-10 absolute and relative', 'hour_columns': len(HOUR_COLUMNS)})
    elif expected_metrics['parse_error_rows']:
        with (Path(manifest['run_dir']) / 'quarantine.csv').open(newline='', encoding='utf-8') as stream:
            rejected = list(csv.DictReader(stream))
        check(label + '/quarantine-raw-values', len(rejected) == expected_metrics['parse_error_rows'] and all('power_raw' in row and 'sub3_raw' in row for row in rejected), rejected)
    check(label + '/no-promoted-grid-on-rejection', expected_accepted or not (Path(manifest['run_dir']) / 'hourly-grid.csv').exists(), manifest['run_dir'])

def main():
    runs = []
    inputs = QA / 'inputs'
    cases = [('edge-cases', True), ('real-10000', True), ('zero', True), ('precision', True), ('duplicate', False), ('invalid-number', False), ('invalid-time', False), ('header-lookalike', False)]
    for label, accepted in cases:
        source = inputs / (label + '.txt')
        manifest = run(source, label)
        runs.append(manifest)
        verify(label, source, manifest, accepted)
    for label in ('bad-structure', 'extra-column'):
        manifest = run(inputs / (label + '.txt'), label)
        runs.append(manifest)
        log = (Path(manifest['run_dir']) / 'sql-client.log').read_text(encoding='utf-8')
        check(label + '/strict-runtime-failure', not manifest['runtime_finished'] and not manifest['validation_accepted'] and len(manifest['jobs']) == 1 and manifest['jobs'][0]['state'] == 'FAILED' and '[ERROR]' in log, manifest['jobs'])
        check(label + '/no-promoted-grid', not (Path(manifest['run_dir']) / 'hourly-grid.csv').exists(), manifest['run_dir'])
    rerun = run(inputs / 'real-10000.txt', 'real-rerun')
    runs.append(rerun)
    verify('real-rerun', inputs / 'real-10000.txt', rerun, True)
    first = next(item for item in runs if item['label'] == 'real-10000')
    check('rerun/identical-grid-bytes', digest(Path(first['run_dir']) / 'hourly-grid.csv') == digest(Path(rerun['run_dir']) / 'hourly-grid.csv'), {'first_job': first['jobs'][0]['jid'], 'second_job': rerun['jobs'][0]['jid']})
    try:
        run(ROOT / 'data/raw/household_power_consumption.txt', 'forbidden-full')
    except ValueError as error:
        check('scope/full-job-blocked-before-submission', 'F04 restricted' in str(error), str(error))
    else:
        check('scope/full-job-blocked-before-submission', False, 'Full input incorrectly allowed')
    manifest = json.loads((QA / 'inputs-manifest.json').read_text(encoding='utf-8'))
    for source, expected in manifest['source_hashes_before'].items():
        mapped = Path('/mnt/' + source[0].lower() + source[2:].replace('\\', '/'))
        check('preservation/' + mapped.name, digest(mapped) == expected, expected)
    check('raw/extracted-bytes-match', digest(ROOT / 'data/raw/household_power_consumption.txt') == manifest['raw_sha256'], manifest['raw_sha256'])
    result = {'captured_at': datetime.now().astimezone().isoformat(), 'status': 'VERIFIED' if all(item['passed'] for item in CHECKS) else 'APPLIED_UNVERIFIED', 'passed': sum(item['passed'] for item in CHECKS), 'total': len(CHECKS), 'checks': CHECKS, 'runs': runs, 'scope': 'F04 only; fixtures are not empirical product results'}
    (QA / 'smoke-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status', 'passed', 'total')}, indent=2), flush=True)
    raise SystemExit(0 if result['status'] == 'VERIFIED' else 1)

if __name__ == '__main__':
    main()
