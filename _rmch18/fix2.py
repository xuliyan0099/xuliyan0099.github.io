import re
p = r"D:\Workspace\MainPage\_rmch18\c18_tail.html"
t = open(p, encoding="utf-8").read()

old_head = "  head(80, 484, '所以这块板的 DVFS 只能降频；低功耗还有三个默认值坑');"
new_head = "  head(80, 508, '所以这块板的 DVFS 只能降频；低功耗还有三个默认值坑');"
assert old_head in t
t = t.replace(old_head, new_head)

ys_old = [518, 552, 586, 620, 654, 688, 722, 756]
ys_new = [542, 575, 608, 641, 674, 707, 740, 773]
lines = [
 '降频不降压只省动态功耗的一部分：待机电流不会因此掉一半，别把 6Q 的 DVFS 表往这块板上套。',
 '坑一：CLPCR 的 LPM[1:0] 复位是 01（WAIT），不是 RUN；想测 RUN 得先写 00。',
 '坑二：VSTBY(bit8) 不置，进 STOP 永远不拉 PMIC_STBY_REQ，电源侧看不到任何动作。',
 '坑三：BYPASS_MMDC_CH0(bit19) 手册要求必须写 1 —— 这颗 MMDC_CH0 根本没接。',
 '进 STOP：先关外设门 → LPM=10 → WFI；出来要等 STBY_COUNT 个 CKIL 与 OSCNT 计完。',
 '出 STOP 慢 5 ms 是正常的：OSCNT 128 个 32 k 周期约 3.9 ms，再加电源从待机电压爬回来。',
 'Linux 侧：clk_summary 里 pll1_sw / periphclk / ahb / ipg / perclk 五个数一对，就知道树对不对。',
 '排查顺序固定：COSC_READY → PLL LOCK → CDHIPR → 根频率 → 门 → 引脚复用。按这个顺序走，不会绕圈。',
]
for oy, ny, s in zip(ys_old, ys_new, lines):
    old = "txt(scene, 80, %d, '%s', 't20w');" % (oy, s)
    new = "txt(scene, 80, %d, '%s', 't20w');" % (ny, s)
    assert old in t, s
    t = t.replace(old, new)

open(p, "w", encoding="utf-8", newline="").write(t)
print("patched")
