# -*- coding: utf-8 -*-
"""第三篇新增章：桥接、组合、装饰、外观、享元、代理。"""

C = {}

C["3.2"] = dict(
    desc="桥接：把 UDS/OBD 与 CAN/LIN 两个维度分开，四种组合不必写四份代码。",
    lede="诊断协议有 UDS 和 OBD，物理层有 CAN 和 LIN。若按“协议 + 物理层”各写一个类，就是 2×2 四份几乎重复的代码；再加一种物理层，要新增四份。<b>桥接把两维各自抽象，中间只留一条引用</b>，组合在运行时决定，新增一侧只改一侧。",
    chips=["2×2 组合不写 4 份", "协议不关心物理层", "物理层不关心服务"],
    s1="""
      <div class="prose">
        <p>坏写法是把两维焊在一起：</p>
        <pre><code>void uds_over_can(const char *svc);
void uds_over_lin(const char *svc);
void obd_over_can(const char *svc);
void obd_over_lin(const char *svc);</code></pre>
        <p>四种组合只是“拼字符串”的差别，却要维护四份函数。真正的问题在后面：</p>
        <ul>
          <li><b>加一个物理层就乘二。</b>再来一个 FlexRay，就要补 UDS/FlexRay、OBD/FlexRay 两份；漏一份就是运行时 404。</li>
          <li><b>协议细节散落。</b>UDS 的会话保持、OBD 的 PID 编码，被复制到每条物理层分支里，改一处要改四遍。</li>
          <li><b>测试矩阵爆炸。</b>2 个协议 × 3 个物理层 = 6 条路径，每条都要单独写用例。</li>
        </ul>
        <p>桥接让协议只依赖“能发一帧”的抽象，物理层只负责“怎么发”。组合放在调用方，两边都能独立扩展。</p>
      </div>""",
    s2_sub="左边是协议，右边是物理层，四条线是四种组合；虚线表示同一协议可以换物理层。",
    fig_title="协议 × 物理层：两维各自抽象",
    fig_tag="bridge",
    boxes=[
        dict(id="uds", x=40, y=70, w=190, h=80, t="UDS", ty="诊断协议", mt="0x22 读数据", note="UDS 只管服务语义：会话、安全访问、DID 编码；它不知道帧最后走在 CAN 还是 LIN。"),
        dict(id="obd", x=40, y=220, w=190, h=80, t="OBD", ty="排放协议", mt="PID 0x0C", note="OBD 的 PID 编码与 UDS 不同，但同样只依赖“发一帧”的抽象。"),
        dict(id="can", x=470, y=70, w=190, h=80, t="CAN", ty="物理层", mt="500kbps / 11bit", note="CAN 只负责把字符串变成帧发出去；它不解析 UDS 服务，也不认识 OBD 的 PID。"),
        dict(id="lin", x=470, y=220, w=190, h=80, t="LIN", ty="物理层", mt="19.2kbps / 主从", note="LIN 的调度表、主从角色都在这一层；换物理层不需要改协议代码。"),
    ],
    arrows=[
        dict(x1=230, y1=110, x2=470, y2=110, label="UDS over CAN"),
        dict(x1=230, y1=118, x2=470, y2=250, label="UDS over LIN", dash=True),
        dict(x1=230, y1=250, x2=470, y2=118, label="OBD over CAN", dash=True),
        dict(x1=230, y1=262, x2=470, y2=262, label="OBD over LIN"),
    ],
    fig_note="点方框：协议与物理层各自只守一边，组合由调用方拼。",
    s3="<p class='subh'>C 版用两张表（link_t、proto_t）在运行时拼；C++ 版用两个抽象基类，组合时只传引用。</p>",
    cfile="bridge.c",
    cppfile="bridge.cpp",
    demo=dict(
        title="四种组合，只换一侧",
        sub="同一句服务请求，依次走 UDS/OBD 与 CAN/LIN 的组合。",
        nodes=[
            dict(id="uds", label="UDS", sub="服务语义"),
            dict(id="obd", label="OBD", sub="PID 语义"),
            dict(id="can", label="CAN", sub="物理层"),
            dict(id="lin", label="LIN", sub="物理层"),
        ],
        steps=[
            dict(hi=["uds", "can"], t="UDS over CAN：协议拼好服务串，交给 CAN 发"),
            dict(hi=["uds", "lin"], t="同一份 UDS，只把物理层换成 LIN，协议代码没动"),
            dict(hi=["obd", "can"], t="换成 OBD：只换协议侧，CAN 仍然只负责发帧"),
            dict(hi=["obd", "lin"], t="OBD over LIN：两侧都换，仍然没有第四份实现"),
            dict(hi=["uds", "obd", "can", "lin"], t="四种组合共用两条抽象；新增 FlexRay 只需加一个物理层"),
        ],
    ),
    rows=[
        ("协议抽象", "<code>proto_t</code> + 函数指针", "<code>Protocol</code> 抽象基类", "C 的协议是结构体，C++ 是类型"),
        ("物理层抽象", "<code>link_t</code> + <code>send()</code>", "<code>Link</code> 抽象基类", "都只暴露“发一帧”"),
        ("组合方式", "运行时给 <code>proto.link</code> 赋值", "构造时传 <code>Link&amp;</code>", "C 可换绑，C++ 用引用固定"),
        ("新增物理层", "加一个 <code>link_t</code> 表项", "加一个派生类", "两边都不动协议"),
        ("生命周期", "静态表，无所有权", "引用，不拥有", "物理层通常比协议活得久"),
    ],
    pitfalls=[
        ("桥接不是“多一层就高级”。", "只有两维确实独立扩展时才值得；如果物理层永远只有 CAN，直接写反而清楚。"),
        ("别让协议知道帧格式。", "协议一旦开始拼 CAN ID、算 DLC，桥接就退化成四份实现；协议只该产出“服务 + 参数”。"),
        ("C 版换绑要防悬空。", "运行时改 <code>proto.link</code> 指向栈上的 <code>link_t</code>，函数返回后就悬空；物理层应是静态或长生命周期对象。"),
        ("C++ 引用成员不可重新绑定。", "<code>Protocol</code> 持 <code>Link&amp;</code> 后不能换物理层；需要运行时切换就用指针或 <code>std::reference_wrapper</code>。"),
        ("组合测试仍要覆盖。", "代码只有两份，但行为有四种；至少每个组合跑一条真实服务，别只测编译通过。"),
    ],
)

