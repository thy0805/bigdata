import hashlib
import json
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E

root = Path(r'D:\Hoctap\bigdata')
qa = root / 'Detaituan8910/.agent/qa/diennang-mssv-20261006'
source = root / 'BaoCao_PhanTich_DuDoan_DienNang_Khung.docx'
expected = 'd2199f0a30ba74234778622d14f4757736faea2eeddfd0d560d162c4f4deacdd'
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
output = root / 'BaoCao_PhanTich_DuDoan_DienNang_Khung_v2.docx'
index = 3
while output.exists():
    output = root / f'BaoCao_PhanTich_DuDoan_DienNang_Khung_v{index}.docx'
    index += 1
with ZipFile(source) as z:
    parts = {n: z.read(n) for n in z.namelist()}
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
w = '{' + ns['w'] + '}'
original = E.fromstring(parts['word/document.xml'])
doc = deepcopy(original)
placeholder = doc.xpath('//w:t[contains(text(),"[MSSV]")]', namespaces=ns)
assert len(placeholder) == 1 and 'Nguyễn Đức Thành Phát' in placeholder[0].text
placeholder[0].text = placeholder[0].text.replace('[MSSV]', '2001230640')
table = doc.find('w:body/w:tbl', ns)
row = table.findall(w + 'tr')[1]
cells = row.findall(w + 'tc')
assert ''.join(cells[2].xpath('.//w:t/text()', namespaces=ns)) == 'Nguyễn Đức Thành Phát'
cell = cells[1]
assert not ''.join(cell.xpath('.//w:t/text()', namespaces=ns)).strip()
saved_cell = deepcopy(cell)
p = cell.find(w + 'p')
run = p.find(w + 'r')
if run is None:
    run = E.SubElement(p, w + 'r')
value = run.find(w + 't')
if value is None:
    value = E.SubElement(run, w + 't')
value.text = '2001230640'
reversed_doc = deepcopy(doc)
reversed_placeholder = reversed_doc.xpath('//w:t[contains(text(),"Nguyễn Đức Thành Phát")]', namespaces=ns)[0]
reversed_placeholder.text = reversed_placeholder.text.replace('2001230640', '[MSSV]')
reversed_row = reversed_doc.find('w:body/w:tbl', ns).findall(w + 'tr')[1]
reversed_row.replace(reversed_row.findall(w + 'tc')[1], saved_cell)
assert E.tostring(reversed_doc, method='c14n') == E.tostring(original, method='c14n')
parts['word/document.xml'] = E.tostring(doc, encoding='UTF-8', xml_declaration=True, standalone=True)
with ZipFile(output, 'x') as z:
    for name, data in parts.items():
        z.writestr(name, data)
with ZipFile(source) as original_zip, ZipFile(output) as final_zip:
    changed = [n for n in original_zip.namelist() if original_zip.read(n) != final_zip.read(n)]
assert changed == ['word/document.xml']
manifest = {'source': str(source), 'source_sha256': expected, 'output': str(output), 'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'mssv': '2001230640', 'changes': ['cover placeholder', 'Phát MSSV assignment cell'], 'changed_parts': changed, 'reverse_edit_restores_original_xml': True}
(qa / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False))
