import hashlib
import json
import re
import zipfile
from pathlib import Path

from docx import Document
from lxml import etree
from PIL import Image, ImageChops

root = Path(r'D:\Hoctap\bigdata\Detaituan8910')
source = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_20261008.docx'
target = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v2_20261008.docx'
qa = root / '.agent/qa/word-uci-caption-math-20261008'
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
checks = {}
details = {}
with zipfile.ZipFile(source) as a, zipfile.ZipFile(target) as b:
    x = etree.fromstring(a.read('word/document.xml'))
    y = etree.fromstring(b.read('word/document.xml'))
    checks['source_hash_unchanged'] = hashlib.sha256(source.read_bytes()).hexdigest() == '51edbc9ba1f27e2d2c194eabca31f8f7fcd15568b5edc5ea1a8cdb9097582fe2'
    checks['both_zip_crc_valid'] = a.testzip() is None and b.testzip() is None
    checks['all_media_bytes_unchanged'] = all(a.read(n) == b.read(n) for n in a.namelist() if n.startswith('word/media/'))
    checks['styles_unchanged'] = a.read('word/styles.xml') == b.read('word/styles.xml')
    checks['numbering_unchanged'] = a.read('word/numbering.xml') == b.read('word/numbering.xml')
    def paragraphs(xml):
        return [(p.xpath('string(w:pPr/w:pStyle/@w:val)', namespaces=ns), ''.join(p.xpath('.//w:t/text()', namespaces=ns))) for p in xml.xpath('./w:body/w:p', namespaces=ns)]
    checks['all_paragraph_styles_and_display_text_unchanged'] = paragraphs(x) == paragraphs(y)
    checks['all_table_xml_unchanged'] = [etree.tostring(t) for t in x.xpath('./w:body/w:tbl', namespaces=ns)] == [etree.tostring(t) for t in y.xpath('./w:body/w:tbl', namespaces=ns)]
    checks['sections_xml_unchanged'] = [etree.tostring(t) for t in x.xpath('.//w:sectPr', namespaces=ns)] == [etree.tostring(t) for t in y.xpath('.//w:sectPr', namespaces=ns)]
    source_math = x.xpath('.//m:oMath', namespaces=ns)
    target_math = y.xpath('.//m:oMath', namespaces=ns)
    checks['three_editable_equations'] = len(target_math) == len(source_math) == 3
    checks['energy_and_rmse_xml_unchanged'] = all(etree.tostring(source_math[i]) == etree.tostring(target_math[i]) for i in (0, 2))
    mae = target_math[1]
    checks['mae_native_absolute_pair'] = mae.xpath('./m:nary/m:e/m:d/m:dPr/m:begChr/@m:val', namespaces=ns) == ['|'] and mae.xpath('./m:nary/m:e/m:d/m:dPr/m:endChr/@m:val', namespaces=ns) == ['|']
    checks['mae_correct_residual'] = ''.join(mae.xpath('./m:nary/m:e/m:d/m:e//m:t/text()', namespaces=ns)) == 'yi-yi' and len(mae.xpath('./m:nary/m:e/m:d/m:e/m:sSub', namespaces=ns)) == 2 and len(mae.xpath('./m:nary/m:e/m:d/m:e/m:sSub/m:e/m:acc', namespaces=ns)) == 1
    checks['mae_limits_and_fraction'] = ''.join(mae.xpath('./m:nary/m:sub//m:t/text()', namespaces=ns)) == 'i=1' and ''.join(mae.xpath('./m:nary/m:sup//m:t/text()', namespaces=ns)) == 'n' and ''.join(mae.xpath('./m:f/m:num//m:t/text()', namespaces=ns)) == '1' and ''.join(mae.xpath('./m:f/m:den//m:t/text()', namespaces=ns)) == 'n'
    caps = [p for p in y.xpath('./w:body/w:p', namespaces=ns) if p.xpath('string(w:pPr/w:pStyle/@w:val)', namespaces=ns) in ('FigureCaption','TableCaption')]
    details['captions'] = [''.join(p.xpath('.//w:t/text()', namespaces=ns)) for p in caps]
    instructions = [s for p in caps for s in p.xpath('.//w:instrText/text() | .//w:fldSimple/@w:instr', namespaces=ns)]
    checks['five_caption_numbers'] = len(caps) == 5 and all(re.match(r'^(Bảng 1\.[1-4]|Hình 1\.1)\. ', text) for text in details['captions'])
    checks['five_numeric_chapter_fields'] = sum('STYLEREF' in s and '\\n' in s and '\\t' in s for s in instructions) == 5
    checks['five_seq_fields'] = sum('SEQ ' in s and '\\s 1' in s for s in instructions) == 5
    rels_a = etree.fromstring(a.read('word/_rels/document.xml.rels'))
    rels_b = etree.fromstring(b.read('word/_rels/document.xml.rels'))
    def links(xml):
        return sorted(el.get('Target') for el in xml if el.get('TargetMode') == 'External' and el.get('Type', '').endswith('/hyperlink'))
    checks['16_external_links_unchanged'] = len(links(rels_b)) == 16 and links(rels_a) == links(rels_b)
    checks['no_probe_or_new_prose'] = not any(s in ''.join(y.xpath('.//w:t/text()', namespaces=ns)) for s in ('QA SEQ probe','Kiểm thử chèn heading','Kiểm thử mục cấp ba','Kiểm thử mục cấp ba'))
