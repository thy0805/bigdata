import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E

root = Path(r'D:\Hoctap\bigdata')
project = root / 'Detaituan8910'
qa = project / '.agent/qa/diennang-khung-20261006'
manifest = json.loads((qa / 'final-manifest.json').read_text(encoding='utf-8'))
outline = json.loads((qa / 'outline.json').read_text(encoding='utf-8'))
native = json.loads((qa / 'final-word.json').read_text(encoding='utf-8-sig'))
field_tests = json.loads((qa / 'final-field-tests.json').read_text(encoding='utf-8-sig'))
pdf = json.loads((qa / 'final-pdf.json').read_text(encoding='utf-8'))
file = Path(manifest['output'])
source = Path(manifest['source'])
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
w = '{' + ns['w'] + '}'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def contents(p):
    with ZipFile(p) as z:
        assert z.testzip() is None
        return {n: z.read(n) for n in z.namelist()}


def text(e):
    return ''.join(e.xpath('.//w:t/text()', namespaces=ns))


parts = contents(file)
original = contents(source)
doc = E.fromstring(parts['word/document.xml'])
srcdoc = E.fromstring(original['word/document.xml'])
styles = E.fromstring(parts['word/styles.xml'])
body = doc.find(w + 'body')
stylemap = {s.get(w + 'styleId'): s for s in styles.findall(w + 'style')}


def effective(sid, path, attr):
    visited = set()
    while sid and sid not in visited:
        visited.add(sid)
        style = stylemap[sid]
        prop = style.find(path, ns)
        if prop is not None and prop.get(w + attr) is not None:
            return prop.get(w + attr)
        base = style.find(w + 'basedOn')
        sid = base.get(w + 'val') if base is not None else None
    group = 'rPr' if path.startswith('w:rPr/') else 'pPr'
    prop = styles.find(f'w:docDefaults/w:{group}Default/' + path, ns)
    return prop.get(w + attr) if prop is not None else None


expected = []
chapter = 0
for block in outline:
    is_chapter = block['heading'].startswith('CHƯƠNG ')
    if is_chapter:
        chapter += 1
        expected.append((f'CHƯƠNG {chapter}.', block['heading'].split('. ', 1)[1]))
    else:
        expected.append(('', block['heading']))
    for i, item in enumerate(block['items'], 1):
        expected.append((f'{chapter}.{i}.' if is_chapter else f'{i}.', item))
actual = [(h['number'], h['text']) for h in native['headings'] if h['style'] not in ['FrontTitle', 'FrontTitleNoTOC']]
assert actual == expected
assert len(expected) == 85
assert len([h for h in native['headings'] if h['level'] == 2]) == 77
assert native['pages'] == len(pdf) == 21
assert native['toc_count'] == 3 and native['table_count'] == 2 and native['figures'] == 1
assert field_tests['inserted_h2'] == '3.2.' and field_tests['following_h2'] == '3.3.' and field_tests['restored_h2'] == '3.2.'
assert field_tests['inserted_h3'] == '3.1.1.'
assert all(field_tests[k] for k in ['toc_detects_inserted', 'toc_detects_h3', 'figure_list_detects_caption', 'table_list_detects_caption'])
assert not field_tests['changes_saved']
main_toc = native['tocs'][0]
toc_entries = [p for p in main_toc.split('\r') if p.strip()]
assert len(toc_entries) == 90
toc_expected = [h for h in native['headings'] if h['style'] != 'FrontTitleNoTOC']
assert len(toc_expected) == 90
roman = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi', 7: 'vii', 8: 'viii'}
for entry, heading in zip(toc_entries, toc_expected):
    expected_title = (heading['number'] + ' ' if heading['number'] else '') + heading['text']
    expected_page = roman[heading['page']] if heading['physical_page'] < 10 else str(heading['page'])
    assert entry == expected_title + '\t' + expected_page, (entry, expected_title, expected_page)
assert not (native['tocs'][1] or '').strip() and not (native['tocs'][2] or '').strip()
assert len(doc.xpath('//w:instrText[contains(text(),"TOC ")]', namespaces=ns)) == 3
assert len(doc.xpath('//w:hyperlink[@w:anchor]', namespaces=ns)) == 90
assert not doc.xpath('//w:fldChar[@w:fldLock="true"]', namespaces=ns)
sections = doc.xpath('//w:sectPr', namespaces=ns)
source_sections = srcdoc.xpath('//w:sectPr', namespaces=ns)
assert len(sections) == 3
for section in sections:
    for tag in ['pgSz', 'pgMar']:
        assert section.find(w + tag).attrib == source_sections[0].find(w + tag).attrib
assert len(doc.xpath('//w:pgBorders', namespaces=ns)) == 1
assert sections[0].find(w + 'pgBorders').attrib == source_sections[0].find(w + 'pgBorders').attrib
assert [s.find(w + 'pgNumType').get(w + 'start') for s in sections] == ['1', '1', '1']
assert sections[1].find(w + 'pgNumType').get(w + 'fmt') == 'lowerRoman'
assert sections[2].find(w + 'pgNumType').get(w + 'fmt', 'decimal') == 'decimal'
relmap = {e.get('Id'): e.get('Target') for e in E.fromstring(parts['word/_rels/document.xml.rels'])}
cover_footer = 'word/' + relmap[sections[0].find(w + 'footerReference').get('{' + ns['r'] + '}id')]
assert not E.fromstring(parts[cover_footer]).xpath('//w:instrText | //w:t', namespaces=ns)
assert len(doc.xpath('//wp:extent', namespaces=ns)) == 1
assert doc.xpath('//wp:extent', namespaces=ns)[0].attrib == srcdoc.xpath('//wp:extent', namespaces=ns)[0].attrib
assert [n for n in parts if n.startswith('word/media/')] == ['word/media/image1.png']
for name in manifest['preserve_only_parts']:
    assert parts[name] == original[name]
