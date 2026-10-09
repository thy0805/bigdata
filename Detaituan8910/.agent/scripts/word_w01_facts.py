import csv
import hashlib
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w01-20261010'
W00 = ROOT / '.agent/qa/word-w00-20261010'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


inventory = read(W00 / 'sources.json')
guards = {}
for label in ['main', 'chapter1', 'chapter2', 'template', 'chapter2_outline']:
    item = inventory[label]
    guards[item['path']] = item['sha256']
guards.update(inventory['protected_extra'])
guards.update({str(ROOT / p): v for p, v in read(W00 / 'evidence-map.json')['source_signature'].items()})
bad = [p for p, value in guards.items() if sha(p) != value]
if bad:
    raise RuntimeError('Source drift: ' + repr(bad))
hourly_path = ROOT / 'data/processed/runs/20261009T102201900234-full/hourly-grid.csv'
with hourly_path.open(encoding='utf-8', newline='') as stream:
    rows = list(csv.DictReader(stream))
for row in rows:
    row['stamp'] = datetime.fromisoformat(row['hour_start'])
    for key in ['energy_kwh', 'observed_energy_kwh', 'sub1_observed_kwh', 'sub2_observed_kwh', 'sub3_observed_kwh']:
        row[key] = float(row[key]) if row[key] not in ('', 'NULL') else None
full = [row for row in rows if row['energy_kwh'] is not None]


def summary(selected):
    valid = [row for row in selected if row['energy_kwh'] is not None]
    low = min(valid, key=lambda row: row['energy_kwh'])
    high = max(valid, key=lambda row: row['energy_kwh'])
    return dict(hours=len(selected), complete_hours=len(valid), incomplete_hours=len(selected)-len(valid),
                observed_kwh=sum(row['observed_energy_kwh'] or 0 for row in selected),
                complete_kwh=sum(row['energy_kwh'] for row in valid),
                mean_kwh=statistics.mean(row['energy_kwh'] for row in valid),
                min_kwh=low['energy_kwh'], min_hour=low['hour_start'], max_kwh=high['energy_kwh'], max_hour=high['hour_start'],
                coverage=sum(int(row['valid_power_count']) for row in selected)/(len(selected)*60),
                subgroups_kwh=[sum(row[f'sub{i}_observed_kwh'] or 0 for row in selected) for i in range(1,4)])


def profile(key):
    result = []
    for value in sorted({key(row['stamp']) for row in full}):
        values = [row['energy_kwh'] for row in full if key(row['stamp']) == value]
        result.append(dict(value=value, complete_hours=len(values), mean_kwh=statistics.mean(values)))
    return result


prediction_path = ROOT / 'models/runs/20261009-phase2b2-a/predictions-test.csv'
with prediction_path.open(encoding='utf-8', newline='') as stream:
    predictions = list(csv.DictReader(stream))
facts = dict(scope='Read existing hourly and saved predictions only; no new inference, fit, Flink run or official Test metric computation',
             captured_at=datetime.now(timezone.utc).isoformat(), hourly_sha256=sha(hourly_path), predictions_sha256=sha(prediction_path),
             hourly_columns=list(rows[0].keys())[:-1], full_dataset=summary(rows),
             example_period_20101120_26=summary([row for row in rows if datetime(2010,11,20) <= row['stamp'] < datetime(2010,11,27)]),
             hour_profile=profile(lambda stamp: stamp.hour), weekday_profile=profile(lambda stamp: stamp.weekday()),
             month_profile=profile(lambda stamp: stamp.month), prediction_columns=list(predictions[0]), first_five_predictions=predictions[:5],
             verified_inputs={p: sha(p) for p in guards})
QA.mkdir(parents=True, exist_ok=True)
(QA / 'preflight.json').write_text(json.dumps(dict(status='VERIFIED', source_checkpoint='ff0e5d7', guards=guards, checks=len(guards), changed=bad), ensure_ascii=False, indent=2), encoding='utf-8')
(QA / 'report-facts.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k:v for k,v in facts.items() if k in ['full_dataset','example_period_20101120_26','prediction_columns','first_five_predictions','hour_profile','weekday_profile','month_profile']}, ensure_ascii=False))
