# -*- coding: utf-8 -*-
"""设计模式全书构建：4 篇 25 章，篇目录 + p1..p4 章节页 + 整书左栏目录。

- 已有页面：从旧路径迁移，保留正文/代码/演示，只重写外壳与章号。
- 新增页面：由 content 字典 + 本文件的模板生成。
"""
import html
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SRC = ROOT / "src"
OUT = SRC / "out"

PARTS = [
    {
        "id": "p1", "no": "一", "title": "基础", "sub": "先把多态讲透",
        "intro": "两个模式之前必须先讲清楚一件事：C 里也能做多态。第一篇只有两章——先给一条“按症状找模式”的路，再把虚表拆开，让后面的每个模式都落在这套机制上。",
        "chapters": [
            {"k": 1, "n": "1.1", "t": "导读：为什么用模式", "en": "HOW TO READ", "s": "按症状找，不按名字背", "min": 15, "f": "c01.html", "old": "p1/c01.html",
             "sec": ["先按症状找，别按名字背", "三条读法", "经典出处与本节的取舍"]},
            {"k": 2, "n": "1.2", "t": "C 也能面向对象", "en": "VTABLE", "s": "手工虚表与三步分派", "min": 25, "f": "c02.html", "old": "p1/c02.html",
             "sec": ["问题：同一段代码，两种形状", "结构：对象里只有一个指针是真的“类型信息”", "两份实现：C 的手工虚表 vs C++ 的 virtual", "单步看一次分派", "四个零件，两种语言", "代价与坑"]},
        ],
    },
    {
        "id": "p2", "no": "二", "title": "创建型", "sub": "对象怎么造，造几份",
        "intro": "创建型回答的是“对象从哪来、来几份”。工厂方法把按名字造对象收进注册表，抽象工厂保证一套零件同代，建造者把多步拼装变成可检查的流程，原型用克隆代替重复初始化，单例把唯一入口守住。",
        "chapters": [
            {"k": 1, "n": "2.1", "t": "工厂方法模式", "en": "FACTORY METHOD", "s": "注册表取驱动", "min": 30, "f": "c01.html", "old": "p3/c02.html",
             "sec": ["问题：新增一个型号就要改 switch", "结构：一张表、两个方向", "两份实现", "按名字取驱动，包括一个不存在的名字", "C 与 C++：一张表，两种造法", "代价与坑"]},
            {"k": 2, "n": "2.2", "t": "抽象工厂模式", "en": "ABSTRACT FACTORY", "s": "一代零件成套交付", "min": 30, "f": "c02.html",
             "sec": ["问题：每个车型自己配零件，配错代", "结构：家族一次交付两个零件", "两份实现", "换一个家族，看零件是否成套", "C 与 C++：两种“成套”", "代价与坑"]},
            {"k": 3, "n": "2.3", "t": "建造者模式", "en": "BUILDER", "s": "把拼帧拆成步骤", "min": 28, "f": "c03.html",
             "sec": ["问题：一帧报文七八个字段，顺序全靠记", "结构：步骤可查、成品只交付一次", "两份实现", "一步一步拼一帧", "C 与 C++：两种链式", "代价与坑"]},
            {"k": 4, "n": "2.4", "t": "原型模式", "en": "PROTOTYPE", "s": "克隆配置，不动原型", "min": 28, "f": "c04.html",
             "sec": ["问题：配置对象到处复制，改一份污染一片", "结构：原型登记，用时克隆", "两份实现", "克隆两份，只改其中一份", "C 与 C++：深拷贝归谁", "代价与坑"]},
            {"k": 5, "n": "2.5", "t": "单例模式", "en": "SINGLETON", "s": "一个入口，一个对象", "min": 28, "f": "c05.html", "old": "p3/c03.html",
             "sec": ["问题：要么到处传，要么到处复制", "结构：一个入口，一个对象", "两份实现", "点三次“取实例”，看初始化次数", "C 与 C++：同一份唯一，两种保证", "代价与坑"]},
        ],
    },
    {
        "id": "p3", "no": "三", "title": "结构型", "sub": "对象怎么接、怎么叠",
        "intro": "结构型管的是“对象之间的接线”。适配器翻译接口，桥接把两维拆开，组合把树压成同一接口，装饰往链上加层，外观收口子系统，享元共享不变部分，代理挡在真实对象前面。",
        "chapters": [
            {"k": 1, "n": "3.1", "t": "适配器模式", "en": "ADAPTER", "s": "两种传感器接同一接口", "min": 28, "f": "c01.html", "old": "p3/c01.html",
             "sec": ["问题：差异会一路渗到业务层", "结构：目标接口在前，适配器在中间", "两份实现", "改原始值，看适配器怎么翻译", "C 与 C++：同一层翻译，两种代价", "代价与坑"]},
            {"k": 2, "n": "3.2", "t": "桥接模式", "en": "BRIDGE", "s": "协议与物理层各管各的", "min": 28, "f": "c02.html",
             "sec": ["问题：协议 × 物理层，组合爆炸", "结构：两维各自抽象，中间只连一条线", "两份实现", "四种组合，只换一侧", "C 与 C++：两种解耦", "代价与坑"]},
            {"k": 3, "n": "3.3", "t": "组合模式", "en": "COMPOSITE", "s": "枝和叶同一接口", "min": 28, "f": "c03.html",
             "sec": ["问题：树形结构，遍历代码越写越像", "结构：枝和叶同一接口", "两份实现", "自检树从根跑到叶", "C 与 C++：谁管孩子", "代价与坑"]},
            {"k": 4, "n": "3.4", "t": "装饰器模式", "en": "DECORATOR", "s": "一层只加一件事", "min": 28, "f": "c04.html",
             "sec": ["问题：每加一个处理就复制一遍读数函数", "结构：一层只加一件事", "两份实现", "换顺序，看结果怎么变", "C 与 C++：链的所有权", "代价与坑"]},
            {"k": 5, "n": "3.5", "t": "外观模式", "en": "FACADE", "s": "上电五步收成一个入口", "min": 26, "f": "c05.html",
             "sec": ["问题：上电五步，每个调用方都背一遍", "结构：一个入口，内部仍可单测", "两份实现", "失败时怎么回滚", "C 与 C++：入口的边界", "代价与坑"]},
            {"k": 6, "n": "3.6", "t": "享元模式", "en": "FLYWEIGHT", "s": "一千个信号，八份描述", "min": 30, "f": "c06.html",
             "sec": ["问题：一千个信号，一千份单位描述", "结构：内部状态共享，外部状态随行", "两份实现", "一千个句柄，八份对象", "C 与 C++：共享的寿命", "代价与坑"]},
            {"k": 7, "n": "3.7", "t": "代理模式", "en": "PROXY", "s": "缓存挡在真存储前", "min": 28, "f": "c07.html",
             "sec": ["问题：每次都打底层，慢且暴露细节", "结构：代理挡在前面", "两份实现", "读两次、写一次，看谁真的下去", "C 与 C++：代理的透明性", "代价与坑"]},
        ],
    },
    {
        "id": "p4", "no": "四", "title": "行为型", "sub": "谁在什么时候做什么",
        "intro": "行为型管的是“流程与责任怎么分”。职责链决定谁处理，命令把动作变成对象，解释器把条件变成树，迭代器藏起存储，中介者收掉两两直连，备忘录留下退路，观察者解耦通知，状态与策略换掉分支，模板方法固定骨架，访问者把统计搬出节点。",
        "chapters": [
            {"k": 1, "n": "4.1", "t": "职责链模式", "en": "CHAIN OF RESPONSIBILITY", "s": "四道关，谁处理谁负责", "min": 28, "f": "c01.html", "old": "p2/c05.html",
             "sec": ["问题：嵌套 if 会越写越深", "结构：一条单向链，四道关", "两份实现", "发一帧，看它死在哪一节", "C 与 C++：谁负责“记得转 next”", "代价与坑"]},
            {"k": 2, "n": "4.2", "t": "命令模式", "en": "COMMAND", "s": "队列与撤销", "min": 30, "f": "c02.html", "old": "p2/c04.html",
             "sec": ["问题：直接调用，就没有“以后”和“回退”", "结构：调用者、命令、接收者", "两份实现", "自己排一次队，再撤两次", "C 与 C++：同一套队列，两种所有权", "代价与坑"]},
            {"k": 3, "n": "4.3", "t": "解释器模式", "en": "INTERPRETER", "s": "诊断条件变成表达式树", "min": 30, "f": "c03.html",
             "sec": ["问题：诊断条件写死在 if 里", "结构：表达式变成树", "两份实现", "三组输入，同一棵树", "C 与 C++：树的归属", "代价与坑"]},
            {"k": 4, "n": "4.4", "t": "迭代器模式", "en": "ITERATOR", "s": "只暴露 next()", "min": 28, "f": "c04.html",
             "sec": ["问题：调用方直接摸数组，换存储就崩", "结构：只暴露 next()", "两份实现", "遍历时跳过无效项", "C 与 C++：迭代器的边界", "代价与坑"]},
            {"k": 5, "n": "4.5", "t": "中介者模式", "en": "MEDIATOR", "s": "所有消息过总线", "min": 28, "f": "c05.html",
             "sec": ["问题：N 个模块两两直连，N² 条线", "结构：所有消息过总线", "两份实现", "三条消息，看谁被通知", "C 与 C++：谁持有谁", "代价与坑"]},
            {"k": 6, "n": "4.6", "t": "备忘录模式", "en": "MEMENTO", "s": "调参之前留一份快照", "min": 26, "f": "c06.html",
             "sec": ["问题：调参调坏了，没有退路", "结构：快照与恢复分开", "两份实现", "改三次，退回第一次", "C 与 C++：快照的可见性", "代价与坑"]},
            {"k": 7, "n": "4.7", "t": "观察者模式", "en": "OBSERVER", "s": "通知名单解耦", "min": 32, "f": "c07.html", "old": "p2/c02.html",
             "sec": ["问题：通知名单被焊死在采样函数里", "结构：发布者只发事件，订阅者各自处理", "两份实现：一份故意先写错", "亲手踩一次“通知中退订”", "同一组角色，两种写法", "代价与坑"]},
            {"k": 8, "n": "4.8", "t": "状态模式", "en": "STATE", "s": "转移表拒绝非法", "min": 30, "f": "c08.html", "old": "p2/c03.html",
             "sec": ["问题：switch 里再套 if，非法组合没人管", "结构：五个状态，十二种合法走法", "两份实现", "点事件，看状态怎么走、怎么被拒", "C 与 C++：同一张表，两种摆放", "代价与坑"]},
            {"k": 9, "n": "4.9", "t": "策略模式", "en": "STRATEGY", "s": "三种 CAN 调度", "min": 30, "f": "c09.html", "old": "p2/c01.html",
             "sec": ["问题：三种规则堆进同一个循环", "结构：上下文只持有一个“会算下一步”的东西", "两份实现", "把队列交给不同策略", "同一组角色，两种写法", "代价与坑"]},
            {"k": 10, "n": "4.10", "t": "模板方法模式", "en": "TEMPLATE METHOD", "s": "骨架固定，步骤可换", "min": 28, "f": "c10.html",
             "sec": ["问题：自检流程抄了四遍，顺序还不一致", "结构：骨架固定，步骤可换", "两份实现", "跑两个变体，看哪步失败", "C 与 C++：谁定义骨架", "代价与坑"]},
            {"k": 11, "n": "4.11", "t": "访问者模式", "en": "VISITOR", "s": "统计逻辑搬出节点", "min": 30, "f": "c11.html",
             "sec": ["问题：统计逻辑散落在每个节点", "结构：accept 与 visit 双向分派", "两份实现", "四个节点，一次统计", "C 与 C++：分派的代价", "代价与坑"]},
        ],
    },
]

