import csv
import hashlib
import json
import re
from copy import deepcopy
from decimal import Decimal
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w02-20261010'
SOURCE = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx'
OUTPUT = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W02_v1_20261010.docx'
CSV = ROOT / 'data/processed/runs/20261009T102201900234-full/hourly-grid.csv'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W = '{' + NS['w'] + '}'
A = '{' + NS['a'] + '}'
source = SOURCE.read_bytes()
sha = lambda b: hashlib.sha256(b).hexdigest()
expected = json.loads((QA / 'preflight.json').read_text(encoding='utf-8'))['source_sha256']
assert sha(source) == expected, 'Source changed after preflight; inspect before continuing'
assert not OUTPUT.exists(), 'Do not overwrite output'
with ZipFile(BytesIO(source)) as z:
    parts = {n: z.read(n) for n in z.namelist()}
doc = E.fromstring(parts['word/document.xml'])
ps = doc.xpath('./w:body/w:p', namespaces=NS)
ts = doc.xpath('./w:body/w:tbl', namespaces=NS)
text = lambda n: ''.join(n.xpath('.//w:t/text()', namespaces=NS))
changes = []
replacements = {
    416: (' tại Bảng 3.1', ''),
    424: ('Kết quả kiểm tra toàn bộ dữ liệu và kết quả theo giờ được tổng hợp tại Bảng 3.2. ', ''),
    436: ('Quy tắc tại Bảng 3.3', 'Quy tắc tổng hợp'),
    439: (' Hình 3.1 dành cho hình minh họa đầu ra tổng hợp theo giờ.', ''),
    443: ('Thống kê trên dữ liệu giờ đã lưu được trình bày tại Bảng 3.4. ', ''),
    455: ('Hình 3.2 dành cho biểu đồ điện năng theo giờ. ', ''),
    475: ('Bộ 11 đặc trưng và thứ tự sử dụng được trình bày tại Bảng 4.1. ', ''),
    480: (' Khoảng trục giờ và số mẫu sử dụng được đối chiếu tại Bảng 4.2.', ''),
    495: ('Bảng 4.3 trình bày kết quả Validation trên 4.727 mẫu. ', ''),
    499: ('Bảng 4.4 trình bày kết quả Test cố định trên 4.590 mốc. ', ''),
    507: (', như vị trí minh họa tại Hình 4.1', ''),
    523: ('Bảng 5.1 ghi công nghệ và vai trò thực tế. ', ''),
    559: (' Các thao tác và quy tắc dữ liệu của từng tab được đối chiếu tại Bảng 5.2.', ''),
    574: ('Phạm vi kiểm thử ở Bảng 5.3', 'Phạm vi kiểm thử'),
}


def plain(p, value):
    runs = p.xpath('.//w:r[w:t]', namespaces=NS)
    rpr = deepcopy(runs[0].find(W + 'rPr')) if runs and runs[0].find(W + 'rPr') is not None else None
    for item in list(p):
        if item.tag not in (W + 'pPr', W + 'bookmarkStart', W + 'bookmarkEnd'):
            p.remove(item)
    run = E.SubElement(p, W + 'r')
    if rpr is not None:
        run.append(rpr)
    node = E.SubElement(run, W + 't')
    node.text = value


for index, (before_span, after_span) in replacements.items():
    p = ps[index]
    before = text(p)
    assert before_span in before, (index, before)
    after = before.replace(before_span, after_span, 1)
    if index == 443:
        after = after.replace(' trong bảng', '')
    plain(p, after)
    changes.append({'index': index, 'before': before, 'after': after,
                    'removed_lead': before_span, 'kind': 'body_prose'})

phat = ts[1].findall(W + 'tr')[1].findall(W + 'tc')[3]
assert not text(phat).strip()
plain(phat.find(W + 'p'), 'Chương 3, 4, 5; lập trình hệ thống; báo cáo Word và xử lý, trình bày dữ liệu bằng Excel.')
changes.append({'kind': 'assignment', 'table': 1, 'row': 1, 'col': 3, 'before': '', 'after': text(phat)})

