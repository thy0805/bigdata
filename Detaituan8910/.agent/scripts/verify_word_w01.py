import hashlib
import io
import json
import re
import subprocess
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E
from PIL import Image

from word_w01_content import CH1_REPLACEMENTS, TABLES, FIGURES, CH2_REPLACE, CH2_14

root = Path(__file__).resolve().parents[2]
qa = root / '.agent/qa/word-w01-20261010'
output = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
source = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx'
n = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math', 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W = '{' + n['w'] + '}'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def package(path):
    with ZipFile(path) as z:
        parts = {key: z.read(key) for key in z.namelist()}
    return parts, E.fromstring(parts['word/document.xml'])


def txt(node):
    return ''.join(node.xpath('.//w:t/text() | .//m:t/text()', namespaces=n))


def style(node):
    values = node.xpath('./w:pPr/w:pStyle/@w:val', namespaces=n)
    return values[0] if values else ''


checks = []


def check(name, passed, evidence=None):
    checks.append({'id': name, 'status': 'PASS' if passed else 'FAIL', 'evidence': evidence})


oldparts, olddoc = package(source)
parts, doc = package(output)
oldbody = list(olddoc.find(W + 'body'))
body = list(doc.find(W + 'body'))
tables = doc.xpath('/w:document/w:body/w:tbl', namespaces=n)
oldtables = olddoc.xpath('/w:document/w:body/w:tbl', namespaces=n)
rb = read(qa / 'word-readback.json')
render = read(qa / 'render-pages.json')
guards = read(qa / 'preflight.json')['guards']
drift = [path for path, expected in guards.items() if sha(path) != expected]
check('source_guards', not drift, {'count': len(guards), 'changed': drift})
check('native_counts', rb['tables'] == 18 and rb['inline_shapes'] == 10 and rb['equations'] == 5 and rb['toc'] == 3, {k: rb[k] for k in ['pages', 'tables', 'inline_shapes', 'equations', 'toc']})
first_old = next(i for i, x in enumerate(oldbody) if x.tag == W + 'tbl')
first_new = next(i for i, x in enumerate(body) if x.tag == W + 'tbl')
check('two_cover_text_unchanged', [txt(x) for x in oldbody[:first_old]] == [txt(x) for x in body[:first_new]])
for index in [0, 1, 3, 4, 5, 6]:
    check(f'old_table_{index+1}_cell_text', oldtables[index].xpath('.//w:tc//w:t/text()', namespaces=n) == tables[index].xpath('.//w:tc//w:t/text()', namespaces=n))
old_terms = [[txt(c) for c in row.findall(W + 'tc')] for row in oldtables[2].findall(W + 'tr')]
new_terms = [[txt(c) for c in row.findall(W + 'tc')] for row in tables[2].findall(W + 'tr')]
check('old_terms_preserved_four_new', new_terms[:len(old_terms)] == old_terms and [r[0] for r in new_terms[len(old_terms):]] == ['HGB', 'Train', 'Validation', 'Test'])
oldmedia = [value for key, value in oldparts.items() if key.startswith('word/media/')]
newmedia = [value for key, value in parts.items() if key.startswith('word/media/')]
check('original_media_bytes', all(value in newmedia for value in oldmedia), {'original': len(oldmedia), 'current': len(newmedia)})
rels = E.fromstring(parts['word/_rels/document.xml.rels'])
relmap = {r.get('Id'):r.get('Target') for r in rels}
drawings = doc.xpath('.//w:drawing', namespaces=n)
placeholder_drawings = [d for d in drawings if any('W01_IMG' in x.get('name','') for x in d.xpath('.//*[local-name()="docPr"]'))]
blacks = [parts['word/'+relmap[d.xpath('.//a:blip/@r:embed',namespaces=n)[0]]] for d in placeholder_drawings]
check('seven_pure_black_placeholders', len(blacks) == 7 and all(Image.open(io.BytesIO(value)).convert('RGB').getextrema() == ((0, 0), (0, 0), (0, 0)) for value in blacks), {'inline_placeholders':len(blacks), 'note':'Word deduplicates and renames identical image parts'})


def math_signature(node):
    attrs = {key: val for key, val in node.attrib.items() if not E.QName(key).localname.startswith('rsid')}
    return (node.tag, attrs, node.text or '', [math_signature(x) for x in node if E.QName(x).localname != 'proofErr'])


