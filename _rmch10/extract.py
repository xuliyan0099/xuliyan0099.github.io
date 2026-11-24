import fitz, os, sys, re

pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
out_dir = r"D:\Workspace\MainPage\_rmch10"
os.makedirs(out_dir, exist_ok=True)
doc = fitz.open(pdf)
parts = []
for p in range(344, 380):
    parts.append("===== PDF page %d =====" % (p + 1))
    parts.append(doc[p].get_text("text"))
text = "\n".join(parts)
with open(os.path.join(out_dir, "ch10.txt"), "w", encoding="utf-8") as f:
    f.write(text)
print("chars:", len(text))
print(text[:1200])
