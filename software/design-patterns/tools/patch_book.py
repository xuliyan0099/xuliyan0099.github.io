# -*- coding: utf-8 -*-
import pathlib

p = pathlib.Path(__file__).resolve().parent / "book.py"
t = p.read_text(encoding="utf-8")

OLD_ALL = 'ALL = [(p, c) for p in PARTS for c in p["chapters"]]'
NEW_ALL = '''from content_a import C as _CA
from content_b import C as _CB
from content_c import C as _CC
CONTENT = {}
CONTENT.update(_CA); CONTENT.update(_CB); CONTENT.update(_CC)

_SUB = {
 "2.1": "工厂按名字造产品", "2.2": "一族控件成套交付", "2.3": "四步施工再校验", "2.4": "克隆出独立副本", "2.5": "一个入口一份配置",
 "3.1": "方钉塞进圆孔", "3.2": "形状与渲染器解耦", "3.3": "枝与叶同一接口", "3.4": "一层只加一件事", "3.5": "一键开关家庭影院", "3.6": "一千棵树两份树型", "3.7": "缓存挡在磁盘前",
 "4.1": "客服逐级升级", "4.2": "编辑与撤销成对", "4.3": "表达式变成树", "4.4": "只暴露 next", "4.5": "消息经房间转发", "4.6": "改坏了退回快照", "4.7": "气温发布与订阅", "4.8": "非法状态转移被拒", "4.9": "排序算法即参数", "4.10": "骨架固定三步可换", "4.11": "统计搬出节点",
}
_SEC2 = {
 "2.1": "结构：客户端、工厂、两个产品", "2.2": "结构：一次交付整族控件", "2.3": "结构：步骤显式、交付前校验", "2.4": "结构：原型登记，用时克隆", "2.5": "结构：唯一入口与唯一实例",
 "3.1": "结构：旧接口、适配器、新零件", "3.2": "结构：两维各自抽象，一条引用", "3.3": "结构：枝递归、叶终止", "3.4": "结构：一层只包一对标签", "3.5": "结构：一个入口编排子系统", "3.6": "结构：共享内部状态，外部状态随行", "3.7": "结构：代理挡在真实对象前",
 "4.1": "结构：一条单向链，逐级升级", "4.2": "结构：调用者、命令、接收者", "4.3": "结构：运算符是节点，数字是叶子", "4.4": "结构：游标 + next", "4.5": "结构：所有消息穿过房间", "4.6": "结构：快照与恢复分离", "4.7": "结构：发布者只发事件", "4.8": "结构：状态决定合法转移", "4.9": "结构：上下文只持有策略", "4.10": "结构：骨架固定，三步可换", "4.11": "结构：accept 与 visit 双向分派",
}
for _p, _c in [(p, c) for p in PARTS for c in p["chapters"]]:
    if _c["n"] in _SUB:
        _c["s"] = _SUB[_c["n"]]
        _c["sec"] = ["问题：坏代码长什么样", _SEC2[_c["n"]], "两份实现：C 与 C++", "运行与演示", "C 与 C++ 对照", "代价与坑"]

ALL = [(p, c) for p in PARTS for c in p["chapters"]]'''
assert OLD_ALL in t
t = t.replace(OLD_ALL, NEW_ALL, 1)

OLD_MAIN = '''    for p, c in ALL:
        if c.get("old"):
            migrate_old(p, c)
        else:
            from content_new import CONTENT
            build_new(p, c, CONTENT[c["n"]])'''
NEW_MAIN = '''    for p, c in ALL:
        if c["n"] in ("1.1", "1.2"):
            migrate_old(p, c)
        else:
            build_new(p, c, CONTENT[c["n"]])'''
assert OLD_MAIN in t
t = t.replace(OLD_MAIN, NEW_MAIN, 1)

OLD_PIT = """    secs.append(section_shell(6, ch["sec"][5], f'<div class="prose"><ul>{pits}</ul></div>'))"""
NEW_PIT = """    ref = c.get("ref")
    ref_html = f'<p class="subh">参考教程：<a href="{ref}" target="_blank" rel="noopener">refactoringguru.cn</a></p>' if ref else ""
    secs.append(section_shell(6, ch["sec"][5], f'<div class="prose">{ref_html}<ul>{pits}</ul></div>'))"""
assert OLD_PIT in t
t = t.replace(OLD_PIT, NEW_PIT, 1)

OLD_DEMO = '''    if '<script src="../assets/dp-demo.js"></script>' not in text:
        text = text.replace('<script src="../assets/dp-nav.js"></script>', '<script src="../assets/dp-nav.js"></script>\\n<script src="../assets/dp-demo.js"></script>')'''
NEW_DEMO = '''    text = text.replace('<script src="../assets/dp-demo.js"></script>', '')
    if '</head>' in text:
        text = text.replace('</head>', '<script src="../assets/dp-demo.js"></script>\\n</head>', 1)'''
assert OLD_DEMO in t
t = t.replace(OLD_DEMO, NEW_DEMO, 1)

p.write_text(t, encoding="utf-8")
print("patched")