C["3.3"] = dict(
    desc="组合：整车、总成、零件组成一棵树，同一套 run() 从根遍历到叶。",
    lede="整车自检要遍历“整车 → 总成 → 零件”。如果枝和叶用两套接口，遍历代码就要在每一层判断“这是组还是零件”。<b>组合模式让枝和叶实现同一个接口</b>：组自己递归孩子，叶只报结果，调用方从根调一次就够。",
    chips=["枝与叶同一接口", "遍历只写一遍", "增删子树不改调用方"],
    s1="""
      <div class="prose">
        <p>坏写法通常是两套结构 + 手写递归：</p>
        <pre><code>if (node-&gt;is_group) {
    for (child in node-&gt;children) run_group(child);
} else {
    run_leaf(node);
}</code></pre>
        <p>这行代码会在每个层级复制一遍，问题随之而来：</p>
        <ul>
          <li><b>层级一深就漏。</b>“总成里还有子总成”时，<code>run_group</code> 忘了递归，孙子节点永远不跑。</li>
          <li><b>统计口径不一。</b>有的分支只算叶子，有的把组也算一项，最后总数对不上。</li>
          <li><b>新增节点类型要改遍历。</b>加一个“虚拟节点”或“占位节点”，所有遍历函数都要动。</li>
        </ul>
        <p>组合把“遍历孩子”收进组自己：组的 <code>run()</code> 负责递归，叶的 <code>run()</code> 只报自己的结果。调用方只看到 <code>run(root)</code>。</p>
      </div>""",
    s2_sub="三层树：整车是根，动力/底盘是枝，发动机、变速箱、ABS 是叶；点方框看每层职责。",
    fig_title="整车自检树：枝和叶同一接口",
    fig_tag="composite",
    boxes=[
        dict(id="root", x=350, y=34, w=180, h=72, t="vehicle", ty="组（根）", mt="run(depth=0)", note="根只做一件事：把 depth 传给孩子，收集每个孩子的结果；它自己不判断零件好坏。"),
        dict(id="power", x=180, y=150, w=180, h=72, t="powertrain", ty="组", mt="engine + gearbox", note="总成是“组”：它递归两个孩子，任一失败就把失败往上抛。"),
        dict(id="chassis", x=520, y=150, w=180, h=72, t="chassis", ty="组", mt="abs", note="同样是组，但只有一个孩子；组合不要求孩子数量一致。"),
        dict(id="eng", x=60, y=268, w=150, h=64, t="engine", ty="叶", mt="PASS", note="叶不递归，只返回自己的通过/失败；它不知道自己在树的第几层。"),
        dict(id="gear", x=230, y=268, w=150, h=64, t="gearbox", ty="叶", mt="FAIL", note="一个叶失败，整棵树的最终结果就是 FAIL；失败原因由调用方按路径定位。"),
        dict(id="abs", x=520, y=268, w=150, h=64, t="abs", ty="叶", mt="PASS", note="叶的接口与组完全一致，所以遍历代码不需要类型判断。"),
    ],
    arrows=[
        dict(x1=420, y1=106, x2=300, y2=150),
        dict(x1=470, y1=106, x2=580, y2=150),
        dict(x1=250, y1=222, x2=170, y2=268),
        dict(x1=310, y1=222, x2=310, y2=268),
        dict(x1=610, y1=222, x2=595, y2=268, label=""),
    ],
    fig_note="点方框：组负责递归，叶负责报结果。",
    s3="<p class='subh'>C 版用孩子数组 + 统一 <code>run_node()</code>；C++ 版用 <code>unique_ptr</code> 容器，析构自动递归。</p>",
    cfile="composite.c",
    cppfile="composite.cpp",
    demo=dict(
        title="自检树从根跑到叶",
        sub="单步看递归顺序：先整车，再动力，最后到底盘。",
        nodes=[
            dict(id="root", label="vehicle", sub="组"),
            dict(id="power", label="powertrain", sub="组"),
            dict(id="eng", label="engine", sub="叶 PASS"),
            dict(id="gear", label="gearbox", sub="叶 FAIL"),
            dict(id="chassis", label="chassis", sub="组"),
            dict(id="abs", label="abs", sub="叶 PASS"),
        ],
        steps=[
            dict(hi=["root"], t="vehicle.run(0)：打印根，开始遍历孩子"),
            dict(hi=["power"], t="进入 powertrain：它是组，继续递归"),
            dict(hi=["eng"], t="engine 是叶：报 PASS，返回到 powertrain"),
            dict(hi=["gear"], t="gearbox 是叶：报 FAIL，powertrain 记为失败"),
            dict(hi=["chassis"], t="powertrain 返回后，进入 chassis"),
            dict(hi=["abs"], t="abs 是叶：报 PASS"),
            dict(hi=["root", "power"], t="整车汇总：任一孩子失败 → FAIL，路径可定位到 gearbox"),
        ],
    ),
    rows=[
        ("孩子容器", "<code>node_t *kids[4]</code>", "<code>vector&lt;unique_ptr&lt;Component&gt;&gt;</code>", "C 固定上限；C++ 动态扩容且自动释放"),
        ("统一接口", "函数指针 <code>run_node</code>", "纯虚 <code>run()</code>", "都让枝和叶长得一样"),
        ("遍历", "组内部递归", "组内部递归", "调用方只调一次根"),
        ("失败传播", "返回 int，逐层与", "返回 bool，逐层与", "口径要统一，别有的层吞掉失败"),
        ("增删子树", "改数组 + nkids", "push_back / erase", "C 要手维护计数，C++ 容器代劳"),
    ],
    pitfalls=[
        ("别在叶里访问父节点。", "叶一旦反向依赖父节点，树就变成图，递归容易成环；需要上下文就通过参数往下传。"),
        ("递归深度要设上限。", "诊断树通常不深，但配置错误可能造出自引用；入口处限制 depth 或检测环。"),
        ("组也可以是空组。", "空组应明确返回“通过”还是“未配置”，别让 0 个孩子默默算 PASS 掩盖配置缺失。"),
        ("C 版孩子数组要初始化。", "<code>kids</code> 未清零、<code>nkids</code> 又写大了，会读到野指针；统一用指定初始化器。"),
        ("统计不要混层。", "“通过率”按叶算还是按组算要写死；否则同一棵树两个报表两个数。"),
    ],
)

