import io, re

p = r"D:\Workspace\MainPage\imx6ull\rm\rm-data.js"
s = io.open(p, encoding="utf-8").read()

m = re.search(r'\{ "n": 21,.*?"pts": \[[^\]]*\] \}', s, re.S)
print("found:", bool(m))
if not m:
    raise SystemExit(1)
blk = m.group(0)

def grab(key):
    mm = re.search(r'"%s": (.*?)(?:,|\n)' % key, blk)
    return mm.group(1).strip().strip(",")

zh = grab("zh"); en = grab("en"); pp = grab("pp")
pages = grab("pages"); pri = grab("pri"); batch = grab("batch")
line = re.search(r'"line": (.*)', blk).group(1).strip().rstrip(",")

pts = [
    "六片选与 128 MB 窗口怎么切",
    "基址 0x021B_8000 与每片选 0x18 步长的寄存器地图",
    "GCR1 位域：DSZ 口宽与 AUS 地址移位",
    "异步读写：RWSC/WWSC 拍数与 133 MHz 换算",
    "同步突发与页读：BCLK/BL/APR",
    "七步启动与五条故障判据",
    "板级现实：EIM 脚被 NAND 与 CSI 借走",
]
new = ('{ "n": 21, "zh": %s, "en": %s, "pp": %s, "pages": %s, "pri": %s, "batch": %s,\n'
       '"line": %s,\n'
       '"pts": [%s],\n'
       '"ready": true }') % (zh, en, pp, pages, pri, batch, line,
                             ", ".join('"%s"' % x for x in pts))

s = s[:m.start()] + new + s[m.end():]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("done", len(s))
print(new)
