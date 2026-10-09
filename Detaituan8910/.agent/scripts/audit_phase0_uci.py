import csv
import hashlib
import io
import json
import math
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(r'D:\Hoctap\bigdata\Detaituan8910')
QA = ROOT / '.agent/qa/phase0-20261008'
SOURCE = Path(r'C:\Users\thy\Downloads\individual+household+electric+power+consumption.zip')
QA.mkdir(parents=True, exist_ok=True)

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def milli(token):
    value = float(token)
    return round(value * 1000)

started = time.perf_counter()
protected = [SOURCE] + sorted(ROOT.glob('*.docx')) + sorted(ROOT.glob('*.pdf'))
hashes_before = {str(p): digest(p) for p in protected}
rows = 0
widths = Counter()
missing_tokens = Counter()
missing_columns = Counter()
invalid_numeric = Counter()
nonfinite = Counter()
negative = Counter()
zero = Counter()
fractional = Counter()
more_than_three_decimals = Counter()
stats = {}
missing_row_patterns = Counter()
invalid_timestamps = []
invalid_timestamp_count = 0
duplicates = 0
nonminute = 0
nonincreasing = 0
non60_steps = 0
time_gaps = []
date_cache = {}
seen_days = {}
hours = {}
missing_runs = []
run_start = None
run_count = 0
previous = None
first = None
last = None
minimum = None
maximum = None
full_numeric_rows = 0
residual_count = 0
negative_residual_count = 0
negative_residual_min = None
negative_residual_numerator = 0
negative_residual_examples = []
negative_residual_counts_by_tolerance = Counter()
delta_examples = []

