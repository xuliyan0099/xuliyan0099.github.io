import fitz, os, re
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)
out = []
for p in range(380, 386):   # 物理页 381-386 -> 0-based 380..385
    out.append("===== PDF page %d =====" % (p + 1))
    out.append(doc[p].get_text("text"))
path = r"D:\Workspace\MainPage\_rmch11\ch11.txt"
os.makedirs(os.path.dirname(path), exist_ok=True)
open(path, "w", encoding="utf-8").write("\n".join(out))
print(len("\n".join(out)))