ALL = [(p, c) for p in PARTS for c in p["chapters"]]
TOTAL_MIN = sum(c["min"] for _, c in ALL)


def esc(s):
    return html.escape(s, quote=False)


def read(p):
    return pathlib.Path(p).read_text(encoding="utf-8-sig")


def write(p, s):
    pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(p).write_text(s, encoding="utf-8", newline="\n")


# ---------------- 数据文件 ----------------

def dump_data():
    out = ["/* 设计模式全书 · 四篇 25 章。章号 = 篇号.章序。 */", "window.DP_PARTS = ["]
    for p in PARTS:
        out.append("  {")
        out.append(f"    id: '{p['id']}', no: '{p['no']}', title: '{p['title']}', sub: '{p['sub']}',")
        out.append(f"    intro: {js_str(p['intro'])},")
        out.append("    chapters: [")
        for c in p["chapters"]:
            secs = ", ".join(js_str(x) for x in c["sec"])
            out.append(
                f"      {{ n: '{c['n']}', t: '{c['t']}', s: '{c['s']}', min: {c['min']}, f: '{c['f']}', sec: [{secs}] }},"
            )
        out.append("    ]")
        out.append("  },")
    out.append("];")
    write(ASSETS / "dp-data.js", "\n".join(out) + "\n")


