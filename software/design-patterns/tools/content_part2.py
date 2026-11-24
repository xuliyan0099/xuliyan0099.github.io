# -*- coding: utf-8 -*-
"""第二篇新增章：2.2 抽象工厂、2.3 建造者、2.4 原型。"""

C = {}

C["2.2"] = dict(
    desc="抽象工厂：一个家族同时交付 CAN 驱动与 NVRAM 驱动，避免不同代零件混搭。",
    lede="车型配置里写着 <code>can=bosch</code>、<code>nvram=conti</code>，两行各自看都合法，装到同一辆车上却可能时序对不上、诊断地址对不上。抽象工厂把“同一代的两个零件”绑成一次交付：<b>要 BOSCH 就两个都是 BOSCH，要 CONTI 就两个都是 CONTI</b>。",
    chips=["一个家族两个零件", "换家族不改调用方", "C 用函数表家族 · C++ 用抽象基类"],
    s1="""
      <div class="prose">
        <p>先看坏写法：每个零件各自按名字取。</p>
        <pre><code>can_t    can   = make_can(cfg-&gt;can);      /* "bosch"  */
nvram_t  nv    = make_nvram(cfg-&gt;nvram);  /* "conti"  */</code></pre>
        <p>问题不在“取不到”，而在<b>取到了也能跑，但组合是错的</b>：</p>
        <ul>
          <li><b>时序假设不同。</b>BOSCH 的 CAN 驱动默认 500kbps、周期 10ms；CONTI 的 NVRAM 写一次要 8ms。两个各自达标，叠在一起就超周期。</li>
          <li><b>诊断地址不同。</b>同一份 UDS 服务，两个供应商的 DID 偏移不一样，混搭后读出来的是隔壁字段。</li>
          <li><b>问题只在实车出现。</b>台架上两个零件都能单测通过，装车才偶发，定位成本极高。</li>
        </ul>
        <p>抽象工厂不改零件本身，只改<b>获取方式</b>：家族对象一次返回两个零件，调用方拿不到“单独换一个”的机会。</p>
      </div>""",
    s2_sub="左边是调用方，中间是家族，右边是两个零件。点方框看每一层负责什么。",
    fig_title="家族一次交付两个零件",
    fig_tag="abstract factory",
    boxes=[
        dict(id="client", x=24, y=140, w=150, h=76, t="调用方", ty="业务 / 初始化", mt="只要一对零件", note="调用方只说“我要 BOSCH 这一代”，不分别指定 CAN 和 NVRAM，从源头断掉混搭的可能。"),
        dict(id="family", x=250, y=140, w=190, h=80, t="family_t / Family", ty="零件家族", mt="make_can + make_nvram", note="家族是唯一知道“哪两个零件属于同一代”的对象；换家族就是整套换，不存在只换一半。"),
        dict(id="can", x=520, y=62, w=190, h=72, t="can_t / Can", ty="通信零件", mt="send(frame)", note="CAN 驱动只暴露 send；具体用哪家的实现由家族决定，调用方看不到供应商名字。"),
        dict(id="nvram", x=520, y=212, w=190, h=72, t="nvram_t / Nvram", ty="存储零件", mt="save(value)", note="NVRAM 与 CAN 同代：写时序、地址布局都按同一份规范来。"),
    ],
    arrows=[
        dict(x1=174, y1=178, x2=250, y2=178, label="取家族"),
        dict(x1=440, y1=160, x2=520, y2=108, label="造 CAN"),
        dict(x1=440, y1=200, x2=520, y2=242, label="造 NVRAM"),
    ],
    fig_note="点方框：家族负责“成套”，零件只负责自己的接口。",
    s3="<p class='subh'>C 版把家族写成“返回两个函数表”的结构；C++ 版把家族写成抽象基类，零件用 unique_ptr 交付。</p>",
    cfile="abstract_factory.c",
    cppfile="abstract_factory.cpp",
    demo=dict(
        title="换一次家族，看两个零件是否成套",
        sub="同一段业务流程，只切换家族；CAN 与 NVRAM 的厂牌始终一致。",
        nodes=[
            dict(id="fam", label="家族", sub="BOSCH / CONTI"),
            dict(id="can", label="CAN", sub="send()"),
            dict(id="nv", label="NVRAM", sub="save()"),
            dict(id="use", label="业务流程", sub="发一帧 + 存一次"),
        ],
        steps=[
            dict(hi=["fam"], t="选家族 BOSCH：一次拿到 CAN 与 NVRAM 两个零件"),
            dict(hi=["can"], t="CAN 零件 = BOSCH，波特率 500k、周期 10ms"),
            dict(hi=["nv"], t="NVRAM 零件 = BOSCH，写周期 8ms，符合同一份时序预算"),
            dict(hi=["use"], t="业务流程：发送 0x18FF50E5，保存标定值 7"),
            dict(hi=["fam", "can", "nv"], t="切到家族 CONTI：两个零件同时换，业务流程一行不改"),
            dict(hi=["use"], t="再跑同一段流程：报文与保存都走 CONTI，没有混搭"),
        ],
    ),
    rows=[
        ("家族", "<code>family_t</code> 结构 + 两个函数指针", "<code>Family</code> 抽象基类", "C 的家族是数据；C++ 的家族是类型"),
        ("零件交付", "返回结构体（函数表按值拷贝）", "返回 <code>unique_ptr</code>", "C 没有所有权概念，靠约定；C++ 由编译器兜底"),
        ("新增家族", "加一组 make_* 函数 + 一条表项", "加一个派生类", "两边都是一处新增，不动调用方"),
        ("混搭可能性", "调用方仍可手动取单个零件", "接口上就拿不到单个零件", "C 要靠代码评审守住，C++ 能靠类型挡住"),
        ("零件生命周期", "静态/栈对象，谁取谁管", "<code>unique_ptr</code> 归调用方", "跨线程共享时要另加锁或引用计数"),
    ],
    pitfalls=[
        ("家族不是“越多越好”。", "两个家族刚好；五个家族会让每个新零件都要乘五份实现，先确认真的存在“整代切换”的需求。"),
        ("别把可变状态塞进家族。", "家族对象应是只读的“说明书”，当前车速、当前档位属于具体零件或上下文。"),
        ("C 版函数表按值返回，别存局部指针。", "函数表里若带指向栈上数据的 <code>void *ctx</code>，返回后会悬空；要么全静态，要么显式传上下文。"),
        ("C++ 版注意虚析构。", "基类析构必须是 <code>virtual</code>，否则 <code>unique_ptr</code> 删除派生对象时只析构基类。"),
        ("测试要成对跑。", "单测每个零件通过不代表组合通过；至少加一组“同代组合”的集成用例，把时序预算跑满。"),
    ],
)

