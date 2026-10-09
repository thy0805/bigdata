import csv
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'pipeline'))
from cluster import environment, fetch, FLINK
from run_full import generate_full, parts, save

QA = ROOT / '.agent/qa/phase1-full-20261009'
cases = [('1/1/2007', False), ('01/01/2007', False), ('9/12/2007', False), ('10/2/2008', False), ('29/2/2008', False), ('31/2/2008', True), ('29/2/2007', True), ('0/1/2007', True), ('1/13/2007', True), ('001/1/2007', True), ('1/1/07', True)]
run = QA / ('date-parser-' + datetime.now().strftime('%Y%m%dT%H%M%S%f'))
run.mkdir()
source = run / 'fixture.txt'
with source.open('w', newline='') as stream:
    writer = csv.writer(stream, delimiter=';')
    writer.writerow(['Date', 'Time', 'Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'])
    for date, invalid in cases:
        writer.writerow([date, '12:00:00', '1.000', '0.100', '230.000', '4.000', '0.000', '0.000', '0.000'])
sql = run / 'job.sql'
sql.write_text(generate_full(source, run / 'output', 'uci-date-parser-fixture'))
before = {j['jid'] for j in fetch('/jobs/overview')['jobs']}
with (run / 'sql-client.log').open('w') as log:
    result = subprocess.run([str(FLINK / 'bin/sql-client.sh'), '-f', str(sql)], env=environment(), stdout=log, stderr=subprocess.STDOUT, timeout=180)
jobs = [j for j in fetch('/jobs/overview')['jobs'] if j['jid'] not in before]
rows = {r[0]: r for r in parts(run / 'output/minutes')}
checks = [{'date': date, 'expected_parse_error': invalid, 'actual': rows.get(date), 'passed': date in rows and rows[date][3] == str(invalid).lower()} for date, invalid in cases]
runtime = len(jobs) == 1 and jobs[0]['state'] == 'FINISHED' and result.returncode == 0 and '[ERROR]' not in (run / 'sql-client.log').read_text()
report = {'scope': 'QA-only synthetic dates, never product', 'jobs': jobs, 'runtime_passed': runtime, 'checks': checks, 'passed': runtime and all(c['passed'] for c in checks), 'run': str(run)}
save(QA / 'date-parser-verification.json', report)
print(json.dumps(report, indent=2), flush=True)
raise SystemExit(0 if report['passed'] else 2)
