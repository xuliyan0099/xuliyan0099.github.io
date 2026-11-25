import os, fitz, re

base = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料"
pdf = None
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".pdf") and "IMX6ULL" in f.upper() and "参考手册" in f:
            pdf = os.path.join(root, f)
doc = fitz.open(pdf)
for i in range(25, 130):
    t = doc[i].get_text("text")
    if "Ethernet" in t:
        lines = [l.strip() for l in t.splitlines() if l.strip()]
        for j, s in enumerate(lines):
            if "Ethernet" in s:
                print(i + 1, "||", " | ".join(lines[max(0, j - 3):j + 2])[:300])
