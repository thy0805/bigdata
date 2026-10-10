import hashlib
import json
import re
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree as E

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w021-20261010'
PREVIOUS = ROOT / '.agent/qa/word-w02-20261010'
SOURCE = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W02_v1_20261010.docx'
OUTPUT = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W02_1_v1_20261010.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + NS['w'] + '}'
sha = lambda b: hashlib.sha256(b).hexdigest()
text = lambda n: ''.join(n.xpath('.//w:t/text()', namespaces=NS))
gate = json.loads((PREVIOUS / 'verification.json').read_text(encoding='utf-8'))
assert gate['status'] == 'PASS' and gate['passed'] == gate['total'] == 53
assert (PREVIOUS / 'page-review.md').is_file()
source = SOURCE.read_bytes()
assert sha(source) == gate['sha256']
assert not OUTPUT.exists(), 'Never overwrite an existing Word version'
QA.mkdir(exist_ok=True)
with ZipFile(BytesIO(source)) as z:
    parts = {n: z.read(n) for n in z.namelist()}
doc = E.fromstring(parts['word/document.xml'])
tbl = doc.xpath('./w:body/w:tbl', namespaces=NS)[0]
before_table = [[text(c) for c in r.findall(W + 'tc')] for r in tbl.findall(W + 'tr')]
assert len(before_table) == 11 and before_table[0][3] == 'Minh chứng'
for row in tbl.findall(W + 'tr')[4:]:
    tbl.remove(row)
grid = tbl.find(W + 'tblGrid')
grid.remove(grid.findall(W + 'gridCol')[3])
widths = [1000, 4000, 2000, 1504]
for c, width in zip(grid, widths):
    c.set(W + 'w', str(width))
rows = [
    ['Tuần', 'Nội dung công việc', 'Thành viên', 'Trạng thái'],
    ['Tuần 1', 'Tiếp nhận đề tài, thống nhất phạm vi, phân công nhiệm vụ và khảo sát bộ dữ liệu UCI.', 'Cả nhóm', 'Đã thực hiện'],
    ['Tuần 2', 'Xử lý, tổng hợp dữ liệu bằng Apache Flink; xây dựng đặc trưng, huấn luyện và đánh giá mô hình dự báo.', 'Nguyễn Đức Thành Phát', 'Đã thực hiện'],
    ['Tuần 3', 'Xây dựng giao diện phân tích và dự báo, kiểm tra kết quả, rà soát báo cáo và chuẩn bị trình bày.', 'Cả nhóm', 'Đang thực hiện'],
]
for ri, row in enumerate(tbl.findall(W + 'tr')):
    row.remove(row.findall(W + 'tc')[3])
    for h in row.xpath('./w:trPr/w:trHeight', namespaces=NS):
        h.getparent().remove(h)
    for ci, cell in enumerate(row.findall(W + 'tc')):
        cell.find('./' + W + 'tcPr/' + W + 'tcW').set(W + 'w', str(widths[ci]))
        p = cell.find(W + 'p')
        rpr = p.find('./' + W + 'r/' + W + 'rPr')
        rpr = deepcopy(rpr) if rpr is not None else E.Element(W + 'rPr')
        for old in list(p):
            if old.tag != W + 'pPr':
                p.remove(old)
        ppr = p.find(W + 'pPr')
        if ri > 0:
            for k in ppr.findall(W + 'keepNext'):
                ppr.remove(k)
        ppr.find(W + 'jc').set(W + 'val', 'center' if ci in (0, 3) else 'left')
        sz = rpr.find(W + 'sz')
        if sz is None:
            sz = E.SubElement(rpr, W + 'sz')
        sz.set(W + 'val', '24')
        fonts = rpr.find(W + 'rFonts')
        if fonts is None:
            fonts = E.SubElement(rpr, W + 'rFonts')
        for key in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
            fonts.set(W + key, 'Times New Roman')
        run = E.SubElement(p, W + 'r')
        run.append(rpr)
        E.SubElement(run, W + 't').text = rows[ri][ci]
pattern = re.compile(r'\s*Truy cập ngày\s+\d{1,2}/\d{1,2}/\d{4}\.')
changes = []
for pi, p in enumerate(doc.xpath('./w:body/w:p', namespaces=NS)):
    before = text(p)
    matches = list(pattern.finditer(before))
    if not matches:
        continue
    nodes = p.xpath('.//w:t', namespaces=NS)
    offset = 0
    spans = []
    for t in nodes:
        value = t.text or ''
        spans.append((t, offset, offset + len(value), value))
        offset += len(value)
    for t, start, end, value in spans:
        cut = set()
        for m in matches:
            cut.update(range(max(start, m.start()) - start, min(end, m.end()) - start))
        t.text = ''.join(ch for i, ch in enumerate(value) if i not in cut)
    after = text(p)
    assert after == pattern.sub('', before)
    changes.append({'index': pi, 'before': before, 'after': after, 'removed': [m.group() for m in matches]})
assert len(changes) == 21 and all(re.match(r'^\[\d+\]', c['before']) for c in changes)
parts['word/document.xml'] = E.tostring(doc, xml_declaration=True, encoding='UTF-8', standalone=True)
with ZipFile(OUTPUT, 'w', ZIP_DEFLATED) as z:
    for name, data in parts.items():
        z.writestr(name, data)
record = {'status': 'APPLIED_UNVERIFIED', 'source': str(SOURCE), 'source_sha256': sha(source),
          'output': str(OUTPUT), 'output_pre_field_sha256': sha(OUTPUT.read_bytes()),
          'schedule_before': before_table, 'schedule_after': rows, 'column_widths_twips': widths,
          'access_date_changes': changes, 'removed_access_dates': 21,
          'schedule_basis': 'Three-week work organization proposed by Thy, not verified elapsed historical weeks; no dates assigned. Week 2 Phat from explicit assignment. Coordination weeks 1 and 3: whole group; week 3 still in progress.',
          'school_rule': 'Mau bao cao_Do an_Khoa luan_2025.docx paragraph235 contains one illustrative accessed-date source; no mandatory accessed-date rule found in source template. Thy requests removal.',
          'retained': '21 numbered sources and live hyperlink relationships, publication years, DOI, all images and chapters'}
(QA / 'changes.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'output': str(OUTPUT), 'schedule_rows': 3, 'columns': 4, 'dates_removed': len(changes)}, ensure_ascii=False))
