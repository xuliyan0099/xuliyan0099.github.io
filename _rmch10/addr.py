import fitz, re
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)
hits = []
for p in range(620, 700):
    t = doc[p].get_text("text")
    for kw in ["CCM_CCGR0", "CCM_CCGR1", "CCM_CCR", "020C4068", "PMU_REG_CORE", "PMU_MISC0", "CCM_CLPCR"]:
        for m in re.finditer(kw, t):
            s = t[max(0, m.start()-80): m.start()+120].replace("\n", " | ")
            hits.append((p+1, kw, s))
for h in hits[:40]:
    print(h[0], h[1], h[2][:190])
print("total", len(hits))
