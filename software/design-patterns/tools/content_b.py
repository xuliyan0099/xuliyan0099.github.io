# -*- coding: utf-8 -*-
"""第三篇：结构型 7 章。"""
from content_lib import mk, bx, ar, LEFT, MID, TOP, BOT

C = {}

C["3.1"] = mk(
    desc="适配器：把方钉包一层，让只认圆孔的旧接口也能接受它。",
    lede="旧接口只接受“半径”，新零件偏偏是“边长”。改旧接口会影响所有调用方，改新零件又违反它自己的规格。适配器夹在中间：<b>对外仍是旧接口，对内把方钉翻译成等效半径</b>。",
    chips=["旧接口不动", "新零件不改", "C 用包装结构 · C++ 用类继承 + 组合"],
    s1="""
      <div class="prose">
        <p>坏写法是让调用方自己换算：</p>
        <pre><code>if (peg_kind == SQUARE)
    ok = round_fits(&amp;hole, peg.width * 2 / 3);
else
    ok = round_fits(&amp;hole, peg.radius);</code></pre>
        <p>换算规则散落到每个调用点；再来一种六角钉，所有地方都要补分支。</p>
        <p>适配器把换算收在一处：它实现旧接口（对外暴露 <code>radius()</code>），内部持有方钉，把边长翻译成等效半径。调用方仍然只认圆孔。</p>
      </div>""",
    s2_sub="左边是圆孔，中间是适配器，右边是方钉。",
    fig_title="旧接口在前，翻译在中间，新零件在后",
    boxes=[
        bx("hole", "RoundHole", "旧接口", "fits(radius)", "圆孔只知道半径，不关心钉子的形状。", *LEFT),
        bx("ad", "SquareAdapter", "适配器", "radius() 翻译", "适配器对外是“圆钉”，内部持有方钉，负责把边长换成半径。", *MID),
        bx("peg", "SquarePeg", "新零件", "width=6/10", "方钉按自己的规格实现，不被迫改成圆形。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "只要半径"), ar(440, 200, 520, 242, "读边长")],
    fig_note="适配器是唯一知道两种规格怎么换算的对象。",
    s3="<p class='subh'>C 版适配器是一个包装结构体，靠函数读内部方钉；C++ 版用继承拿到旧接口、用组合持有方钉。</p>",
    cfile="adapter.c", cppfile="adapter.cpp",
    demo=dict(
        title="两根方钉，一次塞得进、一次塞不进",
        sub="圆孔半径 5，方钉边长 6 和 10。",
        nodes=[dict(id="hole", label="圆孔", sub="半径 5"), dict(id="ad", label="适配器", sub="换算半径"),
               dict(id="p6", label="方钉 6", sub="→4"), dict(id="p10", label="方钉 10", sub="→6")],
        steps=[
            dict(hi=["hole"], t="圆孔：半径 5，只接受半径参数"),
            dict(hi=["ad", "p6"], t="方钉 6 交给适配器，换算成半径 4"),
            dict(hi=["hole"], t="4 ≤ 5，塞得进"),
            dict(hi=["ad", "p10"], t="方钉 10 换算成半径 6"),
            dict(hi=["hole"], t="6 &gt; 5，塞不进：拒绝发生在旧接口里", bad=True),
        ],
    ),
    rows=[
        ("适配器形态", "包装结构 + 换算函数", "继承旧接口 + 组合新零件", "C 没有继承，用结构嵌套"),
        ("调用方看到", "<code>adapter_radius()</code>", "<code>radius()</code> 虚函数", "对外都是旧接口"),
        ("换算规则放哪", "适配器函数里", "适配器成员函数里", "只此一处，改规则不改调用方"),
        ("额外成本", "一次函数调用 + 一次换算", "一次虚调用 + 一次换算", "都很薄，别在适配器里做重活"),
    ],
    pitfalls=[
        ("适配器变成业务层", "它只做接口翻译，不要在适配器里加缓存、重试、权限。"),
        ("换算有损还假装无损", "方钉对角线近似成半径会失真；需要精确时应在接口层说明误差。"),
        ("双向适配", "两个方向都要就写两个适配器，不要一个类同时继承两边，容易循环依赖。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/adapter",
)

C["3.2"] = mk(
    desc="桥接：形状与渲染器各自独立，2×2 组合不需要 4 个子类。",
    lede="图形库要支持圆和方，还要支持矢量与位图两种渲染。按“形状+渲染器”建子类会得到 <code>VectorCircle</code>、<code>BitmapCircle</code>……每加一维就翻倍。桥接把两维拆开：<b>形状只管几何，渲染器只管画</b>，中间连一条引用。",
    chips=["两维独立扩展", "组合不爆炸", "C 用渲染器函数表 · C++ 用抽象基类"],
    s1="""
      <div class="prose">
        <p>坏写法是把渲染方式写进形状：</p>
        <pre><code>void draw_circle_vector(...);
void draw_circle_bitmap(...);
void draw_square_vector(...);
void draw_square_bitmap(...);</code></pre>
        <p>2 种形状 × 2 种渲染 = 4 个函数；再加三角形和 SVG，就是 3×3 = 9 个。增长是乘法。</p>
        <p>桥接之后：形状持有“渲染器接口”，画的时候调 <code>r-&gt;circle(size)</code>。形状 2 种、渲染器 2 种，代码量是加法，组合数还是乘法但实现不用写满。</p>
      </div>""",
    s2_sub="左边是形状，中间是渲染器引用，右边是两种渲染实现。",
    fig_title="形状与渲染器各管一维",
    boxes=[
        bx("shape", "Shape", "形状", "draw() + renderer*", "形状只算几何，具体怎么画交给渲染器。", *LEFT),
        bx("r", "Renderer", "渲染接口", "circle() / square()", "渲染器接口只描述“画什么图元”，不关心形状的名字。", *MID),
        bx("vec", "VectorRenderer", "实现 A", "矢量输出", "矢量渲染：圆输出 r=5，方输出 w=5。", *TOP),
        bx("bmp", "BitmapRenderer", "实现 B", "位图输出", "位图渲染：圆输出半径 5px，方输出边长 5px。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "持有"), ar(440, 160, 520, 100, "画圆"), ar(440, 200, 520, 242, "画方")],
    fig_note="形状与渲染器之间只有一条引用；换渲染器不影响形状。",
    s3="<p class='subh'>C 版渲染器是一张函数表，形状结构里放指针；C++ 版渲染器是抽象基类，形状用引用持有。</p>",
    cfile="bridge.c", cppfile="bridge.cpp",
    demo=dict(
        title="四种组合，只换一侧",
        sub="圆/方 × 矢量/位图，形状代码不变。",
        nodes=[dict(id="shape", label="形状", sub="Circle/Square"), dict(id="r", label="渲染器", sub="Vector/Bitmap"),
               dict(id="vec", label="矢量", sub="r/w"), dict(id="bmp", label="位图", sub="px")],
        steps=[
            dict(hi=["shape", "r", "vec"], t="Circle + VectorRenderer → 矢量圆 r=5"),
            dict(hi=["shape", "r", "vec"], t="Square + VectorRenderer → 矢量方 w=5"),
            dict(hi=["r", "bmp"], t="只换渲染器：Circle + BitmapRenderer"),
            dict(hi=["shape", "bmp"], t="位图圆 半径 5px"),
            dict(hi=["shape", "bmp"], t="位图方 边长 5px；2×2 组合，没有 4 个子类"),
        ],
    ),
    rows=[
        ("渲染器怎么表示", "函数表指针", "抽象基类引用", "C 的渲染器是数据，C++ 是类型"),
        ("形状持有什么", "<code>const renderer_t *</code>", "<code>Renderer&amp;</code>", "都只持一条引用"),
        ("换渲染器", "换指针", "换引用", "形状对象不用重建"),
        ("扩展新维度", "加一种形状或一种渲染器", "同左", "两边各自加，不交叉"),
    ],
    pitfalls=[
        ("把两维又合到一个类里", "只要出现 <code>VectorCircle</code> 这种命名，桥接就白做了。"),
        ("渲染器里读形状私有字段", "渲染器只接收图元参数；否则又耦合成一个整体。"),
        ("引用生命周期不清", "C 版渲染器是静态表没问题；C++ 若用指针，形状不能活得比渲染器久。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/bridge",
)

C["3.3"] = mk(
    desc="组合：文件与文件夹共用一套接口，目录树可以整棵遍历、整棵统计。",
    lede="资源管理器里，文件夹可以装文件，也可以装文件夹。如果“遍历”只认文件夹、“统计”只认文件，调用方就得一路判断类型。组合模式让<b>枝和叶实现同一个接口</b>：对整棵树调用一次，内部自己递归。",
    chips=["枝与叶同接口", "递归收敛在一处", "C 用 is_dir 标记 · C++ 用虚函数"],
    s1="""
      <div class="prose">
        <p>坏写法是调用方自己分类型递归：</p>
        <pre><code>if (node-&gt;is_dir)
    for (each kid) total(kid);
else
    sum += node-&gt;size;</code></pre>
        <p>这段逻辑会在“统计大小”“查找文件”“生成树形图”里各抄一遍，而且每处都要记得处理空目录。</p>
        <p>组合把 <code>total()</code> 放到节点自己身上：目录的 <code>total</code> 累加孩子，文件的 <code>total</code> 返回自身大小。调用方只写 <code>total(root)</code>。</p>
      </div>""",
    s2_sub="左边是调用方，中间是目录节点，右边是文件叶子。",
    fig_title="目录递归孩子，文件返回自身",
    boxes=[
        bx("client", "调用方", "统计 / 查找", "total(root)", "调用方只拿根节点，不再判断类型。", *LEFT),
        bx("dir", "Dir", "枝节点", "total() = Σ kids", "目录负责递归孩子；空目录返回 0。", *MID),
        bx("file", "File", "叶节点", "total() = size", "文件没有孩子，直接返回自己的大小。", *TOP),
        bx("tree", "root/src/a.c", "实际树", "210 字节", "同一接口可以套在任意深度上。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "调用"), ar(440, 160, 520, 100, "递归到文件"), ar(440, 200, 520, 242, "向上汇总")],
    fig_note="枝负责“继续往下”，叶负责“到此为止”。",
    s3="<p class='subh'>C 版用 <code>is_dir</code> 标记区分枝与叶，孩子数组固定容量；C++ 版用虚函数和多态容器。</p>",
    cfile="composite.c", cppfile="composite.cpp",
    demo=dict(
        title="从 root 跑到叶子，再汇总回来",
        sub="root 下有 src 目录和 README，src 下有 a.c、b.c。",
        nodes=[dict(id="root", label="root", sub="目录"), dict(id="src", label="src", sub="目录"),
               dict(id="a", label="a.c", sub="120B"), dict(id="b", label="b.c", sub="80B"), dict(id="r", label="README", sub="10B")],
        steps=[
            dict(hi=["root", "src"], t="root.total 进入 src"),
            dict(hi=["src", "a"], t="src 累加 a.c：120"),
            dict(hi=["src", "b"], t="src 累加 b.c：200"),
            dict(hi=["root", "r"], t="回到 root，累加 README：210"),
            dict(hi=["root"], t="root.total 返回 210 字节"),
        ],
    ),
    rows=[
        ("枝与叶怎么分", "<code>is_dir</code> 字段", "不同子类 + 虚函数", "C 靠标记，C++ 靠类型"),
        ("递归在哪", "节点的 <code>total()</code> 里", "节点的 <code>total()</code> 里", "都不在调用方"),
        ("孩子容量", "固定数组 4 个", "<code>vector&lt;unique_ptr&gt;</code>", "C 版示例简化，真实实现要动态"),
        ("空目录", "返回 0", "返回 0", "必须显式处理，别返回未初始化值"),
    ],
    pitfalls=[
        ("枝和叶接口不一致", "一旦调用方要 <code>if (is_dir)</code>，组合就失效了。"),
        ("递归没有终止条件", "叶节点必须明确“没有孩子”，否则空指针递归。"),
        ("父节点持有孩子又共享所有权", "C++ 用 <code>unique_ptr</code> 明确父子；需要共享时再谈引用计数。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/composite",
)

C["3.4"] = mk(
    desc="装饰器：给文本套一层加粗、再套一层斜体，每层只加一件事。",
    lede="一段文本要支持加粗、斜体、下划线，未来还可能有删除线。每加一种就复制一遍渲染函数，组合顺序也说不清。装饰器把每种效果做成一层：<b>持有一个内层文本，输出时在自己的前后加标记</b>。",
    chips=["一层一件事", "顺序可见", "C 用值传递 · C++ 用包装对象"],
    s1="""
      <div class="prose">
        <p>坏写法是给每个组合写一个函数：</p>
        <pre><code>render_bold(t);
render_bold_italic(t);
render_italic_bold_underline(t);   /* 组合越来越多 */</code></pre>
        <p>N 种效果就有 2^N 种组合，函数名先爆炸。</p>
        <p>装饰器只做单层：<code>bold(t)</code> 返回 <code>&lt;b&gt;…&lt;/b&gt;</code>，<code>italic(t)</code> 返回 <code>&lt;i&gt;…&lt;/i&gt;</code>。叠加就是函数套函数，顺序直接写在调用里。</p>
      </div>""",
    s2_sub="左边是原始文本，中间两层装饰，右边是最终输出。",
    fig_title="每层只负责一对标签",
    boxes=[
        bx("src", "Text", "原始", "hello", "原始文本不带任何标记。", *LEFT),
        bx("bold", "Bold", "装饰 A", "&lt;b&gt;…&lt;/b&gt;", "加粗只负责包一层 b 标签。", *MID),
        bx("it", "Italic", "装饰 B", "&lt;i&gt;…&lt;/i&gt;", "斜体只负责包一层 i 标签。", *TOP),
        bx("out", "Result", "输出", "&lt;i&gt;&lt;b&gt;hello&lt;/b&gt;&lt;/i&gt;", "顺序不同，嵌套就不同；语义由调用方决定。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "包一层"), ar(440, 160, 520, 100, "再包一层"), ar(440, 200, 520, 242, "输出")],
    fig_note="装饰层不改变文本内容，只改变表示。",
    s3="<p class='subh'>C 版装饰是“文本进、文本出”的纯函数，靠值拷贝避免别名；C++ 版装饰对象持有内层文本。</p>",
    cfile="decorator.c", cppfile="decorator.cpp",
    demo=dict(
        title="先加粗再斜体，和反过来有什么不同",
        sub="同一段 hello，两种叠加顺序。",
        nodes=[dict(id="t", label="Text", sub="hello"), dict(id="b", label="Bold", sub="&lt;b&gt;"),
               dict(id="i", label="Italic", sub="&lt;i&gt;"), dict(id="o", label="输出", sub="嵌套结果")],
        steps=[
            dict(hi=["t"], t="原始：hello"),
            dict(hi=["b", "o"], t="套 Bold：&lt;b&gt;hello&lt;/b&gt;"),
            dict(hi=["i", "o"], t="再套 Italic：&lt;i&gt;&lt;b&gt;hello&lt;/b&gt;&lt;/i&gt;"),
            dict(hi=["b"], t="换顺序：先 Italic 再 Bold"),
            dict(hi=["o"], t="得到 &lt;b&gt;&lt;i&gt;hello&lt;/i&gt;&lt;/b&gt;：语义一样，嵌套不同"),
        ],
    ),
    rows=[
        ("装饰怎么实现", "文本值进、文本值出", "装饰对象持有内层", "C 无对象层次，C++ 可动态组合"),
        ("顺序", "调用顺序即嵌套顺序", "构造顺序即嵌套顺序", "顺序由调用方负责"),
        ("拷贝成本", "每次复制整个结构体", "指针/引用传递", "C 版示例文本短，长文本要注意"),
        ("扩展新效果", "加一个函数", "加一个装饰子类", "都不改已有层"),
    ],
    pitfalls=[
        ("装饰层里做业务", "装饰只改表示；加日志、鉴权会让组合语义混乱。"),
        ("顺序被隐式固定", "如果构造函数里自动排序，调用方就失去控制；顺序应显式。"),
        ("C 版缓冲区不够", "拼接后长度会增加，必须按目标容量截断或动态分配。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/decorator",
)

C["3.5"] = mk(
    desc="外观：家庭影院开机四步收成一个 watch_movie()，失败时还能整段回滚。",
    lede="看电视要开投影、开功放、放幕布、调灯光，顺序错了就没画面。每个想播片的地方都抄一遍这四步，迟早漏一步。外观模式提供一个入口：<b>内部按顺序调子系统，对外只暴露“看片”和“结束”</b>。",
    chips=["一个入口", "子系统仍可单独用", "失败可整段回滚"],
    s1="""
      <div class="prose">
        <p>坏写法是每个调用点自己排：</p>
        <pre><code>lights_dim();
projector_on();
amplifier_on();
screen_down();</code></pre>
        <p>四个调用点各写一遍，顺序不一致；投影开机失败时，前面的灯已经调暗、幕布已经放下，没人负责收尾。</p>
        <p>外观把这些收进 <code>watch_movie()</code>：按顺序调，任一步失败就逆序回滚。调用方只说“我要看片”。</p>
      </div>""",
    s2_sub="左边是用户，中间是外观入口，右边是四个子系统。",
    fig_title="入口收口，子系统仍各自可用",
    boxes=[
        bx("user", "用户", "调用方", "watch_movie()", "用户不关心投影、功放、幕布的先后。", *LEFT),
        bx("facade", "TheaterFacade", "外观", "watch / end", "外观知道顺序和回滚，是唯一编排者。", *MID),
        bx("dev", "投影 / 功放 / 幕布 / 灯", "子系统", "各自 on/off", "子系统仍可被单独调用，用于调试。", *TOP),
        bx("rb", "回滚", "异常路径", "逆序关闭", "失败时把已经开的设备关回去，避免半开状态。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "一键"), ar(440, 160, 520, 100, "按序调用"), ar(440, 200, 520, 242, "失败回滚")],
    fig_note="外观不是“新业务”，只是把既有步骤编排好。",
    s3="<p class='subh'>C 版外观是一组函数加一个 started 标记；C++ 版是类，析构时兜底关闭。</p>",
    cfile="facade.c", cppfile="facade.cpp",
    demo=dict(
        title="一键看片，再一键结束",
        sub="四步顺序执行，结束时逆序收尾。",
        nodes=[dict(id="u", label="用户", sub="watch"), dict(id="f", label="外观", sub="编排"),
               dict(id="d", label="设备", sub="灯/投影/功放/幕布"), dict(id="e", label="结束", sub="end_movie")],
        steps=[
            dict(hi=["u", "f"], t="用户调用 watch_movie()"),
            dict(hi=["d"], t="灯光 20% → 投影开机 → 功放 HDMI 1 → 幕布放下"),
            dict(hi=["f", "d"], t="四步全部成功，可以播放"),
            dict(hi=["u", "e"], t="看完调用 end_movie()"),
            dict(hi=["e", "d"], t="关投影、关功放、灯光回升、幕布收起"),
        ],
    ),
    rows=[
        ("入口形态", "一组函数 + 状态标记", "类 + 成员状态", "C 显式传状态，C++ 封装"),
        ("顺序", "函数体内硬编码", "函数体内硬编码", "顺序只此一处"),
        ("失败回滚", "调用方检查返回值", "异常 / 返回值 + 析构兜底", "必须有，不能留在半开状态"),
        ("子系统可用性", "仍可直接调用", "仍可直接调用", "外观不替代子系统"),
    ],
    pitfalls=[
        ("外观变成上帝对象", "只编排已有步骤，不要在外观里发明新业务规则。"),
        ("只做开机不做关机", "有资源获取就必须有释放路径，否则第一次失败就卡住。"),
        ("把子系统藏死", "调试和测试仍需要单独操作设备；外观应是可选入口，不是唯一入口。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/facade",
)

C["3.6"] = mk(
    desc="享元：一千棵树共享两份树型描述，每棵树只多存坐标。",
    lede="一片森林要画一千棵树。每棵树如果都存名字、叶色、纹理，内存很快见底。但这些字段大多数树是一样的。享元把<b>可共享的内部状态抽出来共用，只把坐标这类外部状态留在每棵树上</b>。",
    chips=["内部状态共享", "外部状态随行", "C 用静态表 · C++ 用工厂缓存"],
    s1="""
      <div class="prose">
        <p>坏写法是每棵树复制一份描述：</p>
        <pre><code>typedef struct { char name[16]; int color; int x, y; } tree_t;
/* 1000 棵树 → 1000 份 name 和 color */</code></pre>
        <p>名字和颜色只有两种，却存了一千遍；真正每棵不同的是坐标。</p>
        <p>享元把 <code>tree_type_t</code> 抽出来，按名字查表共享；<code>tree_t</code> 只留一个类型指针和 x/y。一千棵树 → 两份描述 + 一千组坐标。</p>
      </div>""",
    s2_sub="左边是森林，中间是共享类型表，右边是每棵树的外部状态。",
    fig_title="共享不变的部分，随行变化的部分",
    boxes=[
        bx("forest", "Forest", "调用方", "plant(x, y, type)", "森林只负责摆位置，不复制树型。", *LEFT),
        bx("pool", "TypePool", "享元工厂", "get_type(name)", "同一名字只创建一次，之后都返回同一份。", *MID),
        bx("type", "TreeType", "内部状态", "name + color", "可共享：名字、叶色、纹理。", *TOP),
        bx("inst", "Tree", "外部状态", "type* + x/y", "不可共享：每棵树自己的坐标。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "要类型"), ar(440, 160, 520, 100, "查/建"), ar(440, 200, 520, 242, "组合")],
    fig_note="享元省的是“重复的相同数据”，不是“对象本身”。",
    s3="<p class='subh'>C 版类型池是静态数组，按名字线性查；C++ 版用 <code>map</code> 缓存 <code>shared_ptr</code>。</p>",
    cfile="flyweight.c", cppfile="flyweight.cpp",
    demo=dict(
        title="一千棵树，只有两份树型",
        sub="橡树和松树各共享一份描述变量。",
        nodes=[dict(id="f", label="森林", sub="1000 棵"), dict(id="p", label="类型池", sub="2 份"),
               dict(id="t1", label="橡树", sub="color"), dict(id="t2", label="松树", sub="color")],
        steps=[
            dict(hi=["f", "p"], t="森林要种 1000 棵树"),
            dict(hi=["p", "t1"], t="第一棵橡树：创建橡树类型，存入池"),
            dict(hi=["p", "t1"], t="后续橡树：直接复用同一份类型"),
            dict(hi=["p", "t2"], t="松树同理，只创建一份"),
            dict(hi=["f"], t="结果：1000 棵树，共享 2 份描述，每棵只多存 x/y"),
        ],
    ),
    rows=[
        ("共享池", "静态数组 + 线性查名", "<code>map&lt;string, shared_ptr&gt;</code>", "C 版简单，C++ 版查找更快"),
        ("内部状态", "<code>tree_type_t</code> 值", "<code>TreeType</code> 共享对象", "必须不可变"),
        ("外部状态", "每棵树的 x/y", "每棵树的 x/y", "随实例走，不进池"),
        ("省了多少", "1000 份描述 → 2 份", "同左", "省的是重复数据，不是全部内存"),
    ],
    pitfalls=[
        ("共享对象被修改", "内部状态一旦可变，所有树一起变；共享对象必须只读。"),
        ("池无上限", "按用户输入无限建类型会泄漏；类型集合应是有限、可枚举的。"),
        ("把外部状态也塞进共享对象", "坐标、时间戳这类每实例不同的字段不能进池。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/flyweight",
)

C["3.7"] = mk(
    desc="代理：图片查看器里，代理先挡一层，命中缓存就不碰磁盘。",
    lede="打开相册时，一屏几十张图，如果每张都立刻读磁盘，滚动会卡。代理站在真实图片前面：<b>第一次访问才加载，之后命中缓存直接返回</b>。调用方以为自己在用图片，其实先经过代理。",
    chips=["懒加载", "缓存命中", "C 用包装结构 · C++ 用代理类"],
    s1="""
      <div class="prose">
        <p>坏写法是调用方自己管缓存：</p>
        <pre><code>if (!img-&gt;loaded) load_from_disk(img);
use(img-&gt;pixels);</code></pre>
        <p>每个用到图片的地方都要重复这段判断；忘了置 <code>loaded</code> 就重复读盘。</p>
        <p>代理把“加载 + 缓存”收进 <code>get()</code>：内部持有真实对象，未加载时转下去，加载后直接返回像素数。调用方只调 <code>get()</code>。</p>
      </div>""",
    s2_sub="左边是界面，中间是代理，右边是真实图片。",
    fig_title="代理挡在前面，真实对象按需加载",
    boxes=[
        bx("ui", "界面", "调用方", "get(name)", "界面以为拿到的就是图片。", *LEFT),
        bx("proxy", "ImageProxy", "代理", "缓存 + 转发", "代理判断是否已加载；命中就直接返回。", *MID),
        bx("real", "RealImage", "真实对象", "load()", "真正读磁盘、解码像素，只在第一次发生。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "get"), ar(440, 200, 520, 242, "未命中才加载")],
    fig_note="代理不改变图片内容，只改变“何时加载、加载几次”。",
    s3="<p class='subh'>C 版代理是一个持有真实图片结构体的包装；C++ 版代理持有 <code>unique_ptr&lt;Image&gt;</code>，对调用方实现同一接口。</p>",
    cfile="proxy.c", cppfile="proxy.cpp",
    demo=dict(
        title="读三次，只加载一次",
        sub="同一张 photo.jpg 连续访问三次。",
        nodes=[dict(id="ui", label="界面", sub="get"), dict(id="p", label="代理", sub="缓存"),
               dict(id="r", label="真实图片", sub="磁盘"), dict(id="c", label="缓存", sub="pixels")],
        steps=[
            dict(hi=["ui", "p", "r"], t="第一次 get(photo.jpg)：未命中，转给真实对象"),
            dict(hi=["r"], t="真正读取磁盘：photo.jpg"),
            dict(hi=["p", "c"], t="代理记下 pixels，标记已加载"),
            dict(hi=["ui", "p", "c"], t="第二次 get：命中缓存，不碰磁盘"),
            dict(hi=["ui", "p", "c"], t="第三次 get：仍然命中；三次读取只加载一次"),
        ],
    ),
    rows=[
        ("代理形态", "包装结构 + 缓存字段", "代理类 + 真实对象指针", "C 显式组合，C++ 可多态"),
        ("对外接口", "<code>proxy_get()</code>", "<code>get()</code> 虚函数", "调用方无感"),
        ("缓存位置", "真实图片结构体里的 loaded/pixels", "代理或真实对象内部", "只要只有一处写就行"),
        ("线程安全", "示例单线程", "示例单线程", "多线程要加锁，避免重复加载"),
    ],
    pitfalls=[
        ("代理和真实对象接口不一致", "一旦调用方要判断“是不是代理”，透明性就没了。"),
        ("缓存没有失效策略", "文件更新后仍返回旧像素；需要版本号或 mtime。"),
        ("代理里塞权限/日志/重试全都上", "一个代理只做一件事；需要多种横切能力就叠多个代理。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/proxy",
)
