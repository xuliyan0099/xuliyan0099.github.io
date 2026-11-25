import fitz, re
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)
print("=== p699 head ===")
print(doc[698].get_text("text")[:1100].replace("\n"," | "))
print("=== PMU page scan ===")
for p in range(700, 1000):
    t = doc[p].get_text("text")
    if "PMU_REG_CORE" in t or "PMU_MISC0" in t:
        for m in re.finditer(r"20C_8\d{3}", t):
            print(p+1, t[max(0,m.start()-70):m.start()+50].replace("\n"," | ")[:160])
            break