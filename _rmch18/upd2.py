import re
p = r"D:\Workspace\MainPage\imx6ull\rm\rm-data.js"
t = open(p, encoding="utf-8").read()

NEW = {
 15: ["APBH 桥：AHB→APB 通路 + 16 通道 DMA + 向量中断",
      "0x0180_4000 的通道寄存器与 CCW 的四个字",
      "COMMAND 的方向码：DMA_WRITE 是「写进内存」",
      "8 位信号量：INCREMENT 与 PHORE 的启动两步"],
 16: ["三对通道 A/B/C，合计不超过 10 个",
      "Q6.26 定点：44.1k↔48k 的两个常数",
      "FIFO 64 样本 / 阈值 32；ASRCCR 指示当前通道",
      "ASR76K 与 ASR56K：给 200 MHz 处理时钟的标尺"],
 17: ["四段流水：syndrome → KES → Chien → 修正",
      "页布局七个参数与 4K+218 的 spare 预算",
      "DATA0_SIZE 是「4 字节字数」，不是字节数",
      "M2M 环路：编码 → 翻一位 → 解码的三条判据"],
}
for n, pts in NEW.items():
    s = t.find('{ "n": %d,' % n)
    e = t.find('{ "n": %d,' % (n + 1))
    assert s > 0 and e > s
    seg = t[s:e]
    newpts = '"pts": [' + ', '.join('"%s"' % x for x in pts) + ']'
    seg2 = re.sub(r'"pts": \[[^\]]*\]', newpts, seg, count=1)
    t = t[:s] + seg2 + t[e:]
    print("n=%d updated" % n)

open(p, "w", encoding="utf-8", newline="").write(t)