C["3.4"] = dict(
    desc="装饰器：读数流水线逐层加 offset、clamp，顺序可换，底层只读一次。",
    lede="传感器读数进来后要做三件事：加偏移、限幅、必要时再滤波。若每加一个处理就复制一份 <code>read_sensor()</code>，很快就有十几个版本。<b>装饰器把每件事做成一层</b>，层与层串起来，顺序由调用方决定，底层读数只写一次。",
    chips=["一层只做一件事", "顺序可换、可拆", "底层只读一次"],
    s1="""
      <div class="prose">
        <p>坏写法是把处理塞进同一个函数：</p>
        <pre><code>int read_sensor(void) {
    int v = adc_read();
    v += OFFSET;
    if (v &lt; 0) v = 0;
    if (v &gt; 40) v = 40;
    return v;
}</code></pre>
        <p>三个处理看着简单，问题在扩展时爆发：</p>
        <ul>
          <li><b>顺序写死。</b>先限幅再偏移，和先偏移再限幅，结果不同；业务想换顺序只能改函数。</li>
          <li><b>无法只取原始值。</b>标定时需要 raw=42，函数却总是返回处理后的 40。</li>
          <li><b>每加一层就复制。</b>再加中值滤波，又出现 <code>read_sensor_filtered()</code>，调用方开始猜该用哪个。</li>
        </ul>
        <p>装饰器把“取原始值”和“处理”分开：最底层只返回 raw，每一层包住下一层，在它的结果上做一件事。要几层、什么顺序，拼链时决定。</p>
      </div>""",
    s2_sub="一条四段流水线：raw → offset → clamp → 业务；每层只依赖它的内层。",
    fig_title="读数装饰链",
    fig_tag="decorator",
    boxes=[
        dict(id="raw", x=24, y=140, w=160, h=76, t="raw", ty="最底层", mt="read() = 42", note="最底层只做一次真实采样，不做任何加工；标定和诊断可以直接拿它。"),
        dict(id="off", x=210, y=140, w=170, h=76, t="offset", ty="装饰层", mt="+5", note="offset 只关心“在内层结果上加多少”；它不知道内层是 raw 还是另一层装饰。"),
        dict(id="clamp", x=405, y=140, w=170, h=76, t="clamp", ty="装饰层", mt="0..40", note="clamp 只做限幅；顺序换到 offset 之前，42 会先被限成 40，再加 5 得 45。"),
        dict(id="sink", x=600, y=140, w=160, h=76, t="业务", ty="调用方", mt="拿到 40", note="业务只看到最终值；它不关心中间有几层、每层做了什么。"),
    ],
    arrows=[
        dict(x1=184, y1=178, x2=210, y2=178),
        dict(x1=380, y1=178, x2=405, y2=178),
        dict(x1=575, y1=178, x2=600, y2=178),
    ],
    fig_note="点方框：每层只读内层，不知道更外面还有谁。",
    s3="<p class='subh'>C 版用 <code>stage_t</code> 链 + 函数指针；C++ 版用 <code>unique_ptr</code> 串链，析构自动拆。</p>",
    cfile="decorator.c",
    cppfile="decorator.cpp",
    demo=dict(
        title="换顺序，看结果怎么变",
        sub="同一组参数，先 offset 后 clamp 与先 clamp 后 offset 结果不同。",
        nodes=[
            dict(id="raw", label="raw", sub="42"),
            dict(id="off", label="offset", sub="+5"),
            dict(id="clamp", label="clamp", sub="0..40"),
            dict(id="out", label="输出", sub="业务值"),
        ],
        steps=[
            dict(hi=["raw"], t="raw 采样：42"),
            dict(hi=["off"], t="offset 层：42 + 5 = 47"),
            dict(hi=["clamp"], t="clamp 层：47 超过 40，限成 40"),
            dict(hi=["out"], t="业务拿到 40"),
            dict(hi=["off"], t="换顺序：先把 42 限到 40"),
            dict(hi=["clamp"], t="再加 5 → 45，最终值变了：顺序就是语义"),
            dict(hi=["out"], t="所以链的顺序必须显式定义，不能靠“看起来差不多”"),
        ],
    ),
    rows=[
        ("链节点", "<code>stage_t</code> + <code>apply()</code>", "<code>Sensor</code> 派生类", "C 的层是数据，C++ 的层是对象"),
        ("内层引用", "<code>stage_t *inner</code>", "<code>unique_ptr&lt;Sensor&gt; in_</code>", "C 要保证内层活得久；C++ 所有权向上传递"),
        ("调用", "<code>clamp.apply(&amp;clamp, raw)</code>", "<code>clamp-&gt;read(raw)</code>", "都从最外层进，逐层向内"),
        ("顺序", "拼链时决定", "构造时决定", "都一样：顺序是业务语义的一部分"),
        ("拆链", "手改 <code>inner</code>", "<code>reset()</code> 或重建", "C 要小心悬空；C++ 释放即拆"),
    ],
    pitfalls=[
        ("装饰层不能有状态假设。", "offset 层若缓存了“上一次内层值”，换顺序或换内层就会读到过期数据。"),
        ("别在层里做重活。", "每层只做一件事；滤波、标定、限幅混在一层，等于把原来的大函数拆成名字不同的大函数。"),
        ("C 版注意 <code>inner</code> 生命周期。", "内层是栈对象时，外层不能比它活得久；要么全静态，要么显式管理。"),
        ("C++ 版注意虚析构。", "基类析构非虚，<code>unique_ptr</code> 删除时会漏掉派生层的资源。"),
        ("顺序写进文档和测试。", "同一组参数换顺序结果不同，测试要覆盖业务实际使用的顺序，而不是随手拼一条。"),
    ],
)

