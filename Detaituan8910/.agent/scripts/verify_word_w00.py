import hashlib
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w00-20261010'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


checks = []


def check(name, passed, evidence=None):
    checks.append(dict(name=name, passed=bool(passed), evidence=evidence))


inventory = read(QA / 'sources.json')
for label in ['main', 'chapter1', 'chapter2', 'template', 'chapter2_outline']:
    source = inventory[label]
    check(f'original_unchanged:{label}', digest(source['path']) == source['sha256'])
    data = read(QA / f'{label}-inspection.json')
    check(f'package_readback:{label}', data['crc_error'] is None and data['sha256'] == source['sha256'])
for path, expected in inventory['protected_extra'].items():
    check(f'protected_source:{Path(path).name}', digest(path) == expected)

old_word = read(ROOT / '.agent/qa/word-uci-cover-citations-20261008/final-word.json')
main = read(QA / 'main-inspection.json')
hau = read(QA / 'chapter2-inspection.json')
preview = read(QA / 'chapter2-preview.json')
check('main_render_reuse_same_bytes', inventory['main']['sha256'] == 'efc3acdfec05bc264eb3320f2df363241cab29818830a7159cc88aabdb77bdd1' and old_word['pages'] == 37)
check('main_counts', main['top_level_tables'] == 7 and main['drawings'] == 3 and main['equations'] == 3)
check('chapter2_fresh_readonly_preview', preview['read_only'] and not preview['saved_to_source'] and preview['pages'] == 13)
check('chapter2_has14_sections', len(preview['headings']) == 14 and [int(re.match(r'2\.(\d+)\.', b['text']).group(1)) for b in preview['headings']] == list(range(1, 15)))
check('chapter2_source_counts', hau['paragraphs'] == 152 and hau['top_level_tables'] == 0 and hau['drawings'] == 0 and hau['equations'] == 0)
all_body = main['blocks']
end_index = next(i for i,b in enumerate(all_body) if b.get('text') == 'TÀI LIỆU THAM KHẢO' and b.get('style') == 'Heading11')
body_text = '\n'.join(b.get('text', '') if b['kind'] == 'paragraph' else '\n'.join(' '.join(row) for row in b['rows']) for b in all_body[:end_index])
references = [b for b in all_body[end_index:] if re.match(r'^\[\d+\]', b.get('text',''))]
check('body_no_bracket_citations', not re.search(r'\[\d+\]', body_text))
check('sixteen_end_references', len(references) == 16)

schema_path = ROOT / 'data/ml/runs/20261009-phase2a-a/feature-schema.json'
schema = read(schema_path)
split_path = ROOT / 'data/ml/runs/20261009-phase2a-a/split-summary.json'
split = read(split_path)
metrics_path = ROOT / 'models/runs/20261009-phase2b2-a/metrics-test.json'
metrics = read(metrics_path)
final_path = ROOT / 'models/final/hgb-uci-hourly-v1.0-train-only/manifest.json'
final = read(final_path)
flink_path = ROOT / 'data/processed/runs/20261009T102201900234-full/verification.json'
flink = read(flink_path)
model_config = read(ROOT / 'models/runs/20261009-phase2b1-a2/model-config.json')
sql_path = ROOT / '.agent/qa/phase1-full-20261009/runs/20261009T102201900234-full/job.sql'
sql = sql_path.read_text(encoding='utf-8')
check('actual_sql_batch_grouping_not_watermark', "'execution.runtime-mode' = 'BATCH'" in sql and 'GROUP BY FLOOR(event_time TO HOUR)' in sql and 'WATERMARK' not in sql and 'TUMBLE(' not in sql)
check('split_counts_and_schema', [split[k]['eligible_hours'] for k in ['train','validation','test']] == [22513,4727,4590] and len(schema['feature_columns']) == 11 and schema['feature_columns'] == final['feature_columns'])
check('test_metrics_match_locked_manifest', metrics == final['test_metrics'] and metrics['n'] == 4590 and not metrics['refit'] and metrics['models']['hgb']['mae_kwh'] == 0.3220542588291146 and metrics['models']['hgb']['rmse_kwh'] == 0.4634874854716987)
check('fit_and_parameters_locked', final['fitted_rows'] == 22513 and final['no_refit'] and model_config['approved_parameters']['early_stopping'] is False and model_config['approved_parameters']['max_iter'] == 200)
check('audit_hour_counts', flink['audit']['hours'] == 34589 and flink['audit']['complete_hours'] == 34085 and flink['audit']['incomplete_hours'] == 504)

