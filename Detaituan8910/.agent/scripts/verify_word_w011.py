import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile

import pypdfium2 as pdfium
from docx import Document
from lxml import etree as E
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w011-20261010'
OLD_QA = ROOT / '.agent/qa/word-w01-20261010'
SOURCE = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
OUTPUT = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
W = '{' + NS['w'] + '}'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, data):
    (QA / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def package(path):
    with ZipFile(path) as z:
        return {name: z.read(name) for name in z.namelist()}


def semantic(node):
    result, instructions = [], []
    depth = 0

    def walk(element):
        nonlocal depth
        if element.tag == W + 'fldSimple':
            result.append('{FIELD:' + ' '.join(element.get(W + 'instr', '').split()) + '}')
            return
        if element.tag == W + 'fldChar':
            kind = element.get(W + 'fldCharType')
            if kind == 'begin':
                if depth == 0:
                    instructions.clear()
                depth += 1
            elif kind == 'end':
                depth -= 1
                if depth == 0:
                    result.append('{FIELD:' + ' '.join(''.join(instructions).split()) + '}')
            return
        if element.tag == W + 'instrText' and depth:
            instructions.append(element.text or '')
        elif element.tag == W + 't' and not depth:
            result.append(element.text or '')
        elif element.tag == W + 'br' and not depth:
            result.append('\n')
        elif element.tag == W + 'tab' and not depth:
            result.append('\t')
        for child in element:
            walk(child)

    walk(node)
    return ''.join(result)


def canonical(node):
    element = deepcopy(node)
    for item in element.iter():
        for attr in list(item.attrib):
            if E.QName(attr).localname.startswith(('rsid', 'paraId', 'textId')):
                del item.attrib[attr]
    return E.tostring(element, method='c14n')


src = package(SOURCE)
out = package(OUTPUT)
sd = E.fromstring(src['word/document.xml'])
od = E.fromstring(out['word/document.xml'])
sp = sd.xpath('/w:document/w:body/w:p', namespaces=NS)
op = od.xpath('/w:document/w:body/w:p', namespaces=NS)
st = sd.xpath('/w:document/w:body/w:tbl', namespaces=NS)
ot = od.xpath('/w:document/w:body/w:tbl', namespaces=NS)
changes = read(QA / 'changes.json')
rb = read(QA / 'word-readback.json')
old_rb = read(OLD_QA / 'word-readback.json')
checks = []


def check(name, passed, evidence=None):
    checks.append({'id': name, 'status': 'PASS' if passed else 'FAIL', 'evidence': evidence})


guards = read(QA / 'preflight.json')['guards']
drift = [str(path) for path, expected in guards.items() if sha(Path(path)) != expected]
check('source_guards_unchanged', not drift, {'count': len(guards), 'changed': drift})
check('only_document_part_changed_at_authoring', read(QA / 'applied.json')['changed_package_parts'] == ['word/document.xml'])
check('same_package_part_inventory', set(src) == set(out))
check('same_18_tables_and_paragraph_structure', len(st) == len(ot) == 18 and len(sp) == len(op))
allowed_p = {c['index']: c for c in changes if c['kind'] == 'paragraph'}
actual_p = []
unexpected_p = []
for index, (before, after) in enumerate(zip(sp, op)):
    style_before = before.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS)
    if any(style.lower().startswith('toc') for style in style_before):
        continue
    a, b = semantic(before), semantic(after)
    if a != b:
        actual_p.append(index)
        change = allowed_p.get(index)
        expected = a.replace(change['before'], change['after'], 1) if change else None
        if expected != b:
            unexpected_p.append({'index': index, 'before': a, 'after': b, 'expected': expected})
check('prose_diff_exact_whitelist', set(actual_p) == set(allowed_p) and not unexpected_p,
      {'actual_indices': actual_p, 'unexpected': unexpected_p})
