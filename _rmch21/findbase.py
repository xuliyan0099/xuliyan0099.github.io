import os, re, fitz

base = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料"
pdf = None
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".pdf") and "IMX6ULL" in f.upper() and "参考手册" in f:
            pdf = os.path.join(root, f)
doc = fitz.open(pdf)
for i in range(185, 235):
    t = doc[i].get_text("text")
    if "EIM" in t and ("5000" in t or "0800" in t):
        print("PAGE", i + 1)
        for line in t.splitlines():
            s = line.strip()
            if "EIM" in s or "5000_0000" in s or "0800_0000" in s or "57FF" in s:
                print("   ", s)