guide = read(ROOT / '.agent/qa/phase4-data-guide-20261010/technical-verification.json')
signatures = guide['source_signature']
signature_bad = [path for path,expected in signatures.items() if digest(ROOT / path) != expected]
check('locked_source_signature', not signature_bad, dict(total=len(signatures), changed=signature_bad))
frozen = read(ROOT / '.agent/qa/phase4-app-20261009/preflight.json')['files']
changed, missing = [], []
unreadable = []
linux_readback = []
count = 0
for path, expected in frozen.items():
    local = Path(re.sub(r'^/mnt/([a-z])/', lambda match: match.group(1).upper()+':/', path))
    if local == ROOT / 'dashboard/app.py':
        expected = inventory['protected_extra'][str(ROOT / 'dashboard/app.py')]
    try:
        if not local.is_file():
            missing.append(path)
        elif digest(local) != expected:
            changed.append(path)
        else:
            count += 1
    except OSError as error:
        probe = subprocess.run(['wsl.exe','-d','Ubuntu-24.04','--','sha256sum','--',path], capture_output=True, text=True, timeout=30)
        if probe.returncode == 0 and probe.stdout.split()[0] == expected:
            count += 1
            linux_readback.append(path)
        else:
            unreadable.append(dict(path=path,error=str(error),linux_returncode=probe.returncode,linux_stderr=probe.stderr))
check('readable_products_and_code_preserved_since_accepted_ui', not changed and not missing and not unreadable and count == len(frozen), dict(total=len(frozen), matching=count, changed=changed, missing=missing, unreadable=unreadable, unreadable_status='NOT_VERIFIED' if unreadable else 'All sources readable and hash matched', linux_symlink_readback=linux_readback, app_expected='accepted UI at 0d7aa09, not pre-expander snapshot'))

files = ['W00_REVIEW.md','CHAPTER2_REVIEW.md','TABLE_FIGURE_PLAN.md','DRAFTS_FOR_APPROVAL.md','SOURCES.md']
documents = {name:(QA / name).read_text(encoding='utf-8') for name in files}
check('proposal_files_nonempty', all(len(value) > 1000 for value in documents.values()))
rows = re.findall(r'^\| 2\.(\d+), tr\.', documents['CHAPTER2_REVIEW.md'], flags=re.M)
check('fourteen_review_rows', [int(i) for i in rows] == list(range(1,15)))
images = re.findall(r'^\| IMG-(\d+) \|', documents['TABLE_FIGURE_PLAN.md'], flags=re.M)
check('eight_planned_images_not_inserted', images == [f'{i:02d}' for i in range(1,9)] and not list(QA.glob('*.docx')))
check('proposal_exact_metrics_rounding', '0,3221 kWh' in documents['DRAFTS_FOR_APPROVAL.md'] and '0,4635 kWh' in documents['DRAFTS_FOR_APPROVAL.md'])
check('all_semantic_sources_exist', all(p.is_file() for p in [schema_path,split_path,metrics_path,final_path,flink_path,sql_path]))
check('contact_sheets_available', all((QA / name).is_file() for name in ['main-contact-1.png','main-contact-2.png','main-contact-3.png','main-contact-4.png','chapter2-contact-1.png','chapter2-contact-2.png']))
pending_outputs = list(ROOT.glob('*W01*.docx'))
check('no_w01_word_created', not pending_outputs)

evidence = dict(source_checkpoint=inventory['git_head'], scope='W00 read-only survey and proposal; no fit/predict/evaluate/rerun',
                sources={label:{k:v for k,v in item.items() if k != 'path'} for label,item in inventory.items() if isinstance(item,dict) and 'sha256' in item},
                source_signature=signatures, hourly_audit=flink['audit'], feature_columns=schema['feature_columns'], splits=split,
                hgb_config=model_config['approved_parameters'], test_metrics=metrics, source_paths={
                    'sql':sql_path.relative_to(ROOT).as_posix(), 'schema':schema_path.relative_to(ROOT).as_posix(),
                    'split':split_path.relative_to(ROOT).as_posix(),'metrics':metrics_path.relative_to(ROOT).as_posix(),'model':final_path.relative_to(ROOT).as_posix()},
                visual_review=dict(main='37-page contact sheets; detailed pages1,2,20,26; prior same-hash render reused',
                                   chapter2='13-page contact sheets; detailed page8; fresh read-only Word export',
                                   fresh_main_reflow=False, app_screenshots_created=False),
                proposal_hashes={name:digest(QA / name) for name in files})
(QA / 'evidence-map.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
result = dict(status='VERIFIED' if all(c['passed'] for c in checks) else 'APPLIED_UNVERIFIED', captured_at=datetime.now(timezone.utc).isoformat(),
              total_checks=len(checks),passed=sum(c['passed'] for c in checks),checks=checks,
              scope='W00 proposal only; not final DOCX verification or new application QA',
              pending=['Thy/GPT Web approve W01','W01 Word and black placeholders','W02 real screenshots','unconfirmed work schedule/contribution','all16 old references live/content re-audit'] + (['historical Linux venv-probe symlinks NOT_VERIFIED on this Windows environment'] if unreadable else []),
              unchanged=['five DOCX sources','rules','application source','operations source','locked dataset/hourly/features/splits/model/metrics','existing QA'],
              not_performed=['model training/refit','new Test evaluation','Flink rerun','app UI changes/screenshots','DOCX writes','W01/W02/I04/PPT'])
(QA / 'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status=result['status'],passed=result['passed'],total=result['total_checks'],failed=[c for c in checks if not c['passed']]),ensure_ascii=False))