C["2.3"] = dict(
    desc="建造者：把 CAN 帧的 id、数据、CRC 拆成可检查的步骤，最后一次性交付。",
    lede="拼一帧 CAN 报文有七八个字段，顺序错了不一定报错，可能只是 CRC 不对、DLC 不对。<b>建造者把“拼装”变成一条有步骤的流水线</b>：每一步只改一个字段，最后 <code>build()</code> 才交出成品；中途可以校验、可以复用，也可以随时丢弃重来。",
    chips=["步骤可查", "成品只交付一次", "复用 builder 不残留上一帧"],
    s1="""
      <div class="prose">
        <p>常见写法是一个大初始化：</p>
        <pre><code>frame_t f = { id, dlc, {b0,b1,b2}, crc };</p></code></pre>
        <p>字段一多就出三类问题：</p>
        <ul>
          <li><b>顺序靠记。</b>CRC 必须在数据之后算；有人先算 CRC 再填数据，台架上偶尔能过，因为数据恰好没变。</li>
          <li><b>复用会串味。</b>同一个栈上的 <code>frame_t</code> 反复用，上一帧的 <code>data[3..7]</code> 没清，DLC 又写成 8，发出去就是脏数据。</li>
          <li><b>中途失败没法收场。</b>拼到一半发现 id 非法，只能 <code>return</code>，已写进去的半成品留在对象里。</li>
        </ul>
        <p>建造者把每个字段的写入变成一个显式步骤，并提供 <code>start()</code> 清底、<code>build()</code> 交付。调用方看到的是“开始 → 填 id → 填数据 → 算 CRC → 交付”，而不是一堆裸赋值。</p>
      </div>""",
    s2_sub="四个角色排成一条线：调用方发起，builder 累积，成品交付给发送层。",
    fig_title="一帧报文的建造流水线",
    fig_tag="builder",
    boxes=[
        dict(id="client", x=24, y=140, w=150, h=76, t="调用方", ty="诊断 / 周期任务", mt="start → 填字段", note="调用方只按步骤调用，不直接碰 frame_t 的内部字段，也就不会漏清上一帧。"),
        dict(id="builder", x=230, y=140, w=200, h=80, t="builder_t / Builder", ty="累积状态", mt="id / data / crc", note="builder 持有半成品；每一步只改一个字段，可以在任意一步插入校验。"),
        dict(id="frame", x=480, y=140, w=170, h=76, t="frame_t / Frame", ty="成品", mt="只读交付", note="build() 返回一份完整帧；之后 builder 再 start 不会影响已经交出去的副本。"),
        dict(id="tx", x=700, y=140, w=150, h=76, t="CAN 发送", ty="下游", mt="send(frame)", note="发送层只接收成品，不关心中间步骤；失败可以在交付前拦下。"),
    ],
    arrows=[
        dict(x1=174, y1=178, x2=230, y2=178, label="步骤"),
        dict(x1=430, y1=178, x2=480, y2=178, label="build"),
        dict(x1=650, y1=178, x2=700, y2=178, label="交付"),
    ],
    fig_note="点方框：builder 负责累积，frame 只负责被交付。",
    s3="<p class='subh'>C 版是一组 <code>b_*</code> 函数 + 结构体；C++ 版把每个步骤做成返回 <code>Builder&amp;</code> 的链式方法。</p>",
    cfile="builder.c",
    cppfile="builder.cpp",
    demo=dict(
        title="一步一步拼一帧",
        sub="点“单步”：看每个字段何时写入、CRC 何时才能算。",
        nodes=[
            dict(id="id", label="ID", sub="0x18FF50E5"),
            dict(id="data", label="DATA", sub="3 字节"),
            dict(id="crc", label="CRC", sub="最后算"),
            dict(id="build", label="BUILD", sub="交付成品"),
            dict(id="send", label="SEND", sub="发送层"),
        ],
        steps=[
            dict(hi=["id"], t="start() 清底：id=0、dlc=0、crc=0，上一帧不残留"),
            dict(hi=["id"], t="填 id = 0x18FF50E5"),
            dict(hi=["data"], t="填数据 10 20 30，dlc 跟着变成 3"),
            dict(hi=["crc"], t="数据到齐后才算 CRC：sum(id + data) & 0xFF = 0x45"),
            dict(hi=["build"], t="build() 交付 frame1；builder 之后可以重新 start"),
            dict(hi=["data", "build"], t="第二帧复用同一个 builder：dlc 从 3 变 8，没有串上一帧的残留"),
            dict(hi=["send"], t="两帧分别交给发送层，成品互不影响"),
        ],
    ),
    rows=[
        ("半成品放哪", "<code>builder_t.f</code> 内嵌", "<code>Builder::f_</code> 私有成员", "都在 builder 里，调用方拿不到半成品"),
        ("步骤接口", "<code>b_id()</code> / <code>b_data()</code> / <code>b_crc()</code>", "链式 <code>id().data().crc()</code>", "C 靠命名约束顺序，C++ 靠返回值把顺序写进表达式"),
        ("重置", "<code>b_start()</code> 显式清", "<code>start()</code> 重新赋值 <code>Frame{}</code>", "C 要记得清每个字段；C++ 赋值一次全清"),
        ("交付", "按值返回 <code>frame_t</code>", "按值返回 <code>Frame</code>", "都是副本，交付后改 builder 不影响成品"),
        ("超长数据", "<code>b_data()</code> 里截到 8 字节", "同样截到 8 字节", "规则一致，但都要在文档里写明，别让调用方猜"),
    ],
    pitfalls=[
        ("CRC 必须在数据之后。", "链式调用看起来自由，但 <code>crc()</code> 依赖 <code>dlc</code> 与数据；把它写在最前，算出来一定是错的。"),
        ("build() 之后别再改成品。", "按值返回意味着成品是副本；如果后续要改，重新 start 再建一帧，不要绕过 builder 直接改字段。"),
        ("数据截断要报错。", "超过 8 字节静默截断，调用方以为全发出去了；至少要返回状态或日志，不能只截不说。"),
        ("builder 不是线程安全的。", "一个 builder 只给一个任务用；多线程共用要加锁，或者每个线程各建一个。"),
        ("步骤别无限膨胀。", "字段超过十几个、还带条件分支时，考虑把“帧描述”做成表驱动，而不是继续加方法。"),
    ],
)

