import ast
import hashlib
import json
import posixpath
import re
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w021-20261010'
OLD = ROOT / '.agent/qa/word-w02-20261010'
SOURCE = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W02_v1_20261010.docx'
OUTPUT = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W02_1_v1_20261010.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W = '{' + NS['w'] + '}'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda b: hashlib.sha256(b).hexdigest()
text = lambda n: ''.join(n.xpath('.//w:t/text()', namespaces=NS))
package = lambda p: {n: z.read(n) for z in [ZipFile(BytesIO(p.read_bytes()))] for n in z.namelist()}
for name, wanted in [('verify_word_w011.py', ('semantic', 'canonical')), ('verify_word_w02.py', ('relationships', 'section_roles', 'pictures'))]:
    tree = ast.parse((ROOT / '.agent/scripts' / name).read_text(encoding='utf-8'))
    defs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted]
    exec(compile(ast.Module(body=defs, type_ignores=[]), name, 'exec'))
src, out = package(SOURCE), package(OUTPUT)
sd, od = E.fromstring(src['word/document.xml']), E.fromstring(out['word/document.xml'])
sp, op = [d.xpath('./w:body/w:p', namespaces=NS) for d in (sd, od)]
st, ot = [d.xpath('./w:body/w:tbl', namespaces=NS) for d in (sd, od)]
changes = read(QA / 'changes.json')
rb = read(QA / 'word-readback.json')
checks = []


def check(name, passed, evidence=None):
    checks.append({'id': name, 'status': 'PASS' if passed else 'FAIL', 'evidence': evidence})


