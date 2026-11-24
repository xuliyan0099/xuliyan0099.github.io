# -*- coding: utf-8 -*-
"""第四篇新增章：解释器、迭代器、中介者、备忘录、模板方法、访问者。"""

C = {}

C["4.3"] = dict(
    desc="解释器：把 \"TEMP>90 AND RPM<800\" 变成表达式树，换输入重算而不重解析。",
    lede="诊断条件经常写成 <code>if (temp &gt; 90 &amp;&amp; rpm &lt; 800)</code>，改一条规则就要改代码、重新刷写。<b>解释器把条件变成一棵小树</b>：比较是叶子，AND/OR 是枝；换一组输入只重算，换规则只换树。",
    chips=["条件变成树", "比较是叶、逻辑是枝", "换输入不重解析"],
    s1="""
      <div class="prose">
        <p>写死在代码里的条件，问题不在第一条，而在第一百条：</p>
        <pre><code>if (temp &gt; 90 &amp;&amp; rpm &lt; 800) {
    set_fault(DTC_OVERHEAT);
}</code></pre>
        <ul>
          <li><b>规则不可配。</b>不同车型阈值不同，只能各刷一版软件。</li>
          <li><b>组合无法复用。</b>“超温”和“转速低”分别被别的规则用到，只能再抄一遍。</li>
          <li><b>无法静态检查。</b>括号写错、优先级搞反，编译器不报，实车才发现。</li>
        </ul>
        <p>解释器把表达式拆成节点：<code>CMP</code>（变量、比较符、阈值）、<code>AND</code>、<code>OR</code>。树一旦建好，换环境值只调 <code>eval()</code>，不需要重新解析字符串。</p>
      </div>""",
    s2_sub="一棵三节点小树：AND 在顶，两个比较在底；点方框看每个节点怎么求值。",
    fig_title="诊断表达式树：AND + 两个比较",
    fig_tag="interpreter",
    boxes=[
        dict(id="and", x=350, y=40, w=180, h=76, t="AND", ty="逻辑节点", mt="两棵子树都真", note="AND 只负责“两边都为真”；它不关心比较的具体变量，也不关心阈值。"),
        dict(id="t", x=150, y=170, w=220, h=80, t="TEMP > 90", ty="比较节点", mt="var=temp op=>", note="比较节点从上下文取 temp，与 90 比较；阈值可以来自配置，不必写死。"),
        dict(id="r", x=510, y=170, w=220, h=80, t="RPM < 800", ty="比较节点", mt="var=rpm op=<", note="换车型只换阈值或换一棵树；求值路径不变。"),
        dict(id="ctx", x=350, y=280, w=180, h=64, t="ctx", ty="输入", mt="temp / rpm", note="上下文是外部状态：同一棵树可以被不同输入反复求值。"),
    ],
    arrows=[
        dict(x1=380, y1=116, x2=290, y2=170),
        dict(x1=500, y1=116, x2=590, y2=170),
        dict(x1=420, y1=280, x2=420, y2=220, dash=True, label="取值"),
    ],
    fig_note="点方框：逻辑节点只组合，比较节点才碰数据。",
    s3="<p class='subh'>C 版手写静态节点 + 递归 <code>eval()</code>；C++ 版每个节点一个类，子树用 <code>unique_ptr</code> 持有。</p>",
    cfile="interpreter.c",
    cppfile="interpreter.cpp",
    demo=dict(
        title="三组输入，同一棵树",
        sub="树不变，只换 temp/rpm；看哪种组合触发报警。",
        nodes=[
            dict(id="and", label="AND", sub="组合"),
            dict(id="t", label="TEMP>90", sub="比较"),
            dict(id="r", label="RPM<800", sub="比较"),
            dict(id="out", label="结果", sub="报警/正常"),
        ],
        steps=[
            dict(hi=["t"], t="输入 hot：temp=105 → TEMP>90 为真"),
            dict(hi=["r"], t="hot：rpm=700 → RPM<800 为真"),
            dict(hi=["and"], t="AND 两边都真 → 报警"),
            dict(hi=["t"], t="输入 idle：temp=88 → 比较为假"),
            dict(hi=["and"], t="AND 短路：不再算右边，结果正常"),
            dict(hi=["t", "r"], t="输入 fast：temp=95 真、rpm=900 假"),
            dict(hi=["and", "out"], t="AND 为假 → 正常；同一棵树，三种结论"),
        ],
    ),
    rows=[
        ("节点表示", "结构体 + <code>kind</code> 枚举", "多态 <code>Expr</code> 派生类", "C 手写分派；C++ 交给虚函数"),
        ("子树", "裸指针 <code>l/r</code>", "<code>unique_ptr</code>", "C 要保证节点活得比树久；C++ 自动释放"),
        ("求值", "递归 <code>eval()</code>", "虚 <code>eval()</code>", "都一样从根往下"),
        ("短路", "<code>&amp;&amp;</code> 天然短路", "<code>&amp;&amp;</code> 天然短路", "别为了统计把两边都算完"),
        ("换规则", "换一棵树 / 换阈值", "换一棵树 / 换阈值", "树是数据，不是代码"),
    ],
    pitfalls=[
        ("解释器不是解析器。", "本节的树是手工搭的；真要从字符串解析，需要词法、语法、错误恢复，工作量另算。"),
        ("别为一条规则上解释器。", "只有一个 <code>if</code> 时，树反而更难读；规则多、要配置、要复用时才值得。"),
        ("求值要防除零与类型错。", "比较节点目前只做整数；接入浮点、字符串时要显式定义转换与错误。"),
        ("C 版节点生命周期。", "静态节点最安全；一旦动态分配，必须有一处统一释放，否则树越跑越漏。"),
        ("短路会影响副作用。", "比较节点若有日志或计数，AND 短路会让右边不执行；需要统计就单独遍历。"),
    ],
)