with ZipFile(SOURCE) as archive:
    members = [{'name': m.filename, 'size': m.file_size, 'compressed_size': m.compress_size, 'crc32': f'{m.CRC:08x}'} for m in archive.infolist()]
    candidates = [m.filename for m in archive.infolist() if m.filename.lower().endswith('household_power_consumption.txt')]
    if len(candidates) != 1:
        raise RuntimeError(f'Ambiguous TXT: {candidates}')
    member = candidates[0]
    with archive.open(member) as stream:
        reader = csv.reader(io.TextIOWrapper(stream, encoding='utf-8-sig'), delimiter=';')
        columns = next(reader)
        numeric_names = columns[2:]
        stats = {name: {'valid': 0, 'min': None, 'max': None, 'sum': 0.0} for name in numeric_names}
        for row in reader:
            rows += 1
            widths[len(row)] += 1
            if len(row) != len(columns):
                continue
            stamp = None
            try:
                date_text, time_text = row[:2]
                if date_text not in date_cache:
                    date_cache[date_text] = datetime.strptime(date_text, '%d/%m/%Y')
                if len(time_text) != 8 or time_text[2] != ':' or time_text[5] != ':':
                    raise ValueError(time_text)
                hh, mm, ss = int(time_text[:2]), int(time_text[3:5]), int(time_text[6:8])
                stamp = date_cache[date_text].replace(hour=hh, minute=mm, second=ss)
                minute_pos = hh * 60 + mm
                daybits = seen_days.setdefault(stamp.date().isoformat(), bytearray(10800))
                second_pos = minute_pos * 60 + ss
                byte_pos, bit = divmod(second_pos, 8)
                if daybits[byte_pos] & (1 << bit):
                    duplicates += 1
                daybits[byte_pos] |= 1 << bit
                nonminute += int(ss != 0)
            except (ValueError, TypeError) as error:
                invalid_timestamp_count += 1
                if len(invalid_timestamps) < 20:
                    invalid_timestamps.append({'row': rows, 'values': row[:2], 'error': str(error)})
                stamp = None
            if stamp is not None:
                if first is None:
                    first = stamp
                last = stamp
                minimum = stamp if minimum is None else min(minimum, stamp)
                maximum = stamp if maximum is None else max(maximum, stamp)
                if previous is not None:
                    delta = int((stamp - previous).total_seconds())
                    nonincreasing += int(delta <= 0)
                    non60_steps += int(delta != 60)
                    if delta != 60 and len(time_gaps) < 20:
                        time_gaps.append({'previous': previous.isoformat(), 'current': stamp.isoformat(), 'seconds': delta})
                previous = stamp
                hour_key = stamp.replace(minute=0, second=0).isoformat()
                hour = hours.setdefault(hour_key, {'rows': 0, 'valid_power': 0, 'power_milli_sum': 0, 'missing_power': 0})
                hour['rows'] += 1
            values = []
            row_missing = []
            for name, token in zip(numeric_names, row[2:]):
                text = token.strip()
                value = None
                if text in ('', '?'):
                    missing_tokens[text or '<empty>'] += 1
                    missing_columns[name] += 1
                    row_missing.append(name)
                else:
                    try:
                        value = float(text)
                        if not math.isfinite(value):
                            nonfinite[name] += 1
                            value = None
                        else:
                            s = stats[name]
                            s['valid'] += 1
                            s['sum'] += value
                            s['min'] = value if s['min'] is None else min(s['min'], value)
                            s['max'] = value if s['max'] is None else max(s['max'], value)
                            negative[name] += int(value < 0)
                            zero[name] += int(value == 0)
                            fractional[name] += int(value != int(value))
                            more_than_three_decimals[name] += int(len(text.partition('.')[2].rstrip('0')) > 3)
                    except ValueError:
                        invalid_numeric[name] += 1
                values.append(value)
            if row_missing:
                missing_row_patterns['|'.join(row_missing)] += 1
            full_numeric_rows += int(all(value is not None for value in values))
            if stamp is not None:
                if values[0] is not None:
                    hour['valid_power'] += 1
                    hour['power_milli_sum'] += milli(row[2])
                else:
                    hour['missing_power'] += 1
                if values[0] is None:
                    if run_start is None:
                        run_start = stamp
                        run_count = 0
                    run_count += 1
                elif run_start is not None:
                    missing_runs.append({'start': run_start.isoformat(), 'end': (stamp - timedelta(minutes=1)).isoformat(), 'minutes': run_count})
                    run_start = None
                    run_count = 0
            if values[0] is not None and all(v is not None for v in values[4:]):
                residual_count += 1
                numerator = milli(row[2]) * 1000 - 60 * sum(milli(t) for t in row[6:9])
                residual_wh = numerator / 60000
                if numerator < 0:
                    negative_residual_count += 1
                    negative_residual_numerator += numerator
                    negative_residual_min = residual_wh if negative_residual_min is None else min(negative_residual_min, residual_wh)
                    for threshold in (0.01, 0.1, 0.5, 1.0):
                        negative_residual_counts_by_tolerance[str(threshold)] += int(residual_wh < -threshold)
                    if len(negative_residual_examples) < 10:
                        negative_residual_examples.append({'timestamp': stamp.isoformat() if stamp else row[:2], 'global_active_power_kw': values[0], 'sub_metering_wh': values[4:], 'residual_wh': residual_wh})
            if rows % 500000 == 0:
                print(f'Scanned {rows:,} rows in {time.perf_counter() - started:.1f}s', flush=True)
    if run_start is not None:
        missing_runs.append({'start': run_start.isoformat(), 'end': last.isoformat(), 'minutes': run_count})

ordered_hours = sorted(hours)
full_hours = [h for h in ordered_hours if hours[h]['rows'] == 60 and hours[h]['valid_power'] == 60]
full_set = set(full_hours)
incomplete_hours = [h for h in ordered_hours if h not in full_set]
partial_hours = [h for h in ordered_hours if hours[h]['rows'] != 60]
allmissing_hours = [h for h in ordered_hours if hours[h]['valid_power'] == 0]
valid_count_distribution = Counter(h['valid_power'] for h in hours.values())
contiguous_segments = []
segment_start = None
segment_hours = 0
for key in ordered_hours:
    complete = hours[key]['rows'] == 60 and hours[key]['valid_power'] == 60
    if complete:
        if segment_start is None:
            segment_start = key
            segment_hours = 0
        segment_hours += 1
        segment_end = key
    elif segment_start is not None:
        contiguous_segments.append({'start': segment_start, 'end': segment_end, 'hours': segment_hours})
        segment_start = None
if segment_start is not None:
    contiguous_segments.append({'start': segment_start, 'end': segment_end, 'hours': segment_hours})

for s in stats.values():
    s['mean'] = s['sum'] / s['valid'] if s['valid'] else None
