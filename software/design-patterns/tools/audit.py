import re, pathlib, book
root = pathlib.Path(__file__).resolve().parent.parent
bad_n = 0
for p, c in book.ALL:
    f = root / p["id"] / c["f"]
    t = f.read_text(encoding="utf-8")
    hs = re.findall(r'<h2><span class="n">\d+</span>.*?</h2>', t)
    hs = [re.sub(r"<[^>]+>", "", h).strip() for h in hs]
    hs = [re.sub(r"^\d+", "", h).strip() for h in hs]
    ok = hs == c["sec"]
    if not ok:
        bad_n += 1
    print("ok " if ok else "BAD", c["n"], "|", " / ".join(hs)[:80], "|| nav:", " / ".join(c["sec"])[:80])
print("mismatch", bad_n)
