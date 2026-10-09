import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from lxml import etree as E

from word_w01_content import NEW_REFERENCES

root = Path(__file__).resolve().parents[2]
source = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx'
with ZipFile(source) as z:
    rels = E.fromstring(z.read('word/_rels/document.xml.rels'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
    links = {r.get('Id'): r.get('Target') for r in rels if r.get('Type').endswith('/hyperlink')}
    body = E.fromstring(z.read('word/document.xml'))
    items = []
    for p in body.xpath('.//w:body/w:p', namespaces=ns):
        text = ''.join(p.xpath('.//w:t/text()', namespaces=ns))
        if text.startswith('['):
            for h in p.xpath('.//w:hyperlink', namespaces=ns):
                items.append({'reference': int(text[1:text.index(']')]), 'title': text[:text.find('Truy cập')].strip(), 'url': links[h.get('{' + ns['r'] + '}id')]})
items += [{'reference': i, 'title': title, 'url': url} for i, (title, url) in enumerate(NEW_REFERENCES, 17)]

def check(item):
    result = dict(item)
    try:
        response = urlopen(Request(item['url'], headers={'User-Agent': 'Mozilla/5.0 academic-reference-link-check'}), timeout=25)
        result.update(http_status=response.status, final_url=response.url, content_type=response.headers.get('content-type'), status='LINK_REACHABLE' if response.status == 200 else 'ACCESS_RESTRICTED_OR_ERROR')
        response.close()
    except HTTPError as error:
        result.update(status='ACCESS_RESTRICTED_OR_ERROR', http_status=error.code, error=str(error)[:250])
    except (URLError, TimeoutError) as error:
        result.update(status='NETWORK_UNVERIFIED', error=str(error)[:250])
    if 'doi.org/' in item['url']:
        doi = item['url'].split('doi.org/', 1)[1]
        try:
            response = urlopen('https://api.crossref.org/works/' + doi, timeout=25)
            if response.status == 200:
                data = json.load(response)['message']
                result['doi_metadata'] = {'title': data.get('title'), 'year': data.get('published', data.get('issued', {})).get('date-parts'), 'container': data.get('container-title'), 'page': data.get('page'), 'URL': data.get('URL'), 'DOI': data.get('DOI')}
                result['doi_status'] = 'REGISTERED_METADATA_VERIFIED'
            else:
                result['doi_status'] = 'UNVERIFIED'
        except (URLError, TimeoutError, ValueError):
            result['doi_status'] = 'UNVERIFIED'
    return result

with ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(check, items))
out = {'captured_at': datetime.now(timezone.utc).isoformat(), 'scope': 'URL reachability and DOI metadata only; not proof of full-text access', 'references': results, 'reachable': sum(r['status'] == 'LINK_REACHABLE' for r in results), 'restricted_or_unverified': [r['reference'] for r in results if r['status'] != 'LINK_REACHABLE']}
(root / '.agent/qa/word-w01-20261010/reference-audit.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=2))
