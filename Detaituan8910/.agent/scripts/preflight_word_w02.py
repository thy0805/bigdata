import hashlib
import json
import re
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w02-20261010'
SOURCE = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}


def text(node):
    return ''.join(node.xpath('.//w:t/text()', namespaces=NS))


def digest(data):
    return hashlib.sha256(data).hexdigest()


source_bytes = SOURCE.read_bytes()
QA.mkdir(parents=True, exist_ok=True)
image_dir = QA / 'source-images'
image_dir.mkdir(exist_ok=True)
with ZipFile(BytesIO(source_bytes)) as z:
    doc = E.fromstring(z.read('word/document.xml'))
    rels = {x.get('Id'): x.get('Target') for x in E.fromstring(z.read('word/_rels/document.xml.rels'))}
    ps = doc.xpath('./w:body/w:p', namespaces=NS)
    images = []
    leads = []
    for i, p in enumerate(ps):
        value = text(p)
        if i >= 155 and i < 595 and re.search(r'(Hình|Bảng)\s+\d|bảng (dưới|sau)|biểu đồ (bên|dưới)', value, re.I):
            fields = p.xpath('.//w:instrText/text() | .//w:fldSimple/@w:instr', namespaces=NS)
            if not any('SEQ ' in f for f in fields):
                leads.append({'paragraph_index': i, 'text': value, 'decision': 'REVIEW_BEFORE_EDIT'})
        for drawing in p.xpath('.//w:drawing', namespaces=NS):
            rid = drawing.xpath('.//a:blip/@r:embed', namespaces=NS)[0]
            part = 'word/' + rels[rid]
            data = z.read(part)
            image = Image.open(BytesIO(data))
            filename = image_dir / Path(part).name
            if filename.exists():
                assert digest(filename.read_bytes()) == digest(data), filename
            else:
                filename.write_bytes(data)
            caption = text(ps[i + 1]) if i + 1 < len(ps) else ''
            images.append({'paragraph_index': i, 'drawing_name': drawing.xpath('.//wp:docPr/@name', namespaces=NS),
                           'part': part, 'relationship_id': rid, 'sha256': digest(data),
                           'dimensions': image.size, 'extracted_path': str(filename), 'following_caption': caption,
                           'status': 'VISUAL_REVIEW_PENDING'})
    tables = [[[text(c) for c in row.xpath('./w:tc', namespaces=NS)]
               for row in table.xpath('./w:tr', namespaces=NS)]
              for table in doc.xpath('./w:body/w:tbl', namespaces=NS)]
    references = [text(p) for p in ps if re.match(r'^\[\d+\]', text(p))]
    expected_hash = 'fafe4d7485601ba667a468990c1c80e188bf0e7126dd3edaf51059dfca3e2006'
    result = {'status': 'IN_PROGRESS_INPUT_CONFIRMATION_REQUIRED', 'source': str(SOURCE),
              'source_sha256': digest(source_bytes), 'checkpoint_sha256': expected_hash,
              'source_matches_checkpoint': digest(source_bytes) == expected_hash,
              'source_unchanged_during_read': digest(SOURCE.read_bytes()) == digest(source_bytes),
              'tables_count': len(tables), 'equations_count': len(doc.xpath('.//m:oMath', namespaces=NS)),
              'images': images, 'lead_candidates': leads, 'front_tables': tables[:2],
              'references_count': len(references),
              'access_date_occurrences': sum(len(re.findall(r'Truy cập ngày\s+\d{2}/\d{2}/\d{4}', x)) for x in references),
              'package_hashes': {name: digest(z.read(name)) for name in z.namelist()},
              'notes': ['No DOCX edited; source has user changes compared with approved checkpoint.',
                        'Do not overwrite embedded photographs or silently restore old placeholder source.',
                        'Source image directory not supplied by user; embedded images require visual review and confirmation.']}
out = QA / 'preflight.json'
if out.exists():
    raise FileExistsError(out)
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: result[k] for k in ('source_sha256', 'source_matches_checkpoint', 'source_unchanged_during_read', 'tables_count', 'equations_count', 'references_count', 'access_date_occurrences')}, ensure_ascii=False))
print('IMAGES', [(x['following_caption'], x['extracted_path']) for x in images])
print('LEAD_CANDIDATES', len(leads))
