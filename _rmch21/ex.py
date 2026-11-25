import os, fitz

base = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料"
pdf = None
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".pdf") and "IMX6ULL" in f.upper() and "参考手册" in f:
            pdf = os.path.join(root, f)
doc = fitz.open(pdf)
out = []
for i in range(820, 884):   # 物理页 821-884
    out.append("\n===== PAGE %d =====\n" % (i + 1))
    out.append(doc[i].get_text("text"))
txt = "".join(out)
os.makedirs(r"D:\Workspace\MainPage\_rmch21", exist_ok=True)
open(r"D:\Workspace\MainPage\_rmch21\ch21.txt", "w", encoding="utf-8").write(txt)
print("chars", len(txt))
