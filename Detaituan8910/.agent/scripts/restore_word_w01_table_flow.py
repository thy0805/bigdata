import json
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree as E

root = Path(__file__).resolve().parents[2]
qa = root / '.agent/qa/word-w01-20261010'
path = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
source = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx'
n = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + n['w'] + '}'
with ZipFile(source) as z:
    old = E.fromstring(z.read('word/document.xml'))
with ZipFile(path) as z:
    parts = {key: z.read(key) for key in z.namelist()}
doc = E.fromstring(parts['word/document.xml'])
old_tables = old.xpath('/w:document/w:body/w:tbl', namespaces=n)
tables = doc.xpath('/w:document/w:body/w:tbl', namespaces=n)
assert len(old_tables) == 7 and len(tables) == 18
restored = []
for index, (prior, table) in enumerate(zip(old_tables, tables), 1):
    prior_ps = prior.xpath('.//w:p', namespaces=n)
    ps = table.xpath('.//w:p', namespaces=n)
    for number, p in enumerate(ps):
        pr = p.find(W + 'pPr')
        if pr is None:
            continue
        for keep in pr.findall(W + 'keepNext'):
            pr.remove(keep)
        if number < len(prior_ps):
            keeps = prior_ps[number].xpath('./w:pPr/w:keepNext', namespaces=n)
            for keep in keeps:
                pr.append(deepcopy(keep))
    restored.append({'table': index, 'source_paragraphs': len(prior_ps), 'current_paragraphs': len(ps)})
parts['word/document.xml'] = E.tostring(doc, encoding='UTF-8', xml_declaration=True, standalone=True)
with ZipFile(path, 'w', ZIP_DEFLATED) as z:
    for key, value in parts.items():
        z.writestr(key, value)
(qa / 'table-flow-repair.json').write_text(json.dumps({'status': 'APPLIED_UNVERIFIED', 'reason': 'Width selector unintentionally chained source abbreviation table; restore source keepNext only, preserving new terms.', 'restored': restored, 'source_modified': False}, ensure_ascii=False, indent=2), encoding='utf-8')
print('Restored source table flow; render pending')
