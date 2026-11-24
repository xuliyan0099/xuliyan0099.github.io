import pathlib
root = pathlib.Path(r"D:\Workspace\MainPage\software\design-patterns")
bad = []
for p in sorted(root.glob("p[1-4]/*.html")):
    s = p.read_text(encoding="utf-8")
    sec = s.count('<section class="sec"')
    cards = s.count('class="codecard"')
    runs = s.count('<div class="run">')
    refs = s.count("参考教程")
    if (sec, cards, runs) != (7, 2, 2):
        bad.append((str(p.name), sec, cards, runs))
    if p.parent.name != "p1" and refs < 1:
        bad.append((str(p.parent.name) + "/" + p.name, "no ref"))
print("bad", bad)
idx = (root / "index.html").read_text(encoding="utf-8")
print("chrows", idx.count('class="chrow"'))
