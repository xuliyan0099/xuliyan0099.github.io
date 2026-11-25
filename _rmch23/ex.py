import os, pymupdf

base = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料"
pdf = None
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".pdf") and "IMX6ULL" in f.upper() and "参考手册" in f:
            pdf = os.path.join(root, f)
doc = pymupdf.open(pdf)
out = []
for i in range(1034, 1166):          # 0-based: pages 1035..1166
    out.append("===== PAGE %d =====" % (i + 1))
    out.append(doc[i].get_text("text"))
d = r"D:\Workspace\MainPage\_rmch23"
os.makedirs(d, exist_ok=True)
p = os.path.join(d, "ch23.txt")
with open(p, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out))
print(p, len("\n".join(out)))
