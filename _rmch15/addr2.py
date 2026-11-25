import fitz, re
pdf = r'D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf'
doc = fitz.open(pdf)
for pg in (176, 177):
    print('==== page', pg, '====')
    print(doc[pg - 1].get_text('text'))
