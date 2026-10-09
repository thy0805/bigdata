import hashlib
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E

root = Path(r'D:\Hoctap\bigdata')
project = root / 'Detaituan8910'
qa = project / '.agent/qa/diennang-khung-20261006'
source = root / 'ApacheFlink.docx'
output = qa / (sys.argv[1] if len(sys.argv) > 1 else 'candidate.docx')
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
w = '{' + ns['w'] + '}'
r = '{' + ns['r'] + '}'
expected_hash = 'efac5eade11afeff8b17f458b183edcb5f1ca600ebdfbb86e167d895d08662d3'


def text(e):
    return ''.join(e.xpath('.//w:t/text()', namespaces=ns))


def add(parent, tag, **attrs):
    e = E.SubElement(parent, w + tag)
    for k, v in attrs.items():
        e.set(w + k, str(v))
    return e


def prop(parent, tag, **attrs):
    old = parent.find(w + tag)
    if old is not None:
        parent.remove(old)
    return add(parent, tag, **attrs)


def ppr(p):
    e = p.find(w + 'pPr')
    if e is None:
        e = E.Element(w + 'pPr')
        p.insert(0, e)
    return e


def set_text(p, value):
    props = deepcopy(p.find('w:r/w:rPr', ns))
    for e in list(p):
        if e.tag != w + 'pPr':
            p.remove(e)
    for i, line in enumerate(value.split('\n')):
        run = add(p, 'r')
        if props is not None:
            run.append(deepcopy(props))
        if i:
            add(run, 'br')
        t = add(run, 't')
        t.text = line
    return p


def para(value='', style='ReportBody', page_break=None):
    p = E.Element(w + 'p')
    pr = add(p, 'pPr')
    add(pr, 'pStyle', val=style)
    if style in ['ChapterTitle', 'Heading21', 'Heading31']:
        np = add(pr, 'numPr')
        add(np, 'ilvl', val={'ChapterTitle': 0, 'Heading21': 1, 'Heading31': 2}[style])
        add(np, 'numId', val=chapter_num)
    if page_break is not None:
        add(pr, 'pageBreakBefore', val=int(page_break))
    if style == 'ReportBody':
        add(pr, 'keepNext', val=0)
    if value:
        add(add(p, 'r'), 't').text = value
    return p


def field(code):
    p = para()
    prop(ppr(p), 'ind', firstLine=0)
    add(add(p, 'r'), 'fldChar', fldCharType='begin', dirty='true')
    e = add(add(p, 'r'), 'instrText')
    e.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    e.text = ' ' + code + ' '
    add(add(p, 'r'), 'fldChar', fldCharType='separate')
    add(add(p, 'r'), 't').text = ''
    add(add(p, 'r'), 'fldChar', fldCharType='end')
    return p


def xmlbytes(e):
    return E.tostring(e, encoding='UTF-8', xml_declaration=True, standalone=True)


assert hashlib.sha256(source.read_bytes()).hexdigest() == expected_hash
with ZipFile(source) as z:
    parts = {n: z.read(n) for n in z.namelist()}
doc = E.fromstring(parts['word/document.xml'])
styles = E.fromstring(parts['word/styles.xml'])
numbering = E.fromstring(parts['word/numbering.xml'])
settings = E.fromstring(parts['word/settings.xml'])
rels = E.fromstring(parts['word/_rels/document.xml.rels'])
content_types = E.fromstring(parts['[Content_Types].xml'])
body = doc.find(w + 'body')
original = list(body)
source_sections = doc.xpath('//w:sectPr', namespaces=ns)
style_map = {e.get(w + 'styleId'): e for e in styles.findall(w + 'style')}

outline = []
for block in re.split(r'(?m)^### ', (project / 'context.md').read_text(encoding='utf-8'))[1:]:
    lines = block.strip().splitlines()
    heading = lines[0].strip()
    if not (heading.startswith('CHƯƠNG ') or heading in ['MỞ ĐẦU', 'KẾT LUẬN', 'TÀI LIỆU THAM KHẢO']):
        continue
    items = [re.sub(r'^\d+(?:\.\d+)*\.\s+', '', s) for s in lines[1:] if re.match(r'^\d+(?:\.\d+)*\.\s+', s)]
    items = ['Kiểm tra chất lượng dữ liệu' if s == 'Kiểm tra dữ liệu thiếu, trùng lặp và không hợp lệ' else 'Tích hợp mô hình dự đoán' if s == 'Tích hợp mô hình đã huấn luyện để thực hiện dự đoán' else s for s in items]
    outline.append({'heading': heading, 'items': items})