rows = []
first_incomplete = zero = last = None
csv_bytes = CSV.read_bytes()
with CSV.open(encoding='utf-8-sig', newline='') as f:
    for row in csv.DictReader(f):
        if len(rows) < 3:
            rows.append(row)
        if first_incomplete is None and row['record_count'] == '60' and 0 < int(row['valid_power_count']) < 60:
            first_incomplete = row
        if zero is None and row['valid_power_count'] == '0':
            zero = row
        last = row
samples = [rows[0], rows[1], rows[2], first_incomplete, zero, last]
assert all(samples) and len({x['hour_start'] for x in samples}) == 6
assert all((x['is_complete'].lower() == 'true') == (x['energy_kwh'] != 'NULL') for x in samples)
widths = [420, 210, 230, 330, 220, 330]
header_h, row_h, pad = 130, 110, 24
im = Image.new('RGB', (sum(widths) + 2, header_h + row_h * 6 + 2), 'white')
draw = ImageDraw.Draw(im)
font = ImageFont.truetype('C:/Windows/Fonts/times.ttf', 42)
bold = ImageFont.truetype('C:/Windows/Fonts/timesbd.ttf', 42)
headers = ['Giờ bắt đầu', 'Số bản\nghi', 'Phép đo\nhợp lệ', 'Ghi nhận\n(kWh)', 'Đầy đủ', 'Điện năng\n(kWh)']
values = []
for sample in samples:
    dt = sample['hour_start'].split(' ')
    energy = 'NULL' if sample['energy_kwh'] == 'NULL' else str(Decimal(sample['energy_kwh']).quantize(Decimal('0.000001')))
    observed = 'NULL' if sample['observed_energy_kwh'] == 'NULL' else str(Decimal(sample['observed_energy_kwh']).quantize(Decimal('0.000001')))
    values.append([dt[0] + '\n' + dt[1][:5], sample['record_count'], sample['valid_power_count'],
                   observed, 'Có' if sample['is_complete'].lower() == 'true' else 'Không', energy])
x = 0
for col, width in enumerate(widths):
    draw.rectangle((x, 0, x + width, header_h), fill='#e9eef3', outline='#8d959e', width=2)
    draw.multiline_text((x + pad, pad), headers[col], font=bold, fill='black', spacing=8)
    for j, row in enumerate(values):
        y = header_h + j * row_h
        draw.rectangle((x, y, x + width, y + row_h), fill='white', outline='#8d959e', width=2)
        draw.multiline_text((x + pad, y + 12), row[col], font=font, fill='black', spacing=6)
    x += width
buf = BytesIO()
im.save(buf, format='PNG')
parts['word/media/w02-hourly-table.png'] = buf.getvalue()
(QA / 'hourly-table.png').write_bytes(buf.getvalue())
(QA / 'hourly-table-records.json').write_text(json.dumps({'csv': str(CSV), 'sha256': sha(csv_bytes),
    'source_records': samples, 'display_rows': values, 'display_precision': '6 decimal places, source unchanged',
    'columns': headers, 'note': 'Subset of real output columns and six real hours; NULL remains NULL.'}, ensure_ascii=False, indent=2), encoding='utf-8')
