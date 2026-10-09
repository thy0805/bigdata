import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E

root = Path(r'D:\Hoctap\bigdata')
qa = root / 'Detaituan8910/.agent/qa/diennang-khung-20261006'
qa.mkdir(parents=True, exist_ok=True)
source = root / 'ApacheFlink.docx'
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def text(e):
    return ''.join(e.xpath('.//w:t/text()', namespaces=ns))


def props(e):
    return [{E.QName(x).localname: {E.QName(k).localname: v for k, v in x.attrib.items()}} for x in e] if e is not None else []


with ZipFile(source) as z:
    parts = {n: z.read(n) for n in z.namelist()}
doc = E.fromstring(parts['word/document.xml'])
styles = E.fromstring(parts['word/styles.xml'])
body = doc.find('w:body', ns)
report = {
    'source': str(source),
    'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'parts': [{'path': n, 'size': len(b), 'sha256': hashlib.sha256(b).hexdigest()} for n, b in parts.items()],
    'front_body': [{'index': i, 'kind': E.QName(e).localname, 'text': text(e), 'properties': props(e.find('w:pPr', ns)), 'run_properties': [props(x) for x in e.findall('w:r/w:rPr', ns)]} for i, e in enumerate(body) if i < 67],
    'sections': [props(e) for e in doc.xpath('//w:sectPr', namespaces=ns)],
    'styles': [{'id': e.get('{'+ns['w']+'}styleId'), 'name': e.xpath('w:name/@w:val', namespaces=ns), 'properties': props(e.find('w:pPr', ns)), 'runs': props(e.find('w:rPr', ns))} for e in styles.findall('w:style', ns)],
    'defaults': props(styles.find('w:docDefaults/w:rPrDefault/w:rPr', ns)),
    'tables': [[[text(c) for c in row.findall('w:tc', ns)] for row in t.findall('w:tr', ns)] for t in doc.xpath('//w:tbl', namespaces=ns)],
    'body_styles': [{'text': text(e)[:150], 'style': e.xpath('w:pPr/w:pStyle/@w:val', namespaces=ns), 'properties': props(e.find('w:pPr', ns))} for e in body if e.tag.endswith('}p') and text(e)],
}
(qa / 'template-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'sha256': report['sha256'], 'front': [(e['index'], e['text'], e['properties']) for e in report['front_body']], 'tables': [t[:4] for t in report['tables']], 'sections': report['sections'], 'heading_styles': [s for s in report['styles'] if s['id'] in ['Heading11', 'Heading21', 'Heading31', 'FrontTitle', 'FrontTitleNoTOC', 'BodyText', 'BodyText1']]}, ensure_ascii=False, indent=2))
