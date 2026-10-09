from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E

root = Path(__file__).resolve().parents[2]
path = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
with ZipFile(path) as z:
    parts = {name: z.read(name) for name in z.namelist()}
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
doc = E.fromstring(parts['word/document.xml'])
rels = E.fromstring(parts['word/_rels/document.xml.rels'])
old = 'https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/table/sql/queries/group-agg/'
new = 'https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/group-agg/'
for rel in rels:
    if rel.get('Target') == old:
        rel.set('Target', new)
for p in doc.xpath('.//w:body/w:p', namespaces=ns):
    text = ''.join(p.xpath('.//w:t/text()', namespaces=ns))
    if any(text.startswith(f'[{i}]') for i in range(17, 22)):
        for t in p.xpath('.//w:t', namespaces=ns):
            t.text = t.text.replace(old, new).replace('developers (2025)', 'developers (n.d.)').replace('Foundation (2026)', 'Foundation (n.d.)')
parts['word/document.xml'] = E.tostring(doc, encoding='UTF-8', xml_declaration=True, standalone=True)
parts['word/_rels/document.xml.rels'] = E.tostring(rels, encoding='UTF-8', xml_declaration=True, standalone=True)
with ZipFile(path, 'w', ZIP_DEFLATED) as z:
    for name, data in parts.items():
        z.writestr(name, data)
print('Reference path corrected against W00 S14; unverified publication years removed.')
