import ast
import csv
import hashlib
import json
import posixpath
import re
from collections import Counter
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E
from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w02-20261010'
SOURCE = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx'
OUTPUT = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W02_v1_20261010.docx'
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
tree = ast.parse((ROOT / '.agent/scripts/verify_word_w011.py').read_text(encoding='utf-8'))
defs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('semantic', 'canonical')]
exec(compile(ast.Module(body=defs, type_ignores=[]), 'reused-safe-functions', 'exec'))
src, out = package(SOURCE), package(OUTPUT)
sd, od = E.fromstring(src['word/document.xml']), E.fromstring(out['word/document.xml'])
sp, op = [d.xpath('./w:body/w:p', namespaces=NS) for d in (sd, od)]
st, ot = [d.xpath('./w:body/w:tbl', namespaces=NS) for d in (sd, od)]
rb = read(QA / 'word-readback.json')
changes = read(QA / 'changes.json')
checks = []


def check(name, passed, evidence=None):
    checks.append({'id': name, 'status': 'PASS' if passed else 'FAIL', 'evidence': evidence})


def relationships(parts):
    return {r.get('Id'): (r.get('Type'), r.get('Target'), r.get('TargetMode'))
            for r in E.fromstring(parts['word/_rels/document.xml.rels'])}


def pictures(d, parts):
    rels = relationships(parts)
    found = []
    for p in d.xpath('./w:body/w:p', namespaces=NS):
        for b in p.xpath('.//a:blip', namespaces=NS):
            rid = b.get('{' + NS['r'] + '}embed')
            part = posixpath.normpath('word/' + rels[rid][1])
            found.append({'paragraph_index': list(d.xpath('./w:body/w:p', namespaces=NS)).index(p),
                          'part': part, 'sha256': sha(parts[part])})
    return found


check('source_unchanged_current_Thy_revision', sha(SOURCE.read_bytes()) == read(QA / 'preflight.json')['source_sha256'])
check('18_tables_618_top_level_paragraphs', len(st) == len(ot) == 18 and len(sp) == len(op) == 618)
allowed = {c['index']: c for c in changes if c['kind'] == 'body_prose'}
diff, unexpected = [], []
for i, (a, b) in enumerate(zip(sp, op)):
    style = a.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS)
    if any(s.lower().startswith('toc') for s in style):
        continue
    if text(a) != text(b):
        diff.append(i)
        c = allowed.get(i)
        if not c or text(a) != c['before'] or text(b) != c['after']:
            unexpected.append(i)
check('14_prose_diffs_only_exact_whitelist', set(diff) == set(allowed) and not unexpected, {'indices': diff, 'unexpected': unexpected})
check('all_paragraph_styles_preserved', all(a.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS) == b.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS) for a, b in zip(sp, op)))
cell_diff = []
for ti, (a, b) in enumerate(zip(st, ot)):
    ra, rb_ = a.findall(W + 'tr'), b.findall(W + 'tr')
    check('table_' + str(ti) + '_row_column_shape', len(ra) == len(rb_) and all(len(x.findall(W + 'tc')) == len(y.findall(W + 'tc')) for x, y in zip(ra, rb_)))
    for ri, (x, y) in enumerate(zip(ra, rb_)):
        for ci, (u, v) in enumerate(zip(x.findall(W + 'tc'), y.findall(W + 'tc'))):
            if semantic(u) != semantic(v):
                cell_diff.append((ti, ri, ci))
check('only_Phats_assignment_cell_changed', cell_diff == [(1, 1, 3)], cell_diff)
check('Phat_assignment_matches_request', 'Chương 3, 4, 5;' in text(ot[1]) and 'bằng Excel.' in text(ot[1]))
check('unconfirmed_contribution_percentages_blank', all(not text(r.findall(W + 'tc')[4]).strip() for r in ot[1].findall(W + 'tr')[1:]))
check('tables_numeric_values_preserved', all(re.findall(r'\d+(?:[.,/]\d+)*', semantic(a)) == re.findall(r'\d+(?:[.,/]\d+)*', semantic(b)) for i, (a, b) in enumerate(zip(st, ot)) if i != 1))
check('styles_numbering_theme_identical', all(src[n] == out[n] for n in ('word/styles.xml', 'word/numbering.xml', 'word/theme/theme1.xml')))
def section_roles(d, parts):
    rels = relationships(parts)
    nodes = deepcopy(d.xpath('//w:sectPr', namespaces=NS))
    for n in nodes:
        for ref in n.xpath('./w:footerReference|./w:headerReference', namespaces=NS):
            attr = '{' + NS['r'] + '}id'
            ref.set(attr, rels[ref.get(attr)][1])
    return [canonical(n) for n in nodes]