period_samples = []
for key in [ordered_hours[0], full_hours[0], full_hours[len(full_hours) // 2], full_hours[-1], ordered_hours[-1]]:
    h = hours[key]
    period_samples.append({'hour': key, **h, 'energy_observed_kwh': h['power_milli_sum'] / 60000, 'complete': h['rows'] == 60 and h['valid_power'] == 60})
hashes_after = {str(p): digest(p) for p in protected}
report = {
    'scope': 'Full streaming audit only. No training dataset or Flink job/app produced.',
    'source': str(SOURCE), 'sha256': hashes_before[str(SOURCE)], 'members': members, 'member': member,
    'row_count': rows, 'columns': columns, 'separator': ';', 'date_format': '%d/%m/%Y', 'time_format': '%H:%M:%S',
    'width_distribution': dict(widths), 'numeric_stats': stats,
    'missing_cells': dict(missing_columns), 'missing_tokens': dict(missing_tokens),
    'missing_row_count': sum(missing_row_patterns.values()), 'missing_row_patterns': dict(missing_row_patterns),
    'all_numeric_valid_rows': full_numeric_rows, 'all_numeric_valid_percent': full_numeric_rows / rows * 100,
    'invalid_numeric': dict(invalid_numeric), 'nonfinite': dict(nonfinite), 'negative': dict(negative), 'zero': dict(zero),
    'fractional_values': dict(fractional), 'values_more_than_three_decimals': dict(more_than_three_decimals),
    'timestamps': {'first': first.isoformat(), 'last': last.isoformat(), 'min': minimum.isoformat(), 'max': maximum.isoformat(),
                   'invalid_examples': invalid_timestamps, 'invalid_count': invalid_timestamp_count,
                   'duplicates': duplicates, 'nonminute': nonminute, 'nonincreasing_steps': nonincreasing, 'steps_not_60_seconds': non60_steps, 'step_examples': time_gaps,
                   'unique_timestamp_bit_count': sum(byte.bit_count() for bits in seen_days.values() for byte in bits)},
    'hours': {'total': len(hours), 'full_60_rows_and_valid_power': len(full_hours), 'incomplete': len(incomplete_hours),
              'boundary_partial_count': len(partial_hours), 'boundary_partial': {h: hours[h] for h in partial_hours},
              'fully_missing_power': len(allmissing_hours), 'valid_power_count_distribution': dict(sorted(valid_count_distribution.items())),
              'power_milli_sum_all': sum(h['power_milli_sum'] for h in hours.values()), 'energy_observed_all_kwh': sum(h['power_milli_sum'] for h in hours.values()) / 60000,
              'energy_full_hours_kwh': sum(hours[h]['power_milli_sum'] for h in full_hours) / 60000,
              'full_hour_segments_count': len(contiguous_segments), 'full_hour_segments_top5': sorted(contiguous_segments, key=lambda x: x['hours'], reverse=True)[:5],
              'samples': period_samples},
    'missing_power_runs': {'count': len(missing_runs), 'max_minutes': max(r['minutes'] for r in missing_runs), 'top10': sorted(missing_runs, key=lambda r: r['minutes'], reverse=True)[:10]},
    'residual': {'valid_rows': residual_count, 'negative_rows': negative_residual_count, 'min_wh': negative_residual_min,
                 'negative_sum_wh': negative_residual_numerator / 60000, 'count_below_negative_threshold_wh': dict(negative_residual_counts_by_tolerance), 'examples': negative_residual_examples,
                 'method': 'Integer milli-kW/milli-Wh: (power_milli_kw*1000 - 60*sum(submeter_milli_wh))/60000. Raw values not modified; decimal precision audited.'},
    'sources_before': hashes_before, 'sources_after': hashes_after, 'sources_unchanged': hashes_before == hashes_after,
    'elapsed_seconds': time.perf_counter() - started,
    'limitations': ['Statistical extremes are not proven sensor faults.', 'Timezone/DST is not supplied by TXT; timestamps are naive source calendar labels.', 'No full-row business deduplication is applied. Exact timestamp uniqueness plus unique timestamps makes identical-row duplicates impossible for this source.'],
}
(QA / 'dataset-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: report[k] for k in ['row_count', 'missing_row_count', 'all_numeric_valid_percent', 'timestamps', 'hours', 'missing_power_runs', 'residual', 'sources_unchanged', 'elapsed_seconds']}, ensure_ascii=False, indent=2))