C["4.4"] = dict(
    desc="迭代器：故障表只暴露 next()，调用方不再直接摸数组。",
    lede="故障表今天是数组，明天可能换成环形缓冲或链表。调用方若直接 <code>for (i=0; i&lt;n; i++)</code>，存储一换就全改。<b>迭代器只暴露“还有没有、下一个是谁”</b>，内部结构随便换。",
    chips=["只暴露 next()", "跳过无效项", "换存储不改调用方"],
    s1="""
      <div class="prose">
        <p>直接遍历数组的写法很自然，但把存储细节写进了调用方：</p>
        <pre><code>for (int i = 0; i &lt; n; i++)
    if (faults[i].code != 0) handle(&amp;faults[i]);</code></pre>
        <ul>
          <li><b>换存储就崩。</b>改成链表后，<code>faults[i]</code> 不存在了，所有调用方都要重写。</li>
          <li><b>过滤规则散落。</b>“跳过 code=0”的逻辑在每个调用点复制，迟早有一处忘了跳。</li>
          <li><b>越界靠人守。</b><code>n</code> 算错、表被并发写，循环就读到边界外。</li>
        </ul>
        <p>迭代器把“当前位置 + 跳过规则 + 结束条件”收进一个对象；调用方只问 <code>next()</code>，拿不到就不再看。</p>
      </div>""",
    s2_sub="故障表、迭代器、调用方三段；点方框看 next() 如何在内部跳过多余项。",
    fig_title="故障表上的迭代器",
    fig_tag="iterator",
    boxes=[
        dict(id="list", x=24, y=130, w=200, h=100, t="fault_t[]", ty="存储", mt="5 项，含 2 个空", note="存储里可以有无效项（code=0）；调用方不需要知道它们存在。"),
        dict(id="it", x=300, y=130, w=200, h=100, t="fault_iter_t", ty="迭代器", mt="i / n / next()", note="迭代器持有下标与结束条件，next() 内部跳过无效项并返回指针。"),
        dict(id="client", x=580, y=130, w=200, h=100, t="调用方", ty="诊断任务", mt="while(next())", note="调用方只关心“还有没有有效故障”，不关心底层是数组还是链表。"),
    ],
    arrows=[
        dict(x1=224, y1=180, x2=300, y2=180, label="持有"),
        dict(x1=500, y1=180, x2=580, y2=180, label="next()"),
    ],
    fig_note="点方框：迭代器是存储与调用方之间的一层。",
    s3="<p class='subh'>C 版是显式 <code>next()</code>；C++ 版实现 <code>begin()/end()</code>，直接支持 range-for。</p>",
    cfile="iterator.c",
    cppfile="iterator.cpp",
    demo=dict(
        title="遍历时跳过无效项",
        sub="5 项里 2 项 code=0，调用方只看到 3 条有效故障。",
        nodes=[
            dict(id="i0", label="[0]", sub="code=0"),
            dict(id="i1", label="[1]", sub="17"),
            dict(id="i2", label="[2]", sub="code=0"),
            dict(id="i3", label="[3]", sub="42"),
            dict(id="i4", label="[4]", sub="91"),
        ],
        steps=[
            dict(hi=["i0"], t="next() 从 [0] 开始：code=0，跳过"),
            dict(hi=["i1"], t="[1] code=17：返回 O2 heater"),
            dict(hi=["i2"], t="继续： [2] code=0，再跳过"),
            dict(hi=["i3"], t="[3] code=42：返回 misfire"),
            dict(hi=["i4"], t="[4] code=91：返回 CAN bus off"),
            dict(hi=["i0", "i1", "i2", "i3", "i4"], t="越界：返回 NULL，循环自然结束；共 3 条有效故障"),
        ],
    ),
    rows=[
        ("迭代状态", "<code>fault_iter_t</code> 结构", "嵌套 <code>Iter</code> 类", "C 手动 init；C++ begin/end 生成"),
        ("取下一个", "<code>next()</code> 返回指针", "<code>operator++</code> + <code>operator*</code>", "C 要判 NULL；C++ 用范围 for"),
        ("过滤", "<code>next()</code> 内部 while", "<code>skip()</code> 内部 while", "规则只有一处"),
        ("失效", "调用方改表导致下标错位", "容器改动使迭代器失效", "两边都要求遍历期间别改表"),
        ("结束", "<code>NULL</code>", "<code>end()</code> 比较", "语义一致：到末尾就停"),
    ],
    pitfalls=[
        ("遍历时别改表。", "边遍历边删故障会让下标错位或跳过元素；要删就先收集，遍历完再处理。"),
        ("迭代器别返回内部指针。", "返回 <code>&amp;arr[i]</code> 后，表被重排就悬空；必要时返回值拷贝。"),
        ("C++ 迭代器要满足 range-for 的最小接口。", "<code>begin/end</code>、<code>!=</code>、<code>++</code>、<code>*</code> 一个都不能少。"),
        ("过滤规则要写清。", "code=0 是“无故障”还是“未初始化”，语义不同；别让迭代器替业务猜。"),
        ("并发读要加保护。", "诊断任务和故障写入可能并发；至少用双缓冲或读写锁，别让迭代器读到半更新状态。"),
    ],
)

