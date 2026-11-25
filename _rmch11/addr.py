import fitz, re
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)
keys = ["021C4000", "021C0000", "02288000", "021D8000", "020CC000", "021BC000"]
hits = {}
for p in range(158, 260):
    t = doc[p].get_text("text")
    for k in keys:
        if k in t:
            hits.setdefault(k, []).append(p + 1)
for k in keys:
    print(k, hits.get(k))
# CSU base line
for p in range(158, 260):
    t = doc[p].get_text("text")
    if "CSU" in t and "021C" in t:
        for line in t.splitlines():
            if "CSU" in line or "021C" in line:
                print(p+1, line.strip()[:80])
