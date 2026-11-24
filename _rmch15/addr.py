import fitz, re
pdf = r'D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf'
doc = fitz.open(pdf)
for i in range(170, 186):
    t = doc[i].get_text('text')
    for ln in t.split('\n'):
        if re.search(r'\b(APBH|GPMI|BCH|APBX|EPDC|LCDIF)\b', ln):
            print(i + 1, '|', ln.strip())