assert [len(x['items']) for x in outline] == [5, 11, 14, 13, 14, 17, 3, 0]
(qa / 'outline.json').write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding='utf-8')

for role in ['Heading11', 'Heading21', 'Heading31', 'FrontTitle', 'FrontTitleNoTOC', 'ReportBody', 'ReportSubhead', 'TOC1', 'TOC2', 'TOC3', 'FigureCaption', 'TableCaption']:
    if role not in style_map:
        continue
    sr = style_map[role].find(w + 'rPr')
    if sr is None:
        sr = add(style_map[role], 'rPr')
    f = prop(sr, 'rFonts', ascii='Times New Roman', hAnsi='Times New Roman', eastAsia='Times New Roman', cs='Times New Roman')
    prop(sr, 'color', val='000000')


def new_style(style_id, name, base, level=None, num=None, ilvl=None):
    e = E.Element(w + 'style', {w + 'type': 'paragraph', w + 'customStyle': '1', w + 'styleId': style_id})
    add(e, 'name', val=name)
    add(e, 'basedOn', val=base)
    add(e, 'next', val='ReportBody')
    add(e, 'qFormat')
    pr = add(e, 'pPr')
    if level is not None:
        add(pr, 'outlineLvl', val=level)
    if num is not None:
        np = add(pr, 'numPr')
        add(np, 'ilvl', val=ilvl)
        add(np, 'numId', val=num)
    styles.append(e)
    style_map[style_id] = e
    return e


abstract_start = max(int(e.get(w + 'abstractNumId')) for e in numbering.findall(w + 'abstractNum')) + 1
num_start = max(int(e.get(w + 'numId')) for e in numbering.findall(w + 'num')) + 1
chapter_num, intro_num, conclusion_num = num_start, num_start + 1, num_start + 2


def list_def(aid, nid, levels):
    a = E.Element(w + 'abstractNum', {w + 'abstractNumId': str(aid)})
    add(a, 'multiLevelType', val='multilevel' if len(levels) > 1 else 'singleLevel')
    for i, (label, sid) in enumerate(levels):
        lvl = add(a, 'lvl', ilvl=i)
        add(lvl, 'start', val=1)
        add(lvl, 'numFmt', val='decimal')
        if sid:
            add(lvl, 'pStyle', val=sid)
        add(lvl, 'suff', val='space')
        add(lvl, 'lvlText', val=label)
        add(lvl, 'lvlJc', val='left')
        pp = add(lvl, 'pPr')
        add(pp, 'ind', left=0, hanging=0)
        rr = add(lvl, 'rPr')
        add(rr, 'rFonts', ascii='Times New Roman', hAnsi='Times New Roman', eastAsia='Times New Roman', cs='Times New Roman')
    numbering.insert(len(numbering.findall(w + 'abstractNum')), a)
    num = add(numbering, 'num', numId=nid)
    add(num, 'abstractNumId', val=aid)


list_def(abstract_start, chapter_num, [('CHƯƠNG %1.', 'ChapterTitle'), ('%1.%2.', 'Heading21'), ('%1.%2.%3.', 'Heading31')] + [('.'.join(f'%{j}' for j in range(1, i + 2)) + '.', '') for i in range(3, 9)])
list_def(abstract_start + 1, intro_num, [('%1.', 'IntroSectionTitle')])
list_def(abstract_start + 2, conclusion_num, [('%1.', 'ConclusionSectionTitle')])
new_style('ChapterTitle', 'ChapterTitle', 'Heading11', 0, chapter_num, 0)
new_style('IntroSectionTitle', 'IntroSectionTitle', 'Heading21', 1, intro_num, 0)
new_style('ConclusionSectionTitle', 'ConclusionSectionTitle', 'Heading21', 1, conclusion_num, 0)
for sid, ilvl in [('Heading21', 1), ('Heading31', 2)]:
    sp = style_map[sid].find(w + 'pPr')
    np = prop(sp, 'numPr')
    add(np, 'ilvl', val=ilvl)
    add(np, 'numId', val=chapter_num)
    prop(style_map[sid], 'next', val='ReportBody')
if 'Title' not in style_map:
    new_style('Title', 'Title', 'Normal')
