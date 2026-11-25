import os, pymupdf, io
base = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料"
pdf = None
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".pdf") and "IMX6ULL" in f.upper() and "参考手册" in f:
            pdf = os.path.join(root, f)
d = pymupdf.open(pdf)
log = ["count=%d pdf=%s" % (d.page_count, pdf)]
try:
    t = d[2130].get_text("text")
    log.append("ok 2130 len=%d" % len(t))
except Exception as e:
    log.append("ERR %r" % (e,))
    log.append("try 2135 -> %s" % (len(d[2135].get_text())))
with io.open(r"D:\Workspace\MainPage\_rmch34\probe2.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(log))