check('all_body_paragraph_styles_preserved', all(a.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS) == b.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS) for a, b in zip(sp, op)))
cell_changes = {(c['table'], c['row'], c['col']): c for c in changes if c['kind'] in ('cell', 'linebreak')}
cell_diff, cell_errors = [], []
for table_index, (before, after) in enumerate(zip(st, ot)):
    rows_a, rows_b = before.findall(W + 'tr'), after.findall(W + 'tr')
    if len(rows_a) != len(rows_b):
        cell_errors.append({'table': table_index, 'reason': 'row_count'})
        continue
    for row_index, (ra, rb_) in enumerate(zip(rows_a, rows_b)):
        ca, cb = ra.findall(W + 'tc'), rb_.findall(W + 'tc')
        if len(ca) != len(cb):
            cell_errors.append({'table': table_index, 'reason': 'column_count'})
            continue
        for col_index, (aa, bb) in enumerate(zip(ca, cb)):
            a, b = semantic(aa), semantic(bb)
            key = (table_index, row_index, col_index)
            if a != b:
                cell_diff.append(key)
                change = cell_changes.get(key)
                if not change or a != change['before'] or b != change['after']:
                    cell_errors.append({'cell': key, 'before': a, 'after': b})
check('cell_diff_exact_whitelist', set(cell_diff) == set(cell_changes) and not cell_errors,
      {'changed_cells': cell_diff, 'unexpected': cell_errors})
check('time_unit_and_model_name_unchanged_except_break', all(c['after'].replace('\n', '') == c['before'] for c in changes if c['kind'] == 'linebreak'))
check('all_table_numeric_values_unchanged', all(re.findall(r'\d+(?:[.,/]\d+)*', semantic(a)) == re.findall(r'\d+(?:[.,/]\d+)*', semantic(b)) for a, b in zip(st, ot)))
check('all_table_geometry_and_format_preserved', all(canonical(a.find(W + 'tblPr')) == canonical(b.find(W + 'tblPr')) and canonical(a.find(W + 'tblGrid')) == canonical(b.find(W + 'tblGrid')) for a, b in zip(st, ot)))
media = [name for name in src if name.startswith('word/media/')]
check('all_image_parts_byte_identical', all(src[name] == out[name] for name in media), {'parts': media})
check('all_drawings_preserved', [canonical(x) for x in sd.xpath('//w:drawing', namespaces=NS)] == [canonical(x) for x in od.xpath('//w:drawing', namespaces=NS)])
check('seven_black_placeholders_preserved', len(od.xpath('//wp:docPr[starts-with(@name,"W01_")]', namespaces=NS)) == 7)
check('five_native_equations_identical', len(od.xpath('//m:oMath', namespaces=NS)) == 5 and [canonical(x) for x in sd.xpath('//m:oMath', namespaces=NS)] == [canonical(x) for x in od.xpath('//m:oMath', namespaces=NS)])
check('styles_numbering_theme_identical', all(src[name] == out[name] for name in ['word/styles.xml', 'word/numbering.xml', 'word/theme/theme1.xml']))
check('sections_geometry_preserved', [canonical(x) for x in sd.xpath('//w:sectPr', namespaces=NS)] == [canonical(x) for x in od.xpath('//w:sectPr', namespaces=NS)])
check('headers_footers_preserved', all(src[name] == out[name] for name in src if re.match(r'word/(header|footer)\d+\.xml$', name)))
check('relationships_including_21_hyperlinks_preserved', src['word/_rels/document.xml.rels'] == out['word/_rels/document.xml.rels'])
bookmark_names = lambda node: node.xpath('//w:bookmarkStart/@w:name', namespaces=NS)
stable_names = lambda node: [name for name in bookmark_names(node) if not re.fullmatch(r'_Toc\d+', name)]
check('stable_bookmarks_preserved', stable_names(sd) == stable_names(od))
generated = lambda node: [name for name in bookmark_names(node) if re.fullmatch(r'_Toc\d+', name)]
auto_before, auto_after = generated(sd), generated(od)
auto_map = dict(zip(auto_before, auto_after))
check('generated_TOC_bookmarks_rebuilt_one_to_one', len(auto_before) == len(auto_after) == 114 and len(set(auto_after)) == 114,
      {'count': len(auto_after), 'mapping': auto_map})