C["4.5"] = dict(
    desc="中介者：发动机、仪表、制动不两两直连，所有消息走同一条总线。",
    lede="三个模块两两直连是 3 条线，五个模块是 10 条线，十个模块是 45 条。<b>中介者让每个模块只认识总线</b>，消息由总线决定投给谁；新增模块只加一个连接，不改其他人的代码。",
    chips=["N² 条线收成 N 条", "发送方不认识接收方", "路由规则集中一处"],
    s1="""
      <div class="prose">
        <p>两两直连的代码通常长这样：</p>
        <pre><code>engine.brake = &amp;brake;
engine.dash  = &amp;dash;
brake.dash   = &amp;dash;</code></pre>
        <ul>
          <li><b>依赖网越织越密。</b>每加一个模块，都要改已有模块的初始化，漏一条就收不到消息。</li>
          <li><b>路由规则散落。</b>“BRAKE 要广播、TEMP 只给仪表”写在各个发送方里，改规则要翻遍代码。</li>
          <li><b>无法统一审计。</b>想知道谁发了什么，只能逐模块加日志。</li>
        </ul>
        <p>中介者把所有发送改成“发给总线”，总线按主题路由。发送方只认识 <code>bus</code>，接收方只认识自己的处理函数；路由规则只有一份。</p>
      </div>""",
    s2_sub="三个节点围着总线；点方框看一条消息会被投给谁。",
    fig_title="总线式中介者：三个节点，一个路由中心",
    fig_tag="mediator",
    boxes=[
        dict(id="eng", x=60, y=56, w=180, h=76, t="ENGINE", ty="发送方", mt="publish()", note="发动机只把主题交给总线；它不知道仪表和制动是否存在。"),
        dict(id="dash", x=60, y=244, w=180, h=76, t="DASH", ty="接收方", mt="handle()", note="仪表订阅温度类主题；它不关心消息来自发动机还是制动。"),
        dict(id="brake", x=620, y=150, w=180, h=76, t="BRAKE", ty="发送/接收", mt="publish()", note="制动既能发轮速，也能收广播；节点角色可以重叠。"),
        dict(id="bus", x=330, y=130, w=220, h=96, t="mediator / bus", ty="路由中心", mt="route(from, topic)", note="路由规则集中在这里：BRAKE 广播，其余主题只给仪表；改规则只改这一处。"),
    ],
    arrows=[
        dict(x1=240, y1=100, x2=330, y2=150, label="publish"),
        dict(x1=240, y1=270, x2=330, y2=210, label="subscribe", dash=True),
        dict(x1=550, y1=170, x2=620, y2=180, label="route"),
    ],
    fig_note="点方框：发送方只认总线，路由规则只在总线里。",
    s3="<p class='subh'>C 版用节点数组 + 一个 <code>bus_publish()</code>；C++ 版用 <code>Mediator</code> 类持有 <code>Colleague*</code>。</p>",
    cfile="mediator.c",
    cppfile="mediator.cpp",
    demo=dict(
        title="三条消息，看谁被通知",
        sub="BRAKE 广播，TEMP 只给仪表，WHEEL_SPEED 也只给仪表。",
        nodes=[
            dict(id="eng", label="ENGINE", sub="发送"),
            dict(id="dash", label="DASH", sub="接收"),
            dict(id="brake", label="BRAKE", sub="发送/接收"),
            dict(id="bus", label="BUS", sub="路由"),
        ],
        steps=[
            dict(hi=["eng", "bus"], t="ENGINE 发 BRAKE：总线收到，准备广播"),
            dict(hi=["dash", "brake"], t="BRAKE 是广播主题：DASH 与 BRAKE 都被通知（发送方自己跳过）"),
            dict(hi=["eng", "bus"], t="ENGINE 再发 TEMP：主题只给仪表"),
            dict(hi=["dash"], t="只有 DASH 处理 TEMP，BRAKE 不被打扰"),
            dict(hi=["brake", "bus"], t="BRAKE 发 WHEEL_SPEED：仍由总线决定投递"),
            dict(hi=["dash"], t="DASH 收到轮速；三个节点之间没有一条直连"),
        ],
    ),
    rows=[
        ("中心", "<code>mediator_t</code> + 节点数组", "<code>Mediator</code> + <code>vector&lt;Colleague*&gt;</code>", "C 固定上限；C++ 动态加入"),
        ("发送", "<code>bus_publish(bus, from, topic)</code>", "<code>from-&gt;publish(topic)</code>", "C 要显式传总线；C++ 节点持有总线指针"),
        ("路由", "总线内 <code>strcmp</code> 判断", "总线内 <code>topic ==</code> 判断", "规则集中，但仍是硬编码字符串"),
        ("回环", "跳过 <code>from</code>", "跳过 <code>from</code>", "不跳会自己通知自己，递归爆栈"),
        ("新增节点", "加进数组 + 设 <code>bus</code>", "构造 + <code>add()</code>", "两边都不改已有节点"),
    ],
    pitfalls=[
        ("中介者会变成上帝对象。", "所有路由都塞进去，最后它知道每个模块的业务细节；路由规则要按主题分层，必要时拆多个总线。"),
        ("别忘跳过发送方。", "广播时把自己也通知一遍，轻则重复处理，重则递归。"),
        ("同步调用会放大延迟。", "一个 publish 里同步跑完所有接收方，慢的接收方拖住发送方；实时总线要考虑队列或异步。"),
        ("C 版字符串主题易拼错。", "用枚举或常量表，别让 \"BRAKE\" 和 \"BRAKE \" 成为两个主题。"),
        ("死锁风险。", "接收方在回调里再 publish，可能形成环；路由要检测重入或限制深度。"),
    ],
)