C["3.5"] = dict(
    desc="外观：把上电五步收成一个 vehicle_start()，失败按相反顺序回滚。",
    lede="上电不是一句“点火”：继电器吸合、油泵建压、ECU 握手、防盗校验、仪表自检，顺序错了会报故障，失败还要回滚。<b>外观模式把这些收进一个入口</b>，调用方只看到成功/失败；子系统仍然可以单独测试。",
    chips=["一个入口五步顺序", "失败按相反顺序回滚", "子系统仍可单测"],
    s1="""
      <div class="prose">
        <p>没有外观时，每个调用方都背一遍流程：</p>
        <pre><code>ignition_on();
fuel_pump_on();
ecu_handshake();
cluster_self_test();
immobilizer_check();</code></pre>
        <p>只要有一个调用方顺序写错，就出现“能点火但仪表不亮”这类怪故障：</p>
        <ul>
          <li><b>顺序散落。</b>台架脚本、诊断工具、整车控制器各有一份，版本很快不一致。</li>
          <li><b>失败不回滚。</b>油泵建压失败，继电器还吸着，下次上电带着残压。</li>
          <li><b>子系统被绑死。</b>想单独测油泵，必须先跑完整套流程，测试变慢。</li>
        </ul>
        <p>外观提供一个 <code>vehicle_start()</code>：内部按固定顺序调用，任一步失败就按相反顺序撤销，返回明确的错误码。子系统接口不变，仍可被单测直接调用。</p>
      </div>""",
    s2_sub="左边调用方，中间外观，右边三个子系统；点方框看每一步失败时谁负责回滚。",
    fig_title="上电外观：一个入口，五个步骤",
    fig_tag="facade",
    boxes=[
        dict(id="client", x=24, y=140, w=170, h=80, t="调用方", ty="整车控制 / 诊断", mt="只调 start()", note="调用方不再关心顺序与回滚；它只根据返回码决定是否允许起动机。"),
        dict(id="facade", x=230, y=120, w=210, h=120, t="vehicle_start()", ty="外观", mt="顺序 + 回滚", note="外观知道五步的依赖关系；它不实现任何子系统，只编排。"),
        dict(id="ign", x=520, y=44, w=190, h=70, t="ignition", ty="子系统", mt="relay on/off", note="点火继电器：失败时外观负责把它关掉。"),
        dict(id="pump", x=520, y=145, w=190, h=70, t="fuel_pump", ty="子系统", mt="建压 3.0bar", note="油泵：建压失败要停泵，并把点火退回。"),
        dict(id="ecu", x=520, y=246, w=190, h=70, t="ecu", ty="子系统", mt="seed/key", note="ECU 握手：失败要停泵、断点火；每一步都能独立单测。"),
    ],
    arrows=[
        dict(x1=194, y1=180, x2=230, y2=180, label="start"),
        dict(x1=440, y1=145, x2=520, y2=79),
        dict(x1=440, y1=180, x2=520, y2=180),
        dict(x1=440, y1=215, x2=520, y2=281),
    ],
    fig_note="点方框：外观只编排，不替子系统干活。",
    s3="<p class='subh'>C 版是一个函数 + 静态子系统；C++ 版把子系统收进类成员，<code>start()</code> 负责顺序与回滚。</p>",
    cfile="facade.c",
    cppfile="facade.cpp",
    demo=dict(
        title="失败时怎么回滚",
        sub="把 ECU 握手改成失败，看前面两步如何按相反顺序撤销。",
        nodes=[
            dict(id="ign", label="点火", sub="relay"),
            dict(id="pump", label="油泵", sub="3.0 bar"),
            dict(id="ecu", label="ECU", sub="seed/key"),
            dict(id="ready", label="READY", sub="允许起动"),
        ],
        steps=[
            dict(hi=["ign"], t="step1 点火继电器吸合：成功"),
            dict(hi=["pump"], t="step2 油泵建压 3.0 bar：成功"),
            dict(hi=["ecu"], t="step3 ECU 握手：失败（模拟 seed 超时）"),
            dict(hi=["pump"], t="回滚：先停油泵"),
            dict(hi=["ign"], t="再断点火，回到安全状态"),
            dict(hi=["ready"], t="vehicle_start 返回 -3，调用方不允许起动机", bad=True),
        ],
    ),
    rows=[
        ("入口", "<code>int vehicle_start(const char *)</code>", "<code>VehicleFacade::start()</code>", "都只暴露一个成功/失败"),
        ("子系统", "静态函数", "类成员", "C 方便单测；C++ 可注入 mock"),
        ("顺序", "函数体内写死", "成员函数内写死", "顺序属于外观，不该散到调用方"),
        ("回滚", "<code>if</code> 分支里逐级撤销", "同样逐级撤销", "都容易漏；步骤多了要改成状态机"),
        ("错误码", "负值 -1/-2/-3", "负值 -1/-2/-3", "调用方要能区分失败在哪一步"),
    ],
    pitfalls=[
        ("外观不是“上帝类”。", "它只做编排；业务规则、诊断逻辑仍应留在子系统，否则外观会越长越像第二个主程序。"),
        ("回滚要按相反顺序。", "先开的后关、后开的先关；顺序错了会带残压或残留故障码。"),
        ("失败要带步骤号。", "只返回 -1，现场无法判断是点火还是 ECU；至少让错误码对应到具体步骤。"),
        ("别把外观当唯一入口。", "子系统仍需保留可直接调用的接口，否则单测和台架脚本都被迫跑全流程。"),
        ("并发上电要加锁。", "两个任务同时调 <code>start()</code> 会重复吸合继电器；入口处做互斥或状态检查。"),
    ],
)

