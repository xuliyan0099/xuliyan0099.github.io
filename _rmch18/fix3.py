import re, io

def add_next(path, next_file, next_label):
    t = open(path, encoding="utf-8").read()
    m = re.search(r'<a class="bd-btn" href="c\d+\.html" style="text-decoration:none">← RM\d+</a>', t)
    if not m:
        print("NO PREV", path); return
    ins = m.group(0) + '\n        <a class="bd-btn" href="%s" style="text-decoration:none">%s →</a>' % (next_file, next_label)
    t = t[:m.start()] + ins + t[m.end():]
    open(path, "w", encoding="utf-8", newline="").write(t)
    print("next added", path)

def soften(path, old, new):
    t = open(path, encoding="utf-8").read()
    if old not in t:
        print("MISS", old[:20]); return
    t = t.replace(old, new)
    open(path, "w", encoding="utf-8", newline="").write(t)
    print("text fixed", path)

base = r"D:\Workspace\MainPage\imx6ull\rm\\"
add_next(base + "c15.html", "c16.html", "RM16")
add_next(base + "c16.html", "c17.html", "RM17")
add_next(base + "c17.html", "c18.html", "RM18")

soften(r"D:\Workspace\MainPage\_rmch18\c18_tail.html",
       "'CCM 与 SRC 没有门，永远在跑'",
       "'CCM 与 SRC 的 IPG 时钟没有门，永远在跑'")