title_style = style_map['Title']
tsr = title_style.find(w + 'rPr')
if tsr is None:
    tsr = add(title_style, 'rPr')
prop(tsr, 'rFonts', ascii='Times New Roman', hAnsi='Times New Roman', eastAsia='Times New Roman', cs='Times New Roman')
prop(tsr, 'sz', val=40)
prop(tsr, 'b')
prop(tsr, 'color', val='000000')

for e in list(body):
    body.remove(e)
cover = [deepcopy(original[i]) for i in [0, 1, 2, 3, 4, 7, 10, 12, 15, 16, 17, 18, 23]]
for p in cover:
    for br in p.xpath('.//w:br[@w:type="page"] | .//w:lastRenderedPageBreak | .//w:bookmarkStart | .//w:bookmarkEnd', namespaces=ns):
        br.getparent().remove(br)
    prop(ppr(p), 'keepNext', val=1)
    prop(ppr(p), 'pageBreakBefore', val=0)
    prop(ppr(p), 'spacing', before=0, after=120, line=312, lineRule='auto')
prop(ppr(cover[4]), 'spacing', before=0, after=480, line=312, lineRule='auto')
prop(ppr(cover[5]), 'spacing', before=0, after=240, line=312, lineRule='auto')
title = 'PHÂN TÍCH DỮ LIỆU TIÊU THỤ ĐIỆN NĂNG\nVÀ DỰ ĐOÁN NHU CẦU SỬ DỤNG ĐIỆN THEO THỜI GIAN'
set_text(cover[6], title)
prop(ppr(cover[6]), 'pStyle', val='Title')
prop(ppr(cover[6]), 'spacing', before=0, after=240, line=312, lineRule='auto')
set_text(cover[9], '1. [MSSV] - Nguyễn Đức Thành Phát')
set_text(cover[10], '2. 2001230227 - Lý Vũ Nhân Hậu')
set_text(cover[11], '3. 2001230418 - Nguyễn Tuấn Khôi')
for p in cover[9:12]:
    prop(ppr(p), 'spacing', before=0, after=0, line=312, lineRule='auto')
    prop(ppr(p), 'ind', left=900)
prop(ppr(cover[11]), 'spacing', before=0, after=720, line=312, lineRule='auto')
prop(ppr(cover[-1]), 'keepNext', val=0)
lecturer = deepcopy(cover[7])
set_text(lecturer, 'Giảng viên: Nguyễn Thành Ngô')
for rr in lecturer.findall('w:r/w:rPr', ns):
    prop(rr, 'sz', val=28)
    prop(rr, 'szCs', val=28)
cover.insert(8, lecturer)
for p in cover:
    body.append(p)

