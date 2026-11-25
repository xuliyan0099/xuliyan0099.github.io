p = r"D:\Workspace\MainPage\imx6ull\rm\rm-data.js"
t = open(p, encoding="utf-8", newline="").read()

old = '''{ "n": 20, "zh": "ECSPI：主从、片选与 FIFO", "en": "Enhanced Configurable SPI", "pp": "791–820", "pages": 30, "pri": "read", "batch": 2,
          "line": "SPI 的四种模式、片选时序与 FIFO 突发，一次讲透。",
          "pts": ["CPOL/CPHA 与四模式、片选控制", "FIFO、突发长度与 DMA 触发"] }'''

new = '''{ "n": 20, "zh": "ECSPI：主从、片选与 FIFO", "en": "Enhanced Configurable SPI", "pp": "791–820", "pages": 30, "pri": "read", "batch": 2, "ready": true,
          "line": "四线全双工 + 双向 64 深 FIFO；四个基址 × 四条通道，配错一个位就不通。",
          "pts": ["定位：四根线、双向 64×32 FIFO、四路片选与四个基址",
                  "时钟：SCLK = ref ÷(PRE+1) ÷2^POST；60 M 的四个算例",
                  "寄存器：CONREG / CONFIGREG 位域与 STATREG 复位 0x3",
                  "时序：POL/PHA 四模式、SS_CTL 波形、SPI_RDY 与等待",
                  "流程与判据：EN/XCH/TC、RX 溢出，以及四路 SPI 的引脚冲突"] }'''

assert old in t, "entry 20 not found"
t = t.replace(old, new, 1)
open(p, "w", encoding="utf-8", newline="").write(t)
print("ok")
