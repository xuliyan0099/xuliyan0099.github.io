# -*- coding: utf-8 -*-
"""第二篇：创建型 5 章（经典教程场景：物流、GUI、盖房、图形克隆、全局配置）。"""
from content_lib import mk, bx, ar, LEFT, MID, TOP, BOT

C = {}

C["2.1"] = mk(
    desc="工厂方法：客户端只说要哪种运输，具体造卡车还是轮船由工厂决定。",
    lede="物流系统一开始只有卡车，后来加了轮船、飞机。如果“造哪一种”写死在客户端，每加一种交通工具就要改一遍下单代码。工厂方法把这句 <code>new</code> 挪进工厂：<b>客户端只传类型名，工厂返回已经造好的产品</b>。",
    chips=["客户端不 import 具体类", "新增产品只加工厂", "C 用创建函数表 · C++ 用虚函数"],
    s1="""
      <div class="prose">
        <p>坏写法是客户端自己判断：</p>
        <pre><code>Transport *t;
if (strcmp(type, "truck") == 0)      t = truck_new();
else if (strcmp(type, "ship") == 0)  t = ship_new();
else                                 t = NULL;</code></pre>
        <p>它有三个问题：新增“飞机”要改这里；每个调用方都得抄一遍判断；测试要覆盖所有分支组合。</p>
        <p>工厂方法只做一件事：<b>把“选具体类”从客户端搬到工厂</b>。客户端拿到的是统一的产品接口，只调 <code>deliver()</code>，不再关心轮子还是螺旋桨。</p>
      </div>""",
    s2_sub="左边是下单方，中间是工厂，右边是两种产品。点方框看它负责什么。",
    fig_title="客户端只认工厂，不认具体运输工具",
    boxes=[
        bx("client", "客户端", "业务下单", "create(\"truck\")", "客户端只说运输类型，不知道 Truck / Ship 这些类名。", *LEFT),
        bx("factory", "TransportFactory", "工厂", "create(type)", "工厂持有“类型名 → 创建函数”的表；新增产品改表，不改客户端。", *MID),
        bx("truck", "Truck", "产品 A", "deliver()", "卡车负责陆运；它只实现产品接口，不参与“被选中”的过程。", *TOP),
        bx("ship", "Ship", "产品 B", "deliver()", "轮船负责海运；和卡车共用同一个产品接口。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "要产品"), ar(440, 160, 520, 100, "造卡车"), ar(440, 200, 520, 242, "造轮船")],
    fig_note="工厂是唯一知道“有哪些产品”的地方；产品只负责自己的业务。",
    s3="<p class='subh'>C 版把工厂写成一张静态表：名字 + 创建函数；C++ 版写成抽象基类，产品用 <code>unique_ptr</code> 交付，所有权清楚。</p>",
    cfile="factory.c", cppfile="factory.cpp",
    demo=dict(
        title="换一种运输方式，只改传给工厂的名字",
        sub="同一段下单流程，分别要卡车、轮船和一个不存在的类型。",
        nodes=[dict(id="client", label="客户端", sub="create(type)"), dict(id="factory", label="工厂", sub="查表"),
               dict(id="truck", label="卡车", sub="陆运"), dict(id="ship", label="轮船", sub="海运")],
        steps=[
            dict(hi=["client", "factory"], t="客户端调用 create(\"truck\")"),
            dict(hi=["factory", "truck"], t="工厂查到 Truck 的创建函数，返回卡车"),
            dict(hi=["truck"], t="卡车 deliver：陆运 200 箱"),
            dict(hi=["client", "factory", "ship"], t="客户端改传 \"ship\"，同一行代码"),
            dict(hi=["ship"], t="轮船 deliver：海运 800 箱；传 \"plane\" 时工厂返回 NULL"),
        ],
    ),
    rows=[
        ("谁创建产品", "工厂查静态表，调用创建函数", "工厂子类的虚函数 new 出对象", "C 的“类”是表项，C++ 的“类”是类型"),
        ("客户端依赖", "只依赖 <code>transport_t</code> 接口", "只依赖 <code>Transport</code> 接口", "都能换产品而不改调用方"),
        ("未知类型", "查表失败返回 <code>NULL</code>", "抛异常或返回空指针", "错误必须显式处理，不要返回半成品"),
        ("所有权", "静态对象，谁都不能 delete", "<code>unique_ptr</code> 明确归属", "C 版省堆分配，代价是产品不能带走"),
    ],
    pitfalls=[
        ("把工厂当万能", "只有“创建逻辑会变、或需要统一入口”时才值得抽工厂；一个 <code>struct</code> 直接初始化更清楚。"),
        ("返回内部静态对象还允许修改", "多个调用方拿到同一份对象会互相污染；要可变就每次新建。"),
        ("类型名拼错没有兜底", "查表失败必须返回错误，不要默认造第一个产品。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/factory-method",
)

C["2.2"] = mk(
    desc="抽象工厂：浅色/深色两套 GUI 控件成套交付，不会出现浅色按钮配深色复选框。",
    lede="界面有两套主题：浅色和深色。按钮和复选框如果各自按名字创建，很容易配出“浅色按钮 + 深色复选框”。抽象工厂让<b>一个家族一次交出两个控件</b>：选浅色就两个都浅色，选深色就两个都深色。",
    chips=["一次交付整族控件", "换主题不改调用方", "C 用函数表家族 · C++ 用抽象基类"],
    s1="""
      <div class="prose">
        <p>坏写法是两个控件分别取：</p>
        <pre><code>Button   *b = make_button(cfg-&gt;theme);
Checkbox *c = make_checkbox(cfg-&gt;theme2);</code></pre>
        <p>两行都合法，但 <code>theme</code> 和 <code>theme2</code> 一旦不一致，界面就会花。真正的问题不是“取不到”，而是<b>取到了也能跑，只是组合错了</b>。</p>
        <p>抽象工厂把两个 <code>make_*</code> 收进同一个家族对象。调用方只选一次家族，之后所有控件都从它出，从结构上断掉混搭。</p>
      </div>""",
    s2_sub="左边是界面，中间是主题家族，右边是按钮和复选框。",
    fig_title="一个家族，两个控件，同一套配色",
    boxes=[
        bx("client", "界面", "业务代码", "family = light/dark", "界面只选一次主题，不分别指定按钮和复选框。", *LEFT),
        bx("family", "GuiFactory", "控件家族", "button() + checkbox()", "家族是唯一知道“哪两个控件属于同一套主题”的对象。", *MID),
        bx("btn", "Button", "控件 A", "label()", "按钮只负责自己的外观；配色由家族保证一致。", *TOP),
        bx("chk", "Checkbox", "控件 B", "label()", "复选框和按钮同族，不会出现深浅混搭。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "选主题"), ar(440, 160, 520, 100, "造按钮"), ar(440, 200, 520, 242, "造复选框")],
    fig_note="家族负责“成套”；控件只负责自己的接口。",
    s3="<p class='subh'>C 版家族是“两个返回函数表指针”的结构；C++ 版家族是抽象基类，控件用 <code>unique_ptr</code> 交付。</p>",
    cfile="abstract_factory.c", cppfile="abstract_factory.cpp",
    demo=dict(
        title="切一次主题，看两个控件是否成套",
        sub="同一段界面代码，只换家族。",
        nodes=[dict(id="ui", label="界面", sub="选主题"), dict(id="fam", label="家族", sub="light/dark"),
               dict(id="btn", label="按钮", sub="label()"), dict(id="chk", label="复选框", sub="label()")],
        steps=[
            dict(hi=["ui", "fam"], t="界面选浅色家族"),
            dict(hi=["btn"], t="拿到浅色按钮：[ 浅色按钮 ]"),
            dict(hi=["chk"], t="拿到浅色复选框：[ ] 浅色复选框"),
            dict(hi=["ui", "fam"], t="切到深色家族，界面代码不改"),
            dict(hi=["btn", "chk"], t="按钮和复选框同时变深：[ 深色按钮 ] / [x] 深色复选框"),
        ],
    ),
    rows=[
        ("家族怎么表示", "<code>gui_factory_t</code> 两个函数指针", "<code>GuiFactory</code> 抽象基类", "C 的家族是数据，C++ 的家族是类型"),
        ("控件怎么交付", "返回静态控件指针", "<code>unique_ptr&lt;Button&gt;</code>", "C 版不分配堆，C++ 版所有权清晰"),
        ("换主题", "换一个家族结构体", "换一个工厂子类", "调用方都只调一次"),
        ("扩展新控件", "家族结构加一个函数指针", "基类加一个纯虚函数", "两边都要动家族，这是它的代价"),
    ],
    pitfalls=[
        ("把“主题”当成两个独立配置", "只要允许分别指定，就迟早会混搭；要么合成一个家族字段，要么在入口校验。"),
        ("家族里塞太多无关产品", "抽象工厂适合“必须成套”的少量产品；产品一多，家族会变成上帝对象。"),
        ("C 版返回可写静态对象", "两个界面改同一个控件会互相影响；示例只读，真实实现应按需复制。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/abstract-factory",
)

C["2.3"] = mk(
    desc="建造者：把盖房子拆成砌墙、装门、装窗、封顶，最后统一校验交付。",
    lede="盖房子不是一次 <code>malloc</code> 就能完事：墙、门、窗、屋顶有先后，少一步就是半成品。建造者把“怎么一步步拼”收进流程，<b>每一步都可检查，最后只交付一次成品</b>。",
    chips=["步骤显式", "交付前校验", "C 用函数参数 · C++ 用链式调用"],
    s1="""
      <div class="prose">
        <p>坏写法是一个巨大的初始化函数，参数排成一串：</p>
        <pre><code>house_t h = { 4, 1, 2, 1 };  /* 墙、门、窗、屋顶？顺序错了也编译过 */</code></pre>
        <p>位置参数没有名字，调用方靠记忆；漏一个字段就是“能住但漏雨”的半成品，而且没有任何地方能拦住。</p>
        <p>建造者把每个步骤变成一次具名调用，最后 <code>build()</code> 统一校验。顺序、缺项、成品完整度都摆在代码里。</p>
      </div>""",
    s2_sub="左边是施工队，中间是建造者，右边是成品房子。",
    fig_title="四步施工，最后校验一次",
    boxes=[
        bx("client", "施工队", "调用方", "walls/doors/windows/roof", "按步骤调用，不再拼位置参数。", *LEFT),
        bx("builder", "HouseBuilder", "建造者", "add_* + build()", "建造者保存中间状态，build 时检查是否齐全。", *MID),
        bx("check", "校验", "完整性", "walls>=4 ...", "缺墙、缺门、缺屋顶都会被拒绝，不会交付半成品。", *TOP),
        bx("house", "House", "成品", "交付一次", "成品只在 build 成功后出现，之后不再改。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "逐步施工"), ar(440, 160, 520, 100, "校验"), ar(440, 200, 520, 242, "交付")],
    fig_note="建造者持有“正在盖的房子”；校验通过才允许拿走。",
    s3="<p class='subh'>C 版每一步都是 <code>house_t*</code> 上的函数，最后由 <code>build</code> 返回成败；C++ 版用引用串联步骤，<code>build()</code> 返回值对象。</p>",
    cfile="builder.c", cppfile="builder.cpp",
    demo=dict(
        title="盖一次完整的房子，再漏一步试试",
        sub="同一套建造者，分别走完整流程和缺屋顶流程。",
        nodes=[dict(id="team", label="施工队", sub="调用步骤"), dict(id="b", label="建造者", sub="保存状态"),
               dict(id="chk", label="校验", sub="build()"), dict(id="house", label="房子", sub="成品")],
        steps=[
            dict(hi=["team", "b"], t="砌 4 面墙、装 1 扇门、装 2 扇窗"),
            dict(hi=["b"], t="封顶：has_roof = 1"),
            dict(hi=["chk"], t="build() 校验：4 墙 / 1 门 / 2 窗 / 有屋顶"),
            dict(hi=["house"], t="校验通过，交付房子"),
            dict(hi=["chk"], t="第二个建造者漏了封顶：校验失败，拒绝交付", bad=True),
        ],
    ),
    rows=[
        ("步骤怎么表达", "具名函数 <code>add_walls(h, 4)</code>", "链式 <code>w(4).d(1).win(2).roof()</code>", "C 显式传对象，C++ 可连写"),
        ("中间状态放哪", "调用方栈上的 <code>house_t</code>", "建造者对象内部", "C 版无隐藏状态，C++ 版封装更好"),
        ("校验时机", "<code>build()</code> 返回 -1", "<code>build()</code> 返回 optional/抛错", "都必须在交付前"),
        ("成品归属", "值拷贝或指针", "值返回，移动语义", "C 版注意别把栈地址带出去"),
    ],
    pitfalls=[
        ("步骤可以任意跳过", "建造者要能表达“缺项”，并在 build 时拒绝；不要默认补全。"),
        ("build 之后还能改", "成品交付后应视为不可变；否则校验结果立刻失效。"),
        ("把所有业务都塞进建造者", "建造者只管拼装与完整性，不要在里面发网络请求、写数据库。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/builder",
)

C["2.4"] = mk(
    desc="原型：以圆形、方形为原型，克隆出互不影响的新对象。",
    lede="图形编辑器里，复制一个已经调好大小和颜色的圆，比重新 <code>new</code> 再逐字段赋值更可靠。原型模式把“怎么造自己”交给对象本身：<b>调用 clone，拿到一份独立副本</b>。",
    chips=["克隆代替重复初始化", "副本互不影响", "C 由调用方给存储 · C++ 用拷贝构造"],
    s1="""
      <div class="prose">
        <p>坏写法是调用方逐个字段抄：</p>
        <pre><code>shape_t copy;
copy.kind = src-&gt;kind;
copy.size = src-&gt;size;
copy.color = src-&gt;color;   /* 以后加字段，这里必漏 */</code></pre>
        <p>字段一多就漏；如果对象内部还有指针，浅拷贝会让两份共享同一块内存，改一份污染另一份。</p>
        <p>原型让对象自己负责复制：<code>clone(src, &amp;dst)</code>。以后加字段只改 clone，调用方永远只写一行。</p>
      </div>""",
    s2_sub="左边是编辑器，中间是原型登记表，右边是克隆出来的副本。",
    fig_title="原型只读，克隆出来的才归调用方",
    boxes=[
        bx("client", "图形编辑器", "调用方", "clone(\"circle\")", "调用方按名字取原型，再克隆；不直接改原型。", *LEFT),
        bx("reg", "原型登记表", "registry", "circle / square", "登记表保存原始图形，是只读模板。", *MID),
        bx("proto", "原型 Circle", "被克隆者", "size=10", "原型保持不变，克隆多少次都不影响它。", *TOP),
        bx("copy", "副本 Circle", "克隆结果", "size=25", "副本有独立存储，改它不会回写原型。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "按名取原型"), ar(440, 160, 520, 100, "读"), ar(440, 200, 520, 242, "clone 到独立存储")],
    fig_note="克隆的语义是“值复制”；谁提供存储，谁拥有副本。",
    s3="<p class='subh'>C 版 <code>clone(src, out)</code> 由调用方给两块存储，避免静态缓冲被两份副本共享；C++ 版用拷贝构造，副本是独立对象。</p>",
    cfile="prototype.c", cppfile="prototype.cpp",
    demo=dict(
        title="克隆两份圆，只改其中一份",
        sub="原型保持 10，副本 b 改成 25。",
        nodes=[dict(id="ed", label="编辑器", sub="clone"), dict(id="reg", label="登记表", sub="circle"),
               dict(id="a", label="副本 a", sub="size=10"), dict(id="b", label="副本 b", sub="size=25")],
        steps=[
            dict(hi=["ed", "reg"], t="编辑器按名字取到圆形原型"),
            dict(hi=["reg", "a"], t="clone 出副本 a：size=10"),
            dict(hi=["reg", "b"], t="再 clone 出副本 b：size=10"),
            dict(hi=["b"], t="把 b 改成 size=25"),
            dict(hi=["a", "reg"], t="a 仍是 10，原型仍是 10：两份互不影响"),
        ],
    ),
    rows=[
        ("怎么复制", "函数指针 <code>clone(src, out)</code>", "拷贝构造 / <code>clone()</code>", "C 要显式给目标存储"),
        ("副本存储", "调用方栈上的两块对象", "堆上的新对象", "C 版没有隐藏分配"),
        ("加字段", "改 clone 实现", "改拷贝构造", "调用方都不改"),
        ("原型可变吗", "约定只读", "约定只读或返回 const", "原型被改，所有克隆都跟着错"),
    ],
    pitfalls=[
        ("浅拷贝带指针的对象", "内部有堆内存时必须深拷贝，否则副本共享同一块数据。"),
        ("用完即弃的 static 缓冲", "两个副本会指向同一缓冲；C 版应让调用方传入目标对象。"),
        ("把原型当工厂", "原型只负责复制自己；需要“按参数造不同产品”时用工厂方法。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/prototype",
)

C["2.5"] = mk(
    desc="单例：全局配置只初始化一次，所有模块拿到同一个实例。",
    lede="主题、字号、语言这些配置每个模块都要读。到处传参太啰嗦，到处复制又会改出多份。单例把“唯一实例”收在一个入口后面：<b>谁调都拿到同一个地址，初始化只发生一次</b>。",
    chips=["一个入口", "初始化一次", "C 用函数内静态 · C++ 用 Meyers 单例"],
    s1="""
      <div class="prose">
        <p>坏写法是每个模块自己存一份：</p>
        <pre><code>config_t cfg_a = { "light", 12 };
config_t cfg_b = { "light", 12 };   /* 改 a，b 不知道 */</code></pre>
        <p>两份初始值一样，运行一会儿就分叉：设置页改了主题，主窗口还是旧的。</p>
        <p>单例只留一个入口 <code>instance()</code>：第一次调用时初始化，之后都返回同一个对象。它不是“全局变量换皮”，而是<b>把初始化时机和唯一性一起管住</b>。</p>
      </div>""",
    s2_sub="左边三个模块，中间是唯一入口，右边是同一份配置。",
    fig_title="三个调用点，一个地址",
    boxes=[
        bx("a", "设置页", "模块 A", "instance()", "设置页通过入口改主题。", 24, 60, 150, 70),
        bx("b", "主窗口", "模块 B", "instance()", "主窗口通过入口读主题，拿到同一份。", 24, 150, 150, 70),
        bx("c", "日志", "模块 C", "instance()", "日志也走同一个入口，不会出现第三份。", 24, 240, 150, 70),
        bx("inst", "Config::instance", "唯一入口", "static cfg", "入口内部持有唯一对象，并负责首次初始化。", 300, 150, 210, 84),
        bx("cfg", "Config", "唯一实例", "theme/font", "三个模块看到的是同一块内存。", 610, 150, 190, 84),
    ],
    arrows=[ar(174, 95, 300, 175, ""), ar(174, 185, 300, 185, ""), ar(174, 275, 300, 205, ""), ar(510, 192, 610, 192, "同一地址")],
    fig_note="入口负责“有没有”；实例负责“是什么”。",
    s3="<p class='subh'>C 版用函数内 <code>static</code>，初始化天然只跑一次；C++ 版用函数内静态对象（Meyers singleton），C++11 起线程安全。</p>",
    cfile="singleton.c", cppfile="singleton.cpp",
    demo=dict(
        title="点三次入口，看初始化几次、地址是否相同",
        sub="三个模块依次取实例，然后通过一个入口改配置。",
        nodes=[dict(id="a", label="设置页", sub="instance"), dict(id="b", label="主窗口", sub="instance"),
               dict(id="c", label="日志", sub="instance"), dict(id="cfg", label="Config", sub="theme/font")],
        steps=[
            dict(hi=["a", "cfg"], t="设置页第一次调用：初始化配置（只发生一次）"),
            dict(hi=["b", "cfg"], t="主窗口调用：直接返回同一地址，不再初始化"),
            dict(hi=["c", "cfg"], t="日志调用：还是同一地址"),
            dict(hi=["a", "cfg"], t="设置页改成 dark / 16"),
            dict(hi=["c", "cfg"], t="日志读到的也是 dark / 16：没有第二份"),
        ],
    ),
    rows=[
        ("唯一性怎么保证", "函数内 <code>static</code>", "函数内静态对象", "都靠语言级静态存储"),
        ("初始化时机", "首次调用", "首次调用", "懒初始化，不增加启动成本"),
        ("线程安全", "C11 起静态初始化有保证", "C++11 起局部静态初始化线程安全", "旧编译器要自己加锁"),
        ("销毁", "进程结束时释放", "进程结束时析构", "一般不需要手动 delete"),
    ],
    pitfalls=[
        ("把单例当全局变量", "单例适合“确实唯一且到处要读”的配置；普通共享数据用依赖注入更可测。"),
        ("在单例里做重活", "构造函数里读文件、连网络会让首次调用变慢且难测。"),
        ("多线程下双重检查写错", "C++ 直接用局部静态；C 用 <code>pthread_once</code>，不要手写裸双检。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/singleton",
)
