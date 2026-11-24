import fitz, os
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)
out = []
for p in range(386, 390):
    out.append("===== PDF page %d =====" % (p + 1))
    out.append(doc[p].get_text("text"))
path = r"D:\Workspace\MainPage\_rmch12\ch12.txt"
os.makedirs(os.path.dirname(path), exist_ok=True)
open(path, "w", encoding="utf-8").write("\n".join(out))
print(len("\n".join(out)))
