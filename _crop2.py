import fitz, os
base = r"D:\Workspace\IMX6ULL\00_Board_Resources\【正点原子】阿尔法Linux开发板（A盘）-基础资料\02、开发板原理图"
out = r"D:\Workspace\MainPage\imx6ull\assets\img\sch"
core = fitz.open(base+r"\IMX6ULL_CORE_V2.0(核心板原理图).pdf")
mini = fitz.open(base+r"\IMX6ULL_MINI_V2.2(Mini底板原理图).pdf")
jobs = [
 (core,2,"core_p3_ddr.png",(50,45,320,480)),
 (core,2,"core_p3_clk.png",(655,140,800,285)),
 (core,3,"core_p4_emmc.png",(20,40,300,300)),
 (core,3,"core_p4_nand.png",(18,330,420,552)),
 (core,4,"core_p5_lcd.png",(78,110,400,405)),
 (core,4,"core_p5_net.png",(265,135,505,300)),
 (core,5,"core_p6_ctrl.png",(18,40,250,365)),
 (core,5,"core_p6_xtal.png",(330,445,575,552)),
 (core,6,"core_p7_boot.png",(535,50,800,485)),
 (core,7,"core_p8_pin.png",(195,140,725,400)),
 (mini,1,"mini_p2_can.png",(20,40,300,185)),
 (mini,1,"mini_p2_485.png",(18,330,300,560)),
 (mini,2,"mini_p3_phy.png",(95,58,405,295)),
 (mini,2,"mini_p3_rj45.png",(475,115,795,235)),
 (mini,3,"mini_p4_dcdc5.png",(140,58,330,185)),
 (mini,3,"mini_p4_dcdc3.png",(365,58,570,175)),
 (mini,3,"mini_p4_usb.png",(95,238,430,405)),
]
for doc,pi,name,clip in jobs:
    p=doc[pi]; r=fitz.Rect(*clip)
    pix=p.get_pixmap(dpi=300, clip=r, alpha=False, colorspace=fitz.csRGB)
    pix.save(os.path.join(out,name))
    print(name, pix.width, pix.height)
