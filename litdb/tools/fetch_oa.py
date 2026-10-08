"""Fetch open-access PDFs for abstract-only rows of docs/literature/literature_matrix.csv.
Sources: arXiv (from 10.48550/arxiv.* DOIs) and the OpenAlex best_oa_location. No paywall bypass."""
import csv, json, os, sys, urllib.request
OUT = 'litdb/incoming'
UA = {'User-Agent': 'litdb-fetch/1.0'}
def get(url, timeout=40):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
rows = [r for r in csv.DictReader(open('docs/literature/literature_matrix.csv', encoding='utf-8')) if r['read_depth'] == 'ABS']
log = []
for r in rows:
    key, doi = r['key'], r['doi'].strip()
    dest = f'{OUT}/{key}.pdf'
    if os.path.exists(dest):
        continue
    urls = []
    if doi.lower().startswith('10.48550/arxiv.'):
        urls.append('https://arxiv.org/pdf/' + doi.split('arxiv.', 1)[1].lower() + '.pdf')
    try:
        w = json.loads(get('https://api.openalex.org/works/doi:' + doi))
        for loc in [w.get('best_oa_location')] + (w.get('locations') or []):
            if loc and loc.get('pdf_url') and loc['pdf_url'] not in urls:
                urls.append(loc['pdf_url'])
    except Exception as e:
        log.append((key, 'openalex-fail', str(e)[:60]))
    ok = False
    for u in urls[:4]:
        try:
            b = get(u)
            if b[:5] == b'%PDF-':
                open(dest, 'wb').write(b); log.append((key, 'OK', u, len(b))); ok = True; break
        except Exception as e:
            log.append((key, 'fail', u, str(e)[:50]))
    if not ok:
        log.append((key, 'NO-PDF', len(urls)))
for l in log: print(*l)
