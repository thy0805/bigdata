import hashlib
import json
import re
import subprocess
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / '.agent/qa/word-w00-20261010'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math', 'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing', 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
SOURCES = {
    'main': ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx',
    'chapter2': Path('C:/Users/thy/Downloads/HAULYVUNHAN_Chuong2_CoSoLyThuyet_HoanChinh.docx'),
    'template': ROOT.parent / 'Mauwword/Mau bao cao_Do an_Khoa luan_2025.docx',
    'chapter1': ROOT / 'KhoiTuan Tong Quan Bai Toan Chuong 1.docx',
    'chapter2_outline': ROOT / 'HAULYVUNHAN_Chuong2_CoSoLyThuyet.docx',
}


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def text(element):
    return ''.join(element.xpath('.//w:t/text() | .//m:t/text()', namespaces=NS))


QA.mkdir(parents=True, exist_ok=True)
manifest = {}
for label, path in SOURCES.items():
    with ZipFile(path) as package:
        xml = etree.fromstring(package.read('word/document.xml'))
        styles = etree.fromstring(package.read('word/styles.xml'))
        blocks = []
        for index, element in enumerate(xml.find('w:body', NS), 1):
            if element.tag == '{' + NS['w'] + '}p':
                style = element.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS)
                blocks.append(dict(id=f'B{index:03d}', kind='paragraph', style=style[0] if style else '', text=text(element)))
            elif element.tag == '{' + NS['w'] + '}tbl':
                rows = [[text(cell) for cell in row.findall('w:tc', NS)] for row in element.findall('w:tr', NS)]
                blocks.append(dict(id=f'B{index:03d}', kind='table', rows=rows))
        fields = xml.xpath('//w:instrText/text() | //w:fldSimple/@w:instr', namespaces=NS)
        sections = [dict(element.attrib) for element in xml.xpath('//w:sectPr/w:pgSz | //w:sectPr/w:pgMar | //w:sectPr/w:pgNumType', namespaces=NS)]
        style_info = []
        for element in styles.findall('w:style', NS):
            names = element.xpath('./w:name/@w:val', namespaces=NS)
            outline = element.xpath('./w:pPr/w:outlineLvl/@w:val', namespaces=NS)
            if outline or any(token in (names[0] if names else '').lower() for token in ['heading', 'normal', 'chapter', 'caption', 'title', 'front']):
                style_info.append(dict(id=element.get('{' + NS['w'] + '}styleId'), name=names[0] if names else '', outline=outline, xml=etree.tostring(element).decode()))
        result = dict(path=str(path), sha256=digest(path), crc_error=package.testzip(), blocks=blocks, fields=fields, sections=sections, styles=style_info,
                      paragraphs=len(xml.xpath('//w:body//w:p', namespaces=NS)), top_level_tables=len(xml.xpath('/w:document/w:body/w:tbl', namespaces=NS)),
                      drawings=len(xml.xpath('//w:drawing', namespaces=NS)), equations=len(xml.xpath('//m:oMath', namespaces=NS)),
                      media=[dict(name=name, sha256=hashlib.sha256(package.read(name)).hexdigest()) for name in package.namelist() if name.startswith('word/media/')],
                      revisions=len(xml.xpath('//w:ins | //w:del', namespaces=NS)), comments=[name for name in package.namelist() if 'comments' in name.lower()])
        (QA / (label + '-inspection.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        (QA / (label + '-text.txt')).write_text('\n'.join(block['id'] + ' [' + block.get('style', 'table') + '] ' + (block['text'] if block['kind'] == 'paragraph' else '\n'.join(' | '.join(row) for row in block['rows'])) for block in blocks), encoding='utf-8')
        manifest[label] = {key: result[key] for key in ['path', 'sha256', 'paragraphs', 'top_level_tables', 'drawings', 'equations', 'revisions', 'comments']}
extra = [ROOT.parent / '.agent/rule.md', Path('C:/Users/thy/Downloads/rule.md'), ROOT / 'dashboard/app.py', ROOT / 'operations/services.py']
manifest['protected_extra'] = {str(path): digest(path) for path in extra}
manifest['git_head'] = subprocess.check_output(['git', '-c', 'safe.directory=' + ROOT.parent.as_posix(), '-C', str(ROOT.parent), 'rev-parse', 'HEAD']).decode().strip()
(QA / 'sources.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False, indent=2))
