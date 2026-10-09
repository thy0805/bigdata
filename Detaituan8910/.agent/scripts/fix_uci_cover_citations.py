from copy import copy, deepcopy
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import hashlib
import json
import re

ROOT = Path(r'D:\Hoctap\bigdata\Detaituan8910')
SOURCE = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v2_20261008.docx'
TARGET = ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx'
TEMPLATE = ROOT.parent / 'Mauwword/Mau bao cao_Do an_Khoa luan_2025.docx'
QA = ROOT / '.agent/qa/word-uci-cover-citations-20261008'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + NS['w'] + '}'
MARKER = re.compile(r'[ \t]*\[\d+(?:\s*[-–,;]\s*\d+)*\](?:[ \t]*[,;][ \t]*(?=\[))?')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def text(e):
    return ''.join(e.xpath('.//w:t/text()', namespaces=NS))

def put(parent, name, attrs):
    node = parent.find(W + name)
    if node is None:
        node = etree.SubElement(parent, W + name)
    for key, value in attrs.items():
        node.set(W + key, str(value))
    return node

def font(props, size, bold):
    put(props, 'rFonts', {'ascii': 'Times New Roman', 'hAnsi': 'Times New Roman', 'eastAsia': 'Times New Roman', 'cs': 'Times New Roman'})
    put(props, 'sz', {'val': 2 * size})
    put(props, 'szCs', {'val': 2 * size})
    put(props, 'b', {'val': '1' if bold else '0'})
    put(props, 'bCs', {'val': '1' if bold else '0'})
    put(props, 'i', {'val': '0'})
    put(props, 'color', {'val': '000000'})
    for n in props:
        if n.tag in (W + 'rFonts', W + 'color'):
            for k in list(n.attrib):
                if 'Theme' in k or 'theme' in k:
                    del n.attrib[k]

if TARGET.exists():
    raise FileExistsError(TARGET)
hashes = {str(p): sha(p) for p in (SOURCE, TEMPLATE)}
if hashes[str(SOURCE)] != 'a69a0adcd4b007ba0cb15f29afc635342b08d939d52ed1e54de6cd34e7d2f6f5':
    raise RuntimeError('Source changed; inspect current saved file first')
with ZipFile(SOURCE) as src, ZipFile(TEMPLATE) as tpl:
    root = etree.fromstring(src.read('word/document.xml'))
    body = root.find('w:body', NS)
    children = list(body)
    template_body = list(etree.fromstring(tpl.read('word/document.xml')).find('w:body', NS))
    map_outer = [0, 1, 2, 3, 4, 7, 10, 12, 15, 16, 17, 18, 23]
    map_inner = [24, 25, 26, 27, 28, 31, 34, 36, 38, 39, 41, 42, 43, 44, 47]
    covers = []
    for index, template_index in enumerate(map_outer + map_inner):
        p = children[index]
        before = text(p)
        old_props = p.find('w:pPr', NS)
        if old_props is not None:
            p.remove(old_props)
        props = deepcopy(template_body[template_index].find('w:pPr', NS))
        for node in list(props):
            if node.tag in (W + 'sectPr', W + 'numPr', W + 'pStyle'):
                props.remove(node)
        p.insert(0, props)
        inner = index >= 13
        role = index - 13 if inner else index
        size = 14
        bold = role in (1, 2)
        before_pt = 0
        after_pt = 6
        line = 240
        if role == 3:
            size = 16
            after_pt = 0
        elif role == 4:
            after_pt = 58
        elif role == 5:
            size, bold = 16, True
            after_pt = 36 if inner else 48
        elif role == 6:
            size, bold = 20, True
            after_pt = 18
            line = 276
        elif role == 7:
            size = 16
            after_pt = 18 if inner else 48
        elif not inner and role == 8:
            bold = True
        elif inner and role in (8, 9, 10):
            bold = True
            if role == 9:
                after_pt = 20
        members = role in ((11, 12, 13) if inner else (9, 10, 11))
        date = role == (14 if inner else 12)
        if members:
            after_pt = 0
            line = 312
        if date:
            before_pt = 76 if inner else 80
            after_pt = 0
        put(props, 'spacing', {'before': before_pt * 20, 'after': after_pt * 20, 'line': line, 'lineRule': 'auto'})
        put(props, 'jc', {'val': 'left' if members else 'center'})
        put(props, 'ind', {'left': 1440 if members else 0, 'right': 0, 'firstLine': 0})
        put(props, 'keepNext', {'val': '0'})
        put(props, 'keepLines', {'val': '1'})
        put(props, 'pageBreakBefore', {'val': '1' if index == 13 else '0'})
        endprops = put(props, 'rPr', {})
        font(endprops, size, bold)
        for r in p.findall('w:r', NS):
            if r.find('w:t', NS) is not None:
                rprops = r.find('w:rPr', NS)
                if rprops is None:
                    rprops = etree.Element(W + 'rPr')
                    r.insert(0, rprops)
                font(rprops, size, bold)
        if role == 6:
            for e in list(p):
                if e.tag != W + 'pPr':
                    p.remove(e)
            lines = ['PHÂN TÍCH DỮ LIỆU TIÊU THỤ ĐIỆN NĂNG', 'VÀ DỰ ĐOÁN NHU CẦU SỬ DỤNG ĐIỆN', 'THEO THỜI GIAN']
            for n, value in enumerate(lines):
                r = etree.SubElement(p, W + 'r')
                font(etree.SubElement(r, W + 'rPr'), size, bold)
                if n:
                    etree.SubElement(r, W + 'br')
                etree.SubElement(r, W + 't').text = value
        covers.append({'index': index, 'template_index': template_index, 'before': before, 'after': text(p), 'size': size, 'bold': bold, 'member_block': members, 'spacing_before': before_pt, 'spacing_after': after_pt})
    refs = False
    edits = []
    for p in body.iter(W + 'p'):
        value = text(p)
        if value == 'TÀI LIỆU THAM KHẢO':
            refs = True
        if refs:
            continue
        matches = list(MARKER.finditer(value))
        if not matches:
            continue
        delete = set(i for m in matches for i in range(m.start(), m.end()))
        pos = 0
        for node in p.xpath('.//w:t', namespaces=NS):
            old = node.text or ''
            node.text = ''.join(c for i, c in enumerate(old, pos) if i not in delete)
            pos += len(old)
        edits.append({'before': value, 'after': text(p), 'markers': [m.group().strip() for m in matches]})
    out_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    with ZipFile(TARGET, 'w') as out:
        for member in src.infolist():
            out.writestr(copy(member), out_xml if member.filename == 'word/document.xml' else src.read(member.filename))
if any(sha(Path(p)) != h for p, h in hashes.items()):
    raise RuntimeError('Source hash changed')
with ZipFile(TARGET) as check:
    if check.testzip() is not None:
        raise RuntimeError('Output CRC failed')
manifest = {'source_hashes': hashes, 'output': str(TARGET), 'sha256': sha(TARGET), 'cover_edits': covers, 'citation_edits': edits, 'removed_markers': sum(len(e['markers']) for e in edits), 'changed_parts_before_word': ['word/document.xml']}
(QA / 'patch-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'output': str(TARGET), 'removed_markers': manifest['removed_markers'], 'edited_paragraphs': len(edits), 'source_unchanged': True}, ensure_ascii=False))
