from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E

root = Path(__file__).resolve().parents[2]
path = root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
with ZipFile(path) as z:
    parts = {name: z.read(name) for name in z.namelist()}
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + ns['w'] + '}'
doc = E.fromstring(parts['word/document.xml'])
styles = E.fromstring(parts['word/styles.xml'])
source = styles.xpath('./w:style[@w:styleId="Heading11"]', namespaces=ns)[0]
heading = styles.xpath('./w:style[@w:styleId="Heading1"]', namespaces=ns)[0]
for tag in ('pPr', 'rPr'):
    old = heading.find(W + tag)
    if old is not None:
        heading.remove(old)
    heading.append(deepcopy(source.find(W + tag)))
numbering = E.fromstring(parts['word/numbering.xml'])
level = numbering.xpath('./w:abstractNum[@w:abstractNumId="2"]/w:lvl[@w:ilvl="0"]', namespaces=ns)[0]
level.find(W + 'pStyle').set(W + 'val', 'Heading1')
for p in doc.xpath('.//w:body/w:p[w:pPr/w:pStyle[@w:val="Heading1"]]', namespaces=ns):
    pr = p.find(W + 'pPr')
    old = pr.find(W + 'numPr')
    if old is not None:
        pr.remove(old)
    num = E.SubElement(pr, W + 'numPr')
    E.SubElement(num, W + 'ilvl').set(W + 'val', '0')
    E.SubElement(num, W + 'numId').set(W + 'val', '4')
parts['word/document.xml'] = E.tostring(doc, encoding='UTF-8', xml_declaration=True, standalone=True)
parts['word/styles.xml'] = E.tostring(styles, encoding='UTF-8', xml_declaration=True, standalone=True)
parts['word/numbering.xml'] = E.tostring(numbering, encoding='UTF-8', xml_declaration=True, standalone=True)
with ZipFile(path, 'w', ZIP_DEFLATED) as z:
    for name, data in parts.items():
        z.writestr(name, data)
print('Native Heading1 explicitly linked to existing nine-level numbering; source title formatting retained.')