def js_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


# ---------------- 左栏整书目录 ----------------

NAV_JS = r"""/* 设计模式全书 · 左栏整书目录：四篇 25 章全部列出，当前章展开小节 */
(function () {
  'use strict';

  function curFile() {
    var seg = location.pathname.split('/');
    var f = seg[seg.length - 1];
    return f && f.indexOf('.html') > 0 ? f : 'index.html';
  }
  function curPart() {
    var seg = location.pathname.split('/');
    return seg.length > 1 ? seg[seg.length - 2] : '';
  }
  function hashPart() {
    var h = location.hash.replace('#', '');
    return h === 'p1' || h === 'p2' || h === 'p3' || h === 'p4' ? h : '';
  }

  window.dpNav = function (partId) {
    var parts = window.DP_PARTS || [];
    if (!parts.length) return;

    var file = curFile();
    var pid = partId || curPart() || hashPart();
    var active = null;
    parts.forEach(function (p) {
      p.chapters.forEach(function (c) { if (p.id === pid && c.f === file) active = c; });
    });

    var head = document.getElementById('sideHead');
    if (head) head.innerHTML = '设计模式全书 · 25 章<label for="navChk" class="nav-x" aria-label="收起目录">✕</label>';

    var list = document.getElementById('sideList');
    if (list) {
      list.innerHTML = '';
      parts.forEach(function (p) {
        var ph = document.createElement('li');
        ph.className = 'part-h';
        var pidx = 'index.html#' + p.id;
        ph.innerHTML = '<a href="' + (file === 'index.html' ? pidx : '../index.html#' + p.id) + '">' +
          '篇' + p.no + '<b>' + p.title + '</b><i>' + p.chapters.length + '</i></a>';
        list.appendChild(ph);

        p.chapters.forEach(function (c) {
          var li = document.createElement('li');
          var a = document.createElement('a');
          a.href = (p.id === pid && file !== 'index.html') ? c.f : '../' + p.id + '/' + c.f;
          if (file === 'index.html') a.href = p.id + '/' + c.f;
          a.innerHTML = '<span class="no">' + c.n + '</span><span>' + c.t +
            '<span class="sub">' + c.s + '</span></span>';
          var isActive = active && c === active;
          if (isActive) a.className = 'active';
          li.appendChild(a);
          if (isActive) {
            var sub = document.createElement('ol');
            sub.className = 'side-sub';
            c.sec.forEach(function (t, i) {
              var sli = document.createElement('li');
              var sa = document.createElement('a');
              sa.href = '#s' + (i + 1);
              sa.innerHTML = '<i>' + ('0' + (i + 1)).slice(-2) + '</i>' + t;
              sli.appendChild(sa);
              sub.appendChild(sli);
            });
            li.appendChild(sub);
          }
          list.appendChild(li);
        });
      });
    }

    var flat = [];
    parts.forEach(function (p) { p.chapters.forEach(function (c) { flat.push({ pid: p.id, n: c.n, f: c.f, t: c.t }); }); });
    var gi = -1;
    flat.forEach(function (c, i) { if (c.pid === pid && c.f === file) gi = i; });
    var prev = gi > 0 ? flat[gi - 1] : null;
    var next = gi > -1 && gi < flat.length - 1 ? flat[gi + 1] : null;

    var vol = document.getElementById('volNav');
    if (vol && gi > -1) {
      var base = '../';
      vol.innerHTML = (prev
        ? '<a href="' + base + prev.pid + '/' + prev.f + '">← ' + prev.n + '</a>'
        : '<a href="../index.html">← 目录</a>') +
        (next ? '<a class="nx" href="' + base + next.pid + '/' + next.f + '">' + next.n + ' →</a>'
              : '<a class="nx" href="../index.html">目录 →</a>');
    }

    var cn = document.getElementById('chNav');
    if (cn && gi > -1) {
      var bh = '';
      bh += '<a href="' + (prev ? '../' + prev.pid + '/' + prev.f : '../index.html') + '"><span>' +
        (prev ? '上一章' : '返回') + '</span><b>' + (prev ? '← ' + prev.n + ' ' + prev.t : '← 全书目录') + '</b></a>';
      bh += '<a class="nx" href="' + (next ? '../' + next.pid + '/' + next.f : '../index.html') + '"><span>' +
        (next ? '下一章' : 'END') + '</span><b>' + (next ? next.n + ' ' + next.t + ' →' : '读完 · 回到全书目录') + '</b></a>';
      cn.innerHTML = bh;
    }
  };

  window.dpToc = function () {
    var host = document.getElementById('toc');
    if (!host) return;
    var h = '';
    (window.DP_PARTS || []).forEach(function (p) {
      var total = p.chapters.reduce(function (a, c) { return a + c.min; }, 0);
      h += '<div class="part-block" id="' + p.id + '">' +
        '<div class="part-head2"><h2>' + p.no + '　' + p.title + '</h2>' +
        '<span class="pk">PART ' + p.no + '</span>' +
        '<span class="pc">' + p.chapters.length + ' 章 · 约 ' + total + ' 分钟</span></div>' +
        '<p class="pl">' + p.intro + '</p><div class="chlist">';
      p.chapters.forEach(function (c) {
        h += '<a class="chrow" href="' + p.id + '/' + c.f + '">' +
          '<span class="cn">' + c.n + '</span>' +
          '<span class="ct"><b>' + c.t + '</b><i>' + c.s + '</i></span>' +
          '<span class="cm">' + c.min + ' 分钟</span><span class="ca">→</span></a>';
      });
      h += '</div></div>';
    });
    host.innerHTML = h;
  };
})();
"""


