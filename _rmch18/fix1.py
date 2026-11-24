p = r"D:\Workspace\MainPage\_rmch18\c18_tail.html"
t = open(p, encoding="utf-8").read()
t = t.replace("① CCSR[3]=1：切到 step_clk", "① CCSR[2]=1：切到 step_clk")
t = t.replace("⑥ CCSR[3]=0：切回 pll1_main", "⑥ CCSR[2]=0：切回 pll1_main")
t = t.replace("CCSR[7:3] SECONDARY：0 = PFD2 400", "CCSR[3] SECONDARY：0 = PFD2 400")
open(p, "w", encoding="utf-8", newline="").write(t)
print("ok", t.count("CCSR[2]"), t.count("CCSR[3]"))
