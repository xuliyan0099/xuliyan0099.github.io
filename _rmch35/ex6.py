import pymupdf
pp = open(r"D:\Workspace\MainPage\_rmch35\pdfpath.txt", encoding="utf-8").read().strip()
doc = pymupdf.open(pp)
out = []
for i in range(2202, 2376):
    out.append("===== PAGE %d =====" % (i + 1))
    out.append(doc[i].get_text("text"))
op = r"D:\Workspace\MainPage\_rmch35\ch35.txt"
txt = "\n".join(out)
open(op, "w", encoding="utf-8").write(txt)
print(doc.page_count, len(txt))