def dump_nav():
    write(ASSETS / "dp-nav.js", NAV_JS)


# ---------------- 演示引擎 ----------------

DEMO_JS = r"""/* 通用演示引擎：一串步骤点亮结构里的节点，并写日志 */
(function () {
  'use strict';
  window.dpDemo = function (cfg) {
    var box = document.getElementById('demo');
    if (!box) return;
    var flow = document.getElementById('dflow');
    var log = document.getElementById('dlog');
    var bar = document.getElementById('dbar');
    var idx = -1;
    var timer = null;

    (cfg.nodes || []).forEach(function (n) {
      var d = document.createElement('button');
      d.type = 'button';
      d.className = 'dchip';
      d.id = 'chip-' + n.id;
      d.innerHTML = '<b>' + n.label + '</b>' + (n.sub ? '<i>' + n.sub + '</i>' : '');
      if (n.note) {
        d.title = n.note;
        d.addEventListener('click', function () {
          var t = document.getElementById('dnote');
          if (t) t.textContent = n.note;
        });
      }
      flow.appendChild(d);
    });

    function paint() {
      (cfg.nodes || []).forEach(function (n) {
        var el = document.getElementById('chip-' + n.id);
        if (el) el.classList.remove('on');
      });
      var st = cfg.steps[Math.max(0, idx)];
      if (!st) return;
      (st.hi || []).forEach(function (id) {
        var el = document.getElementById('chip-' + id);
        if (el) el.classList.add('on');
      });
      if (bar) {
        bar.textContent = (idx + 1) + ' / ' + cfg.steps.length + '　' + st.t;
        bar.className = 'dbar' + (st.bad ? ' bad' : '');
      }
    }
    function step() {
      if (idx >= cfg.steps.length - 1) return false;
      idx++;
      paint();
      var st = cfg.steps[idx];
      var d = document.createElement('div');
      if (st.bad) d.className = 'bad';
      d.innerHTML = '<em>' + ('0' + (idx + 1)).slice(-2) + '</em>' + st.t;
      log.appendChild(d);
      log.scrollTop = log.scrollHeight;
      return true;
    }
    function reset() {
      stop();
      idx = -1; log.innerHTML = '';
      (cfg.nodes || []).forEach(function (n) {
        var el = document.getElementById('chip-' + n.id);
        if (el) el.classList.remove('on');
      });
      if (bar) { bar.textContent = '未开始'; bar.className = 'dbar'; }
    }
    function play() {
      if (timer) { stop(); return; }
      timer = setInterval(function () { if (!step()) stop(); }, 900);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }

    var bPrev = document.getElementById('dPrev');
    var bNext = document.getElementById('dNext');
    var bPlay = document.getElementById('dPlay');
    var bReset = document.getElementById('dReset');
    if (bPrev) bPrev.onclick = function () { reset(); for (var i = 0; i <= idx; i++) { } };
    if (bNext) bNext.onclick = function () { stop(); step(); };
    if (bPlay) bPlay.onclick = play;
    if (bReset) bReset.onclick = reset;
    reset();
  };
})();
"""


