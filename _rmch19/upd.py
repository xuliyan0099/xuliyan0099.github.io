p = r"D:\Workspace\MainPage\imx6ull\rm\rm-data.js"
t = open(p, encoding="utf-8", newline="").read()

old = '''{ "n": 19, "zh": "CMOS 摄像头接口 CSI", "en": "CMOS Sensor Interface", "pp": "751–790", "pages": 40, "pri": "read", "batch": 4,
          "line": "并行摄像头的打包方式、同步信号与出图地址。",
          "pts": ["8/16 位数据打包与 RGB/YUV 排列", "CCIR656 内嵌同步与 DMA 出图"] }'''

new = '''{ "n": 19, "zh": "CMOS 摄像头接口 CSI", "en": "CMOS Sensor Interface", "pp": "751–790", "pages": 40, "pri": "read", "batch": 4, "ready": true,
          "line": "没有 IPU 的 6ULL 怎么收图：位宽接法、打包字节序、双缓冲 DMA。",
          "pts": ["定位：3 个 FIFO + 2 条 DMA，不做 debayer 与缩放",
                  "接线：8 位接 DATA[9:2]；专用 pad 只有 DATA00–07",
                  "寄存器 0x021C_4000 段；CSICR1 复位 0x4000_0800 的两位",
                  "DMA 四参数与 stride：FB1/FB2、行宽−图像宽、宽高的单位",
                  "启动七步 + CSISR 判据 + CR19 水位诊断"] }'''

assert old in t, "entry 19 not found"
t = t.replace(old, new, 1)
open(p, "w", encoding="utf-8", newline="").write(t)
print("ok")
