from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

qa = Path('D:/Hoctap/bigdata/Detaituan8910/.agent/qa/word-uci-20261008')
manifest = json.loads((qa / 'build-manifest.json').read_text(encoding='utf-8'))


def check(pair):
    number, ref = pair
    try:
        with urlopen(Request(ref[-1], headers={'User-Agent': 'Mozilla/5.0'}), timeout=20) as response:
            response.read(4096)
            return {'number': number, 'url': ref[-1], 'status': response.status, 'resolved': response.url, 'content_type': response.headers.get('Content-Type', '')}
    except HTTPError as exc:
        return {'number': number, 'url': ref[-1], 'status': exc.code, 'resolved': exc.url}
    except (URLError, TimeoutError) as exc:
        return {'number': number, 'url': ref[-1], 'error': str(exc)}


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, enumerate(manifest['refs'], 1)))
(qa / 'reference-links.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(results, ensure_ascii=False, indent=2))