check('section_geometry_and_footer_roles_preserved', section_roles(sd, src) == section_roles(od, out))
check('headers_footers_preserved', all(src[n] == out[n] for n in src if re.match(r'word/(header|footer)\d+\.xml$', n)))
check('two_cover_paragraphs_preserved', [semantic(p) for p in sp[:25]] == [semantic(p) for p in op[:25]])
check('five_native_math_equations_identical', len(od.xpath('//m:oMath', namespaces=NS)) == 5 and [canonical(x) for x in sd.xpath('//m:oMath', namespaces=NS)] == [canonical(x) for x in od.xpath('//m:oMath', namespaces=NS)])
sr, rr = relationships(src), relationships(out)
hyper = lambda d, rs: [(text(h), rs[h.get('{' + NS['r'] + '}id')][1]) for h in d.xpath('//w:hyperlink[@r:id]', namespaces=NS)]
check('21_live_external_reference_relationships_preserved', hyper(sd, sr) == hyper(od, rr) and len(hyper(od, rr)) == 21)
refs = lambda ps_: [text(p) for p in ps_ if re.match(r'^\[\d+\]', text(p))]
check('21_references_unchanged_at_W02', refs(sp) == refs(op) and len(refs(op)) == 21)
check('access_dates_not_removed_before_W021', sum('Truy cập ngày' in r for r in refs(op)) == 21)
body = '\n'.join(text(p) for p in op[155:597] if not p.xpath('./w:pPr/w:pStyle[@w:val="TableCaption" or @w:val="FigureCaption"]', namespaces=NS))
leads = re.findall(r'(?i)(?:Hình|Bảng)\s+\d+\.\d+|(?:biểu đồ|bảng)\s+(?:bên|dưới)\s+(?:dưới|đây)', body)
check('no_redundant_numbered_body_leads', not leads, leads)
caps = [p['text'] for p in rb['paragraphs'] if p['style'] in ('TableCaption', 'FigureCaption')]
check('23_captions_8_figures_15_tables', len(caps) == 23 and sum(t.startswith('Hình') for t in caps) == 8 and sum(t.startswith('Bảng') for t in caps) == 15, caps)
check('captions_preserved', [text(p) for p in sp if p.xpath('./w:pPr/w:pStyle[@w:val="TableCaption" or @w:val="FigureCaption"]', namespaces=NS)] == caps)
check('native_field_counts_pages', rb['pages'] == 69 and rb['tables'] == 18 and rb['equations'] == 5 and rb['toc'] == 3 and rb['inline_shapes'] == 10)
check('field_results_no_errors', not any(re.search(r'Error!|Lỗi!|Reference source not found|Bookmark not defined', f['result']) for f in rb['fields']))
bookmarks = od.xpath('//w:bookmarkStart/@w:name', namespaces=NS)
codes = od.xpath('//w:instrText/text()|//w:fldSimple/@w:instr', namespaces=NS)
targets = [m.group(1) for code in codes for m in re.finditer(r'\b(?:REF|PAGEREF)\s+(\S+)', code)]
check('remaining_crossrefs_have_bookmark_targets', all(t in bookmarks for t in targets), {'targets': len(targets)})
check('five_chapters_69_numbered_subheadings', sum(p['style'] == 'Heading 1' for p in rb['paragraphs']) == 5 and sum(p['style'] == 'Heading 21' for p in rb['paragraphs']) == 69)
si, oi = pictures(sd, src), pictures(od, out)
check('10_inline_images_with_seven_W02_slots', len(si) == len(oi) == 10)
check('logo_and_original_H11_bytes_preserved', [p['sha256'] for p in si[:3]] == [p['sha256'] for p in oi[:3]])
check('five_active_screenshot_bytes_preserved_in_package', all(p['sha256'] in {sha(b) for n, b in out.items() if n.startswith('word/media/')} for p in si if p['paragraph_index'] in (508, 552, 555, 563, 568)))
check('original_Excel_screenshot_preserved_in_source_and_QA', sha((QA / 'source-images/image3.png').read_bytes()) == si[3]['sha256'])
check('H32_uses_correct_Overview_source', oi[4]['sha256'] == si[6]['sha256'])
check('all_seven_active_figures_nonblack', all(sum(ImageStat.Stat(Image.open(BytesIO(out[p['part']])).convert('RGB')).mean) > 20 for p in oi[3:]))
records = read(QA / 'hourly-table-records.json')
csvpath = Path(records['csv'])
check('Flink_hourly_CSV_hash_preserved', sha(csvpath.read_bytes()) == records['sha256'])
with csvpath.open(encoding='utf-8-sig', newline='') as f:
    actual = {r['hour_start']: r for r in csv.DictReader(f) if r['hour_start'] in {x['hour_start'] for x in records['source_records']}}
check('all_six_H31_rows_match_locked_CSV', all(actual[x['hour_start']] == x for x in records['source_records']) and len(actual) == 6)
check('H31_keeps_NULL_not_zero', records['display_rows'][4][3] == 'NULL' and records['display_rows'][4][5] == 'NULL' and records['display_rows'][0][5] == 'NULL')
check('H31_generated_image_matches_embedded_bytes', oi[3]['sha256'] == sha((QA / 'hourly-table.png').read_bytes()))
guards = read(ROOT / '.agent/qa/word-w011-20261010/preflight.json')['guards']
guardresults = [{'path': p, 'expected': h, 'actual': sha(Path(p).read_bytes())} for p, h in guards.items()]
check('37_existing_product_source_template_guards_unchanged', len(guardresults) == 37 and all(x['expected'] == x['actual'] for x in guardresults), guardresults)
render = read(QA / 'render-pages.json')
check('69_page_PNGs_no_empty_page', len(render['pages']) == 69 and all(Path(p['image']).is_file() and len(p['text'].strip()) > 20 for p in render['pages']))
result = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
          'artifact_status': 'APPLIED_UNVERIFIED_UNTIL_VISUAL_REVIEW', 'output': str(OUTPUT),
          'sha256': sha(OUTPUT.read_bytes()), 'source_sha256': sha(SOURCE.read_bytes()),
          'passed': sum(c['status'] == 'PASS' for c in checks), 'total': len(checks), 'checks': checks,
          'active_images': oi, 'guard_scope': '37 explicit sources/products/templates, not a renewed whole-runtime snapshot'}
(QA / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: result[k] for k in ('status', 'passed', 'total', 'sha256')}, ensure_ascii=False))
print(json.dumps([c for c in checks if c['status'] == 'FAIL'], ensure_ascii=False, indent=2))
