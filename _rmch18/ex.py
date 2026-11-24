import os, io, fitz
base = r"D:\Workspace\IMX6ULL\00_Board_Resources"
target = None
for root, ds, fs in os.walk(base):
    for f in fs:
        if f == "IMX6ULL参考手册.pdf":
            target = os.path.join(root, f)
print("found:", target)
doc = fitz.open(target)
print("pages", doc.page_count)
out = io.StringIO()
for p in range(624, 750):
    out.write("\n===== PHYS PAGE %d =====\n" % (p + 1))
    out.write(doc[p].get_text("text"))
doc.close()
os.makedirs(r"D:\Workspace\MainPage\_rmch18", exist_ok=True)
open(r"D:\Workspace\MainPage\_rmch18\ch18.txt", "w", encoding="utf-8").write(out.getvalue())
print("chars", len(out.getvalue()))
