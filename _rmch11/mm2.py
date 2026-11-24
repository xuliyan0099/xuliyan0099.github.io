import fitz
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)
for p in range(168, 200):
    t = doc[p].get_text("text")
    for name in ["SJC", "DCP", "SNVS", "OCRAM", "ROMCP", "TZASC", "CSU"]:
        pass
    lines = [l.strip() for l in t.splitlines()]
    for i, l in enumerate(lines):
        if l in ("SJC", "DCP", "SNVS", "OCRAM", "ROMCP", "TZASC", "CSU", "CAAM", "AIPS-3", "AIPS-1"):
            print(p+1, l, "|", lines[max(0,i-2)], lines[max(0,i-1)], "->", lines[i+1] if i+1<len(lines) else "")