doc = Document(target)
checks['seven_tables_three_sections'] = len(doc.tables) == 7 and len(doc.sections) == 3
word = json.loads((qa / 'final-word.json').read_text(encoding='utf-8-sig'))
base_word = json.loads((qa / 'source-word.json').read_text(encoding='utf-8-sig'))
checks['37_pages_92_headings_three_tocs'] = word['pages'] == 37 and len(word['headings']) == 92 and word['toc_count'] == 3
checks['heading_number_and_pages_unchanged'] = word['headings'] == base_word['headings']
checks['three_toc_contents_unchanged'] = word['tocs'] == base_word['tocs']
field_update = json.loads((qa / 'field-update.json').read_text(encoding='utf-8-sig'))
checks['word_update_correct_caption_results'] = field_update['captions'] == details['captions'] and field_update['equations'] == 3
probes = json.loads((qa / 'caption-probes.json').read_text(encoding='utf-8-sig'))
checks['seq_and_lists_insert_delete_pass'] = all(probes['checks'].values()) and probes['changes_saved'] is False
headings = json.loads((qa / 'heading-probes.json').read_text(encoding='utf-8-sig'))
checks['toc_heading_probes_pass'] = headings['inserted_h2'] == '3.2.' and headings['following_h2'] == '3.3.' and headings['restored_h2'] == '3.2.' and headings['inserted_h3'] == '3.1.1.' and headings['toc_detects_inserted'] and headings['toc_detects_h3'] and headings['changes_saved'] is False
changed_pages = []
for page in range(1, 38):
    left = Image.open(qa / f'source-render/page-{page}.png').convert('RGB')
    right = Image.open(qa / f'final-render/page-{page}.png').convert('RGB')
    if left.size != right.size or ImageChops.difference(left, right).getbbox():
        changed_pages.append(page)
checks['only_math_page_visually_changed'] = changed_pages == [20]
details['pixel_changed_pages'] = changed_pages
checks['all_other_36_pages_pixel_identical'] = len(changed_pages) == 1
math_page = Image.open(qa / 'final-render/page-20.png').convert('RGB')
checks['no_red_error_glyphs_on_math_page'] = not any(r > 150 and g < 120 and b < 120 and r > 1.4 * max(g, b) for r, g, b in math_page.getdata())
pages = json.loads((qa / 'final-pdf.json').read_text(encoding='utf-8'))
checks['no_rendered_field_errors'] = all(not re.search(r'Error!|Lỗi!|Bookmark not defined|Reference source not found', p['text'], re.I) for p in pages)
details['source_native_render'] = 'Caption numbers and MAE bars are already correct in source Word/PDF render; user-reported third-party renderer is unavailable locally. Changed fields to numeric-only standard switches and MAE to paired OMML delimiter.'
details['cross_renderer_limit'] = 'Packaged LibreOffice unavailable; native Word/PDFium verified, no guarantee of every third-party parser.'
report = {'status': 'PASS' if all(checks.values()) else 'FAIL', 'source': str(source), 'target': str(target), 'target_sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'checks': checks, 'details': details}
(qa / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'status':report['status'],'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'changed_pages':changed_pages,'sha256':report['target_sha256']}, ensure_ascii=False))
if not all(checks.values()):
    raise SystemExit(1)