def dump_demo():
    write(ASSETS / "dp-demo.js", DEMO_JS)


def demo_block(cfg):
    nodes = ", ".join(
        "{id:%s,label:%s,sub:%s,note:%s}" % (js_str(n["id"]), js_str(n["label"]), js_str(n.get("sub", "")), js_str(n.get("note", "")))
        for n in cfg["nodes"]
    )
    steps = ", ".join(
        "{hi:[%s],t:%s%s}" % (", ".join(js_str(x) for x in s.get("hi", [])), js_str(s["t"]), ",bad:true" if s.get("bad") else "")
        for s in cfg["steps"]
    )
    return f"""
<div class="demo" id="demo">
  <div class="demo-h"><b>{cfg['title']}</b><span>{cfg.get('sub','')}</span></div>
  <div class="stage">
    <div class="dflow" id="dflow"></div>
    <div class="dbar" id="dbar">未开始</div>
    <div class="dctl">
      <button class="btn" id="dPrev">复位</button>
      <button class="btn" id="dNext">单步</button>
      <button class="btn" id="dPlay">自动</button>
      <button class="btn" id="dReset">清日志</button>
    </div>
    <div class="dnote" id="dnote">点上面的方框，看它在这次流程里负责什么。</div>
    <div class="log" id="dlog"></div>
  </div>
</div>
<script>dpDemo({{nodes:[{nodes}],steps:[{steps}]}});</script>
"""