C["3.6"] = dict(
    desc="享元：1000 个 CAN 信号共用 8 份单位/缩放描述，只存指针或 shared_ptr。",
    lede="整车上千个信号，每个都要带单位、缩放、偏移。若每个信号各存一份字符串和系数，光描述就占掉可观内存，缓存命中也会变差。<b>享元把“不随信号变化的部分”抽出来共享</b>，每个信号只留一个指向描述的句柄。",
    chips=["1000 个信号 8 份描述", "内部状态共享", "外部状态随信号走"],
    s1="""
      <div class="prose">
        <p>坏写法是每个信号自带一份描述：</p>
        <pre><code>typedef struct {
    char unit[8];      /* "kPa" 重复一千次 */
    double scale;
    int raw;           /* 这个才是变的 */
} signal_t;</code></pre>
        <p>问题不在“能不能跑”，而在放大之后：</p>
        <ul>
          <li><b>内存翻倍。</b>8 字节单位 × 1000 个信号，加上对齐填充，描述比数据还大。</li>
          <li><b>改一处要改一千处。</b>单位从 kPa 改成 bar，所有信号的副本都要遍历修改。</li>
          <li><b>比较变慢。</b>判断“两个信号同单位”要逐字符比较，而不是比较一个指针。</li>
        </ul>
        <p>享元把描述拆成“内部状态”（单位、缩放，可共享）与“外部状态”（raw 值，随信号走）。内部状态进池，外部状态留在信号对象里。</p>
      </div>""",
    s2_sub="左边是信号句柄，中间是工厂，右边是共享描述池；一千个句柄只指向八份描述。",
    fig_title="信号句柄与共享描述",
    fig_tag="flyweight",
    boxes=[
        dict(id="sig", x=24, y=130, w=180, h=90, t="signal[]", ty="一千个句柄", mt="指针 + raw", note="每个信号只存“指向描述的指针 + 当前 raw 值”；raw 是外部状态，绝不进池。"),
        dict(id="factory", x=250, y=130, w=190, h=90, t="intern()", ty="工厂", mt="按 unit 查重", note="工厂负责“有就复用、没有才新建”；它是共享的唯一入口。"),
        dict(id="pool", x=500, y=62, w=210, h=90, t="描述池", ty="内部状态", mt="8 份", note="池里是单位与缩放，一经创建不再修改；改单位等于换一份描述。"),
        dict(id="raw", x=500, y=218, w=210, h=90, t="raw 值", ty="外部状态", mt="随信号变化", note="raw 不进池：同一单位的两个信号，raw 可以完全不同。"),
    ],
    arrows=[
        dict(x1=204, y1=160, x2=250, y2=160, label="intern"),
        dict(x1=440, y1=160, x2=500, y2=107, label="取描述"),
        dict(x1=440, y1=190, x2=500, y2=250, label="带 raw", dash=True),
    ],
    fig_note="点方框：共享的是描述，不是数值。",
    s3="<p class='subh'>C 版用静态池 + 指针数组；C++ 版用 <code>shared_ptr</code>，引用计数就是“还有多少信号在用”。</p>",
    cfile="flyweight.c",
    cppfile="flyweight.cpp",
    demo=dict(
        title="一千个句柄，八份对象",
        sub="看信号数、池大小与指针是否相同。",
        nodes=[
            dict(id="s0", label="sig[0]", sub="unit=C"),
            dict(id="s8", label="sig[8]", sub="unit=C"),
            dict(id="pool", label="描述池", sub="8 份"),
            dict(id="mem", label="内存", sub="描述只一份"),
        ],
        steps=[
            dict(hi=["pool"], t="注册 8 个单位：C、kPa、rpm、%、V、A、km/h、deg"),
            dict(hi=["s0"], t="sig[0] 取 C：池里没有，新建一份描述"),
            dict(hi=["s8"], t="sig[8] 也取 C：命中已有描述，不再新建"),
            dict(hi=["s0", "s8"], t="两个句柄指向同一份描述：指针比较为真"),
            dict(hi=["pool"], t="继续注册到 1000 个信号：池仍是 8 份"),
            dict(hi=["mem"], t="描述内存不随信号数增长；只有 raw 值按信号数增长"),
        ],
    ),
    rows=[
        ("共享对象", "静态 <code>sig_t pool[8]</code>", "<code>shared_ptr&lt;const Signal&gt;</code>", "C 固定上限；C++ 可扩容且自动释放"),
        ("查重", "<code>strcmp</code> 线性扫描", "<code>map</code> 查找", "池小的时候线性也够；大了换哈希"),
        ("句柄", "<code>const sig_t *</code>", "<code>shared_ptr</code> 拷贝", "C 要保证池不重排；C++ 引用计数托管"),
        ("外部状态", "信号结构里的 <code>raw</code>", "调用时传入的 <code>raw</code>", "两者都不能塞进共享对象"),
        ("释放", "进程生命周期", "最后一个句柄释放时", "C 版通常不释放；C++ 版可能提前回收"),
    ],
    pitfalls=[
        ("不要把 raw 放进享元。", "一旦把当前值塞进共享描述，两个信号就互相串数据；共享对象必须不可变。"),
        ("池不能边用边扩容重排。", "C 版用数组存池，扩容后旧指针全部失效；要么预分配上限，要么存索引不存指针。"),
        ("字符串比较不是免费的。", "一千个信号逐个 <code>strcmp</code> 也会慢；单位数量固定时，先做一次映射再按 id 取。"),
        ("共享对象的生命周期。", "C++ 的 <code>shared_ptr</code> 会让描述活得比预期久；确认没有长生命周期句柄时再指望回收。"),
        ("别为省内存牺牲可读性。", "只有描述确实重复且量大时才值得；十个信号用享元，收益不如直接写清楚。"),
    ],
)

