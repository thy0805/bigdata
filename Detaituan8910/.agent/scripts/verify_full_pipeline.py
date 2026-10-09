import argparse
import csv
import hashlib
import json
import re
import time
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/phase1-full-20261009'
COLUMNS = ['hour_start', 'record_count', 'distinct_minute_count', 'valid_power_count', 'observed_energy_kwh', 'is_complete', 'energy_kwh', 'sub1_valid_count', 'sub2_valid_count', 'sub3_valid_count', 'sub1_observed_kwh', 'sub2_observed_kwh', 'sub3_observed_kwh', 'negative_residual_count']
HEADER = ['Date', 'Time', 'Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
TOLERANCE = Decimal('1e-8')
MODULUS = 2**256

def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()

def native(path):
    if path.startswith('/mnt/'):
        return Path(path[5].upper() + ':/' + path[7:]) if __import__('os').name == 'nt' else Path(path)
    if re.match(r'^[A-Za-z]:[\\/]', path) and __import__('os').name != 'nt':
        return Path('/mnt/' + path[0].lower() + '/' + path[3:].replace('\\', '/'))
    return Path(path)

def numbers(row):
    result = []
    for value in row:
        value = value.strip()
        if value in ('', '?'):
            result.append(None)
        else:
            if not re.fullmatch(r'[+]?[0-9]+(?:\.[0-9]{1,6})?', value):
                raise ValueError('Malformed numeric source')
            parsed = Decimal(value)
            assert parsed.is_finite() and parsed >= 0
            result.append(parsed)
    return result

def stamp(date, clock):
    assert re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', date) and re.fullmatch(r'\d{2}:\d{2}:00', clock)
    day, month, year = map(int, date.split('/'))
    value = datetime(year, month, day, int(clock[0:2]), int(clock[3:5]))
    return value

def fingerprint(row):
    return int.from_bytes(hashlib.sha256(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode()).digest(), 'big')

def oracle(raw):
    started = time.monotonic()
    hours = {}
    previous = first = last = None
    total = missing_rows = missing_cells = negatives = raw_fingerprint = 0
    residual_min = None
    with raw.open(encoding='utf-8', newline='') as stream:
        reader = csv.reader(stream, delimiter=';')
        assert next(reader) == HEADER
        for row in reader:
            assert len(row) == 9
            timestamp = stamp(*row[:2])
            if first is None:
                first = timestamp
            if previous is not None:
                assert timestamp == previous + timedelta(minutes=1), 'Source timeline gap/duplicate/order change'
            previous = last = timestamp
            total += 1
            values = numbers(row[2:])
            missing = sum(v is None for v in values)
            missing_cells += missing
            missing_rows += missing > 0
            raw_fingerprint = (raw_fingerprint + fingerprint(row)) % MODULUS
            key = timestamp.replace(minute=0)
            if key not in hours:
                hours[key] = {'rows': 0, 'minute_bits': 0, 'counts': [0] * 4, 'sums': [Decimal(0)] * 4, 'negatives': 0}
            group = hours[key]
            group['rows'] += 1
            group['minute_bits'] |= 1 << timestamp.minute
            selected = [values[0], *values[4:7]]
            for index, value in enumerate(selected):
                if value is not None:
                    group['counts'][index] += 1
                    group['sums'][index] += value
            if all(value is not None for value in selected):
                residual = values[0] * Decimal(1000) / Decimal(60) - sum(values[4:7])
                if residual < 0:
                    group['negatives'] += 1
                    negatives += 1
                residual_min = residual if residual_min is None else min(residual_min, residual)
            if total % 500000 == 0:
                print(json.dumps({'oracle_rows': total, 'seconds': round(time.monotonic() - started, 2)}), flush=True)
    expected = {}
    complete = 0
    for key, group in hours.items():
        counts, sums = group['counts'], group['sums']
        distinct = group['minute_bits'].bit_count()
        is_complete = group['rows'] == distinct == counts[0] == 60
        complete += is_complete
        energy = sums[0] / Decimal(60) if counts[0] else None
        expected[key] = [key, group['rows'], distinct, counts[0], energy, is_complete, energy if is_complete else None, *counts[1:], *[sums[i] / Decimal(1000) if counts[i] else None for i in range(1, 4)], group['negatives']]
    audit = {'rows': total, 'columns': len(HEADER), 'hours': len(hours), 'complete_hours': complete, 'incomplete_hours': len(hours) - complete, 'zero_valid_power_hours': sum(v[3] == 0 for v in expected.values()), 'missing_measurement_rows': missing_rows, 'missing_cells': missing_cells, 'negative_residual_rows': negatives, 'residual_min_wh': str(residual_min), 'first_minute': str(first), 'last_minute': str(last), 'raw_row_multiset_sha256_sum': hex(raw_fingerprint), 'seconds': time.monotonic() - started, 'timeline_contiguous_unique': True}
    return expected, audit, first

def verify(run_id):
    product = ROOT / 'data/processed/runs' / run_id
    support = QA / 'runs' / run_id
    assert product.is_dir() and support.is_dir()
    manifest = json.loads((support / 'manifest.json').read_text())
    checks = []
    def check(name, good, details=None):
        checks.append({'name': name, 'passed': bool(good), 'details': details})
    source = ROOT / 'data/raw/household_power_consumption.txt'
    source_hash = digest(source)
    check('raw_hash_before_oracle', source_hash == manifest['source_sha256_before'])
    reference, audit, first = oracle(source)
    mismatches = []
    mismatch_count = 0
    max_errors = {COLUMNS[i]: Decimal(0) for i in (4, 6, 10, 11, 12)}
    visited = set()
    cells = nulls = 0
    with (product / 'hourly-grid.csv').open(encoding='utf-8', newline='') as stream:
        reader = csv.reader(stream)
        check('hourly_schema_14_exact', next(reader) == COLUMNS)
        for row in reader:
            assert len(row) == 14
            key = datetime.fromisoformat(row[0])
            check_unique = key not in visited
            visited.add(key)
            expected = reference.get(key)
            if expected is None or not check_unique:
                mismatch_count += 1
                mismatches.append({'hour': str(key), 'error': 'unexpected/duplicate hour'})
                continue
            for i, (actual, value) in enumerate(zip(row, expected)):
                cells += 1
                if value is None:
                    nulls += 1
                    good = actual == 'NULL'
                elif i == 0:
                    good = datetime.fromisoformat(actual) == value
                elif i == 5:
                    good = actual == str(value).lower()
                elif i in (4, 6, 10, 11, 12):
                    good = actual != 'NULL'
                    if good:
                        difference = abs(Decimal(actual) - value)
                        max_errors[COLUMNS[i]] = max(max_errors[COLUMNS[i]], difference)
                        good = difference <= TOLERANCE
                else:
                    good = actual == str(value)
                if not good:
                    mismatch_count += 1
                    if len(mismatches) < 30:
                        mismatches.append({'hour': str(key), 'column': COLUMNS[i], 'expected': str(value), 'actual': actual})
    check('100_percent_hour_keys', visited == set(reference))
    check('100_percent_hourly_cells', mismatch_count == 0, {'hours': len(visited), 'cells': cells, 'null_cells': nulls, 'mismatch_count': mismatch_count, 'examples': mismatches[:30], 'max_abs_energy_error_kwh': {k: str(v) for k, v in max_errors.items()}})
    bitmap = bytearray((audit['rows'] + 7) // 8)
    count = errors = minute_fingerprint = negatives = missing_cells = 0
    minute_examples = []
    max_residual = Decimal(0)
    for path in sorted((product / 'flink-parts/minutes').glob('part-*')):
        with path.open(encoding='utf-8', newline='') as stream:
            for row in csv.reader(stream):
                count += 1
                assert len(row) == 17
                original = row[:2] + row[10:17]
                minute_fingerprint = (minute_fingerprint + fingerprint(original)) % MODULUS
                timestamp = stamp(*row[:2])
                offset = int((timestamp - first).total_seconds() // 60)
                good = 0 <= offset < audit['rows']
                if good:
                    mask = 1 << (offset % 8)
                    good = not bitmap[offset // 8] & mask
                    bitmap[offset // 8] |= mask
                values = numbers(row[10:17])
                missing = sum(v is None for v in values)
                missing_cells += missing
                good = good and datetime.fromisoformat(row[2]) == timestamp and row[3] == 'false' and row[4] == str(missing)
                selected = [values[0], *values[4:7]]
                for actual, expected in zip(row[5:9], selected):
                    good = good and (actual == 'NULL' if expected is None else actual != 'NULL' and Decimal(actual) == expected)
                if any(v is None for v in selected):
                    good = good and row[9] == 'NULL'
                else:
                    expected = values[0] * Decimal(1000) / Decimal(60) - sum(values[4:7])
                    if row[9] == 'NULL':
                        good = False
                    else:
                        actual = Decimal(row[9])
                        difference = abs(actual - expected)
                        max_residual = max(max_residual, difference)
                        good = good and difference <= Decimal('1e-8') and (actual < 0) == (expected < 0)
                        negatives += actual < 0
                if not good:
                    errors += 1
                    if len(minute_examples) < 10:
                        minute_examples.append({'row': count, 'timestamp': str(timestamp), 'actual': row})
                if count % 500000 == 0:
                    print(json.dumps({'minute_output_checked': count}), flush=True)
    check('all_minute_output_fields_and_residual_sign', count == audit['rows'] and errors == 0, {'rows': count, 'errors': errors, 'examples': minute_examples, 'max_residual_error_wh': str(max_residual)})
    check('minute_timestamp_coverage_unique', sum(v.bit_count() for v in bitmap) == audit['rows'])
    check('all_raw_fields_preserved_multiset_fingerprint', hex(minute_fingerprint) == audit['raw_row_multiset_sha256_sum'])
    check('missing_and_negative_minutes_match_raw', missing_cells == audit['missing_cells'] and negatives == audit['negative_residual_rows'])
    metrics = manifest['metrics']
    check('metrics_match_independent_raw', metrics == {'total_input_rows': audit['rows'] + 1, 'header_rows': 1, 'data_rows': audit['rows'], 'parse_error_rows': 0, 'missing_cells': audit['missing_cells']})
    reference_counts = {'rows': 2075259, 'columns': 9, 'hours': 34589, 'complete_hours': 34085, 'incomplete_hours': 504, 'zero_valid_power_hours': 421, 'missing_measurement_rows': 25979, 'negative_residual_rows': 1050}
    check('audit_reference_counts_only_tests_not_pipeline', all(audit[key] == value for key, value in reference_counts.items()), audit)
    check('job_FINISHED_exit0_no_error', len(manifest['jobs']) == 1 and manifest['jobs'][0]['state'] == 'FINISHED' and manifest['client_exit_code'] == 0 and '[ERROR]' not in (support / 'sql-client.log').read_text())
    check('runtime_frozen_SQL', manifest['runtime']['flink-version'] == '2.3.0' and digest(ROOT / 'pipeline/hourly.sql') == manifest['template_sha256'])
    for artifact in manifest['artifacts']:
        path = product / artifact['path']
        check('artifact_hash:' + artifact['path'], path.is_file() and path.stat().st_size == artifact['bytes'] and digest(path) == artifact['sha256'])
    source_guard = json.loads((ROOT / '.agent/qa/phase1-smoke-20261009/inputs-manifest.json').read_text())
    for path, expected in source_guard['source_hashes_before'].items():
        check('source_unchanged:' + path, digest(native(path)) == expected)
    check('raw_hash_after_oracle', digest(source) == source_hash == manifest['source_sha256_after'])
    report = {'captured_at': datetime.now().astimezone().isoformat(), 'run_id': run_id, 'status': 'VERIFIED' if all(c['passed'] for c in checks) else 'APPLIED_UNVERIFIED', 'passed': sum(c['passed'] for c in checks), 'total_checks': len(checks), 'independent_oracle': 'Raw stream -> Decimal per-hour reference; never used as product output. Source/output minute multiset SHA256 sum plus full unique contiguous timestamp coverage; validates each minute residual from raw fields.', 'tolerance_kwh': str(TOLERANCE), 'audit': audit, 'checks': checks}
    (support / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (product / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('run_id', 'status', 'passed', 'total_checks', 'audit')}, indent=2), flush=True)
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run_id')
    args = parser.parse_args()
    assert re.fullmatch(r'[0-9T]+-(full|rerun)', args.run_id)
    report = verify(args.run_id)
    raise SystemExit(0 if report['status'] == 'VERIFIED' else 2)
