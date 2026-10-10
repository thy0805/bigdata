import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w011-20261010'
SOURCE = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
OUTPUT = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx'
EXPECTED = '4a47523a0bfe9c2a035df66c9fedff2e33a776dcb8c2ec01b50be8dd0d33f591'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + NS['w'] + '}'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
assert not OUTPUT.exists(), 'Output exists; do not overwrite'
with ZipFile(SOURCE) as archive:
    parts = {name: archive.read(name) for name in archive.namelist()}
doc = E.fromstring(parts['word/document.xml'])
paragraphs = doc.xpath('/w:document/w:body/w:p', namespaces=NS)
tables = doc.xpath('/w:document/w:body/w:tbl', namespaces=NS)
changes = []


def text(node):
    return ''.join(node.xpath('.//w:t/text()', namespaces=NS))


def prose(index, after, location, tail=False):
    paragraph = paragraphs[index]
    nodes = paragraph.xpath('.//w:t', namespaces=NS)
    target = nodes[-1] if tail else next(n for n in nodes if n.text and n.text.strip())
    if not tail:
        assert len(nodes) == 1, (index, len(nodes))
    changes.append({'kind': 'paragraph', 'index': index, 'location': location,
                    'before': target.text, 'after': after})
    target.text = after
    if after.startswith(' ') or after.endswith(' '):
        target.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


prose(418, 'Nguồn: UCI Machine Learning Repository; kết quả khảo sát tệp dữ liệu gốc.', '3.2 chú nguồn Bảng 3.1')
prose(426, 'Nguồn: kết quả kiểm tra toàn bộ tệp gốc và đối chiếu đầu ra Apache Flink.', '3.4 chú nguồn Bảng 3.2')
prose(445, 'Nguồn: thống kê từ tệp điện năng theo giờ do Apache Flink tạo.', '3.8 chú nguồn Bảng 3.4')
old = paragraphs[554].xpath('.//w:t', namespaces=NS)[-1].text
assert old.endswith('; số hiệu được đặt trước các ảnh chức năng ở những mục tiếp theo.')
prose(554, old.replace('; số hiệu được đặt trước các ảnh chức năng ở những mục tiếp theo.', '.'), '5.11 bỏ lời điều phối số hiệu hình', tail=True)
prose(561, 'Nguồn: dashboard/app.py, data_service.py, predictor.py và kết quả kiểm thử trên trình duyệt.', '5.12 chú nguồn Bảng 5.2')
prose(574, ' gồm chuỗi UCI → dữ liệu giờ Flink → feature → model → dashboard. Kết quả ghi nhận 119/119 phép kiểm chức năng và vận hành đạt, cùng 7/7 phép kiểm hồ sơ và bảo toàn sản phẩm đạt, tổng cộng 126/126. Nhóm kiểm hồ sơ không được tính là kiểm thử chức năng. Kết quả phản ánh trạng thái hệ thống tại thời điểm kiểm tra.', '5.15 phân biệt119 chức năng/vận hành và7 hồ sơ', tail=True)
assert text(paragraphs[575]).endswith('Phạm vi kiểm thử ứng dụng trong hồ sơ Phase 4')
prose(575, '. Phạm vi kiểm thử và đối chiếu hồ sơ hệ thống', 'Caption Bảng 5.3', tail=True)
prose(576, 'Nguồn: kết quả kiểm thử ứng dụng và đối chiếu hồ sơ; chưa kiểm tra khởi động lại toàn bộ Windows/WSL.', '5.15 chú nguồn Bảng 5.3')
prose(578, 'Phần giới thiệu dữ liệu được kiểm tra riêng bằng 75 phép kiểm kỹ thuật và 7 phép kiểm trên trình duyệt ở 1366 × 768/1920 × 1080. Các số lượt kiểm này được báo cáo riêng, không cộng với đợt kiểm trước để tránh đếm trùng.', '5.15 kết quả kiểm riêng phần giới thiệu dữ liệu')
prose(580, 'Kiểm thử đã xác nhận các tab, bộ lọc, chỉ số, biểu đồ và suy luận trong phạm vi dữ liệu đã xác minh. Các phép thử lỗi nguồn dữ liệu, mô hình và cổng kiểm tra khả năng báo lỗi và tránh dừng tiến trình không thuộc hệ thống. Khởi động, dừng và phục hồi dịch vụ đã được kiểm trong môi trường cục bộ; việc khởi động lại toàn bộ Windows/WSL chưa được kiểm thử và tự khởi động dịch vụ chưa được triển khai.', '5.16 giữ phạm vi và giới hạn vận hành')
prose(581, 'Kịch bản trình diễn chưa được chuẩn bị trong phạm vi thực hiện. Kết quả kiểm thử kỹ thuật không thay thế việc nghiệm thu của người dùng. Hệ thống chưa được đo hiệu năng trên nhiều máy, kiểm thử tải trong môi trường vận hành thực tế hoặc đánh giá độ sẵn sàng dịch vụ.', '5.16 bỏ I04/Phase4/VERIFIED, giữ giới hạn')


