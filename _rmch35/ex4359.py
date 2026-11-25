import pymupdf, os
base = r"D:\Workspace\MainPage\_rmch35"
pdf = open(os.path.join(base, "pdfpath.txt"), encoding="utf-8").read().strip()
d = pymupdf.open(pdf)
ranges = {
    43:(3075,3090),
    44:(3091,3106),
    45:(3107,3144),
    46:(3145,3378),
    47:(3379,3414),
    48:(3415,3450),
    49:(3451,3464),
    50:(3465,3496),
    51:(3497,3528),
    52:(3529,3536),
    53:(3537,3558),
    54:(3559,3560),
    55:(3561,3640),
    56:(3641,3900),
    57:(3901,3946),
    58:(3947,4078),
    59:(4079,4098),
}
for n,(a,b) in ranges.items():
    out = r"D:\Workspace\MainPage\_rmch%d" % n
    os.makedirs(out, exist_ok=True)
    buf = []
    for p in range(a-1, b):
        buf.append("\n===== PAGE %d =====\n" % (p+1))
        buf.append(d[p].get_text())
    txt = "".join(buf)
    open(os.path.join(out, "ch%d.txt" % n), "w", encoding="utf-8").write(txt)
    print(n, len(txt), b-a+1)