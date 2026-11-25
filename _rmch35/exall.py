import pymupdf, os
base = r"D:\Workspace\MainPage\_rmch35"
pdf = open(os.path.join(base, "pdfpath.txt"), encoding="utf-8").read().strip()
d = pymupdf.open(pdf)
print("pages", d.page_count, "title", d.metadata.get("title"))
ranges = {36:(2377,2380),37:(2381,2434),38:(2435,2440),39:(2441,2472),40:(2473,2488),
          41:(2489,2964),42:(2965,3074),60:(4099,4116)}
for n,(a,b) in ranges.items():
    out = r"D:\Workspace\MainPage\_rmch%d" % n
    os.makedirs(out, exist_ok=True)
    buf = []
    for p in range(a-1, b):
        buf.append("\n===== PAGE %d =====\n" % (p+1))
        buf.append(d[p].get_text())
    txt = "".join(buf)
    open(os.path.join(out, "ch%d.txt" % n), "w", encoding="utf-8").write(txt)
    print(n, len(txt), b-a+1)