field_codes = lambda node: [' '.join(x.split()) for x in node.xpath('//w:instrText/text() | //w:fldSimple/@w:instr', namespaces=NS)]
mapped_codes = [re.sub(r'_Toc\d+', lambda m: auto_map.get(m.group(), m.group()), code) for code in field_codes(sd)]
check('all_field_instructions_preserved_with_exact_TOC_id_mapping', mapped_codes == field_codes(od))
targets = [m.group(1) for code in field_codes(od) for m in [re.search(r'\bPAGEREF\s+(_Toc\d+)\b', code)] if m]
check('all_generated_PAGEREF_targets_exist', len(targets) == 114 and set(targets) == set(auto_after))
positions = lambda node: [node.getroottree().getpath(x.getparent()) for x in node.xpath('//w:bookmarkStart', namespaces=NS) if re.fullmatch(r'_Toc\d+', x.get(W + 'name', ''))]
check('generated_TOC_bookmark_positions_preserved', positions(sd) == positions(od))
check('two_covers_preserved_text', [semantic(p) for p in sp[:25]] == [semantic(p) for p in op[:25]])
check('native_counts_unchanged', all(rb[key] == old_rb[key] for key in ('pages', 'tables', 'inline_shapes', 'equations', 'toc')), {key: rb[key] for key in ('pages', 'tables', 'inline_shapes', 'equations', 'toc')})
headings = [p for p in rb['paragraphs'] if p['style'] == 'Heading 21']
check('69_heading_numbers_preserved', [(p['text'], p['label']) for p in headings] == [(p['text'], p['label']) for p in old_rb['paragraphs'] if p['style'] == 'Heading 21'] and len(headings) == 69)
check('fields_have_no_error_results', not any(re.search(r'Error!|Lỗi!|Reference source not found|Bookmark not defined', f['result']) for f in rb['fields']))
caps = [p for p in rb['paragraphs'] if p['style'] in ('TableCaption', 'FigureCaption')]
old_caps = [p for p in old_rb['paragraphs'] if p['style'] in ('TableCaption', 'FigureCaption')]
new_caption = 'Bảng 5.3. Phạm vi kiểm thử và đối chiếu hồ sơ hệ thống'
check('all_23_caption_numbers_preserved_only_T53_title_changed', len(caps) == 23 and [p['text'] for p in caps] == [new_caption if p['text'].startswith('Bảng 5.3.') else p['text'] for p in old_caps])
check('new_T53_caption_in_automatic_list', any(p['style'].lower().startswith('toc') and p['text'].startswith(new_caption) for p in rb['paragraphs']))
chapters345 = '\n'.join(semantic(p) for p in op[411:585]) + '\n' + semantic(ot[17])
check('no_internal_QA_coordination_tokens_in_chapters345', not re.search(r'\b(?:I0[1-5]|Phase\s*4|VERIFIED|QA|gate|DATA_AUDIT)\b|snapshot QA|Codex', chapters345, re.I))
body = od.find(W + 'body')
ref_index = next(i for i, node in enumerate(body) if 'TÀI LIỆU THAM KHẢO' == ''.join(node.xpath('.//w:t/text()', namespaces=NS)))
check('no_bracket_citations_before_references', not re.search(r'\[\d+\]', '\n'.join(semantic(x) for x in list(body)[:ref_index])))
reference_texts = [p['text'] for p in rb['paragraphs'] if re.match(r'^\[\d+\]', p['text'])]
check('21_reference_entries_unchanged', reference_texts == [p['text'] for p in old_rb['paragraphs'] if re.match(r'^\[\d+\]', p['text'])] and len(reference_texts) == 21)
check('119_functional_and_7_document_checks_kept_distinct', '119/119' in semantic(op[574]) and '7/7' in semantic(op[574]) and '126/126' in semantic(op[574]) and 'Nhóm kiểm hồ sơ không được tính là kiểm thử chức năng.' in semantic(op[574]))
check('model_metrics_feature_tables_preserved', all(semantic(st[i]) == semantic(ot[i]) for i in (11, 12, 13, 14)))
frozen = read(ROOT / '.agent/qa/phase4-app-20261009/preflight.json')['files']
changed, missing, unreadable = [], [], []
matching = 0
for path, expected in frozen.items():
    local = Path(re.sub(r'^/mnt/([a-z])/', lambda m: m.group(1).upper() + ':/', path))
    if local == ROOT / 'dashboard/app.py':
        expected = guards[str(local)]
    try:
        if not local.is_file():
            missing.append(path)
        elif sha(local) != expected:
            changed.append(path)
        else:
            matching += 1
    except OSError:
        result = subprocess.run(['wsl.exe', '-d', 'Ubuntu-24.04', '--', 'sha256sum', '--', path], capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.split()[0] == expected:
            matching += 1
        else:
            unreadable.append(path)
preservation = {'total': len(frozen), 'matching': matching, 'changed': changed, 'missing': missing, 'unreadable': unreadable}
preservation['status'] = 'FAIL' if changed or missing else 'INCOMPLETE' if unreadable else 'PASS'
preservation['limits'] = 'Three pre-existing DrvFS venv runtime reparse links are unreadable through Windows and WSL (No such device); no environment repair attempted. Do not claim 1571/1571 in this run.'
save('preservation.json', preservation)
checks.append({'id': '1571_locked_artifact_snapshot', 'status': preservation['status'], 'evidence': preservation})
expected_links = {str(ROOT.as_posix()).replace('D:/', '/mnt/d/') + '/.agent/qa/phase1-smoke-20261009/venv-probe/bin/' + name for name in ('python', 'python3', 'python3.12')}
check('all_accessible_locked_artifacts_unchanged', matching == 1568 and set(unreadable) == expected_links and not changed and not missing,
      {'matching': matching, 'unreadable_runtime_links': unreadable})
font_source = ast.parse((ROOT / '.agent/scripts/audit_word_w01_fonts.py').read_text(encoding='utf-8'))
audit_def = next(x for x in font_source.body if isinstance(x, ast.FunctionDef) and x.name == 'audit')
font_namespace = {'ZipFile': ZipFile, 'E': E, 'Counter': Counter, 'ns': {'w': NS['w']}, 'W': W}
exec(compile(ast.Module(body=[audit_def], type_ignores=[]), 'font-audit', 'exec'), font_namespace)
font_result = {'template': font_namespace['audit'](ROOT.parent / 'Mauwword/Mau bao cao_Do an_Khoa luan_2025.docx'),
               'output': font_namespace['audit'](OUTPUT), 'source': font_namespace['audit'](SOURCE)}
save('font-audit.json', font_result)
check('font_roles_match_W01_and_school_template', not font_result['output']['font_exceptions'] and font_result['output']['styles'] == font_result['source']['styles'] and font_result['output']['default_rPr'] == font_result['source']['default_rPr'])
out_dir = QA / 'render'
out_dir.mkdir(exist_ok=True)
pdf = pdfium.PdfDocument(QA / 'W01-native.pdf')
pages = []
for index, page in enumerate(pdf):
    path = out_dir / f'page-{index + 1:03}.png'
    image = page.render(scale=2).to_pil().convert('RGB')
    image.save(path)
    old_image = Image.open(OLD_QA / 'render' / path.name).convert('RGB')
    difference = ImageChops.difference(image, old_image)
    box = difference.getbbox()
    pages.append({'page': index + 1, 'pixel_identical_to_W01': box is None,
                  'changed_bbox': box, 'image': str(path), 'text_chars': len(page.get_textpage().get_text_range().strip())})
    page.close()
save('page-diff.json', {'page_count': len(pages), 'changed_pages': [p['page'] for p in pages if not p['pixel_identical_to_W01']],
                        'identical_pages': [p['page'] for p in pages if p['pixel_identical_to_W01']], 'pages': pages})
check('67_pages_rendered_no_empty_page', len(pages) == 67 and all(p['text_chars'] > 20 for p in pages))
result = {'status': 'FAIL' if any(c['status'] == 'FAIL' for c in checks) else 'INCOMPLETE' if any(c['status'] == 'INCOMPLETE' for c in checks) else 'PASS', 'artifact_status': 'APPLIED_UNVERIFIED_UNTIL_VISUAL_REVIEW',
          'output': str(OUTPUT), 'sha256': sha(OUTPUT), 'source_sha256': sha(SOURCE),
          'checks': checks, 'passed': sum(c['status'] == 'PASS' for c in checks), 'total': len(checks),
          'changed_pages': [p['page'] for p in pages if not p['pixel_identical_to_W01']]}
save('verification.json', result)
print(json.dumps({key: result[key] for key in ('status', 'passed', 'total', 'changed_pages')}, ensure_ascii=False))
print(json.dumps([c for c in checks if c['status'] != 'PASS'], ensure_ascii=False, indent=2))
