from pathlib import Path
import json
from PIL import Image, ImageDraw
import pypdfium2 as pdfium

root = Path(__file__).resolve().parents[2]
qa = root / '.agent/qa/word-w00-20261010'
old = root / '.agent/qa/word-uci-cover-citations-20261008/final-render'
pdf = pdfium.PdfDocument(qa / 'chapter2-readonly-preview.pdf')
target = qa / 'chapter2-preview'
target.mkdir(exist_ok=True)
for i in range(len(pdf)):
    pdf[i].render(scale=1.7).to_pil().save(target / f'page-{i+1}.png')
groups = [('main', [old / f'page-{i}.png' for i in range(1, 38)]), ('chapter2', [target / f'page-{i}.png' for i in range(1, len(pdf)+1)])]
for label, files in groups:
    for start in range(0, len(files), 12):
        items = files[start:start+12]
        sheet = Image.new('RGB', (1080, 1254), '#c5c9cc')
        draw = ImageDraw.Draw(sheet)
        for j, path in enumerate(items):
            img = Image.open(path).convert('RGB')
            img.thumbnail((260, 380))
            x, y = (j % 4)*270, (j//4)*418
            sheet.paste(img, (x+(270-img.width)//2, y+24))
            draw.text((x+8, y+5), f'{label}: {path.stem}', fill='black')
        sheet.save(qa / f'{label}-contact-{start//12+1}.png')
print(json.dumps({'main_pages_reused': 37, 'chapter2_pages_fresh': len(pdf), 'preview_only': True}))
