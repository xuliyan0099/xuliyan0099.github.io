import fitz
pdf = r'D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf'
out = r'D:\Workspace\MainPage\_rmch16\ch16.txt'
doc = fitz.open(pdf)
parts = []
for i in range(504, 562):
    parts.append('\n===== PDF PAGE %d =====\n' % (i + 1))
    parts.append(doc[i].get_text('text'))
txt = ''.join(parts)
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(txt)
print(len(txt))
