# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path(__file__).resolve().parent / "book.py"
t = p.read_text(encoding="utf-8")

OLD = 'from content_c import C as _CC'
NEW = '''from content_c import C as _CC
from prod_a import P as _PA
from prod_b import P as _PB
from prod_c import P as _PC
PROD = {}
PROD.update(_PA); PROD.update(_PB); PROD.update(_PC)'''
assert OLD in t
t = t.replace(OLD, NEW, 1)

OLD2 = '''        _c["sec"] = ["问题：坏代码长什么样", _SEC2[_c["n"]], "两份实现：C 与 C++", "运行与演示", "C 与 C++ 对照", "代价与坑"]'''
NEW2 = '''        _c["sec"] = ["问题：坏代码长什么样", _SEC2[_c["n"]], "两份实现：C 与 C++", "运行与演示", "C 与 C++ 对照", "代价与坑", "生产实例与 PlantUML"]'''
assert OLD2 in t
t = t.replace(OLD2, NEW2, 1)

OLD3 = '''    secs.append(section_shell(6, ch["sec"][5], f'<div class="prose">{ref_html}<ul>{pits}</ul></div>'))'''
NEW3 = '''    secs.append(section_shell(6, ch["sec"][5], f'<div class="prose">{ref_html}<ul>{pits}</ul></div>'))
    prod = PROD.get(ch["n"])
    if prod:
        kind = "class" if ("class " in prod["puml"] or "interface " in prod["puml"]) else ("state" if "-->" in prod["puml"] and "participant" not in prod["puml"] else "sequence")
        slug = "dp-" + ch["n"].replace(".", "-")
        cons = "".join(f"<li>{esc(x)}</li>" for x in prod["cons"])
        body7 = f\'\'\'
    <p class="subh">{esc(prod["title"])}</p>
    <div class="prose">
      {prod["lead"]}
      <h3 class="mini-h">生产约束</h3>
      <ul class="cons">{cons}</ul>
    </div>
    <div class="fig puml-fig">
      <div class="fig-h"><b>PlantUML · {kind}</b><span>plantuml.com 渲染</span></div>
      <div class="puml-shot"><img src="../assets/puml/{slug}.svg" alt="{esc(prod["title"])} 的 PlantUML 图" loading="lazy"></div>
    </div>
    <details class="puml-box"><summary>PlantUML 源码 · {slug}.puml</summary><pre><code>{esc(prod["puml"].strip())}</code></pre></details>
    \'\'\'
        secs.append(section_shell(7, "生产实例与 PlantUML", body7))'''
assert OLD3 in t
t = t.replace(OLD3, NEW3, 1)
p.write_text(t, encoding="utf-8")
print("patched")