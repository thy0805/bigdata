from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import hashlib
import json
import re

ROOT = Path(r'D:\Hoctap\bigdata\Detaituan8910')
QA = ROOT / '.agent/qa/word-uci-cover-citations-20261008'
PATHS = [ROOT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v2_20261008.docx', ROOT.parent / 'Mauwword/Mau bao cao_Do an_Khoa luan_2025.docx']
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def txt(e):
    return ''.join(e.xpath('.//w:t/text()', namespaces=NS))

records = []
for path in PATHS:
    with ZipFile(path) as package:
        root = etree.fromstring(package.read('word/document.xml'))
        styles = etree.fromstring(package.read('word/styles.xml'))
        children = list(root.find('w:body', NS))
        entries = []
        for i, e in enumerate(children[:54]):
            entries.append({'index': i, 'tag': etree.QName(e).localname, 'text': txt(e), 'pPr': etree.tostring(e.find('w:pPr', NS), encoding='unicode') if e.find('w:pPr', NS) is not None else None, 'runs': [{'text': txt(r), 'rPr': etree.tostring(r.find('w:rPr', NS), encoding='unicode') if r.find('w:rPr', NS) is not None else None} for r in e.findall('w:r', NS)]})
        refs = False
        markers = []
        for i, e in enumerate(children):
            value = txt(e)
            if value == 'TÀI LIỆU THAM KHẢO':
                refs = True
            if '[' in value:
                markers.append({'index': i, 'references': refs, 'text': value, 'matches': re.findall(r'\[\d+(?:\s*[-–,;]\s*\d+)*\]', value)})
        records.append({'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'children': entries, 'markers': markers, 'normal_style': etree.tostring(styles.xpath('./w:style[@w:styleId="Normal"]', namespaces=NS)[0], encoding='unicode')})
(QA / 'inspection.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
for r in records:
    print(r['path'], r['sha256'])
    for p in r['children']:
        print(p['index'], repr(p['text']), re.sub(r'<[^>]+>', '', p['pPr'] or ''), [(s['text'], re.findall(r'w:(?:sz|b|i|rFonts)[^>]*', s['rPr'] or '')) for s in p['runs'] if s['text']])
    print('marker paragraphs', len(r['markers']), 'body markers', sum(len(m['matches']) for m in r['markers'] if not m['references']))