C["3.7"] = dict(
    desc="代理：在真实 NVRAM 前加缓存与写穿，读两次只打一次底层。",
    lede="NVRAM 读一次要几十微秒，诊断任务却会在一个周期里重复读同一个地址。<b>代理在真实存储前挡一层</b>：命中缓存就直接返回，写操作写穿保证一致；调用方看到的接口与真实对象完全一样。",
    chips=["接口透明", "缓存 + 写穿", "底层只被真正需要时调用"],
    s1="""
      <div class="prose">
        <p>没有代理时，调用方直接打底层：</p>
        <pre><code>int v1 = nvram_read(3);
int v2 = nvram_read(3);   /* 同一周期又读一次 */</code></pre>
        <p>直接访问带来三类代价：</p>
        <ul>
          <li><b>重复读。</b>一个诊断周期读同一位十几次，每次都等 NVRAM 时序。</li>
          <li><b>写后读不一致。</b>写完立刻读，底层还在忙，读回旧值。</li>
          <li><b>细节外泄。</b>调用方开始关心地址对齐、页切换、忙等待，业务代码被存储细节污染。</li>
        </ul>
        <p>代理把缓存、写穿、权限检查收在一层：读先看缓存，写先写底层再更新缓存。调用方仍然只调 <code>read()</code>/<code>write()</code>，接口不变。</p>
      </div>""",
    s2_sub="调用方 → 代理 → 真实存储；点方框看缓存命中与写穿的路径。",
    fig_title="NVRAM 代理：缓存挡在真存储前",
    fig_tag="proxy",
    boxes=[
        dict(id="client", x=24, y=140, w=170, h=80, t="调用方", ty="诊断 / 标定", mt="read / write", note="调用方看到的接口与直接访问真实存储完全一致，不需要知道代理存在。"),
        dict(id="proxy", x=240, y=110, w=210, h=130, t="proxy", ty="代理", mt="cache + 写穿", note="代理持有缓存与有效位；命中就不打底层，写操作一定写穿。"),
        dict(id="real", x=520, y=140, w=190, h=80, t="real nvram", ty="真实存储", mt="REAL[16]", note="真实存储只负责真正的读写时序；它不知道上面有没有缓存。"),
    ],
    arrows=[
        dict(x1=194, y1=180, x2=240, y2=180, label="read/write"),
        dict(x1=450, y1=160, x2=520, y2=160, label="miss"),
        dict(x1=450, y1=210, x2=520, y2=210, label="write"),
        dict(x1=520, y1=190, x2=450, y2=190, label="value", dash=True),
    ],
    fig_note="点方框：代理决定这次要不要真的下去。",
    s3="<p class='subh'>C 版用 <code>nv_t</code> 函数表 + 缓存数组；C++ 版用 <code>Proxy : Nvram</code>，对调用方完全透明。</p>",
    cfile="proxy.c",
    cppfile="proxy.cpp",
    demo=dict(
        title="读两次、写一次，看谁真的下去",
        sub="观察 [NVRAM] 与 [PROXY] 两类日志的出现次数。",
        nodes=[
            dict(id="c", label="调用方", sub="read/write"),
            dict(id="cache", label="缓存", sub="valid[16]"),
            dict(id="real", label="真实存储", sub="REAL[3]"),
        ],
        steps=[
            dict(hi=["c"], t="read(3)：代理先查 valid[3]"),
            dict(hi=["cache", "real"], t="未命中：代理下去读 REAL[3]=11，写入缓存"),
            dict(hi=["c"], t="read(3) 第二次：命中缓存，不再打底层"),
            dict(hi=["cache"], t="write(3,25)：先写穿到底层"),
            dict(hi=["real"], t="REAL[3] 变成 25；缓存同步为 25"),
            dict(hi=["c"], t="再 read(3)：命中，返回 25，与底层一致"),
        ],
    ),
    rows=[
        ("接口", "<code>nv_t</code> 两张函数表", "<code>Nvram</code> 纯虚基类", "都保持读/写两个动作"),
        ("缓存", "<code>cache[16] + valid[16]</code>", "<code>array&lt;int,16&gt; + array&lt;bool,16&gt;</code>", "容量固定，够用即可"),
        ("写策略", "写穿 + 更新缓存", "写穿 + 更新缓存", "一致性优先于写性能"),
        ("所有权", "代理内嵌 <code>real</code> 表", "持有 <code>Nvram&amp;</code>", "C++ 可代理任意实现"),
        ("失效", "手清 <code>valid</code>", "<code>valid_</code> 重置", "多核共享时要加锁或版本号"),
    ],
    pitfalls=[
        ("写穿不是写回。", "写回策略下，掉电会丢未落盘数据；车规存储通常要求写穿，别为了性能改成写回。"),
        ("缓存要能失效。", "别的核或 DMA 改了真实存储，代理还返回旧值；至少提供 <code>invalidate(addr)</code>。"),
        ("地址越界要先查。", "代理不能替真实存储兜住越界；入口处做范围检查，别让 <code>cache[addr]</code> 先越界。"),
        ("C 版函数表强转要小心。", "把 <code>nv_t*</code> 当成 <code>proxy_t*</code> 依赖“首成员”布局；结构体加字段时别把 <code>real</code> 挪走。"),
        ("代理别偷偷做业务。", "权限校验、审计可以，但不要顺手改值；代理的职责是访问控制，不是业务规则。"),
    ],
)

__all__ = ["C"]
