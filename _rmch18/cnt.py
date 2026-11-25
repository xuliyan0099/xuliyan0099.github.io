import re
for f in [r"D:\Workspace\MainPage\imx6ull\rm\c17.html", r"D:\Workspace\MainPage\imx6ull\rm\c18.html"]:
    t = open(f, encoding="utf-8").read()
    ms = re.findall(r'<span class="bd-reading-(?:name|value)">[^<]*</span>', t)
    print(f, len(ms))
    for m in ms:
        print("   ", m)