oldmath = olddoc.xpath('.//m:oMath', namespaces=n)
newmath = doc.xpath('.//m:oMath', namespaces=n)
check('original_three_math_structures', [math_signature(x) for x in oldmath] == [math_signature(x) for x in newmath[:3]])
check('native_mae_delimiters', len(doc.xpath('.//m:dPr/m:begChr[@m:val="|"]', namespaces=n)) == 2 and len(doc.xpath('.//m:dPr/m:endChr[@m:val="|"]', namespaces=n)) == 2)
old_ch_start = next(i for i,x in enumerate(oldbody) if style(x) == 'ChapterTitle')
old_ch_end = next(i for i,x in enumerate(oldbody[old_ch_start+1:], old_ch_start+1) if style(x) == 'ChapterTitle')
new_ch_start = next(i for i,x in enumerate(body) if style(x) == 'Heading1')
new_ch_end = next(i for i,x in enumerate(body[new_ch_start+1:], new_ch_start+1) if style(x) == 'Heading1')
expected_ch1 = [CH1_REPLACEMENTS.get(i+1, txt(x)) for i,x in enumerate(oldbody) if old_ch_start <= i < old_ch_end and x.tag == W+'p']
actual_ch1 = [txt(x) for x in body[new_ch_start:new_ch_end] if x.tag == W+'p']
check('ch1_only_four_prose_replacements', expected_ch1 == actual_ch1, {'source_paragraphs': len(expected_ch1), 'output_paragraphs': len(actual_ch1), 'replaced_source_blocks': list(CH1_REPLACEMENTS)})
headings = [p for p in rb['paragraphs'] if p['style'] == 'Heading 1']
check('five_native_chapter_numbers', [p['label'] for p in headings] == [f'CHƯƠNG {i}.' for i in range(1,6)])
sections = [p for p in rb['paragraphs'] if p['style'] == 'Heading 21']
check('sixty_nine_native_section_numbers', [p['label'] for p in sections] == [f'{ch}.{i}.' for ch,count in [(1,11),(2,14),(3,13),(4,14),(5,17)] for i in range(1,count+1)])
check('opening_and_conclusion_subheadings', len([p for p in rb['paragraphs'] if p['style']=='IntroSectionTitle']) == 5 and len([p for p in rb['paragraphs'] if p['style']=='ConclusionSectionTitle']) == 3)
for key, value in TABLES.items():
    index = 7 + list(TABLES).index(key)
    rows = [[txt(cell) for cell in row.findall(W+'tc')] for row in tables[index].findall(W+'tr')]
    check('table_' + key + '_exact_values', rows == [value[3]] + value[5])
    check('table_' + key + '_caption_above', style(tables[index].getprevious()) == 'TableCaption')
    check('table_' + key + '_header_and_auto_height', bool(tables[index].xpath('./w:tr[1]/w:trPr/w:tblHeader', namespaces=n)) and not tables[index].xpath('./w:tr/w:trPr/w:trHeight[@w:hRule="exact"]', namespaces=n))
