import json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E

root = Path(__file__).resolve().parents[2]
qa = root / '.agent/qa/word-w01-20261010'
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + ns['w'] + '}'


def audit(path):
    with ZipFile(path) as z:
        doc = E.fromstring(z.read('word/document.xml'))
        styles = E.fromstring(z.read('word/styles.xml'))
    lookup = {s.get(W + 'styleId'): s for s in styles.findall(W + 'style')}
    default_r = styles.find('w:docDefaults/w:rPrDefault/w:rPr', ns)
    default_p = styles.find('w:docDefaults/w:pPrDefault/w:pPr', ns)

    def chain(name):
        result, seen = [], set()
        while name and name in lookup and name not in seen:
            seen.add(name)
            s = lookup[name]
            result.append(s)
            base = s.find(W + 'basedOn')
            name = base.get(W + 'val') if base is not None else None
        return result[::-1]

    def resolve(p, run=None):
        ps = p.xpath('./w:pPr/w:pStyle/@w:val', namespaces=ns)
        name = ps[0] if ps else 'Normal'
        layers = [default_r] + [s.find(W + 'rPr') for s in chain(name)]
        if run is not None:
            rs = run.xpath('./w:rPr/w:rStyle/@w:val', namespaces=ns)
            if rs:
                layers += [s.find(W + 'rPr') for s in chain(rs[0])]
            layers.append(run.find(W + 'rPr'))
        props = {}
        for layer in layers:
            if layer is not None:
                for item in layer:
                    tag = E.QName(item).localname
                    if tag == 'rFonts':
                        props['font'] = item.get(W + 'ascii', props.get('font'))
                    elif tag == 'sz':
                        props['pt'] = int(item.get(W + 'val')) / 2
                    elif tag == 'b':
                        props['bold'] = item.get(W + 'val', '1') not in ['0', 'false']
        return name, props

    distribution = Counter()
    exceptions = []
    paragraph_styles = {}
    for p in doc.xpath('/w:document/w:body//w:p', namespaces=ns):
        style, props = resolve(p)
        paragraph_styles[style] = props
        for r in p.findall(W + 'r'):
            text = ''.join(r.xpath('.//w:t/text()', namespaces=ns))
            if not text.strip():
                continue
            _, rp = resolve(p, r)
            distribution[(style, rp.get('font'), rp.get('pt'))] += 1
            if rp.get('font') not in ['Times New Roman', 'Symbol']:
                exceptions.append({'style': style, 'text': text[:100], **rp})
    return {'path': str(path), 'styles': paragraph_styles, 'distribution': [{'style': k[0], 'font': k[1], 'pt': k[2], 'runs': v} for k, v in distribution.items()], 'font_exceptions': exceptions,
            'default_rPr': E.tostring(default_r).decode() if default_r is not None else None,
            'default_pPr': E.tostring(default_p).decode() if default_p is not None else None,
            'template_instructions': [''.join(p.xpath('.//w:t/text()', namespaces=ns)) for p in doc.xpath('/w:document/w:body/w:p', namespaces=ns) if any(x in ''.join(p.xpath('.//w:t/text()', namespaces=ns)).lower() for x in ['times new roman', 'cỡ chữ', 'line spacing', 'lề trái', 'before', 'after'])]}


result = {'template': audit(root.parent / 'Mauwword/Mau bao cao_Do an_Khoa luan_2025.docx'), 'output': audit(root / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx')}
(qa / 'font-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'font_exceptions': result['output']['font_exceptions'], 'output_styles': result['output']['styles'], 'template_instructions': result['template']['template_instructions']}, ensure_ascii=False, indent=2))