for srcname, target in manifest['footer_source_target_map'].items():
    assert parts[target] == original[srcname]
for sid, size, level in [('Heading11', '36', '0'), ('Heading21', '28', '1'), ('Heading31', '26', '2')]:
    style = stylemap[sid]
    assert effective(sid, 'w:rPr/w:sz', 'val') == size
    assert effective(sid, 'w:pPr/w:spacing', 'line') == '312'
    assert effective(sid, 'w:pPr/w:outlineLvl', 'val') == level
    assert style.find('w:pPr/w:keepNext', ns) is not None
    assert style.find('w:rPr/w:color', ns).get(w + 'val') == '000000'
assert stylemap['ReportBody'].find('w:pPr/w:ind', ns).get(w + 'firstLine') == '454'
assert stylemap['ReportBody'].find('w:pPr/w:spacing', ns).get(w + 'line') == '312'
assert stylemap['Heading11'].find('w:pPr/w:pageBreakBefore', ns) is not None
start = next(i for i, p in enumerate(body) if p.find('w:pPr/w:pStyle', ns) is not None and p.find('w:pPr/w:pStyle', ns).get(w + 'val') == 'Heading11' and text(p) == 'MỞ ĐẦU')
blank_slots = 0
for p in list(body)[start:]:
    if p.tag == w + 'p' and p.find('w:pPr/w:pStyle', ns) is not None:
        sid = p.find('w:pPr/w:pStyle', ns).get(w + 'val')
        if sid == 'ReportBody':
            assert not text(p)
            blank_slots += 1
assert blank_slots == 78
tables = body.findall(w + 'tbl')
assert [len(t.findall(w + 'tr')) for t in tables] == [4, 2]
assert all(not text(c) for row in tables[0].findall(w + 'tr')[1:] for c in [row.findall(w + 'tc')[3]])
assert all(not text(c) for c in tables[1].findall(w + 'tr')[1].findall(w + 'tc'))
assert 'No table of contents entries found.' not in text(body)
for page in pdf:
    assert page['text'].strip()
    assert 'No table of contents' not in page['text']
    assert (qa / f'final-render/page-{page["page"]}.png').exists()
core = E.fromstring(parts['docProps/core.xml'])
assert all(not e.text for e in core if E.QName(e).localname in ['creator', 'lastModifiedBy'])
assert digest(source) == manifest['source_sha256'] == 'efac5eade11afeff8b17f458b183edcb5f1ca600ebdfbb86e167d895d08662d3'
assert digest(file) == manifest['output_sha256']
member_baselines = json.loads((project / '.agent/qa/chapter-outlines/verification.json').read_text(encoding='utf-8-sig'))
members = []
for path, baseline, chapter_index in [(project / 'KhoiTuan_Chuong1_TongQuanBaiToan.docx', member_baselines[0], 1), (project / 'HAULYVUNHAN_Chuong2_CoSoLyThuyet.docx', member_baselines[1], 2)]:
    assert digest(path) == baseline['sha256']
    memberdoc = E.fromstring(contents(path)['word/document.xml'])
    paragraphs = [text(p) for p in memberdoc.findall('w:body/w:p', ns) if text(p)]
    expected_member = [outline[chapter_index]['heading']] + [f'{chapter_index}.{i}. {item}' for i, item in enumerate(outline[chapter_index]['items'], 1)]
    assert paragraphs == expected_member
    members.append({'path': str(path), 'unchanged_from_20261001_baseline': True, 'sha256': digest(path), 'headings_match': True})
report = {'status': 'VERIFIED', 'output': str(file), 'sha256': digest(file), 'pages': 21, 'main_parts': 8, 'h2_count': 77, 'chapter_h2_counts': [11, 14, 13, 14, 17], 'toc_entries': 90, 'toc_fields': 3, 'sections': 3, 'native_tables': 2, 'logo_images': 1, 'blank_body_slots': blank_slots, 'main_toc_numbers_match_all_native_headings': True, 'native_update_and_numbering_tests': field_tests, 'source_unchanged_sha256': digest(source), 'member_sources': members, 'visual_review': {'pages': list(range(1, 22)), 'renderer': 'native Microsoft Word PDF export + PDFium at scale 2', 'all_pages_inspected': True, 'packaged_renderer_unavailable': 'soffice.exe not on PATH', 'issues_remaining': []}, 'pending_identity': 'MSSV Nguyễn Đức Thành Phát differs between old cover and assignment table; placeholder retained', 'dataset_scope': 'not inspected or modified; academic prose and experiments not created'}
(qa / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'status': report['status'], 'pages': 21, 'h2_count': 77, 'toc_entries': 90, 'source_unchanged': True, 'members_unchanged': True, 'sha256': report['sha256']}, ensure_ascii=False))