C["4.6"] = dict(
    desc="备忘录：改标定前存一份快照，调坏了能原样退回。",
    lede="现场调参最怕“越调越远”：增益、偏移、模式改了十几轮，想回到最初那版却没有记录。<b>备忘录把“当前状态”存成一份不可变快照</b>，需要时整体恢复；原对象不用暴露内部字段给外部。",
    chips=["改前先存", "快照不可变", "恢复是整体替换"],
    s1="""
      <div class="prose">
        <p>没有快照时，回退靠“记得原来的值”：</p>
        <pre><code>ecu.gain = 30;   /* 原来是多少？ */
ecu.offset = -8; /* 谁记了？ */</code></pre>
        <ul>
          <li><b>回退不完整。</b>只记住 gain，忘了 mode，恢复后状态是混合的。</li>
          <li><b>快照被污染。</b>把 <code>calib_t*</code> 直接存起来，后续改原对象，快照跟着变。</li>
          <li><b>外部乱改。</b>为了让调用方能恢复，把内部字段全暴露，封装名存实亡。</li>
        </ul>
        <p>备忘录把快照做成独立值：保存时拷贝，恢复时整体替换；快照只给原对象读写，外部只能“拿着”，不能“改里面的字段”。</p>
      </div>""",
    s2_sub="原对象、快照、保管者三方：点方框看谁有权读写快照。",
    fig_title="标定快照：保存与恢复分开",
    fig_tag="memento",
    boxes=[
        dict(id="orig", x=40, y=130, w=210, h=100, t="Ecu / calib_t", ty="原对象", mt="gain/offset/mode", note="原对象负责产生快照与从快照恢复；它是唯一能读写快照内部的人。"),
        dict(id="mem", x=330, y=130, w=210, h=100, t="memento", ty="快照", mt="值拷贝，不可变", note="快照保存的是当时的完整状态；之后改原对象不会影响它。"),
        dict(id="care", x=620, y=130, w=180, h=100, t="Caretaker", ty="保管者", mt="只存不用", note="保管者只负责把快照放好、按需交回；它不解析、不修改快照内容。"),
    ],
    arrows=[
        dict(x1=250, y1=165, x2=330, y2=165, label="save()"),
        dict(x1=330, y1=200, x2=250, y2=200, label="restore()", dash=True),
        dict(x1=540, y1=180, x2=620, y2=180, label="保管"),
    ],
    fig_note="点方框：原对象写快照，保管者只搬运。",
    s3="<p class='subh'>C 版快照是结构体值；C++ 版把 <code>Memento</code> 的字段设为私有，只对 <code>Ecu</code> 开放。</p>",
    cfile="memento.c",
    cppfile="memento.cpp",
    demo=dict(
        title="改三次，退回第一次",
        sub="看快照是否随原对象变化。",
        nodes=[
            dict(id="s0", label="初始", sub="12/0/1"),
            dict(id="snap", label="快照", sub="12/0/1"),
            dict(id="s1", label="调参后", sub="30/-8/3"),
            dict(id="back", label="恢复", sub="12/0/1"),
        ],
        steps=[
            dict(hi=["s0"], t="初始标定：gain=12 offset=0 mode=1"),
            dict(hi=["snap"], t="save()：拷贝一份完整快照"),
            dict(hi=["s1"], t="现场调参：gain=30 offset=-8 mode=3"),
            dict(hi=["snap"], t="快照仍是 12/0/1：值拷贝，不受影响"),
            dict(hi=["back"], t="restore()：三个字段整体换回"),
            dict(hi=["s1"], t="恢复后原对象 12/0/1；之后再改也不会污染旧快照"),
        ],
    ),
    rows=[
        ("快照", "<code>memento_t</code> 内嵌 <code>calib_t</code>", "<code>Memento</code> 私有字段", "C 靠约定不碰；C++ 用访问控制"),
        ("保存", "<code>save(&amp;ecu)</code> 值拷贝", "<code>ecu.save()</code>", "都要求深拷贝"),
        ("恢复", "<code>restore(&amp;ecu, &amp;m)</code>", "<code>ecu.restore(m)</code>", "整体替换，不逐字段挑"),
        ("可见性", "结构体公开，谁都能改", "仅 <code>friend Ecu</code> 可读写", "C++ 能把“不可变”落到编译期"),
        ("多份历史", "自己开数组存", "<code>vector&lt;Memento&gt;</code>", "要撤销栈就多存几份"),
    ],
    pitfalls=[
        ("快照必须是深拷贝。", "配置里有字符串或指针时，浅拷贝只复制地址，原对象一改快照就变。"),
        ("别把快照当历史日志。", "备忘录通常只保一份；需要多级撤销要显式做栈，并限制深度。"),
        ("频繁保存有成本。", "每改一个字段存一次，内存和拷贝开销都上来；按“一次调参会话”存一次更合理。"),
        ("恢复不等于回滚外部副作用。", "标定恢复了，已经写进 NVRAM 的值、已经发出的报文不会自动撤回。"),
        ("快照别跨线程共享。", "一个快照被两个线程同时恢复，读到的可能是半更新状态；要么加锁，要么每线程各存一份。"),
    ],
)