check('W02_source_preserved', sha(SOURCE.read_bytes()) == changes['source_sha256'] == read(OLD / 'verification.json')['sha256'])
check('Thy_W011_source_preserved', sha((ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx').read_bytes()) == read(OLD / 'preflight.json')['source_sha256'])
check('18_tables_618_paragraphs', len(st) == len(ot) == 18 and len(sp) == len(op) == 618)
rows = ot[0].findall(W + 'tr')
schedule = [[text(c) for c in r.findall(W + 'tc')] for r in rows]
check('schedule_exact_four_columns_three_weeks', schedule == changes['schedule_after'] and len(rows) == 4 and all(len(r.findall(W + 'tc')) == 4 for r in rows), schedule)
check('Minh_chung_column_deleted_not_hidden', len(ot[0].find(W + 'tblGrid')) == 4 and 'Minh chứng' not in text(ot[0]))
check('four_widths_match_cells_and_table', [int(c.get(W + 'w')) for c in ot[0].find(W + 'tblGrid')] == changes['column_widths_twips'] and sum(changes['column_widths_twips']) == 8504 and all([int(c.find('./' + W + 'tcPr/' + W + 'tcW').get(W + 'w')) for c in r.findall(W + 'tc')] == changes['column_widths_twips'] for r in rows))
check('schedule_TNR_12_no_fixed_height', all(f == 'Times New Roman' for f in ot[0].xpath('.//w:rFonts/@w:ascii', namespaces=NS)) and all(s == '24' for s in ot[0].xpath('.//w:sz/@w:val', namespaces=NS)) and not ot[0].xpath('.//w:trHeight[@w:hRule="exact"]', namespaces=NS))
check('no_fabricated_schedule_dates_or_presentation_completion', not re.search(r'\d{1,2}/\d{1,2}|hoàn thành thuyết trình|bảo vệ thành công', text(ot[0]), re.I))
check('week_three_in_progress', schedule[3][3] == 'Đang thực hiện')
for i, (a, b) in enumerate(zip(st, ot)):
    if i:
        check('table_' + str(i) + '_unchanged_semantics', semantic(a) == semantic(b))
check('Phat_assignment_and_blank_percentages_preserved', 'Chương 3, 4, 5;' in text(ot[1]) and 'bằng Excel.' in text(ot[1]) and all(not text(r.findall(W + 'tc')[4]).strip() for r in ot[1].findall(W + 'tr')[1:]))
allowed = {c['index']: c for c in changes['access_date_changes']}
diff, unexpected = [], []
for i, (a, b) in enumerate(zip(sp, op)):
    styles = a.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS)
    if any(s.lower().startswith('toc') for s in styles):
        continue
    if text(a) != text(b):
        diff.append(i)
        c = allowed.get(i)
        if not c or text(a) != c['before'] or text(b) != c['after']:
            unexpected.append(i)
check('only_21_exact_reference_date_deletions', set(diff) == set(allowed) and len(diff) == 21 and not unexpected, {'indices': diff, 'unexpected': unexpected})
check('all_paragraph_styles_preserved', all(a.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS) == b.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS) for a, b in zip(sp, op)))
check('no_access_date_labels_remain', not re.search(r'Truy cập ngày|Ngày truy cập|Xem ngày|Accessed:', text(od), re.I))
refs = [text(p) for p in op if re.match(r'^\[\d+\]', text(p))]
check('21_references_numbered_in_original_order', [int(re.match(r'^\[(\d+)\]', r).group(1)) for r in refs] == list(range(1, 22)))
hyper = lambda d, rs: [(text(h), rs[h.get('{' + NS['r'] + '}id')][1], rs[h.get('{' + NS['r'] + '}id')][2]) for h in d.xpath('//w:hyperlink[@r:id]', namespaces=NS)]
check('21_external_hyperlinks_text_URL_mode_preserved', hyper(sd, relationships(src)) == hyper(od, relationships(out)) and len(hyper(od, relationships(out))) == 21)
check('publication_years_DOI_versions_retained', all(re.findall(r'\d+(?:[.,/]\d+)*', re.sub(r'\s*Truy cập ngày\s+\d{1,2}/\d{1,2}/\d{4}\.', '', c['before'])) == re.findall(r'\d+(?:[.,/]\d+)*', c['after']) for c in allowed.values()))
check('two_cover_paragraphs_unchanged', [semantic(p) for p in sp[:25]] == [semantic(p) for p in op[:25]])
check('section_geometry_and_footer_roles_preserved', section_roles(sd, src) == section_roles(od, out))
check('headers_footers_preserved', all(src[n] == out[n] for n in src if re.match(r'word/(header|footer)\d+\.xml$', n)))
check('styles_numbering_theme_identical', all(src[n] == out[n] for n in ('word/styles.xml', 'word/numbering.xml', 'word/theme/theme1.xml')))
check('five_equations_identical', len(od.xpath('//m:oMath', namespaces=NS)) == 5 and [canonical(n) for n in sd.xpath('//m:oMath', namespaces=NS)] == [canonical(n) for n in od.xpath('//m:oMath', namespaces=NS)])
check('all_ten_inline_image_bytes_unchanged', [(x['paragraph_index'], x['sha256']) for x in pictures(sd, src)] == [(x['paragraph_index'], x['sha256']) for x in pictures(od, out)])
check('image_dimensions_and_crops_unchanged', [canonical(n) for n in sd.xpath('//wp:inline', namespaces=NS)] == [canonical(n) for n in od.xpath('//wp:inline', namespaces=NS)])
caps = lambda d: [text(p) for p in d.xpath('./w:body/w:p[w:pPr/w:pStyle[@w:val="FigureCaption" or @w:val="TableCaption"]]', namespaces=NS)]
check('all_23_captions_preserved', caps(sd) == caps(od) and len(caps(od)) == 23)
check('native_Word_counts_fields_and_pages', rb['tables'] == 18 and rb['equations'] == 5 and rb['inline_shapes'] == 10 and rb['toc'] == 3 and rb['pages'] > 60, rb['pages'])
check('field_results_no_errors', not any(re.search(r'Error!|Lỗi!|Reference source not found|Bookmark not defined', f['result']) for f in rb['fields']))
bookmarks = od.xpath('//w:bookmarkStart/@w:name', namespaces=NS)
codes = od.xpath('//w:instrText/text()|//w:fldSimple/@w:instr', namespaces=NS)
targets = [m.group(1) for code in codes for m in re.finditer(r'\b(?:REF|PAGEREF)\s+(\S+)', code)]
check('cross_reference_targets_exist', all(t in bookmarks for t in targets))
check('five_chapters_69_subheadings', sum(p['style'] == 'Heading 1' for p in rb['paragraphs']) == 5 and sum(p['style'] == 'Heading 21' for p in rb['paragraphs']) == 69)
body = '\n'.join(text(p) for p in op[155:597] if not p.xpath('./w:pPr/w:pStyle[@w:val="TableCaption" or @w:val="FigureCaption"]', namespaces=NS))
check('redundant_body_leads_not_reintroduced', not re.search(r'(?:Hình|Bảng)\s+\d+\.\d+|(?:biểu đồ|bảng)\s+(?:bên|dưới)\s+(?:dưới|đây)', body, re.I))
guards = read(ROOT / '.agent/qa/word-w011-20261010/preflight.json')['guards']
guardresults = [{'path': p, 'expected': h, 'actual': sha(Path(p).read_bytes())} for p, h in guards.items()]
check('37_product_source_template_guards_unchanged', len(guardresults) == 37 and all(x['expected'] == x['actual'] for x in guardresults), guardresults)
render = read(QA / 'render-pages.json')
check('render_matches_native_count_no_blank_pages', render['page_count'] == rb['pages'] and all(Path(p['image']).is_file() and len(p['text'].strip()) > 20 for p in render['pages']))
oldrender = read(OLD / 'render-pages.json')
identical, changed = [], []
for new, old in zip(render['pages'], oldrender['pages']):
    with Image.open(new['image']) as ni, Image.open(old['image']) as oi:
        (identical if ni.size == oi.size and ImageChops.difference(ni.convert('RGB'), oi.convert('RGB')).getbbox() is None else changed).append(new['page'])
(QA / 'page-diff.json').write_text(json.dumps({'pixel_identical': identical, 'changed': changed, 'new_pages': rb['pages'], 'old_pages': oldrender['page_count']}, indent=2), encoding='utf-8')
result = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
          'artifact_status': 'APPLIED_UNVERIFIED_UNTIL_VISUAL_REVIEW', 'output': str(OUTPUT),
          'sha256': sha(OUTPUT.read_bytes()), 'source_sha256': sha(SOURCE.read_bytes()),
          'passed': sum(c['status'] == 'PASS' for c in checks), 'total': len(checks), 'checks': checks,
          'pages': rb['pages'], 'guard_scope': '37 explicit sources/products/templates; no whole-runtime audit or model execution',
          'hyperlink_scope': 'DOCX external relationship validity and unchanged URL, not renewed HTTP availability test'}
(QA / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: result[k] for k in ('status', 'passed', 'total', 'sha256', 'pages')}, ensure_ascii=False))
print(json.dumps([c for c in checks if c['status'] == 'FAIL'], ensure_ascii=False, indent=2))
