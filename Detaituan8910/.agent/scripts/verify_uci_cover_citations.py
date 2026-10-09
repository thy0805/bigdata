from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from PIL import Image, ImageChops
from copy import deepcopy
import hashlib
import json
import re

ROOT = Path(r'D:\Hoctap\bigdata\Detaituan8910')
QA = ROOT / '.agent/qa/word-uci-cover-citations-20261008'
SOURCE = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v2_20261008.docx'
TARGET = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx'
BASE_QA = ROOT / '.agent/qa/word-uci-caption-math-20261008'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
W = '{' + NS['w'] + '}'
MARKER = re.compile(r'[ \t]*\[\d+(?:\s*[-–,;]\s*\d+)*\](?:[ \t]*[,;][ \t]*(?=\[))?')

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def txt(e):
    return ''.join(e.xpath('.//w:t/text()', namespaces=NS))

def style(p):
    v = p.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS)
    return v[0] if v else 'Normal'

def c14n(e):
    return etree.tostring(e, method='c14n')

def reference_xml(e):
    copy = deepcopy(e)
    for node in copy.iter():
        node.attrib.pop('{http://schemas.microsoft.com/office/word/2010/wordml}textId', None)
    return c14n(copy)

def body_inventory(body, strip):
    references = False
    result = []
    for child in list(body)[29:]:
        for p in child.iter(W + 'p'):
            value = txt(p)
            if value == 'TÀI LIỆU THAM KHẢO':
                references = True
            if style(p).upper().startswith('TOC'):
                continue
            if strip and not references:
                value = MARKER.sub('', value)
            result.append((style(p), value))
    return result

