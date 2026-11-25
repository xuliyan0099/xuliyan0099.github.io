import io, re

p = r"D:\Workspace\MainPage\imx6ull\rm\rm-data.js"
s = io.open(p, encoding="utf-8").read()

m = re.search(r'\{ "n": 22,.*?"pts": \[[^\]]*\] \}', s, re.S)
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
    "六个子单元：MAC/uDMA/FIFO/MDIO/PTP/MIB 的交接点",
    "基址 0x0218_8000 与常用寄存器偏移表",
    "ECR/RCR/TCR 四个必配位：ETHEREN、MII_MODE、RMII_MODE、FDEN",
    "MDIO 事务：MMFR 位域与 MSCR 的 2.5 MHz 上限",
    "32 字节描述符：R/E/L/W 位与环的 wrap",
    "十步初始化顺序与 EIR 中断位",
    "RMII 板级现实：KSZ8081、50 MHz 参考时钟、PHY 地址",
    "七条排查判据：内环回、link、ARP 三段法",
]
new = ('{ "n": 22, "zh": %s, "en": %s, "pp": %s, "pages": %s, "pri": %s, "batch": %s,\n'
       '"line": %s,\n'
       '"pts": [%s],\n'
       '"ready": true }') % (zh, en, pp, pages, pri, batch, line,
                             ", ".join('"%s"' % x for x in pts))

s = s[:m.start()] + new + s[m.end():]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("done")
print(new)