def cell(table, row, col):
    return tables[table].findall(W + 'tr')[row].findall(W + 'tc')[col]


def table_text(table, row, col, after):
    element = cell(table, row, col)
    nodes = element.xpath('.//w:t', namespaces=NS)
    assert len(nodes) == 1
    changes.append({'kind': 'cell', 'table': table, 'row': row, 'col': col,
                    'location': f'Bảng 5.3 ô{row},{col}', 'before': nodes[0].text, 'after': after})
    nodes[0].text = after


table_text(17, 0, 0, 'Nhóm kiểm tra')
table_text(17, 1, 0, 'Đối chiếu nguồn / tích hợp')
table_text(17, 5, 2, 'Ba tab, tương tác và đối chiếu ảnh giao diện')
table_text(17, 6, 0, 'Đối chiếu hồ sơ')
table_text(17, 6, 2, 'Kiểm tính đầy đủ hồ sơ và bảo toàn sản phẩm')


def soft_break(table, row, col, before, split, location):
    element = cell(table, row, col)
    nodes = element.xpath('.//w:t', namespaces=NS)
    assert len(nodes) == 1 and nodes[0].text == before
    first, second = split
    assert first + second == before
    node = nodes[0]
    node.text = first
    br = E.Element(W + 'br')
    tail = E.Element(W + 't')
    tail.text = second
    node.addnext(br)
    br.addnext(tail)
    changes.append({'kind': 'linebreak', 'table': table, 'row': row, 'col': col,
                    'location': location, 'before': before, 'after': first + '\n' + second,
                    'normalized_identical': True})


soft_break(7, 2, 2, 'Giờ:phút:giây', ('Giờ:phút:', 'giây'), 'Bảng 3.1 đơn vị Time')
soft_break(15, 5, 2, 'HistGradientBoostingRegressor', ('HistGradient', 'BoostingRegressor'), 'Bảng 5.1 tên mô hình HGB')
parts['word/document.xml'] = E.tostring(doc, xml_declaration=True, encoding='UTF-8', standalone=True)
with ZipFile(SOURCE) as original, ZipFile(OUTPUT, 'w') as result:
    for item in original.infolist():
        result.writestr(item, parts[item.filename])
with ZipFile(SOURCE) as original, ZipFile(OUTPUT) as result:
    changed_parts = [name for name in original.namelist() if original.read(name) != result.read(name)]
assert changed_parts == ['word/document.xml']
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
guards = json.loads((ROOT / '.agent/qa/word-w01-20261010/preflight.json').read_text(encoding='utf-8-sig'))['guards']
guards[str(SOURCE)] = EXPECTED
source_qa = ROOT / '.agent/qa/word-w01-20261010'
for name in ('verification.json', 'final-verification.json', 'field-probe.json', 'font-audit.json', 'manifest.json', 'image-registry.json'):
    guards[str(source_qa / name)] = hashlib.sha256((source_qa / name).read_bytes()).hexdigest()
(QA / 'preflight.json').write_text(json.dumps({'status': 'VERIFIED', 'source_checkpoint': 'd66a3c9', 'guards': guards}, ensure_ascii=False, indent=2), encoding='utf-8')
(QA / 'changes.json').write_text(json.dumps(changes, ensure_ascii=False, indent=2), encoding='utf-8')
(QA / 'applied.json').write_text(json.dumps({'status': 'APPLIED_UNVERIFIED', 'output': str(OUTPUT), 'sha256_before_field_update': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), 'changed_package_parts': changed_parts, 'change_count': len(changes)}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'status': 'APPLIED_UNVERIFIED', 'output': str(OUTPUT), 'changes': len(changes), 'changed_parts': changed_parts}, ensure_ascii=False))