rels = E.fromstring(parts['word/_rels/document.xml.rels'])
rel_ns = '{http://schemas.openxmlformats.org/package/2006/relationships}'
rid = 'rIdW02HourlyTable'
E.SubElement(rels, rel_ns + 'Relationship', Id=rid,
    Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', Target='media/w02-hourly-table.png')
parts['word/_rels/document.xml.rels'] = E.tostring(rels, xml_declaration=True, encoding='UTF-8', standalone=True)
image_specs = [
    (440, 'F31', rid, (1742, 792), None, 'Ảnh bảng từ sáu bản ghi thật của hourly-grid.csv'),
    (456, 'F32', 'rId14', (2489, 1190), (550, 463, 1500, 900), 'Biểu đồ điện năng theo giờ trong ảnh Tổng quan Thy đã chèn'),
    (508, 'F41', None, (2409, 1194), (1000, 220, 2385, 1185), 'Biểu đồ Thực tế và HGB trong ảnh Dự báo Thy đã chèn'),
    (552, 'F51', None, (2489, 1190), (550, 0, 1910, 1190), 'Ảnh Tổng quan Thy đã chèn, bỏ lề trống trái và phải'),
    (555, 'F52', None, (1422, 1102), None, 'Ảnh phần giới thiệu dataset và 11 đặc trưng Thy đã chèn'),
    (563, 'F53', None, (1067, 987), None, 'Ảnh tab Phân tích Thy đã chèn'),
    (568, 'F54', None, (1405, 1193), None, 'Ảnh tab Dự báo Thy đã chèn'),
]
registry = []
for index, key, new_rid, dims, rect, description in image_specs:
    p = ps[index]
    drawing = p.find('.//' + W + 'drawing')
    assert drawing is not None
    blip = drawing.find('.//' + A + 'blip')
    if new_rid:
        blip.set('{' + NS['r'] + '}embed', new_rid)
    fill = drawing.find('.//{' + NS['pic'] + '}blipFill')
    for old in fill.findall(A + 'srcRect'):
        fill.remove(old)
    width, height = dims
    if rect:
        left, top, right, bottom = rect
        assert 0 <= left < right <= width and 0 <= top < bottom <= height
        crop = E.Element(A + 'srcRect')
        for name, value in {'l': left / width, 't': top / height,
                            'r': (width - right) / width, 'b': (height - bottom) / height}.items():
            crop.set(name, str(round(value * 100000)))
        blip.addnext(crop)
        width, height = right - left, bottom - top
    cx = round(14.5 * 360000)
    cy = round(cx * height / width)
    for extent in drawing.xpath('.//wp:extent | .//a:xfrm/a:ext', namespaces=NS):
        extent.set('cx', str(cx))
        extent.set('cy', str(cy))
    docpr = drawing.find('.//{' + NS['wp'] + '}docPr')
    docpr.set('descr', description)
    pp = p.find(W + 'pPr')
    if pp is None:
        pp = E.Element(W + 'pPr')
        p.insert(0, pp)
    for prop in ('keepNext', 'keepLines'):
        if pp.find(W + prop) is None:
            E.SubElement(pp, W + prop)
    registry.append({'key': key, 'paragraph_index': index, 'caption': text(ps[index + 1]),
        'relationship_id': blip.get('{' + NS['r'] + '}embed'), 'source_dimensions': dims,
        'word_crop_pixels': rect, 'display_width_cm': 14.5, 'display_height_cm': cy / 360000,
        'description': description, 'status': 'APPLIED_UNVERIFIED'})
parts['word/document.xml'] = E.tostring(doc, xml_declaration=True, encoding='UTF-8', standalone=True)
with ZipFile(BytesIO(source)) as original, ZipFile(OUTPUT, 'w') as out:
    for item in original.infolist():
        out.writestr(item, parts[item.filename])
    out.writestr('word/media/w02-hourly-table.png', parts['word/media/w02-hourly-table.png'])
(QA / 'changes.json').write_text(json.dumps(changes, ensure_ascii=False, indent=2), encoding='utf-8')
(QA / 'image-registry.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
(QA / 'applied.json').write_text(json.dumps({'status': 'APPLIED_UNVERIFIED', 'source_hash': expected,
    'output': str(OUTPUT), 'output_hash_before_fields': sha(OUTPUT.read_bytes()),
    'changed_existing_parts': ['word/document.xml', 'word/_rels/document.xml.rels'],
    'new_part': 'word/media/w02-hourly-table.png'}, ensure_ascii=False, indent=2), encoding='utf-8')
assert sha(SOURCE.read_bytes()) == expected
assert sha(CSV.read_bytes()) == sha(csv_bytes)
print(json.dumps({'output': str(OUTPUT), 'prose_changes': 14, 'images': 7, 'status': 'APPLIED_UNVERIFIED'}, ensure_ascii=False))
