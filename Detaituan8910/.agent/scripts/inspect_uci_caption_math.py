import hashlib
import json
import sys
import zipfile
from pathlib import Path

from lxml import etree

source = Path(sys.argv[1])
destination = Path(sys.argv[2])
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with zipfile.ZipFile(source) as package:
    xml = etree.fromstring(package.read('word/document.xml'))
    captions = []
    equations = []
    for p in xml.xpath('./w:body/w:p', namespaces=ns):
        style = p.xpath('string(w:pPr/w:pStyle/@w:val)', namespaces=ns)
        if style in ('TableCaption', 'FigureCaption'):
            fields = p.xpath('.//w:instrText/text() | .//w:fldSimple/@w:instr', namespaces=ns)
            captions.append({'style': style, 'text': ''.join(p.xpath('.//w:t/text()', namespaces=ns)), 'fields': fields, 'xml': etree.tostring(p, encoding='unicode')})
        for math in p.xpath('.//m:oMath', namespaces=ns):
            equations.append({'text': ''.join(math.xpath('.//m:t/text()', namespaces=ns)), 'xml': etree.tostring(math, encoding='unicode'), 'characters': math.xpath('.//m:chr/@m:val | .//m:begChr/@m:val | .//m:endChr/@m:val', namespaces=ns)})
    styles = etree.fromstring(package.read('word/styles.xml'))
    result = {'source': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'captions': captions, 'equations': equations, 'chapter_style': [etree.tostring(s, encoding='unicode') for s in styles.xpath('./w:style[@w:styleId="ChapterTitle"]', namespaces=ns)]}
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'sha256': result['sha256'], 'captions': [{k: c[k] for k in ('style', 'text', 'fields')} for c in captions], 'equations': equations}, ensure_ascii=False))
