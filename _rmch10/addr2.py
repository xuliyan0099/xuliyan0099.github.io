import fitz, re
pdf = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\07、I.MX6U参考资料\02、I.MX6ULL芯片资料\IMX6ULL参考手册.pdf"
doc = fitz.open(pdf)

print("=== CG semantics p699-700 ===")
for p in (698, 699):
    t = doc[p].get_text("text")
    i = t.find("These bits are used to turn on/off")
    print(p + 1, t[i:i+900].replace("\n", " | ") if i >= 0 else "no")

print("=== PMU regs ===")
pat = re.compile(r"(PMU_(REG_CORE|MISC0|MISC1|MISC2|REG_1P1|REG_2P5|REG_SOC))\b")
seen = set()
for p in range(760, 900):
    t = doc[p].get_text("text")
    m = re.search(r"Module Memory Map[\s\S]{0,4000}", t)
    for mm in re.finditer(r"20C_8\d{3}", t):
        s = t[max(0, mm.start()-90): mm.start()+70].replace("\n", " | ")
        key = s[:90]
        if key not in seen:
            seen.add(key)
            print(p + 1, s[:170])
            break
