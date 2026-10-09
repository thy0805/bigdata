import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(r'D:\Hoctap\bigdata\Detaituan8910')
DOCS = ROOT / 'docs/phase0-20261008'
QA = ROOT / '.agent/qa/phase0-resume-20261009'
NAMES = ['DATA_AUDIT.md', 'TECHNICAL_ARCHITECTURE.md', 'APP_UI_SPEC.md', 'IMPLEMENTATION_PLAN.md', 'OPEN_DECISIONS.md']
audit = json.loads((ROOT / '.agent/qa/phase0-20261008/dataset-audit.json').read_text(encoding='utf-8'))
dataset = json.loads((QA / 'dataset-verification.json').read_text(encoding='utf-8'))
environment = json.loads((QA / 'environment.json').read_text(encoding='utf-8'))
texts = {name: (DOCS / name).read_text(encoding='utf-8') for name in NAMES}

def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            value.update(block)
    return value.hexdigest()

checks = {'five_documents_exist': len(texts) == 5, 'dataset_checks_pass': all(dataset['checks'].values()), 'wsl_version_2': re.search(r'Ubuntu-24\.04\s+Running\s+2', environment['wsl_distros']['stdout']) is not None, 'linux_python_312': environment['linux']['python'].startswith('3.12.'), 'localhost_probe_pass': environment['windows_to_wsl_http'].get('body') == 'phase0-wsl-localhost-ok' and environment.get('http_probe_exit') == 0, 'pyflink_not_installed': environment['linux']['packages']['apache-flink'] is None, 'cp312_wheel_exists': bool(environment['linux']['https_pypi'].get('cp312_linux_wheels'))}
local_links = []
urls = set()
for name, body in texts.items():
    checks[name + '_has_title'] = body.startswith('# ')
    checks[name + '_utf8_no_replacement_or_thai'] = '\ufffd' not in body and re.search(r'[\u0e00-\u0e7f]', body) is None
    checks[name + '_balanced_fences'] = body.count('```') % 2 == 0
    for target in re.findall(r'\]\(([^)]+)\)', body):
        if target.startswith('https://'):
            urls.add(target)
        elif not target.startswith('#'):
            resolved = ((DOCS / target.split('#')[0]).resolve())
            local_links.append({'document': name, 'target': target, 'exists': resolved.exists()})
checks['local_links_resolve'] = all(entry['exists'] for entry in local_links)
data_text = texts['DATA_AUDIT.md']
for key, value in [('rows', audit['row_count']), ('missing', audit['missing_row_count']), ('total_hours', audit['hours']['total']), ('full_hours', audit['hours']['full_60_rows_and_valid_power']), ('incomplete', audit['hours']['incomplete']), ('residual_negative', audit['residual']['negative_rows'])]:
    checks['audit_number_' + key] = format(value, ',').replace(',', '.') in data_text
checks['audit_hash_in_doc'] = audit['sha256'] in data_text
checks['sample_not_claimed_full_rescan'] = 'không phải lần kiểm độc lập thứ hai trên mọi dòng' in data_text
checks['missing_policy_keeps_grid_and_null'] = all(term in data_text for term in ['Giữ trục đủ 34.589 giờ', 'NULL cho giờ không đầy đủ', 'không nội suy'])
architecture = texts['TECHNICAL_ARCHITECTURE.md']
checks['no_claim_flink_running'] = 'chưa cài Flink hoặc thực thi pipeline' in architecture
checks['sql_is_real_flink_not_pandas'] = all(term in architecture for term in ['Flink SQL', 'Không tiền tổng hợp giờ bằng Pandas', 'CSV nhiều part'])
checks['bounded_not_fake_realtime'] = all(term in architecture for term in ['BATCH', 'Chưa có job kiểm Event Time watermark', 'không gọi replay là công tơ trực tiếp'])
checks['storage_reality_flagged'] = 'không đồng nghĩa ổ C thật còn dung lượng đó' in architecture
plan = texts['IMPLEMENTATION_PLAN.md']
checks['phase1_requires_approval'] = 'Giai đoạn 1 chưa được phê duyệt' in plan and 'Chỉ sau phê duyệt Giai đoạn 1 mới F01' in plan
checks['forecast_leakage_guards'] = all(term in plan for term in ['Không random split', 'early_stopping=False', 'full hourly grid', 'không nhìn test', 'cùng eligible timestamps'])
checks['ui_3_tabs_and_history'] = all(term in texts['APP_UI_SPEC.md'] for term in ['Tổng quan, Phân tích, Dự báo', 'không chọn mốc tương lai hôm nay', 'không chạy full Flink job hoặc train lại'])
checks['locked_choices_not_reopened'] = all(term in texts['OPEN_DECISIONS.md'] for term in ['LOCKED theo Thy', 'Không London, không nhiều hộ', 'không còn quyết định'])
checks['source_hashes_still_match'] = all(digest(path) == expected for path, expected in audit['sources_after'].items())

def check_url(url):
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=15) as response:
            return {'url': url, 'status': response.status, 'final_url': response.url}
    except Exception as error:
        return {'url': url, 'error': str(error)}

with ThreadPoolExecutor(max_workers=6) as pool:
    links = list(pool.map(check_url, sorted(urls)))
checks['official_links_http_ok'] = all(entry.get('status') == 200 for entry in links)
report = {'captured_at': datetime.now().astimezone().isoformat(), 'checks': checks, 'passed': sum(checks.values()), 'total': len(checks), 'documents': {name: {'sha256': digest(DOCS/name), 'bytes': (DOCS/name).stat().st_size, 'lines': body.count('\n')} for name,body in texts.items()}, 'local_links': local_links, 'official_links': links, 'limits': ['No Flink install/job/model/UI runtime was executed. Version compatibility is based on official documentation and release wheel metadata, not a dependency-install test.', 'Reuse full dataset scan with matching hash; current independent recalculation covers 10000 rows and two hours, not every record.']}
(QA / 'documents-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
