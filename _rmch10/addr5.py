import fitz
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)
for p in (698, 699, 700):
    t = doc[p].get_text("text")
    i = t.find("Table 18-")
    print(p+1, t[:200].replace("\n"," | ")[:100])
    j = t.find("CG(i)")
    print(t[j:j+1200].replace("\n"," | ")[:1200])
    print("-----")