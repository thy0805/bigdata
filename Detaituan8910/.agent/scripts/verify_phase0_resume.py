import csv
import hashlib
import io
import json
import subprocess
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

ROOT = Path(r'D:\Hoctap\bigdata\Detaituan8910')
QA = ROOT / '.agent/qa/phase0-resume-20261009'
QA.mkdir(parents=True, exist_ok=True)
AUDIT = ROOT / '.agent/qa/phase0-20261008/dataset-audit.json'
PROBE = '/mnt/d/Hoctap/bigdata/Detaituan8910/.agent/scripts/probe_linux_phase0_resume.py'

def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            value.update(block)
    return value.hexdigest()

def command(args):
    result = subprocess.run(args, capture_output=True, timeout=25)
    def decode(value):
        return value.decode('utf-16-le' if b'\x00' in value else 'utf-8', errors='replace').strip()
    return {'exit_code': result.returncode, 'stdout': decode(result.stdout), 'stderr': decode(result.stderr)}

environment = {'captured_at': datetime.now().astimezone().isoformat(), 'wsl_status': command(['wsl', '--status']), 'wsl_version': command(['wsl', '--version']), 'wsl_distros': command(['wsl', '-l', '-v'])}
linux = command(['wsl', '-d', 'Ubuntu-24.04', '--', 'python3', PROBE])
environment['linux'] = json.loads(linux['stdout']) if linux['exit_code'] == 0 else linux
server = subprocess.Popen(['wsl', '-d', 'Ubuntu-24.04', '--', 'python3', '-u', PROBE, '--http-probe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
try:
    port = json.loads(server.stdout.readline())['port']
    with urlopen(f'http://127.0.0.1:{port}/', timeout=8) as response:
        environment['windows_to_wsl_http'] = {'port': port, 'status': response.status, 'body': response.read().decode()}
    server.communicate(timeout=18)
    environment['http_probe_exit'] = server.returncode
except Exception as error:
    environment['windows_to_wsl_http'] = {'error': str(error)}
    server.communicate(timeout=20)
(QA / 'environment.json').write_text(json.dumps(environment, ensure_ascii=False, indent=2), encoding='utf-8')

audit = json.loads(AUDIT.read_text(encoding='utf-8'))
source = Path(audit['source'])
hash_before = digest(source)
checks = {'zip_hash_matches_full_audit': hash_before == audit['sha256']}
with ZipFile(source) as archive:
    member = archive.getinfo(audit['member'])
    checks['zip_member_metadata_matches'] = member.file_size == audit['members'][0]['size'] and f'{member.CRC:08x}' == audit['members'][0]['crc32']
    frame = []
    with archive.open(member) as stream:
        reader = csv.DictReader(io.TextIOWrapper(stream, encoding='utf-8-sig'), delimiter=';')
        checks['schema_matches'] = reader.fieldnames == audit['columns']
        for number, row in enumerate(reader):
            frame.append(row)
            if number == 9999:
                break
hour_sums = {}
for row in frame:
    stamp = datetime.strptime(row['Date'] + ' ' + row['Time'], '%d/%m/%Y %H:%M:%S')
    key = stamp.replace(minute=0, second=0).isoformat()
    value = hour_sums.setdefault(key, {'count': 0, 'valid': 0, 'power': Decimal(0)})
    value['count'] += 1
    if row['Global_active_power'].strip() not in ('', '?'):
        value['valid'] += 1
        value['power'] += Decimal(row['Global_active_power'])
samples = []
for sample in audit['hours']['samples'][:2]:
    value = hour_sums[sample['hour']]
    match = value['count'] == sample['rows'] and value['valid'] == sample['valid_power'] and value['power'] * 1000 == sample['power_milli_sum']
    checks['hour_' + sample['hour']] = match
    samples.append({'hour': sample['hour'], 'rows': value['count'], 'valid': value['valid'], 'independent_decimal_energy_kwh': str(value['power'] / 60), 'matches_audit': match})
start = datetime.fromisoformat(audit['timestamps']['first'])
end = datetime.fromisoformat(audit['timestamps']['last'])
checks['row_count_matches_minute_span'] = int((end-start).total_seconds()/60)+1 == audit['row_count']
checks['hour_count_matches_hour_span'] = int((end.replace(minute=0)-start.replace(minute=0)).total_seconds()/3600)+1 == audit['hours']['total']
distribution = audit['hours']['valid_power_count_distribution']
checks['distribution_matches_hour_count'] = sum(distribution.values()) == audit['hours']['total']
checks['distribution_matches_valid_power_count'] = sum(int(k)*v for k,v in distribution.items()) == audit['numeric_stats']['Global_active_power']['valid']
checks['missing_plus_valid_equals_rows'] = audit['missing_row_count'] + audit['all_numeric_valid_rows'] == audit['row_count']
checks['complete_plus_incomplete_equals_hours'] = audit['hours']['full_60_rows_and_valid_power'] + audit['hours']['incomplete'] == audit['hours']['total']
checks['hash_unchanged_after_read'] = digest(source) == hash_before
protected = {path: {'expected': expected, 'actual': digest(path)} for path, expected in audit['sources_after'].items() if Path(path).exists()}
checks['protected_sources_unchanged'] = all(entry['expected'] == entry['actual'] for entry in protected.values())
report = {'captured_at': datetime.now().astimezone().isoformat(), 'source': str(source), 'sha256': hash_before, 'audit_artifact_sha256': digest(AUDIT), 'method': 'Reuse prior full scan; independently parse first 10000 rows using Decimal, check sample hours, timestamp-span and count invariants, and verify protected hashes. Not a second full dataset scan.', 'sample_rows_read': len(frame), 'checks': checks, 'samples': samples, 'protected_sources': protected}
(QA / 'dataset-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'environment': environment, 'dataset_checks': checks, 'samples': samples}, ensure_ascii=False, indent=2))
sys.exit(0 if all(checks.values()) else 1)
