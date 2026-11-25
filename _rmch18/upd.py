import re, json
p = r"D:\Workspace\MainPage\imx6ull\rm\rm-data.js"
t = open(p, encoding="utf-8").read()

start = t.find('{ "n": 18,')
assert start > 0
end = t.find('{ "n": 27,')
seg = t[start:end]

newpts = ('"pts": ["两个源与七颗 PLL：谁给谁当母体", "PLL / PFD 的公式与 0x020C_8000 段寄存器", '
          '"CBCDR / CACCR / CSCMR1：528→264→132→66 是怎么分出来的", '
          '"CCGR0–6 的 112 个门与 LPCG 四输入与门", '
          '"改频顺序：step_clk、PLL 重锁、CDHIPR 握手", '
          '"实测：读三个寄存器 + CLKO 探头 + 这块板只能降频"]')

seg2 = re.sub(r'"pts": \[[^\]]*\]', newpts, seg, count=1)
t = t[:start] + seg2 + t[end:]
open(p, "w", encoding="utf-8", newline="").write(t)
print("pts updated", 'ready": true' in seg2)
