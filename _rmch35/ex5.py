import os, pymupdf
base = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、IMX6ULL芯片资料"
hits = []
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".pdf") and "IMX6ULL" in f.upper() and "参考手册" in f:
            hits.append(os.path.join(root, f))
print("hits", len(hits))
for h in hits:
    d = pymupdf.open(h)
    print(d.page_count, h)