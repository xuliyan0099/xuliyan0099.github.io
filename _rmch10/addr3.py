import fitz, re
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)
for p in range(695, 702):
    t = doc[p].get_text("text")
    for kw in ["CG(i)", "clock is off", "CG0", "all modes"]:
        i = t.find(kw)
        if i >= 0:
            print("p", p+1, kw, "->", t[i:i+300].replace("\n"," | "))
            break