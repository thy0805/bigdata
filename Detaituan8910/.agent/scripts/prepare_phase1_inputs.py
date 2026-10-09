import csv
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(r'D:\Hoctap\bigdata\Detaituan8910')
QA = ROOT / '.agent/qa/phase1-smoke-20261009'
AUDIT = json.loads((ROOT / '.agent/qa/phase0-20261008/dataset-audit.json').read_text(encoding='utf-8'))

def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            value.update(block)
    return value.hexdigest()

guard = {path: digest(path) for path in AUDIT['sources_before']}
assert guard == AUDIT['sources_before']
raw = ROOT / 'data/raw/household_power_consumption.txt'
raw.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(AUDIT['source']) as archive:
    with archive.open(AUDIT['member']) as stream:
        original_hash = hashlib.sha256()
        if not raw.exists():
            with raw.open('xb') as output:
                for block in iter(lambda: stream.read(1048576), b''):
                    original_hash.update(block)
                    output.write(block)
        else:
            for block in iter(lambda: stream.read(1048576), b''):
                original_hash.update(block)
assert digest(raw) == original_hash.hexdigest()
fixtures = QA / 'inputs'
fixtures.mkdir(exist_ok=True)
real = fixtures / 'real-10000.txt'
with raw.open('rb') as source, real.open('wb') as output:
    output.write(source.readline())
    for index in range(10000):
        output.write(source.readline())

header = AUDIT['columns']
def row(stamp, power='1', subs=('10', '10', '10')):
    return [stamp.strftime('%d/%m/%Y'), stamp.strftime('%H:%M:%S'), power, '0.1', '230', '5', *subs]

def write(name, rows):
    with (fixtures / name).open('w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output, delimiter=';', lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)

start = datetime(2006, 1, 1)
rows = []
for hour in range(7):
    if hour == 5:
        continue
    for minute in range(60):
        item = row(start + timedelta(hours=hour, minutes=minute))
        if hour == 1 and minute == 59:
            item[2] = '?'
        if hour == 2:
            item[2:] = ['?', '?', '?', '?', '?', '?', '']
        if hour == 3:
            item[2] = '0.6'
        if hour == 4 and minute == 0:
            item = row(start + timedelta(hours=hour), power='0.06', subs=('10', '10', '10'))
        rows.append(item)
write('edge-cases.txt', rows)
write('duplicate.txt', [row(start), row(start)])
write('invalid-number.txt', [row(start, power='abc')])
write('invalid-time.txt', [['31/02/2006', '00:00:00', *row(start)[2:]]])
write('bad-structure.txt', [row(start)[:-1]])
write('extra-column.txt', [row(start) + ['extra']])
write('header-lookalike.txt', [['Date', 'Time', 'changed', *header[3:]]])
write('zero.txt', [row(start + timedelta(minutes=i), power='0', subs=('0', '0', '0')) for i in range(60)])
write('precision.txt', [row(start, power='0.018', subs=('0.1', '0.2', '0')), row(start + timedelta(minutes=1), power='0.012', subs=('0.1', '0.1', '0'))])
result = {
    'captured_at': datetime.now().astimezone().isoformat(),
    'source_zip': AUDIT['source'], 'source_zip_sha256': digest(AUDIT['source']),
    'raw_path': str(raw), 'raw_bytes': raw.stat().st_size, 'raw_sha256': digest(raw),
    'raw_matches_zip_member_bytes': digest(raw) == original_hash.hexdigest(),
    'sample_rows': 10000, 'real_sample_sha256': digest(real),
    'fixtures_are_test_only': True, 'source_hashes_before': guard,
    'disk_after_preparation': {'C': shutil.disk_usage('C:/')._asdict(), 'D': shutil.disk_usage('D:/')._asdict()},
}
(QA / 'inputs-manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
