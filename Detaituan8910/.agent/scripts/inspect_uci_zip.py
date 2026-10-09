import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

source = Path(r'C:\Users\thy\Downloads\individual+household+electric+power+consumption.zip')
qa = Path(r'D:\Hoctap\bigdata\Detaituan8910\.agent\qa\word-uci-20261008')
qa.mkdir(parents=True, exist_ok=True)
digest = hashlib.sha256(source.read_bytes()).hexdigest()
with ZipFile(source) as archive:
    entries = [{'name': f.filename, 'bytes': f.file_size, 'compressed_bytes': f.compress_size, 'crc32': f'{f.CRC:08x}'} for f in archive.infolist()]
    target = next(f.filename for f in archive.infolist() if f.filename.endswith('household_power_consumption.txt'))
    with archive.open(target) as stream:
        reader = csv.reader(io.TextIOWrapper(stream, encoding='utf-8-sig'), delimiter=';')
        header = next(reader)
        rows = 0
        widths = Counter()
        missing = Counter()
        first = []
        last = None
        for row in reader:
            rows += 1
            widths[len(row)] += 1
            if len(first) < 3:
                first.append(row)
            last = row
            for index, value in enumerate(row):
                if value.strip() in ('', '?'):
                    missing[header[index]] += 1
report = {'path': str(source), 'sha256': digest, 'entries': entries, 'member': target, 'separator': ';', 'columns': header, 'rows': rows, 'row_width_counts': dict(widths), 'missing_cells_per_column': dict(missing), 'first_rows': first, 'last_row': last, 'checks': 'Full row count/width/missing-token scan; CRC verified by fully reading ZIP member. No extraction, cleaning, training, numeric-validity or time-gap audit.', 'partitioned_folder': 'Not found by recursive search under D:/Hoctap/bigdata; user supplied original ZIP instead.'}
(qa / 'dataset-inspection.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
