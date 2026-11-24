import fitz, os
pdf = r'D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf'
out = r'D:\Workspace\MainPage\_rmch15\ch15.txt'
doc = fitz.open(pdf)
parts = []
for i in range(464, 504):   # physical pages 465..504
    p = doc[i]
    parts.append('\n===== PDF PAGE %d =====\n' % (i + 1))
    parts.append(p.get_text('text'))
txt = ''.join(parts)
with open(out, 'w', encoding='utf-8') as f:
    f.write(txt)
print(len(txt))