rid_max = max(int(e.get('Id')[3:]) for e in rels if e.get('Id', '').startswith('rId'))
empty_footer_id = f'rId{rid_max + 1}'
rel_ns = '{http://schemas.openxmlformats.org/package/2006/relationships}'
E.SubElement(rels, rel_ns + 'Relationship', Id=empty_footer_id, Type=ns['r'] + '/footer', Target='footer3.xml')
footer = E.Element(w + 'ftr', nsmap={'w': ns['w']})
footer.append(E.Element(w + 'p'))
parts['word/footer3.xml'] = xmlbytes(footer)
ct_ns = '{http://schemas.openxmlformats.org/package/2006/content-types}'
E.SubElement(content_types, ct_ns + 'Override', PartName='/word/footer3.xml', ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml')


def section_boundary(section):
    p = E.Element(w + 'p')
    pr = add(p, 'pPr')
    add(pr, 'spacing', before=0, after=0, line=20, lineRule='exact')
    add(add(pr, 'rPr'), 'sz', val=2)
    pr.append(section)
    body.append(p)


cover_sec = deepcopy(source_sections[0])
for ref in cover_sec.findall(w + 'footerReference'):
    ref.set(r + 'id', empty_footer_id)
prop(cover_sec, 'type', val='nextPage')
prop(cover_sec, 'pgNumType', fmt='decimal', start=1)
section_boundary(cover_sec)
front_sec = deepcopy(source_sections[0])
for e in front_sec.findall(w + 'pgBorders'):
    front_sec.remove(e)
prop(front_sec, 'type', val='nextPage')

body.append(para('BẢNG PHÂN CÔNG CÔNG VIỆC', 'FrontTitle', False))
assignment = deepcopy(original[49])
for i, row in enumerate(assignment.findall(w + 'tr')[1:]):
    cells = row.findall(w + 'tc')
    values = [str(i + 1), '' if i == 0 else ['2001230227', '2001230418'][i - 1], ['Nguyễn Đức Thành Phát', 'Lý Vũ Nhân Hậu', 'Nguyễn Tuấn Khôi'][i], '']
    for cell, value in zip(cells, values):
        p = cell.find(w + 'p')
        set_text(p, value)
        for extra in cell.findall(w + 'p')[1:]:
            cell.remove(extra)
        prop(ppr(p), 'keepNext', val=1 if i < 2 else 0)
body.append(assignment)
body.append(para())
body.append(para('LỜI CẢM ƠN', 'FrontTitle'))
body.append(para())
body.append(para('MỤC LỤC', 'FrontTitleNoTOC'))
toc_mapping = 'FrontTitle,1,Heading 11,1,ChapterTitle,1,Heading 21,2,IntroSectionTitle,2,ConclusionSectionTitle,2,Heading 31,3'
body.append(field(f'TOC \\h \\z \\t "{toc_mapping}"'))
body.append(para('DANH MỤC CÁC KÝ HIỆU, CHỮ VIẾT TẮT VÀ THUẬT NGỮ', 'FrontTitle'))
glossary = deepcopy(doc.xpath('//w:tbl', namespaces=ns)[0]) if False else deepcopy(next(t for t in original if t.tag == w + 'tbl' and 'Ký hiệu / thuật ngữ' in text(t)))
rows = glossary.findall(w + 'tr')
blank_row = deepcopy(rows[1])
for row in rows[1:]:
    glossary.remove(row)
for cell in blank_row.findall(w + 'tc'):
    p = cell.find(w + 'p')
    set_text(p, '')
    prop(ppr(p), 'keepNext', val=0)
    for extra in cell.findall(w + 'p')[1:]:
        cell.remove(extra)
glossary.append(blank_row)
body.append(glossary)
body.append(para())
for title_text, caption_style in [('DANH MỤC HÌNH', 'FigureCaption'), ('DANH MỤC BẢNG', 'TableCaption')]:
    body.append(para(title_text, 'FrontTitle'))
    body.append(field(f'TOC \\h \\z \\t "{caption_style},1"'))
    body.append(para())
section_boundary(front_sec)

for i, block in enumerate(outline):
    heading = block['heading']
    is_chapter = heading.startswith('CHƯƠNG ')
    heading_style = 'ChapterTitle' if is_chapter else 'Heading11'
    value = re.sub(r'^CHƯƠNG \d+\.\s+', '', heading) if is_chapter else heading
    body.append(para(value, heading_style, False if i == 0 else None))
    if not block['items']:
        body.append(para())
    for item in block['items']:
        item_style = 'IntroSectionTitle' if heading == 'MỞ ĐẦU' else 'ConclusionSectionTitle' if heading == 'KẾT LUẬN' else 'Heading21'
        body.append(para(item, item_style))
        body.append(para())
end_sec = deepcopy(source_sections[1])
prop(end_sec, 'type', val='nextPage')
body.append(end_sec)
prop(settings, 'updateFields', val='true')
parts['word/document.xml'] = xmlbytes(doc)
parts['word/styles.xml'] = xmlbytes(styles)
parts['word/numbering.xml'] = xmlbytes(numbering)
parts['word/settings.xml'] = xmlbytes(settings)
parts['word/_rels/document.xml.rels'] = xmlbytes(rels)
parts['[Content_Types].xml'] = xmlbytes(content_types)
core = E.fromstring(parts['docProps/core.xml'])
for e in core:
    if E.QName(e).localname in ['creator', 'lastModifiedBy', 'title', 'subject', 'description', 'keywords']:
        e.text = ''
parts['docProps/core.xml'] = xmlbytes(core)
with ZipFile(output, 'x') as z:
    for name, data in parts.items():
        z.writestr(name, data)
manifest = {'source': str(source), 'source_sha256': expected_hash, 'candidate': str(output), 'h2_count': 77, 'main_parts': 8, 'num_ids': {'chapter': chapter_num, 'introduction': intro_num, 'conclusion': conclusion_num}, 'deliberately_empty': ['all prose', 'assignment tasks', 'glossary entries', 'figures list', 'tables list', 'references']}
(qa / 'build-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False))
