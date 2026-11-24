import fitz, json, re
base = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\02、开发板原理图"
for tag,fn in [("core",r"IMX6ULL_CORE_V2.0(核心板原理图).pdf")]:
    d=fitz.open(base+"\\"+fn)
    for i,p in enumerate(d):
        print("="*20,"PAGE",i+1)
        b=p.get_text("blocks")
        b.sort(key=lambda x:(round(x[1]/6),x[0]))
        for x in b:
            t=" ".join(x[4].split())
            if t: print(f"[{x[0]:.0f},{x[1]:.0f}] {t}")