# ---------------- 结构图 ----------------

def svg_diagram(boxes, arrows, label=""):
    parts = [f'<svg viewBox="0 0 880 360" role="img" aria-label="{esc(label or "结构图")}">',
             '  <defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
             '<path d="M0 0 L10 5 L0 10 z" fill="#5876a4"/></marker></defs>']
    for b in boxes:
        parts.append(
            f'  <g class="node" data-role="{b["id"]}" data-note="{esc(b.get("note", ""))}">'
            f'<rect x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" rx="10"/>'
            f'<text class="nm" x="{b["x"]+14}" y="{b["y"]+24}">{esc(b["t"])}</text>'
            f'<text class="ty" x="{b["x"]+14}" y="{b["y"]+43}">{esc(b.get("ty",""))}</text>'
            f'<text class="mt" x="{b["x"]+14}" y="{b["y"]+61}">{esc(b.get("mt",""))}</text></g>'
        )
    for a in arrows:
        dash = ' stroke-dasharray="5 4"' if a.get("dash") else ""
        parts.append(
            f'  <line x1="{a["x1"]}" y1="{a["y1"]}" x2="{a["x2"]}" y2="{a["y2"]}" stroke="#5876a4" stroke-width="1.4"{dash} marker-end="url(#ar)"/>'
        )
        if a.get("label"):
            parts.append(
                f'  <text x="{(a["x1"]+a["x2"])/2}" y="{(a["y1"]+a["y2"])/2-8}" fill="#8fa3c4" font-size="10.5" text-anchor="middle">{esc(a["label"])}</text>'
            )
    parts.append('</svg>')
    return "\n".join(parts)


def code_card(lang, fn, path):
    code = read(path).replace("\r\n", "\n").rstrip()
    return f"""
      <div class="codecard">
        <div class="ch"><span class="lang">{lang}</span><span class="fn">{fn}</span><button class="copy">复制</button></div>
        <pre><code>{esc(code)}</code></pre>
      </div>"""


def run_block(tag, cmd, path):
    out = read(path).replace("\r\n", "\n").rstrip()
    return f"""
    <div class="run">
      <div class="ch"><b>RUN</b><span>{cmd}</span></div>
      <pre>{esc(out)}</pre>
    </div>"""


def section_shell(i, title, body, sub=""):
    h = f'<p class="subh">{sub}</p>' if sub else ""
    return f"""
  <section class="sec" id="s{i}">
    <h2><span class="n">0{i}</span>{title}</h2>
    {h}
    {body}
  </section>"""


def page_shell(part, ch, title, desc, body, chips, lede):
    pn = part["no"]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{ch['n']} {ch['t']} {ch['en']} · C 与 C++ 双实现</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#08090c">
<link rel="stylesheet" href="../assets/pd.css">
<script src="../assets/dp-demo.js"></script>
</head>
<body>
<div class="bg" aria-hidden="true"></div>

<header class="topbar">
  <div class="topbar-in">
    <label for="navChk" class="nav-toggle">☰ 目录</label>
    <a class="brand" href="../index.html"><i></i>设计模式<small>C / C++ 双实现</small></a>
    <span class="tb-sp"></span>
    <a class="tb" href="../p1/c01.html">导读</a>
    <a class="tb" href="../../../index.html">知识库</a>
    <a class="tb" href="../index.html">目录</a>
  </div>
</header>

<input type="checkbox" id="navChk" class="nav-chk" hidden>
<label for="navChk" class="nav-mask" aria-hidden="true"></label>

<div class="shell">
  <aside id="sidebar">
    <div class="vol-h" id="sideHead">设计模式全书 · 25 章<label for="navChk" class="nav-x" aria-label="收起目录">✕</label></div>
    <ol id="sideList"></ol>
    <div class="vol-nav" id="volNav"></div>
  </aside>

  <div class="wrap">
  <div class="ch-meta"><span class="lv">篇{pn} · {part['title']}</span><span class="sep">/</span>第 {ch['k']} 章<span class="sep">/</span>约 {ch['min']} 分钟</div>
  <h1>{ch['t']}<span class="en">{ch['en']}</span></h1>
  <p class="lede">{lede}</p>
  <div class="chips">{chips}</div>
{body}
  <div class="ch-nav" id="chNav"></div>
  </div>
</div>