manifest = load(QA / 'patch-manifest.json')
checks = {}
checks['all_source_hashes_unchanged'] = all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in manifest['source_hashes'].items())
checks['original_report_hash_unchanged'] = hashlib.sha256((ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_20261008.docx').read_bytes()).hexdigest() == '51edbc9ba1f27e2d2c194eabca31f8f7fcd15568b5edc5ea1a8cdb9097582fe2'
with ZipFile(SOURCE) as source, ZipFile(TARGET) as target:
    checks['source_and_output_crc_valid'] = source.testzip() is None and target.testzip() is None
    sr = etree.fromstring(source.read('word/document.xml'))
    tr = etree.fromstring(target.read('word/document.xml'))
    sb, tb = sr.find('w:body', NS), tr.find('w:body', NS)
    checks['all_media_bytes_unchanged'] = all(source.read(n) == target.read(n) for n in source.namelist() if n.startswith('word/media/'))
    checks['styles_and_numbering_bytes_unchanged'] = all(source.read(n) == target.read(n) for n in ['word/styles.xml', 'word/numbering.xml'])
    checks['header_footer_bytes_unchanged'] = all(source.read(n) == target.read(n) for n in source.namelist() if re.match(r'word/(header|footer)\d+\.xml$', n))
    checks['section_geometry_and_border_unchanged'] = [c14n(e) for e in sr.xpath('.//w:sectPr', namespaces=NS)] == [c14n(e) for e in tr.xpath('.//w:sectPr', namespaces=NS)]
    checks['all_three_equations_xml_unchanged_from_v2'] = [c14n(e) for e in sr.xpath('.//m:oMath', namespaces=NS)] == [c14n(e) for e in tr.xpath('.//m:oMath', namespaces=NS)] and len(tr.xpath('.//m:oMath', namespaces=NS)) == 3
    checks['mae_native_absolute_delimiter'] = len(tr.xpath('.//m:d[m:dPr/m:begChr[@m:val="|"]][m:dPr/m:endChr[@m:val="|"]]', namespaces=NS)) == 1
    checks['outside_cover_text_and_styles_equal_except_removed_markers'] = body_inventory(sb, True) == body_inventory(tb, False)
    refs = False
    body_markers, reference_numbers, references = [], [], []
    for p in tb.iter(W + 'p'):
        value = txt(p)
        if value == 'TÀI LIỆU THAM KHẢO':
            refs = True
        if not refs:
            body_markers.extend(MARKER.findall(value))
        elif re.match(r'^\[\d+\]', value):
            reference_numbers.append(int(re.match(r'^\[(\d+)\]', value).group(1)))
            references.append(reference_xml(p))
    source_refs = [reference_xml(p) for p in sb.iter(W + 'p') if re.match(r'^\[\d+\]', txt(p))]
    checks['zero_citation_markers_before_references'] = len(body_markers) == 0
    checks['29_markers_removed_exactly'] = manifest['removed_markers'] == 29
    checks['16_reference_entries_numbers_and_xml_preserved'] = reference_numbers == list(range(1, 17)) and source_refs == references
    checks['16_hyperlinks_preserved'] = len(tr.xpath('.//w:hyperlink[@r:id]', namespaces=NS)) == 16 and [c14n(e) for e in sr.xpath('.//w:hyperlink[@r:id]', namespaces=NS)] == [c14n(e) for e in tr.xpath('.//w:hyperlink[@r:id]', namespaces=NS)]
    checks['seven_tables_keep_geometry_and_rows'] = len(tb.findall('w:tbl', NS)) == 7 and [(c14n(e.find('w:tblPr', NS)), c14n(e.find('w:tblGrid', NS)), len(e.findall('w:tr', NS))) for e in sb.findall('w:tbl', NS)] == [(c14n(e.find('w:tblPr', NS)), c14n(e.find('w:tblGrid', NS)), len(e.findall('w:tr', NS))) for e in tb.findall('w:tbl', NS)]
    checks['three_images_geometry_unchanged'] = len(tr.xpath('.//w:drawing', namespaces=NS)) == 3 and [c14n(e) for e in sr.xpath('.//w:drawing', namespaces=NS)] == [c14n(e) for e in tr.xpath('.//w:drawing', namespaces=NS)]
    covers = list(tb)[:28]
    cover_text = '\n'.join(txt(e) for e in covers)
    members = [('2001230640', 'Nguyễn Đức Thành Phát'), ('2001230227', 'Lý Vũ Nhân Hậu'), ('2001230418', 'Nguyễn Tuấn Khôi')]
    checks['three_confirmed_members_on_both_covers'] = all(cover_text.count(f'{n} – {name}') == 2 for n, name in members)
    checks['teacher_preserved'] = cover_text.count('Nguyễn Thành Ngô') == 1
    checks['cover_font_sizes_match_template_roles'] = all(all(v == '40' for v in list(tb)[i].xpath('.//w:r[w:t]/w:rPr/w:sz/@w:val', namespaces=NS)) for i in [6, 19]) and all(list(tb)[i].xpath('.//w:r[w:t]/w:rPr/w:sz/@w:val', namespaces=NS) == ['32'] for i in [7, 20])
    checks['members_consistently_left_aligned'] = all(list(tb)[i].xpath('./w:pPr/w:jc/@w:val', namespaces=NS) == ['left'] and list(tb)[i].xpath('./w:pPr/w:ind/@w:left', namespaces=NS) == ['1440'] for i in [9, 10, 11, 24, 25, 26])
    captions = [txt(p) for p in tb.iter(W + 'p') if style(p) in ('TableCaption', 'FigureCaption')]
    checks['five_correct_caption_numbers'] = len(captions) == 5 and [re.match(r'^(Bảng|Hình) (\d+\.\d+)', s).group() for s in captions] == ['Bảng 1.1', 'Bảng 1.2', 'Bảng 1.3', 'Bảng 1.4', 'Hình 1.1']
    fields = tr.xpath('.//w:fldSimple/@w:instr|.//w:instrText/text()', namespaces=NS)
    checks['numeric_chapter_fields_and_seq_preserved'] = len([s for s in fields if 'STYLEREF "ChapterTitle"' in s and '\\n' in s and '\\t' in s]) == 5 and len([s for s in fields if re.search(r'\bSEQ (Table|Figure)', s)]) == 5

word = load(QA / 'final-word.json')
base_word = load(BASE_QA / 'final-word.json')
pages = load(QA / 'final-pdf.json')
checks['37_pages_three_tocs_92_headings'] = word['pages'] == 37 and word['toc_count'] == 3 and len(word['headings']) == 92 and len(pages) == 37
checks['headings_and_pages_unchanged'] = word['headings'] == base_word['headings']
checks['three_toc_results_unchanged'] = word['tocs'] == base_word['tocs']
checks['blank_parts_and_ch2_ch5_render_pixel_identical'] = all(ImageChops.difference(Image.open(QA / f'final-render/page-{n}.png').convert('RGB'), Image.open(BASE_QA / f'final-render/page-{n}.png').convert('RGB')).getbbox() is None for n in list(range(3, 14)) + list(range(27, 38)))
checks['caption_insert_delete_and_list_probes_pass'] = all(load(QA / 'caption-probes.json')['checks'].values())
heading = load(QA / 'heading-probes.json')
checks['heading_toc_probes_pass'] = heading['inserted_h2'] == '3.2.' and heading['following_h2'] == '3.3.' and heading['restored_h2'] == '3.2.' and heading['inserted_h3'] == '3.1.1.' and heading['toc_detects_inserted'] and heading['toc_detects_h3']
checks['arabic_footer_1_to_25_increments'] = all(re.match(rf'^{n - 12}\r?\n', pages[n - 1]['text']) for n in range(13, 38))
checks['roman_front_i_to_x'] = all(pages[n - 1]['text'].splitlines()[0] == label for n, label in zip(range(3, 13), ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']))
checks['no_rendered_field_errors'] = not any(re.search(r'Error!|Reference source not found|Bookmark not defined|Lỗi!|Ошибка', p['text'], re.I) for p in pages)
result = {'status': 'PASS' if all(checks.values()) else 'FAIL', 'target': str(TARGET), 'sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest(), 'checks': checks, 'pages': 37, 'removed_markers': 29, 'remaining_body_markers': len(body_markers), 'reference_count': len(reference_numbers), 'captions': captions, 'render_limit': 'Native Microsoft Word/PDFium verified; packaged LibreOffice unavailable, no verification of GPT-web renderer.'}
(QA / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'status': result['status'], 'passed': sum(checks.values()), 'total': len(checks), 'failed': [k for k, v in checks.items() if not v], 'sha256': result['sha256']}, ensure_ascii=False))
if not all(checks.values()):
    raise SystemExit(1)