C["2.4"] = dict(
    desc="原型：配置原型登记在册，用时克隆一份，改副本不动原版。",
    lede="诊断配置有十几项：超时、重试、波特率、过滤表。每次初始化都从头赋值，代码重复还容易漏项。<b>原型模式先把一份“标准配置”登记成原型，用的时候按名字克隆</b>，再在副本上改；原型永远不被业务代码碰到。",
    chips=["原型只读", "克隆即得完整配置", "改副本不污染原型"],
    s1="""
      <div class="prose">
        <p>坏写法通常长这样：</p>
        <pre><code>config_t cfg = { "default", 500, 3 };
/* 另一个模块又抄一遍，改了两个字段 */</code></pre>
        <p>重复初始化带来三个后果：</p>
        <ul>
          <li><b>字段漏填。</b>新增一个 <code>bus_off_recovery</code>，三处初始化只改了两处，第三处默默用 0。</li>
          <li><b>共享同一份。</b>为了省事把指针传出去，A 模块改超时，B 模块的重试也跟着变。</li>
          <li><b>默认值散落。</b>“快速模式”的 120ms 只写在某个注释里，没人知道它和“默认模式”差在哪。</li>
        </ul>
        <p>原型把“标准长什么样”收进注册表，克隆负责复制。<b>原型是只读的模板，副本是调用方自己的</b>，两者从类型上就该分开。</p>
      </div>""",
    s2_sub="注册表按名字找原型，克隆产出独立副本；原型始终不动。",
    fig_title="登记原型，按名字克隆",
    fig_tag="prototype",
    boxes=[
        dict(id="reg", x=24, y=130, w=190, h=100, t="原型注册表", ty="PROTOS / map", mt="default / fast", note="注册表只存“原型对象”，不存业务状态；查找按名字，找不到就明确报 miss。"),
        dict(id="proto", x=270, y=130, w=190, h=100, t="原型 config_t", ty="只读模板", mt="timeout=120 retry=1", note="原型是默认值的唯一出处；任何业务代码都不应直接修改它。"),
        dict(id="a", x=530, y=62, w=180, h=76, t="副本 A", ty="clone", mt="可独立修改", note="克隆得到完整字段，改 A 的超时不会影响 B，也不会影响原型。"),
        dict(id="b", x=530, y=200, w=180, h=76, t="副本 B", ty="clone", mt="可独立修改", note="两个副本互不影响；生命周期归各自调用方。"),
    ],
    arrows=[
        dict(x1=214, y1=180, x2=270, y2=180, label="按名字"),
        dict(x1=460, y1=160, x2=530, y2=110, label="clone"),
        dict(x1=460, y1=200, x2=530, y2=232, label="clone"),
    ],
    fig_note="点方框：原型只读，副本才有写权限。",
    s3="<p class='subh'>C 版的克隆是结构体整体赋值；C++ 版由 <code>clone()</code> 返回 <code>unique_ptr</code>，注册表只持有原型。</p>",
    cfile="prototype.c",
    cppfile="prototype.cpp",
    demo=dict(
        title="克隆两份，只改其中一份",
        sub="看 timeout 在原型、副本 A、副本 B 之间是否互相影响。",
        nodes=[
            dict(id="proto", label="原型 fast", sub="timeout=120"),
            dict(id="a", label="副本 A", sub="timeout=120"),
            dict(id="b", label="副本 B", sub="timeout=120"),
            dict(id="check", label="回读原型", sub="应仍为 120"),
        ],
        steps=[
            dict(hi=["proto"], t="注册原型 fast：timeout=120、retry=1"),
            dict(hi=["a"], t="clone → 副本 A，字段完整复制"),
            dict(hi=["b"], t="再 clone → 副本 B，与 A 互不共享"),
            dict(hi=["b"], t="改 B：timeout=90、name=fast-tuned"),
            dict(hi=["a"], t="副本 A 仍是 120；改 B 没有波及 A"),
            dict(hi=["check"], t="回读原型：timeout 仍是 120，原型未被写"),
            dict(hi=["proto"], t="查一个不存在的名字 slow：明确返回 miss，而不是造一份默认配置"),
        ],
    ),
    rows=[
        ("原型存放", "<code>proto_t PROTOS[]</code> 静态数组", "<code>map&lt;string, unique_ptr&lt;Config&gt;&gt;</code>", "C 固定上限；C++ 可动态增删"),
        ("克隆动作", "结构体整体赋值", "<code>clone()</code> 返回 <code>unique_ptr</code>", "C 的深拷贝靠“没有指针成员”；C++ 要在 clone 里写清楚"),
        ("副本所有权", "调用方栈/静态对象", "<code>unique_ptr</code> 独占", "C 要自己保证生命周期；C++ 由所有权类型表达"),
        ("找不到原型", "返回 <code>NULL</code>", "返回空指针 / 抛异常", "都要显式处理，别偷偷造默认对象"),
        ("新增原型", "加一条表项", "注册表插入一项", "两边都不改调用方"),
    ],
    pitfalls=[
        ("浅拷贝是最常见的坑。", "结构体里一旦有指针或字符串指针，整体赋值只复制地址；C 版要么禁止指针成员，要么写显式 deep_clone。"),
        ("原型必须只读。", "把原型指针直接交给业务代码，等于把“模板”变成“共享全局变量”；接口上只暴露 clone。"),
        ("克隆不是免费。", "配置很大时，克隆比“读一份只读视图”更贵；如果业务只读，考虑返回 <code>const</code> 引用。"),
        ("注册表要防并发。", "启动阶段登记、运行期只读最安全；运行期动态注册要加锁。"),
        ("C++ 版注意切片。", "<code>clone()</code> 必须是虚函数并返回 <code>unique_ptr</code>，否则通过基类指针克隆会得到基类副本。"),
    ],
)

__all__ = ["C"]