tablecaps = [p for p in rb['paragraphs'] if p['style'] == 'TableCaption']
figcaps = [p for p in rb['paragraphs'] if p['style'] == 'FigureCaption']
expected_tables = [f'Bảng {ch}.{i}.' for ch,count in [(1,4),(3,4),(4,4),(5,3)] for i in range(1,count+1)]
expected_figures = ['Hình 1.1.'] + [f'Hình {value[0]}.{value[1]}.' for value in FIGURES.values()]
check('native_caption_restart_per_chapter', [re.match(r'Bảng \d+\.\d+\.',p['text']).group() for p in tablecaps] == expected_tables and [re.match(r'Hình \d+\.\d+\.',p['text']).group() for p in figcaps] == expected_figures)
bookmark_names = set(doc.xpath('.//w:bookmarkStart/@w:name', namespaces=n))
codes = doc.xpath('.//w:instrText/text() | .//w:fldSimple/@w:instr', namespaces=n)
refnames = [re.search(r'REF\s+(\S+)', c).group(1) for c in codes if c.strip().startswith('REF ')]
check('references_resolve_bookmarks', all(name in bookmark_names for name in refnames), {'refs': len(refnames), 'missing': sorted(set(refnames)-bookmark_names)})
check('all_new_tables_figures_cited', all('W01_'+key in refnames for key in list(TABLES)+list(FIGURES)))
check('no_field_error', not any('Error!' in f['result'] or 'Lỗi!' in f['result'] for f in rb['fields']))
check('toc_and_two_lists_native', len([c for c in codes if c.strip().startswith('TOC ')]) == 3)
toc_results = [f['result'] for f in rb['fields'] if f['code'].strip().startswith('TOC ')]
check('toc_contains_all_sections', all(p['text'].casefold() in toc_results[0].casefold() for p in sections) and all(p['text'].casefold() in toc_results[1].casefold() for p in figcaps) and all(p['text'].casefold() in toc_results[2].casefold() for p in tablecaps))
refstart = next(i for i,x in enumerate(body) if txt(x)=='TÀI LIỆU THAM KHẢO' and style(x)=='Heading11')
check('no_bracket_citations_in_body', not re.search(r'\[\d+\]', '\n'.join(txt(x) for x in body[:refstart])))
endrefs = [txt(x) for x in body[refstart:] if re.match(r'^\[\d+\]',txt(x))]
check('twenty_one_ordered_references', [int(re.match(r'^\[(\d+)\]',x).group(1)) for x in endrefs] == list(range(1,22)))
relations = E.fromstring(parts['word/_rels/document.xml.rels'])
external = [x for x in relations if x.get('Type','').endswith('/hyperlink') and x.get('TargetMode')=='External']
check('twenty_one_live_hyperlink_relationships', len(external)==21)
check('fonts_match_school_template', not read(qa/'font-audit.json')['output']['font_exceptions'])
check('render_all_pages_exist', render['page_count']==rb['pages'] and all(Path(p['image']).is_file() for p in render['pages']))
check('no_unintended_empty_pages', all(len(re.sub(r'\s','',p['text']))>20 for p in render['pages']))
ack = [p for p in rb['paragraphs'] if p['text'].startswith(('Nhóm xin gửi lời cảm ơn','Báo cáo có thể còn','Nhóm xin chân thành cảm ơn'))]
check('acknowledgment_eight_nine_lines', sum(p['lines'] for p in ack) in [8,9], {'actual_word_lines':sum(p['lines'] for p in ack)})
heading57 = next(p for p in sections if p['label']=='5.7.')
check('section_57_actual_batch_title', heading57['text']=='XỬ LÝ DẤU THỜI GIAN TRONG FLINK SQL BATCH' or heading57['text']=='Xử lý dấu thời gian trong Flink SQL BATCH')
schema = read(root/'data/ml/runs/20261009-phase2a-a/feature-schema.json')
check('feature_table_locked_order', [r[0] for r in TABLES['T41'][5]] == schema['feature_columns'])
metric = read(root/'models/runs/20261009-phase2b2-a/metrics-test.json')
check('test_metrics_read_saved_not_recomputed', metric['n']==4590 and metric['models']['hgb']['mae_kwh']==0.3220542588291146 and metric['models']['hgb']['rmse_kwh']==0.4634874854716987 and TABLES['T44'][5][-1][1:]==['0,3221','0,4635'])
sql = (root/'.agent/qa/phase1-full-20261009/runs/20261009T102201900234-full/job.sql').read_text(encoding='utf-8')
check('source_sql_is_batch_floor_groupby', "'execution.runtime-mode' = 'BATCH'" in sql and 'GROUP BY FLOOR(event_time TO HOUR)' in sql and 'WATERMARK' not in sql)
frozen = read(root/'.agent/qa/phase4-app-20261009/preflight.json')['files']
changed, missing, unreadable, linux = [], [], [], []
count = 0
for p, expected in frozen.items():
    local = Path(re.sub(r'^/mnt/([a-z])/', lambda m:m.group(1).upper()+':/',p))
    if local == root/'dashboard/app.py':
        expected = guards[str(local)]
    try:
        if not local.is_file():
            missing.append(p)
        elif sha(local)!=expected:
            changed.append(p)
        else:
            count+=1
    except OSError:
        proc=subprocess.run(['wsl.exe','-d','Ubuntu-24.04','--','sha256sum','--',p],capture_output=True,text=True,timeout=30)
        if proc.returncode==0 and proc.stdout.split()[0]==expected:
            count+=1
            linux.append(p)
        else:
            unreadable.append(p)
preservation={'total':len(frozen),'matching':count,'changed':changed,'missing':missing,'unreadable':unreadable,'linux_hash_readback':linux,'app_expected':'accepted data-guide UI snapshot'}
check('all_prior_products_preserved', count==len(frozen) and not changed and not missing and not unreadable,preservation)
(qa/'preservation.json').write_text(json.dumps(preservation,ensure_ascii=False,indent=2),encoding='utf-8')
result={'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','artifact_status':'APPLIED_UNVERIFIED_UNTIL_VISUAL_AND_FIELD_PROBE','output':str(output),'sha256':sha(output),'pages':rb['pages'],'checks':checks,'passed':sum(c['status']=='PASS' for c in checks),'total':len(checks),'limits':['No training, model inference, Test re-evaluation or Flink rerun','W02 placeholders remain','Native Word/PDFium render; bundled LibreOffice unavailable']}
(qa/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'passed':result['passed'],'total':result['total'],'failed':[c for c in checks if c['status']=='FAIL']},ensure_ascii=False,indent=2))