C["4.10"] = dict(
    desc="模板方法：自检顺序固定，电源/通信/传感器三步由子类实现。",
    lede="台架自检和现场自检的步骤完全一样：电源、通信、传感器，任何一步失败就中止。差别只在每步的具体实现。<b>模板方法把顺序写在一个 <code>run()</code> 里，把每步留成可覆写的钩子</b>，两个变体共用同一套日志和短路规则。",
    chips=["骨架只写一遍", "步骤可替换", "失败立即中止"],
    s1="""
      <div class="prose">
        <p>复制流程的写法：</p>
        <pre><code>int bench_test(void) { power(); comm(); sensor(); ... }
int field_test(void) { power(); comm(); sensor(); ... }</code></pre>
        <p>两份代码看起来一样，实际已经开始漂移：</p>
        <ul>
          <li><b>顺序不一致。</b>现场版为了快，把传感器挪到通信前面，失败日志就对不上。</li>
          <li><b>短路规则不同。</b>台架版继续跑完，现场版第一步失败就退出，统计口径不同。</li>
          <li><b>加一步要改多处。</b>新增“绝缘检查”，两份都要改，第三份测试桩又漏了。</li>
        </ul>
        <p>模板方法只保留一个 <code>run()</code>：顺序、日志、短路都在骨架里；子类只实现 <code>power()/comm()/sensor()</code>。新增步骤只改骨架一处。</p>
      </div>""",
    s2_sub="骨架在左，两个变体在右；点方框看失败如何中止后续步骤。",
    fig_title="自检骨架与两个变体",
    fig_tag="template method",
    boxes=[
        dict(id="tpl", x=40, y=110, w=240, h=130, t="run()", ty="模板骨架", mt="power → comm → sensor", note="骨架负责顺序、日志、失败中止；它不实现任何一步的具体逻辑。"),
        dict(id="bench", x=420, y=56, w=210, h=90, t="bench", ty="变体", mt="三步都成功", note="台架变体三步都返回成功，用来验证骨架本身。"),
        dict(id="field", x=420, y=206, w=210, h=90, t="field", ty="变体", mt="sensor 失败", note="现场变体在传感器步失败；骨架立即中止，不再跑后续步骤。"),
    ],
    arrows=[
        dict(x1=280, y1=150, x2=420, y2=101),
        dict(x1=280, y1=200, x2=420, y2=251),
    ],
    fig_note="点方框：骨架不关心步骤怎么实现，只关心顺序与失败。",
    s3="<p class='subh'>C 版用函数指针表；C++ 版 <code>run()</code> 非虚、三个步骤虚函数。</p>",
    cfile="template_method.c",
    cppfile="template_method.cpp",
    demo=dict(
        title="跑两个变体，看哪步失败",
        sub="同一骨架，bench 全过，field 在 sensor 步失败。",
        nodes=[
            dict(id="power", label="power", sub="step1"),
            dict(id="comm", label="comm", sub="step2"),
            dict(id="sensor", label="sensor", sub="step3"),
            dict(id="res", label="result", sub="PASS/FAIL"),
        ],
        steps=[
            dict(hi=["power"], t="bench：step1 power OK"),
            dict(hi=["comm"], t="bench：step2 comm OK"),
            dict(hi=["sensor"], t="bench：step3 sensor OK"),
            dict(hi=["res"], t="bench result PASS"),
            dict(hi=["power"], t="field：step1 power OK"),
            dict(hi=["comm"], t="field：step2 comm OK"),
            dict(hi=["sensor"], t="field：step3 sensor FAIL → 立即中止，不再打印 PASS", bad=True),
        ],
    ),
    rows=[
        ("骨架", "<code>run(const selftest_t*)</code>", "<code>SelfTest::run()</code>（非虚）", "顺序只写一份"),
        ("步骤", "三个函数指针", "三个纯虚函数", "C 换表项；C++ 换派生类"),
        ("失败", "返回 0 并立即 return", "返回 false 并立即 return", "短路规则一致"),
        ("日志", "骨架里统一打印", "骨架里统一打印", "变体不再各自打日志"),
        ("新增步骤", "改结构体 + 骨架", "加虚函数 + 骨架", "只改骨架一处，变体补实现"),
    ],
    pitfalls=[
        ("骨架不能太胖。", "把业务判断塞进 <code>run()</code>，子类就失去意义；骨架只该管顺序、日志、短路。"),
        ("虚函数别在构造/析构里调。", "构造时派生类还没建好，调用会分派到基类版本。"),
        ("C 版函数指针要判空。", "表项漏填就是空指针调用，直接崩；初始化时统一校验。"),
        ("失败要带步骤。", "只返回 false，现场不知道是哪步；骨架应输出步骤名或错误码。"),
        ("别把模板方法当“万能流程”。", "步骤之间若有复杂条件分支，硬套骨架会让每个钩子都带一堆参数，反而更难读。"),
    ],
)

