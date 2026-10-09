from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree as E

from word_w01_content import CH5

root = Path(__file__).resolve().parents[2]
path = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
n = {'w': W[1:-1]}
with ZipFile(path) as z:
    parts = {key: z.read(key) for key in z.namelist()}
doc = E.fromstring(parts['word/document.xml'])
for p in doc.xpath('/w:document/w:body/w:p', namespaces=n):
    text = ''.join(p.xpath('.//w:t/text()', namespaces=n))
    if text.startswith('Kiểm thử tích hợp đối chiếu chuỗi nguồn UCI'):
        for child in list(p):
            if child.tag != W + 'pPr':
                p.remove(child)
        target = CH5[15].split('\n\n')[0]
        before, after = target.split('{T53}')
        for value in [before, after]:
            if value == after:
                field = E.SubElement(p, W + 'fldSimple')
                field.set(W + 'instr', ' REF W01_T53 \\h ')
                r = E.SubElement(field, W + 'r')
                E.SubElement(r, W + 't').text = 'Bảng 5.3'
            r = E.SubElement(p, W + 'r')
            t = E.SubElement(r, W + 't')
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            t.text = value
    elif text.startswith('Lượt chỉnh phần giới thiệu dữ liệu có hồ sơ riêng'):
        ts = p.xpath('.//w:t', namespaces=n)
        ts[0].text = CH5[15].split('\n\n')[-1]
        for t in ts[1:]:
            t.text = ''
parts['word/document.xml'] = E.tostring(doc, encoding='UTF-8', xml_declaration=True, standalone=True)
with ZipFile(path, 'w', ZIP_DEFLATED) as z:
    for key, value in parts.items():
        z.writestr(key, value)
print('Added live reference to Table 5.3; removed report-production sentence')
