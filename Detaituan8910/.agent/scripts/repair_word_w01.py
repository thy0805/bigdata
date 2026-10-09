import json
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree as E

root = Path(__file__).resolve().parents[2]
qa = root / '.agent/qa/word-w01-20261010'
path = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
n = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + n['w'] + '}'
with ZipFile(path) as z:
    parts = {key: z.read(key) for key in z.namelist()}
doc = E.fromstring(parts['word/document.xml'])
styles = E.fromstring(parts['word/styles.xml'])
base = styles.xpath('./w:style[@w:styleId="ChapterTitle"]', namespaces=n)[0]
alias = deepcopy(base)
alias.set(W + 'styleId', 'Heading1')
alias.attrib.pop(W + 'customStyle', None)
alias.find(W + 'name').set(W + 'val', 'heading 1')
styles.append(alias)
heads = doc.xpath('.//w:body/w:p/w:pPr/w:pStyle[@w:val="ChapterTitle"]', namespaces=n)
assert len(heads) == 5
for head in heads:
    head.set(W + 'val', 'Heading1')
for field in doc.xpath('.//w:fldSimple', namespaces=n):
    code = field.get(W + 'instr', '')
    if 'STYLEREF "ChapterTitle"' in code:
        field.set(W + 'instr', code.replace('STYLEREF "ChapterTitle"', 'STYLEREF "Heading 1"'))
for field in doc.xpath('.//w:instrText', namespaces=n):
    code = field.text or ''
    if 'STYLEREF "ChapterTitle"' in code:
        field.text = code.replace('STYLEREF "ChapterTitle"', 'STYLEREF "Heading 1"')
    if 'TOC ' in code and 'ChapterTitle,1' in code:
        field.text = code.replace('ChapterTitle,1', 'ChapterTitle,1,Heading 1,1')
for table in doc.xpath('.//w:tbl[.//w:tblW[@w:w="8504"]]', namespaces=n):
    rows = table.findall(W + 'tr')
    for row in rows[:-1]:
        for pr in row.xpath('.//w:p/w:pPr', namespaces=n):
            if pr.find(W + 'keepNext') is None:
                pr.append(E.Element(W + 'keepNext'))
for p in doc.xpath('.//w:body/w:p', namespaces=n):
    text = ''.join(p.xpath('.//w:t/text()', namespaces=n))
    if text.startswith('Nhóm xin gửi lời cảm ơn'):
        ts = p.xpath('.//w:t', namespaces=n)
        ts[-1].text += ' Các kiến thức về dữ liệu, kiến trúc xử lý và cách đánh giá kết quả giúp nhóm xác định phạm vi thực hiện của đề tài.'
    if text.startswith('Hướng phát triển có thể gồm dữ liệu mới/nhiều hộ'):
        ts = p.xpath('.//w:t', namespaces=n)
        ts[0].text = 'Hướng phát triển gồm bổ sung dữ liệu mới/nhiều hộ, đánh giá nhiều horizon và nguồn cập nhật. Các mở rộng cần quy tắc chất lượng, đánh giá và vận hành riêng; chưa được triển khai trong hệ thống hiện tại.'
        for other in ts[1:]:
            other.text = ''
    if text.startswith(tuple(f'[{i}]' for i in range(17, 22))):
        for r in p.xpath('.//w:r', namespaces=n):
            rp = r.find(W + 'rPr')
            if rp is None:
                rp = E.Element(W + 'rPr')
                r.insert(0, rp)
            for tag, val in [('sz', '24'), ('color', '000000')]:
                x = rp.find(W + tag)
                if x is None:
                    x = E.SubElement(rp, W + tag)
                x.set(W + 'val', val)
parts['word/document.xml'] = E.tostring(doc, encoding='UTF-8', xml_declaration=True, standalone=True)
parts['word/styles.xml'] = E.tostring(styles, encoding='UTF-8', xml_declaration=True, standalone=True)
with ZipFile(path, 'w', ZIP_DEFLATED) as z:
    for key, value in parts.items():
        z.writestr(key, value)
(qa / 'format-repair.json').write_text(json.dumps({'status': 'APPLIED_UNVERIFIED', 'reason': 'SEQ chapter restart needs native Heading 1; custom outline level alone did not reset.', 'changes': ['Five chapter titles use native Heading1 cloned from ChapterTitle layout; numbering and text preserved', 'STYLEREF and TOC recognize native chapter style', 'New short tables kept together', 'Acknowledgment expanded with same approved meaning; actual lines need recheck', '5.17 future paragraph shortened to prevent near-empty continuation', 'New references use matching black 12pt text'], 'forbidden_sources_modified': False}, ensure_ascii=False, indent=2), encoding='utf-8')
print('W01 format repair applied; verification pending')
