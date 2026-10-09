import hashlib
import json
import sys
import zipfile
from copy import copy, deepcopy
from pathlib import Path

from lxml import etree

root = Path(r'D:\Hoctap\bigdata\Detaituan8910')
source = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_20261008.docx'
target = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v2_20261008.docx'
qa = root / '.agent/qa/word-uci-caption-math-20261008'
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
if target.exists() and '--verify-existing' not in sys.argv:
    raise FileExistsError(target)
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
if source_hash != '51edbc9ba1f27e2d2c194eabca31f8f7fcd15568b5edc5ea1a8cdb9097582fe2':
    raise ValueError('Source checkpoint changed')
with zipfile.ZipFile(source) as package:
    xml = etree.fromstring(package.read('word/document.xml'))
    count = 0
    for p in xml.xpath('./w:body/w:p', namespaces=ns):
        if p.xpath('string(w:pPr/w:pStyle/@w:val)', namespaces=ns) not in ('TableCaption', 'FigureCaption'):
            continue
        for field in p.xpath('.//w:fldSimple', namespaces=ns):
            if 'STYLEREF' in field.get('{' + ns['w'] + '}instr', ''):
                field.set('{' + ns['w'] + '}instr', ' STYLEREF "ChapterTitle" \\n \\t ')
                count += 1
        for instruction in p.xpath('.//w:instrText', namespaces=ns):
            if 'STYLEREF' in (instruction.text or ''):
                instruction.text = ' STYLEREF "ChapterTitle" \\n \\t '
                count += 1
    if count != 5:
        raise ValueError(f'Expected 5 chapter fields, got {count}')
    maths = xml.xpath('.//m:oMath', namespaces=ns)
    mae = [m for m in maths if ''.join(m.xpath('.//m:t/text()', namespaces=ns)).startswith('MAE=')]
    if len(mae) != 1:
        raise ValueError('Expected one MAE')
    argument = mae[0].xpath('./m:nary/m:e', namespaces=ns)[0]
    children = list(argument)
    if len(children) != 5 or children[0].xpath('string(m:t)', namespaces=ns) != '|' or children[-1].xpath('string(m:t)', namespaces=ns) != '|':
        raise ValueError('Unexpected MAE argument')
    delimiter = etree.Element('{' + ns['m'] + '}d')
    properties = etree.SubElement(delimiter, '{' + ns['m'] + '}dPr')
    for name, value in (('begChr', '|'), ('endChr', '|'), ('grow', '1')):
        element = etree.SubElement(properties, '{' + ns['m'] + '}' + name)
        element.set('{' + ns['m'] + '}val', value)
    control = mae[0].xpath('./m:nary/m:naryPr/m:ctrlPr', namespaces=ns)
    if control:
        properties.append(deepcopy(control[0]))
    inner = etree.SubElement(delimiter, '{' + ns['m'] + '}e')
    for child in children[1:-1]:
        inner.append(deepcopy(child))
    for child in children:
        argument.remove(child)
    argument.append(delimiter)
    new_xml = etree.tostring(xml, xml_declaration=True, encoding='UTF-8', standalone=True)
    if not target.exists():
        with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as output:
            for member in package.infolist():
                output.writestr(copy(member), new_xml if member.filename == 'word/document.xml' else package.read(member.filename))
    with zipfile.ZipFile(target) as output:
        if output.testzip() is not None or output.read('word/document.xml') != new_xml:
            raise ValueError('Patched package mismatch')
        unchanged_parts = all(package.read(name) == output.read(name) for name in package.namelist() if name != 'word/document.xml')
manifest = {'source': str(source), 'target': str(target), 'source_sha256': source_hash, 'patched_sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'changed_part': 'word/document.xml', 'other_parts_unchanged_before_word_save': unchanged_parts, 'caption_chapter_fields': count, 'caption_field': 'STYLEREF "ChapterTitle" \\n \\t', 'mae_change': 'Replace two literal bars with one native OMML delimiter pair; retain inner residual expression', 'rmse_energy_unchanged': True}
(qa / 'patch-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False))
