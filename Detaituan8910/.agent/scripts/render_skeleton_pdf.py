import json
import sys
from pathlib import Path

import pypdfium2 as pdfium

qa = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(r'D:\Hoctap\bigdata\Detaituan8910\.agent\qa\diennang-khung-20261006')
stem = sys.argv[1]
pdf = pdfium.PdfDocument(qa / f'{stem}.pdf')
folder = qa / f'{stem}-render'
folder.mkdir(exist_ok=True)
pages = []
for index, page in enumerate(pdf):
    page.render(scale=2).to_pil().convert('RGB').save(folder / f'page-{index + 1}.png')
    pages.append({'page': index + 1, 'width': page.get_width(), 'height': page.get_height(), 'text': page.get_textpage().get_text_range()})
(qa / f'{stem}-pdf.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'pages': len(pages), 'folder': str(folder)}, ensure_ascii=False))
