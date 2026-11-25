import pymupdf
p = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、IMX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = pymupdf.open(p)
out = []
for i in range(2202, 2376):
    out.append("===== PAGE %d =====" % (i + 1))
    out.append(doc[i].get_text("text"))
d = r"D:\Workspace\MainPage\_rmch35"
op = d + r"\ch35.txt"
txt = "\n".join(out)
with open(op, "w", encoding="utf-8") as fh:
    fh.write(txt)
print(op, len(txt))
