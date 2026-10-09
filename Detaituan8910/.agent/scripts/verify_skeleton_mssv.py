import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E
from PIL import Image, ImageChops

root = Path(r'D:\Hoctap\bigdata')
qa = root / 'Detaituan8910/.agent/qa/diennang-mssv-20261006'
previous = root / 'Detaituan8910/.agent/qa/diennang-khung-20261006'
manifest = json.loads((qa / 'manifest.json').read_text(encoding='utf-8'))
source = Path(manifest['source'])
output = Path(manifest['output'])
native = json.loads((qa / 'final-word.json').read_text(encoding='utf-8-sig'))
before = json.loads((previous / 'final-word.json').read_text(encoding='utf-8-sig'))
assert native['pages'] == before['pages'] == 21
for key in ['headings', 'sections', 'tocs', 'toc_count', 'table_count', 'figures']:
    assert native[key] == before[key], key
with ZipFile(source) as oldzip, ZipFile(output) as newzip:
    assert newzip.testzip() is None
    assert oldzip.namelist() == newzip.namelist()
    assert [name for name in oldzip.namelist() if oldzip.read(name) != newzip.read(name)] == ['word/document.xml']
    doc = E.fromstring(newzip.read('word/document.xml'))
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
text = ''.join(doc.xpath('//w:t/text()', namespaces=ns))
assert text.count('2001230640') == 2
assert '[MSSV]' not in text and '20012306640' not in text
assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest['source_sha256']
assert hashlib.sha256(output.read_bytes()).hexdigest() == manifest['output_sha256']
changed_pages = []
for page in range(1, 22):
    a = Image.open(previous / f'final-render/page-{page}.png').convert('RGB')
    b = Image.open(qa / f'final-render/page-{page}.png').convert('RGB')
    assert a.size == b.size
    if ImageChops.difference(a, b).getbbox():
        changed_pages.append(page)
assert changed_pages == [1, 2]
report = {'status': 'APPLIED_UNVERIFIED', 'output': str(output), 'output_sha256': manifest['output_sha256'], 'mssv': '2001230640', 'occurrences': 2, 'pages': 21, 'headings_numbering_toc_sections_unchanged': True, 'only_document_part_changed': True, 'reverse_edit_restores_xml': manifest['reverse_edit_restores_original_xml'], 'changed_render_pages': changed_pages, 'pages_3_to_21_pixel_identical': True, 'source_unchanged': True, 'visual_review_pending': True, 'packaged_renderer_error': 'LibreOffice soffice.exe not found on PATH; diagnosed and used native Word PDF + PDFium scale 2'}
(qa / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
