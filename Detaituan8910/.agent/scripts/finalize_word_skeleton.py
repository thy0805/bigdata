import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E

root = Path(r'D:\Hoctap\bigdata')
qa = root / 'Detaituan8910/.agent/qa/diennang-khung-20261006'
candidate = qa / (sys.argv[1] if len(sys.argv) > 1 else 'candidate-v2.docx')
source = root / 'ApacheFlink.docx'
base_output = root / 'BaoCao_PhanTich_DuDoan_DienNang_Khung.docx'
output = base_output
index = 2
if len(sys.argv) > 2 and sys.argv[2] == '--repair-owned-output':
    existing = json.loads((qa / 'final-manifest.json').read_text(encoding='utf-8'))
    output = Path(existing['output'])
    assert hashlib.sha256(output.read_bytes()).hexdigest() == existing['output_sha256']
else:
    while output.exists():
        output = base_output.with_stem(base_output.stem + f'_v{index}')
        index += 1
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
w = '{' + ns['w'] + '}'
with ZipFile(candidate) as z:
    parts = {n: z.read(n) for n in z.namelist()}
with ZipFile(source) as z:
    original = {n: z.read(n) for n in z.namelist()}


def xmlbytes(e):
    return E.tostring(e, encoding='UTF-8', xml_declaration=True, standalone=True)


doc = E.fromstring(parts['word/document.xml'])
for table in doc.findall('w:body/w:tbl', ns):
    for cell in table.findall('w:tr/w:tc', ns):
        pr = cell.find(w + 'tcPr')
        borders = pr.find(w + 'tcBorders')
        if borders is not None:
            pr.remove(borders)
        borders = E.SubElement(pr, w + 'tcBorders')
        for side in ['top', 'left', 'bottom', 'right']:
            E.SubElement(borders, w + side, {w + 'val': 'single', w + 'sz': '6', w + 'space': '0', w + 'color': '000000'})
for p in doc.findall('w:body/w:p', ns):
    code = ''.join(p.xpath('.//w:instrText/text()', namespaces=ns))
    if 'TOC ' in code and ('FigureCaption,1' in code or 'TableCaption,1' in code):
        inside = False
        for element in list(p):
            f = element.find(w + 'fldChar')
            if f is not None and f.get(w + 'fldCharType') == 'separate':
                inside = True
            elif f is not None and f.get(w + 'fldCharType') == 'end':
                inside = False
            elif inside:
                p.remove(element)
for field in doc.xpath('//w:fldChar[@w:fldCharType="begin"]', namespaces=ns):
    field.set(w + 'dirty', 'false')
parts['word/document.xml'] = xmlbytes(doc)
settings = E.fromstring(parts['word/settings.xml'])
update = settings.find(w + 'updateFields')
if update is not None:
    update.set(w + 'val', 'false')
parts['word/settings.xml'] = xmlbytes(settings)
preserve = ['word/theme/theme1.xml', 'word/fontTable.xml', 'word/media/image1.png', 'word/footnotes.xml', 'word/endnotes.xml', 'word/webSettings.xml']
for name in preserve:
    parts[name] = original[name]
rel_map = {e.get('Id'): e.get('Target') for e in E.fromstring(parts['word/_rels/document.xml.rels'])}
footer_map = {}
for section_index, source_footer in [(1, 'word/footer1.xml'), (2, 'word/footer2.xml')]:
    section = doc.xpath('//w:sectPr', namespaces=ns)[section_index]
    ref = section.find(w + 'footerReference')
    target = 'word/' + rel_map[ref.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
    parts[target] = original[source_footer]
    footer_map[source_footer] = target
core = E.fromstring(parts['docProps/core.xml'])
for e in core:
    if E.QName(e).localname in ['creator', 'lastModifiedBy', 'title', 'subject', 'description', 'keywords']:
        e.text = ''
parts['docProps/core.xml'] = xmlbytes(core)
with ZipFile(output, 'w' if len(sys.argv) > 2 and sys.argv[2] == '--repair-owned-output' else 'x') as z:
    for name, data in parts.items():
        z.writestr(name, data)
manifest = {'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'candidate': str(candidate), 'output': str(output), 'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'preserve_only_parts': preserve, 'footer_source_target_map': footer_map, 'empty_lists': 'dynamic fields retained with intentionally empty cached results', 'main_toc': 'refreshed by native Word; unlocked and updateable'}
(qa / 'final-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False))
