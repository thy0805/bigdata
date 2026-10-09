import json
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[2]
qa = root / '.agent/qa/word-w01-20261010'
pdf = pdfium.PdfDocument(qa / 'W01-native.pdf')
out = qa / 'render'
out.mkdir(exist_ok=True)
for stale in out.glob('page-*.png'):
    if int(stale.stem.split('-')[-1]) > len(pdf):
        archived = qa / 'render-superseded'
        archived.mkdir(exist_ok=True)
        stale.rename(archived / stale.name)
pages = []
for index, page in enumerate(pdf):
    path = out / f'page-{index + 1:03}.png'
    page.render(scale=2).to_pil().save(path)
    text = page.get_textpage().get_text_range()
    pages.append({'page': index + 1, 'text': text, 'image': str(path)})
    page.close()
for start in range(0, len(pages), 8):
    group = pages[start:start + 8]
    sheet = Image.new('RGB', (1360, 990), '#ccd1d5')
    draw = ImageDraw.Draw(sheet)
    for offset, page in enumerate(group):
        im = Image.open(page['image']).convert('RGB')
        im.thumbnail((328, 462))
        x, y = (offset % 4) * 340, (offset // 4) * 495
        sheet.paste(im, (x + (340 - im.width) // 2, y + 27))
        draw.text((x + 10, y + 7), f"W01 page {page['page']}", fill='black')
    sheet.save(out / f'contact-{start // 8 + 1:02}.png')
(qa / 'render-pages.json').write_text(json.dumps({'renderer': 'Microsoft Word native PDF + PDFium scale=2; packaged renderer unavailable (soffice.exe absent)', 'page_count': len(pages), 'pages': pages}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'pages': len(pages), 'png_count': len(list(out.glob('page-*.png'))), 'contact_sheets': len(list(out.glob('contact-*.png')))}, ensure_ascii=False))
