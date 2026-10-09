from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree as E

from word_w01_content import CH4

root = Path(__file__).resolve().parents[2]
path = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
n = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + n['w'] + '}'
with ZipFile(path) as z:
    parts = {key: z.read(key) for key in z.namelist()}
doc = E.fromstring(parts['word/document.xml'])
replacements = CH4[14].split('\n\n')
for p in doc.xpath('/w:document/w:body/w:p', namespaces=n):
    text = ''.join(p.xpath('.//w:t/text()', namespaces=n))
    replacement = None
    if text.startswith('Model được lưu bằng joblib'):
        replacement = replacements[0]
    elif text.startswith('Dashboard kiểm nguồn dữ liệu và model trước khi suy luận.'):
        replacement = replacements[1]
    if replacement:
        ts = p.xpath('.//w:t', namespaces=n)
        ts[0].text = replacement
        for t in ts[1:]:
            t.text = ''
table = doc.xpath('/w:document/w:body/w:tbl', namespaces=n)[2]
existing = ''.join(table.xpath('.//w:t/text()', namespaces=n))
for values in [('HGB', 'HistGradientBoostingRegressor', 'Mô hình hồi quy tăng cường gradient dùng trong thực nghiệm'), ('Train', 'Training set', 'Tập dữ liệu huấn luyện mô hình'), ('Validation', 'Validation set', 'Tập kiểm định để lựa chọn mô hình'), ('Test', 'Test set', 'Tập kiểm thử cuối sau khi khóa mô hình')]:
    if values[0] in existing:
        continue
    row = deepcopy(table.findall(W + 'tr')[-1])
    for cell, value in zip(row.findall(W + 'tc'), values):
        ts = cell.xpath('.//w:t', namespaces=n)
        ts[0].text = value
        for t in ts[1:]:
            t.text = ''
        for keep in cell.xpath('.//w:keepNext', namespaces=n):
            keep.getparent().remove(keep)
    table.append(row)
parts['word/document.xml'] = E.tostring(doc, encoding='UTF-8', xml_declaration=True, standalone=True)
with ZipFile(path, 'w', ZIP_DEFLATED) as z:
    for key, value in parts.items():
        z.writestr(key, value)
print('W01 concise 4.14 and four glossary terms applied; render pending')