<script src="../assets/pd.js"></script>
<script src="../assets/dp-data.js"></script>
<script src="../assets/dp-nav.js"></script>
<script>dpNav('{part['id']}');</script>
</body>
</html>
"""


def build_new(part, ch, c):
    boxes, arrows = c["boxes"], c["arrows"]
    secs = []
    secs.append(section_shell(1, ch["sec"][0], c["s1"]))
    diagram = f"""
    <div class="fig">
      <div class="fig-h"><b>{c['fig_title']}</b><span>{c.get('fig_tag','structure')}</span></div>
      <div class="diagram">
{svg_diagram(boxes, arrows, c['fig_title'])}
      </div>
      <div class="rolebar"><span class="rb-h">职责</span><span class="rb-t">{c['fig_note']}</span></div>
    </div>"""
    secs.append(section_shell(2, ch["sec"][1], c.get("s2", ""), c.get("s2_sub", "")) .replace("</section>", diagram + "\n  </section>"))
    body3 = (c.get("s3", "") + code_card("C", c["cfile"], SRC / c["cfile"]) +
             run_block("C", "./" + c["cfile"].replace(".c", ".exe"), OUT / (c["cfile"].replace(".c", ".txt")) ) +
             code_card("C++", c["cppfile"], SRC / c["cppfile"]) +
             run_block("C++", "./" + c["cppfile"].replace(".cpp", "_cpp.exe"), OUT / (c["cppfile"].replace(".cpp", "_cpp.txt"))))
    secs.append(section_shell(3, ch["sec"][2], body3))
    secs.append(section_shell(4, ch["sec"][3], demo_block(c["demo"])))
    rows = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>" for r in c["rows"]
    )
    table = f"""
    <div class="tbl">
      <table>
        <thead><tr><th>角色</th><th>C 版</th><th>C++ 版</th><th>差别意味着什么</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""
    secs.append(section_shell(5, ch["sec"][4], table))
    pits = "".join(f"<li><b>{p[0]}</b>{p[1]}</li>" for p in c["pitfalls"])
    secs.append(section_shell(6, ch["sec"][5], f'<div class="prose"><ul>{pits}</ul></div>'))

    chips = "".join(f'<span class="chip{" ok" if i == 0 else ""}">{x}</span>' for i, x in enumerate(c["chips"]))
    page = page_shell(part, ch, ch["t"], c["desc"], "\n".join(secs), chips, c["lede"])
    write(ROOT / part["id"] / ch["f"], page)


# ---------------- 旧页迁移 ----------------

