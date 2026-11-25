import os, pymupdf, io
base = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料"
lines = []
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".pdf"):
            p = os.path.join(root, f)
            try:
                d = pymupdf.open(p)
                lines.append("%d\t%s" % (d.page_count, p))
            except Exception as e:
                lines.append("ERR\t%s\t%s" % (f, e))
with io.open(r"D:\Workspace\MainPage\_rmch34\probe.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))