C["4.11"] = dict(
    desc="访问者：节点只负责 accept，统计逻辑放进 visitor，新增统计不改节点。",
    lede="诊断树里有 ECU、传感器、执行器三类节点。要统计数量、找最老故障、导出报告，若每个节点自己写一套 <code>count()</code>，节点类会越来越胖。<b>访问者把“遍历时的动作”搬出去</b>：节点只提供 <code>accept()</code>，visitor 决定要做什么。",
    chips=["accept + visit 双向分派", "统计搬出节点", "新增统计不改节点"],
    s1="""
      <div class="prose">
        <p>把统计写进节点，最初只有一行：</p>
        <pre><code>if (node-&gt;kind == ECU) ecus++;
else if (node-&gt;kind == SENSOR) sensors++;</code></pre>
        <ul>
          <li><b>每加一种统计就改节点。</b>数量、最老故障、导出 JSON，全塞进同一个类。</li>
          <li><b>类型判断散落。</b><code>switch (kind)</code> 在每个统计函数里复制，新增节点类型要全改。</li>
          <li><b>节点被迫认识业务。</b>节点本是数据结构，却开始依赖报表格式。</li>
        </ul>
        <p>访问者把动作分成独立对象：节点只回答“我是什么类型”，visitor 针对每种类型写一个 <code>visit()</code>。新增统计只加一个 visitor，节点一行不改。</p>
      </div>""",
    s2_sub="三类节点在左，visitor 在右；箭头是 accept 后的双向分派。",
    fig_title="accept / visit 双向分派",
    fig_tag="visitor",
    boxes=[
        dict(id="ecu", x=50, y=48, w=200, h=76, t="Ecu", ty="节点", mt="accept(v)", note="ECU 节点只把自己的类型告诉 visitor，不关心 visitor 要统计什么。"),
        dict(id="sensor", x=50, y=148, w=200, h=76, t="Sensor", ty="节点", mt="accept(v)", note="传感器节点同样只做分派；节点之间没有继承关系之外的知识。"),
        dict(id="act", x=50, y=248, w=200, h=76, t="Actuator", ty="节点", mt="accept(v)", note="执行器节点也一样；新增节点类型时，visitor 接口要补一个 visit。"),
        dict(id="visitor", x=430, y=120, w=260, h=150, t="Visitor", ty="访问者", mt="visit(Ecu/Sensor/Act)", note="visitor 持有统计状态；一次遍历结束后统一 report。"),
    ],
    arrows=[
        dict(x1=250, y1=86, x2=430, y2=150, label="accept"),
        dict(x1=250, y1=186, x2=430, y2=186, label="accept"),
        dict(x1=250, y1=286, x2=430, y2=235, label="accept"),
    ],
    fig_note="点方框：节点只分派，visitor 才做统计。",
    s3="<p class='subh'>C 版用 <code>accept</code> 函数指针 + 一个 visitor 结构；C++ 版是标准双分派：<code>Element::accept(Visitor&amp;)</code>。</p>",
    cfile="visitor.c",
    cppfile="visitor.cpp",
    demo=dict(
        title="四个节点，一次统计",
        sub="同一遍遍历，visitor 分别处理 ECU、传感器、执行器。",
        nodes=[
            dict(id="e1", label="engine_ecu", sub="ECU"),
            dict(id="s1", label="o2_sensor", sub="SENSOR"),
            dict(id="a1", label="injector", sub="ACTUATOR"),
            dict(id="e2", label="abs_ecu", sub="ECU"),
            dict(id="v", label="Counter", sub="visitor"),
        ],
        steps=[
            dict(hi=["e1", "v"], t="engine_ecu.accept(counter)：分派到 visit(Ecu)"),
            dict(hi=["s1", "v"], t="o2_sensor.accept：分派到 visit(Sensor)"),
            dict(hi=["a1", "v"], t="injector.accept：分派到 visit(Actuator)"),
            dict(hi=["e2", "v"], t="abs_ecu.accept：又一条 ECU"),
            dict(hi=["v"], t="遍历结束：ECU=2，SENSOR=1，ACTUATOR=1"),
            dict(hi=["v"], t="新增“导出 JSON”只写一个新 visitor，节点一行不改"),
        ],
    ),
    rows=[
        ("分派", "<code>accept</code> 函数指针 + <code>visit</code>", "虚 <code>accept</code> + 虚 <code>visit</code>", "C 手写两跳；C++ 编译器生成"),
        ("节点", "<code>node_t</code> + <code>kind</code>", "<code>Ecu/Sensor/Actuator</code> 类", "C 用整数区分；C++ 用类型"),
        ("visitor", "结构体 + 计数", "<code>Counter : Visitor</code>", "统计状态归 visitor"),
        ("新增统计", "加一个 visitor 函数", "加一个派生 visitor", "都不改节点"),
        ("新增节点类型", "加 kind + 改 visit", "加类 + 扩 Visitor 接口", "两边都要动接口，这是代价"),
    ],
    pitfalls=[
        ("访问者不是“遍历器”。", "它只负责“访问到某节点时做什么”；遍历顺序仍由树或调用方决定。"),
        ("接口扩张是硬代价。", "新增节点类型要改所有 visitor；节点类型稳定、统计多变时，访问者才划算。"),
        ("别在 visit 里改节点。", "遍历中修改结构会让后续访问错位；要改就收集后统一处理。"),
        ("C 版函数指针要判空。", "<code>accept</code> 或 <code>visit</code> 漏填会直接崩；初始化时统一校验。"),
        ("C++ 版注意 const 正确性。", "visitor 统计会改自身状态，<code>visit</code> 不能声明为 const；节点的 <code>accept</code> 可以是 const。"),
    ],
)

__all__ = ["C"]