def migrate_old(part, ch):
    old = ROOT / ch["old"]
    if not old.exists():
        return  # 已迁移过，源文件已删除
    text = read(old)
    pn = part["no"]

    text = re.sub(r"<title>.*?</title>", f"<title>{ch['n']} {ch['t']} {ch['en']} · C 与 C++ 双实现</title>", text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{esc(ch["t"])}：C 与 C++ 双实现，含结构图、运行输出与可点演示。">', text, count=1, flags=re.S)
    text = re.sub(
        r'<div class="ch-meta">.*?</div>',
        f'<div class="ch-meta"><span class="lv">篇{pn} · {part["title"]}</span><span class="sep">/</span>第 {ch["k"]} 章<span class="sep">/</span>约 {ch["min"]} 分钟</div>',
        text, count=1, flags=re.S,
    )
    text = re.sub(r'<div class="vol-h">.*?</div>', f'<div class="vol-h" id="sideHead">设计模式全书 · 25 章<label for="navChk" class="nav-x" aria-label="收起目录">✕</label></div>', text, count=1, flags=re.S)
    text = re.sub(r'<div class="ch-nav">.*?</div>', '<div class="ch-nav" id="chNav"></div>', text, count=1, flags=re.S)
    text = text.replace("dpNav('p1')", f"dpNav('{part['id']}')").replace("dpNav('p2')", f"dpNav('{part['id']}')").replace("dpNav('p3')", f"dpNav('{part['id']}')")
    if '<script src="../assets/dp-demo.js"></script>' not in text:
        text = text.replace('<script src="../assets/dp-nav.js"></script>', '<script src="../assets/dp-nav.js"></script>\n<script src="../assets/dp-demo.js"></script>')
    # 旧页面里的静态“第 X 章”或旧章号链接由 chNav 统一接管
    write(ROOT / part["id"] / ch["f"], text)


# ---------------- 首页 ----------------

def build_index():
    parts = PARTS
    body = f"""
  <div class="ch-meta"><span class="lv">设计模式全书</span><span class="sep">/</span>四篇 25 章<span class="sep">/</span>C 与 C++ 双实现</div>
  <h1>设计模式：从一张函数表，到一个可替换的对象</h1>
  <p class="lede">这套东西不背定义。每个模式都走同一条线：先看它在真实代码里长什么样（通常是坏的），再画清结构，然后给两份实现——一份 C 的（结构体首成员放函数表指针，手工虚表），一份 C++ 的（虚函数 + <code>unique_ptr</code>/<code>shared_ptr</code>）。两份代码用 gcc/g++ <code>-Wall -Wextra</code> 零警告编译，页面上的 RUN 输出就是实际跑出来的结果。场景全部来自车载与嵌入式：CAN 调度、ECU 状态机、报文过滤、驱动注册、传感器适配。</p>
  <div class="chips"><span class="chip ok">四篇 25 章</span><span class="chip">23 个 GoF 模式全实现</span><span class="chip">每章 6 节</span></div>

  <section class="sec" id="s0">
    <h2><span class="n">0</span>　四篇的关系</h2>
    <div class="prose">
      <p>第一篇不是模式，是地基：1.1 给一条“按症状找模式”的路，1.2 把 C 的多态拆开——对象首字节放函数表指针，调用先取表、再按偏移取地址、最后把对象自己当第一个参数。后面每一章的 C 版，都是这三步的变体。</p>
      <p>第二篇管“怎么造”：工厂方法按名字取驱动，抽象工厂保证一套零件同代，建造者把拼装拆成步骤，原型用克隆代替重复初始化，单例守住唯一入口。第三篇管“怎么接”：适配器、桥接、组合、装饰、外观、享元、代理。第四篇管“流程与责任”：职责链、命令、解释器、迭代器、中介者、备忘录、观察者、状态、策略、模板方法、访问者。</p>
      <p>建议顺序读；赶时间就按症状跳，每一章的 01 节都先写“坏代码长什么样”，对上了再往下看。</p>
    </div>
  </section>

  <div id="toc"></div>

  <div class="ch-nav">
    <a href="../../../index.html"><span>返回</span><b>← 知识库</b></a>
    <a class="nx" href="p1/c01.html"><span>开始</span><b>1.1 导读：为什么用模式 →</b></a>
  </div>
"""
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>设计模式 · 四篇 25 章 · C 与 C++ 双实现</title>
<meta name="description" content="23 个 GoF 设计模式全部实现：每章问题、结构图、C 与 C++ 两份代码、真实 RUN 输出、可点演示。">
<meta name="theme-color" content="#08090c">
<link rel="stylesheet" href="assets/pd.css">
</head>
<body>
<div class="bg" aria-hidden="true"></div>
<header class="topbar">
  <div class="topbar-in">
    <label for="navChk" class="nav-toggle">☰ 目录</label>
    <a class="brand" href="index.html"><i></i>设计模式<small>C / C++ 双实现</small></a>
    <span class="tb-sp"></span>
    <a class="tb" href="p1/c01.html">导读</a>
    <a class="tb" href="../../../index.html">知识库</a>
    <a class="tb" href="index.html">目录</a>
  </div>
</header>
<input type="checkbox" id="navChk" class="nav-chk" hidden>
<label for="navChk" class="nav-mask" aria-hidden="true"></label>
<div class="shell">
  <aside id="sidebar">
    <div class="vol-h" id="sideHead">设计模式全书 · 25 章<label for="navChk" class="nav-x" aria-label="收起目录">✕</label></div>
    <ol id="sideList"></ol>
    <div class="vol-nav" id="volNav"></div>
  </aside>
  <div class="wrap">
{body}
  </div>
</div>
<script src="assets/pd.js"></script>
<script src="assets/dp-data.js"></script>
<script src="assets/dp-nav.js"></script>
<script>dpNav(''); dpToc();</script>
</body>
</html>
"""
    write(ROOT / "index.html", page)


def clean_old():
    for p in ("p1/c01.html", "p1/c02.html", "p2/c01.html", "p2/c02.html", "p2/c03.html",
              "p2/c04.html", "p2/c05.html", "p3/c01.html", "p3/c02.html", "p3/c03.html"):
        f = ROOT / p
        if f.exists() and p not in {c.get("old") for _, c in ALL}:
            f.unlink()


def main():
    dump_data()
    dump_nav()
    dump_demo()
    for p, c in ALL:
        if c.get("old"):
            migrate_old(p, c)
        else:
            from content_new import CONTENT
            build_new(p, c, CONTENT[c["n"]])
    build_index()
    # 删掉迁移前的旧文件（新文件已写到目标路径；若旧路径本身也是新章节路径则保留）
    targets = {ROOT / q["id"] / s["f"] for q, s in ALL}
    for p, c in ALL:
        if c.get("old"):
            old = ROOT / c["old"]
            new = ROOT / p["id"] / c["f"]
            if old != new and old.exists() and old not in targets:
                old.unlink()
    print("built", len(ALL), "chapters")


if __name__ == "__main__":
    main()


