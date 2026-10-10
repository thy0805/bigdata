import argparse
import json
from pathlib import Path

import pypdfium2 as pdfium

parser = argparse.ArgumentParser()
parser.add_argument('qa')
args = parser.parse_args()
qa = Path(args.qa)
out = qa / 'render'
out.mkdir(exist_ok=True)
pages = []
with pdfium.PdfDocument(qa / 'W01-native.pdf') as pdf:
    for index, page in enumerate(pdf):
        filename = out / f'page-{index + 1:03}.png'
        page.render(scale=2).to_pil().save(filename)
        pages.append({'page': index + 1, 'image': str(filename),
                      'text': page.get_textpage().get_text_range()})
        page.close()
(qa / 'render-pages.json').write_text(json.dumps({'renderer': 'Native Microsoft Word PDF / PDFium scale 2',
    'page_count': len(pages), 'pages': pages}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'pages': len(pages), 'render': str(out)}, ensure_ascii=False))
