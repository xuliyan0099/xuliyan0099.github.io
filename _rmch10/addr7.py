import fitz, re
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)
for p in range(700, 900):
    t = doc[p].get_text("text")
    if "PMU" in t and "20C_8" in t:
        m = re.search(r"20C_8\d{3}", t)
        print(p+1, t[max(0,m.start()-120):m.start()+60].replace("\n"," | ")[:200])