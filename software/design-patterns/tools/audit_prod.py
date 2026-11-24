import glob, os, re

pages = sorted(glob.glob('p[234]/c*.html'))
bad, rows = [], []
for f in pages:
    t = open(f, encoding='utf-8').read()
    n = t.count('<section class="sec"')
    m = re.search(r'assets/puml/dp-(\d+)-(\d+)\.svg', t)
    if n != 7 or not m:
        bad.append((f, n, bool(m)))
        continue
    svg = 'assets/puml/dp-%s-%s.svg' % (m.group(1), m.group(2))
    s = open(svg, encoding='utf-8').read(320)
    w = re.search(r'width="(\d+)px"', s)
    h = re.search(r'height="(\d+)px"', s)
    rows.append((os.path.basename(f), int(w.group(1)) if w else 0, int(h.group(1)) if h else 0))

print('pages', len(rows), 'bad', bad)
print('svg width range', min(r[1] for r in rows), max(r[1] for r in rows))
print('svg height range', min(r[2] for r in rows), max(r[2] for r in rows))
for r in rows:
    if r[1] > 1200:
        print('wide', r)
