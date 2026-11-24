# -*- coding: utf-8 -*-
"""第四篇：行为型 11 章。"""
from content_lib import mk, bx, ar, LEFT, MID, TOP, BOT

C = {}

C["4.1"] = mk(
    desc="职责链：客服 FAQ → 技术支持 → 工程师，工单逐级升级。",
    lede="用户工单难度不同：改密码 FAQ 就能答，连不上要找技术支持，服务器 500 得工程师上。如果写成层层嵌套的 <code>if</code>，每加一级就再缩进一层。职责链把每一级串起来：<b>能处理就处理，处理不了就交给下一级</b>。",
    chips=["逐级升级", "链的顺序可配", "C 用 next 指针 · C++ 用 unique_ptr 链"],
    s1="""
      <div class="prose">
        <p>坏写法是嵌套判断：</p>
        <pre><code>if (level == 1) faq();
else if (level == 2) tech();
else if (level == 3) engineer();
else printf("没人处理");</code></pre>
        <p>每加一级就改这段；某一级想“先看情况再决定转不转”，<code>else if</code> 根本表达不了。</p>
        <p>职责链把“判断”分散到各级：每级只回答“这事我管不管”，不管就 <code>next</code>。顺序改了只改接线。</p>
      </div>""",
    s2_sub="左边是工单，中间三级处理者，右边是兜底工程师。",
    fig_title="一条单向链，谁接谁负责",
    boxes=[
        bx("ticket", "工单", "请求", "L1/L2/L3", "请求只带等级和描述，不指定处理人。", *LEFT),
        bx("faq", "FAQ", "第 1 级", "level<=1", "FAQ 只处理最简单的；其余转下一级。", 250, 56, 190, 74),
        bx("tech", "技术支持", "第 2 级", "level<=2", "技术支持接住 L2，再接不住就继续转。", 250, 150, 190, 74),
        bx("eng", "工程师", "兜底", "全部都接", "最后一级不再转，保证请求不会悬空。", 250, 244, 190, 74),
    ],
    arrows=[ar(174, 178, 250, 93, ""), ar(440, 93, 250, 187, "转"), ar(440, 187, 250, 281, "转")],
    fig_note="每级只判断“我能不能”，不判断“后面还有谁”。",
    s3="<p class='subh'>C 版处理者是结构体 + <code>next</code> 指针；C++ 版用 <code>unique_ptr</code> 串链，父节点持有子节点。</p>",
    cfile="chain.c", cppfile="chain.cpp",
    demo=dict(
        title="三张工单，看它停在哪一级",
        sub="L1 改密码、L2 连不上、L3 服务器 500。",
        nodes=[dict(id="t", label="工单", sub="L1/L2/L3"), dict(id="f", label="FAQ", sub="≤1"),
               dict(id="tech", label="技术支持", sub="≤2"), dict(id="eng", label="工程师", sub="兜底")],
        steps=[
            dict(hi=["t", "f"], t="L1「怎么改密码」→ FAQ 接住"),
            dict(hi=["t", "f", "tech"], t="L2「客户端连不上」→ FAQ 不管，转技术支持"),
            dict(hi=["tech"], t="技术支持接住 L2"),
            dict(hi=["t", "f", "tech", "eng"], t="L3「服务器 500」→ 一路转下来"),
            dict(hi=["eng"], t="工程师兜底处理 L3"),
        ],
    ),
    rows=[
        ("链怎么接", "<code>handler.next</code> 指针", "<code>unique_ptr&lt;Handler&gt;</code>", "C 手动接，C++ 所有权随链"),
        ("判断在哪", "每级的 <code>handle_fn</code>", "每级的 <code>canHandle</code>", "都分散到各级"),
        ("兜底", "最后一级无条件处理", "最后一级无条件处理", "没有兜底就会丢请求"),
        ("顺序调整", "改 next 指向", "改 setNext 调用", "都不改各级实现"),
    ],
    pitfalls=[
        ("链没有兜底", "请求一路传到空指针还没人接，必须有一级无条件处理。"),
        ("每级都处理又都转", "同一请求被处理两次；要么处理后返回，要么只转不处理。"),
        ("链成环", "A→B→A 会死循环；构造时保证单向。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/chain-of-responsibility",
)

C["4.2"] = mk(
    desc="命令：编辑器的追加与撤销，动作被封装成可排队、可回退的对象。",
    lede="编辑器要支持撤销。如果每次输入都直接改字符串，撤销时根本不知道该退到哪。命令模式把“一次编辑”封装成对象：<b>执行和撤销成对出现，历史栈自然可回放</b>。",
    chips=["执行/撤销成对", "历史栈可回放", "C 用命令数组 · C++ 用多态命令"],
    s1="""
      <div class="prose">
        <p>坏写法是直接改：</p>
        <pre><code>text[len++] = 'H';
text[len++] = 'i';     /* 想撤销？已经改完了 */</code></pre>
        <p>没有记录“改之前是什么”，也没有“反向操作”，撤销只能靠整份快照，代价大且粒度粗。</p>
        <p>命令把每次编辑变成 <code>{kind, ch}</code>：执行时改文本，撤销时做反向。历史栈里存命令，不存整份文本。</p>
      </div>""",
    s2_sub="左边是调用者，中间是命令历史，右边是编辑器。",
    fig_title="调用者不直接改文本，只发命令",
    boxes=[
        bx("inv", "Invoker", "调用者", "run / undo", "调用者只负责执行和回退，不知道命令内部。", *LEFT),
        bx("cmd", "Command", "命令", "execute + undo", "每个命令自带正反两个操作。", *MID),
        bx("hist", "History", "历史栈", "Hi! → Hi → H", "按顺序压栈，撤销时弹栈。", *TOP),
        bx("ed", "Editor", "接收者", "text/len", "文本状态只在接收者里，命令通过它改。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "run"), ar(440, 160, 520, 100, "压栈"), ar(440, 200, 520, 242, "改文本")],
    fig_note="命令是“意图的对象化”；接收者才是状态的唯一持有者。",
    s3="<p class='subh'>C 版命令是 <code>{kind, ch}</code> 的小结构，历史用数组；C++ 版每个命令是对象，历史用 <code>vector&lt;unique_ptr&gt;</code>。</p>",
    cfile="command.c", cppfile="command.cpp",
    demo=dict(
        title="输入三个字符，再撤两次",
        sub="Hi! → 撤销 → Hi → 撤销 → H。",
        nodes=[dict(id="inv", label="调用者", sub="run/undo"), dict(id="cmd", label="命令", sub="Append"),
               dict(id="h", label="历史", sub="栈"), dict(id="ed", label="编辑器", sub="text")],
        steps=[
            dict(hi=["inv", "cmd", "h"], t="执行 Append('H')，命令入栈"),
            dict(hi=["inv", "cmd", "h", "ed"], t="执行 Append('i')、Append('!')：文本 Hi!"),
            dict(hi=["inv", "h", "ed"], t="撤销一次：弹栈，Append('!') 反向删除 → Hi"),
            dict(hi=["inv", "h", "ed"], t="再撤销：→ H"),
            dict(hi=["cmd"], t="历史栈里剩下的命令仍可继续撤销"),
        ],
    ),
    rows=[
        ("命令形态", "<code>{kind, ch}</code> 结构", "多态 <code>Command</code> 对象", "C 用数据描述，C++ 用类型"),
        ("历史容器", "固定数组 + 计数", "<code>vector&lt;unique_ptr&gt;</code>", "C 版容量固定，真实实现要动态"),
        ("撤销", "<code>undo()</code> 反向操作", "<code>undo()</code> 虚函数", "必须与 execute 严格配对"),
        ("谁改状态", "接收者 <code>editor_t</code>", "接收者 <code>Editor</code>", "命令本身不存业务状态"),
    ],
    pitfalls=[
        ("execute 和 undo 不对称", "执行改了三个字段，撤销只回滚两个，历史立刻错位。"),
        ("命令里存业务状态", "状态应集中在接收者；命令只存“做了什么”。"),
        ("撤销栈无限增长", "长会话要限制深度或合并同类命令，否则内存持续上涨。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/command",
)

C["4.3"] = mk(
    desc="解释器：把 (2+3)*4 写成表达式树，求值就是后序遍历。",
    lede="如果条件逻辑长成 <code>(a + b) * c</code>，用一串 <code>if</code> 拼会越来越难改。解释器把表达式拆成树：<b>叶子是数字，节点是运算符，求值就是递归下降</b>。",
    chips=["表达式即树", "求值即递归", "C 用 kind 标记 · C++ 用多态节点"],
    s1="""
      <div class="prose">
        <p>坏写法是把优先级写进函数：</p>
        <pre><code>if (op == '+') return a + b;
if (op == '*') return a * b;   /* 括号和嵌套在哪 */</code></pre>
        <p>运算符一多，优先级和括号就要靠调用顺序硬编码，没法表达“任意嵌套”。</p>
        <p>解释器把表达式建成树：<code>Add(2,3)</code> 是一个节点，<code>Mul(Add(2,3),4)</code> 是它的父节点。求值递归到叶子，结构天然表达优先级。</p>
      </div>""",
    s2_sub="左边是根节点，中间是加法子树，右边是两个数字叶子。",
    fig_title="运算符是节点，数字是叶子",
    boxes=[
        bx("mul", "Mul", "根节点", "l * r", "乘法节点只负责把两个孩子求值再相乘。", *LEFT),
        bx("add", "Add", "子节点", "l + r", "加法节点同理，不关心孩子是数字还是表达式。", *MID),
        bx("n2", "Number 2", "叶子", "2", "叶子直接返回自己的值。", 520, 56, 190, 74),
        bx("n3", "Number 3", "叶子", "3", "另一个叶子。", 520, 212, 190, 74),
    ],
    arrows=[ar(174, 178, 250, 178, "左孩子"), ar(440, 160, 520, 100, ""), ar(440, 200, 520, 242, "")],
    fig_note="节点的职责只有“求值”，括号和优先级由树的形状表达。",
    s3="<p class='subh'>C 版用 <code>kind</code> 标记节点类型，孩子是指针；C++ 版每个节点一个子类，用 <code>unique_ptr</code> 组树。</p>",
    cfile="interpreter.c", cppfile="interpreter.cpp",
    demo=dict(
        title="同一棵树，求一次 (2+3)*4",
        sub="从根往下，再往上汇总。",
        nodes=[dict(id="mul", label="Mul", sub="*"), dict(id="add", label="Add", sub="+"),
               dict(id="a", label="2", sub="叶子"), dict(id="b", label="3", sub="叶子")],
        steps=[
            dict(hi=["mul"], t="从根 Mul 开始"),
            dict(hi=["mul", "add"], t="先求左子树 Add"),
            dict(hi=["add", "a", "b"], t="Add 求两个叶子：2 + 3 = 5"),
            dict(hi=["mul"], t="回到 Mul，右孩子是 4"),
            dict(hi=["mul"], t="5 * 4 = 20"),
        ],
    ),
    rows=[
        ("节点区分", "<code>kind</code> 0/1/2", "不同子类 + 虚函数", "C 用标记，C++ 用类型"),
        ("孩子", "左右指针", "<code>unique_ptr&lt;Expr&gt;</code>", "都表达二叉树"),
        ("求值", "<code>eval()</code> 递归", "<code>eval()</code> 虚函数递归", "同一套后序"),
        ("扩展运算符", "加一个 kind 分支", "加一个节点子类", "C 要改 switch，C++ 只加类"),
    ],
    pitfalls=[
        ("树里存共享子表达式", "同一节点被两个父亲持有，C++ 用 <code>unique_ptr</code> 会直接崩；需要共享就上 <code>shared_ptr</code>。"),
        ("节点做类型转换", "求值只依赖孩子接口，不要在 Add 里判断孩子是不是 Number。"),
        ("递归太深", "长表达式会爆栈；真实场景要限制深度或改显式栈。"),
    ],
    ref="https://www.runoob.com/design-pattern/interpreter-pattern.html",
)

C["4.4"] = mk(
    desc="迭代器：调用方只写 next()，不关心底层是数组还是链表。",
    lede="集合的存储方式会变：今天是数组，明天是链表。如果调用方直接写下标 <code>a[i]</code>，换存储就要改遍所有遍历。迭代器把“怎么走”封装起来：<b>调用方只要 next()，拿到下一个元素或结束</b>。",
    chips=["遍历与存储解耦", "统一 next 接口", "C 用游标结构 · C++ 用 begin/end"],
    s1="""
      <div class="prose">
        <p>坏写法是暴露下标：</p>
        <pre><code>for (int i = 0; i &lt; n; i++)
    sum += data[i];</code></pre>
        <p>换成链表后 <code>data[i]</code> 不成立，所有循环都要重写；如果集合内部有“跳过无效项”的规则，也会散落到每个调用方。</p>
        <p>迭代器只暴露 <code>next()</code>：内部记住走到哪，调用方写 <code>while ((p = next(&amp;it)))</code>。存储换了，迭代器实现换，调用方不动。</p>
      </div>""",
    s2_sub="左边是调用方，中间是迭代器游标，右边是集合。",
    fig_title="游标记住位置，调用方只看下一个",
    boxes=[
        bx("client", "调用方", "求和", "while(next)", "不写下标，不关心数组还是链表。", *LEFT),
        bx("it", "Iterator", "游标", "data/n/i", "游标持有集合引用和当前位置。", *MID),
        bx("coll", "Collection", "集合", "10 20 30 40 50", "集合只提供数据和长度。", *TOP),
        bx("end", "end", "结束", "NULL", "越界返回空，循环自然结束。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "next"), ar(440, 160, 520, 100, "取元素"), ar(440, 200, 520, 242, "到头")],
    fig_note="迭代器是“位置 + 取下一个”的组合，不是集合本身。",
    s3="<p class='subh'>C 版迭代器是一个带下标的游标结构；C++ 版实现 <code>begin/end</code>，直接支持 range-for。</p>",
    cfile="iterator.c", cppfile="iterator.cpp",
    demo=dict(
        title="遍历五个数，求总和",
        sub="调用方只调 next，不碰下标。",
        nodes=[dict(id="c", label="调用方", sub="while"), dict(id="i", label="迭代器", sub="i=0..4"),
               dict(id="d", label="集合", sub="10..50"), dict(id="e", label="结束", sub="NULL")],
        steps=[
            dict(hi=["c", "i", "d"], t="next 返回 10"),
            dict(hi=["i", "d"], t="next 返回 20、30"),
            dict(hi=["i", "d"], t="next 返回 40、50"),
            dict(hi=["i", "e"], t="再 next：越界，返回 NULL"),
            dict(hi=["c"], t="循环结束，总和 150"),
        ],
    ),
    rows=[
        ("迭代器形态", "游标结构 + <code>next</code>", "<code>begin()/end()</code> + <code>operator++</code>", "C 手动，C++ 可 range-for"),
        ("结束条件", "返回 <code>NULL</code>", "<code>it != end()</code>", "都不能越界读"),
        ("存储耦合", "迭代器知道数组", "迭代器持有容器引用", "调用方都不知道"),
        ("跳过无效项", "在 <code>next</code> 里过滤", "在 <code>operator++</code> 里过滤", "规则收敛一处"),
    ],
    pitfalls=[
        ("迭代器比集合活得久", "集合销毁后游标悬空；C++ 用引用要保证生命周期。"),
        ("遍历中修改集合", "一边 next 一边 push 会让游标失效；需要快照或显式失效检测。"),
        ("返回内部指针", "C 版返回元素地址，集合扩容后地址失效；要么值拷贝，要么约定不扩容。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/iterator",
)

C["4.5"] = mk(
    desc="中介者：聊天室里所有消息经房间转发，用户之间不互相持有。",
    lede="三个用户两两直连是 3 条线，十个用户就是 45 条。每加一个人，所有人都要认识他。中介者把连线收到中间：<b>用户只认识房间，房间负责转发</b>。",
    chips=["N² 降到 N", "用户互不持有", "C 用房间数组 · C++ 用类"],
    s1="""
      <div class="prose">
        <p>坏写法是用户互相保存指针：</p>
        <pre><code>alice.to[0] = &amp;bob; alice.to[1] = &amp;carol;
bob.to[0] = &amp;alice; /* 每加一个人，所有人都要改 */</code></pre>
        <p>连线数量随人数平方增长，而且“谁在线、谁能收”这类规则散落在每个用户里。</p>
        <p>中介者让用户只持有 <code>room</code>：发消息调 <code>send(from, msg)</code>，房间遍历名单转发。加人只改房间名单。</p>
      </div>""",
    s2_sub="左边是三个用户，中间是聊天室，右边是转发目标。",
    fig_title="所有线穿过房间，用户之间不直连",
    boxes=[
        bx("alice", "Alice", "用户", "send(msg)", "只认识 room，不知道 Bob/Carol 的地址。", 24, 60, 150, 70),
        bx("bob", "Bob", "用户", "send(msg)", "同样只认识 room。", 24, 150, 150, 70),
        bx("carol", "Carol", "用户", "send(msg)", "同样只认识 room。", 24, 240, 150, 70),
        bx("room", "ChatRoom", "中介者", "users[] + send", "房间持有名单，负责广播。", 300, 150, 200, 84),
        bx("all", "其他人", "接收方", "收到消息", "发送者自己不再收一遍。", 610, 150, 190, 84),
    ],
    arrows=[ar(174, 95, 300, 175, ""), ar(174, 185, 300, 185, ""), ar(174, 275, 300, 205, ""), ar(500, 192, 610, 192, "转发")],
    fig_note="中介者知道“谁在名单里”，用户只知道“往哪发”。",
    s3="<p class='subh'>C 版房间是用户指针数组；C++ 版房间是类，用户持有房间指针。</p>",
    cfile="mediator.c", cppfile="mediator.cpp",
    demo=dict(
        title="两条消息，看谁被通知",
        sub="Alice 和 Bob 先后发言，Carol 都收到。",
        nodes=[dict(id="a", label="Alice", sub="发送"), dict(id="room", label="ChatRoom", sub="名单"),
               dict(id="b", label="Bob", sub="接收/发送"), dict(id="c", label="Carol", sub="接收")],
        steps=[
            dict(hi=["a", "room"], t="Alice 调 room.send(\"晚上好\")"),
            dict(hi=["room", "b", "c"], t="房间遍历名单：Bob、Carol 收到，Alice 跳过"),
            dict(hi=["b", "room"], t="Bob 调 room.send(\"在的\")"),
            dict(hi=["room", "a", "c"], t="房间转发：Alice、Carol 收到"),
            dict(hi=["room"], t="三个用户互不知道对方地址，只认识 room"),
        ],
    ),
    rows=[
        ("中介者形态", "<code>chat_t</code> + 用户数组", "<code>ChatRoom</code> 类", "C 用数组，C++ 用容器"),
        ("用户持有什么", "<code>chat_t*</code>", "<code>ChatRoom*</code>", "都只有一条反向引用"),
        ("广播规则", "遍历 <code>users[]</code>", "遍历 <code>users_</code>", "规则只在中介者里"),
        ("扩展", "加人进数组", "加人进容器", "用户代码不改"),
    ],
    pitfalls=[
        ("中介者变成上帝对象", "所有业务都塞进房间，它会长成第二个“万能模块”；只做路由和名单。"),
        ("用户和中介者互相持有又销毁", "C++ 用裸指针要约定谁先死；必要时用弱引用。"),
        ("广播包含发送者", "自己收到自己的消息，通常要显式排除。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/mediator",
)

C["4.6"] = mk(
    desc="备忘录：编辑器改坏了，用快照退回上一次的文本和光标。",
    lede="调参数、写文本时，改错是常事。如果只保留当前状态，就没有退路。备忘录把“某一刻的状态”复制出来单独保存：<b>编辑继续改原对象，需要时再把快照倒回去</b>。",
    chips=["快照与对象分离", "恢复即覆盖", "C 用值结构 · C++ 用 friend 封装"],
    s1="""
      <div class="prose">
        <p>坏写法是“撤销”直接清空：</p>
        <pre><code>editor.text[0] = 0;   /* 只能回到空，回不到上一个版本 */</code></pre>
        <p>要回到任意一步，就得在每次修改前保存整份状态；但状态里有游标、选区、滚动位置，调用方不一定都拿得到。</p>
        <p>备忘录由对象自己产出快照：<code>save()</code> 复制一份，<code>restore()</code> 覆盖回去。调用方只保管快照，不直接改内部字段。</p>
      </div>""",
    s2_sub="左边是编辑器，中间是快照，右边是恢复后的状态。",
    fig_title="快照是值复制，编辑不影响它",
    boxes=[
        bx("ed", "Editor", "原对象", "text + cursor", "编辑器是唯一能读写全部状态的对象。", *LEFT),
        bx("snap", "Memento", "快照", "hello / 5", "快照保存当时的值，之后不再变。", *MID),
        bx("edit", "编辑后", "新状态", "hello world / 11", "编辑继续改原对象，快照不受影响。", *TOP),
        bx("back", "恢复", "回退", "hello / 5", "restore 把快照值写回原对象。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "save"), ar(440, 160, 520, 100, "继续改"), ar(440, 200, 520, 242, "restore")],
    fig_note="调用方只保管快照，不透视内部字段。",
    s3="<p class='subh'>C 版快照就是同构的值结构，复制即可；C++ 版把字段设为私有，用 <code>friend</code> 让编辑器访问。</p>",
    cfile="memento.c", cppfile="memento.cpp",
    demo=dict(
        title="改一次，退回快照",
        sub="hello → hello world → 恢复 hello。",
        nodes=[dict(id="ed", label="Editor", sub="hello"), dict(id="m", label="快照", sub="hello/5"),
               dict(id="new", label="编辑后", sub="world/11"), dict(id="back", label="恢复", sub="hello/5")],
        steps=[
            dict(hi=["ed", "m"], t="初始 hello，光标 5；save 出快照"),
            dict(hi=["ed", "new"], t="继续编辑成 hello world，光标 11"),
            dict(hi=["m"], t="快照仍是 hello / 5，没有被污染"),
            dict(hi=["ed", "back"], t="调用 restore"),
            dict(hi=["ed"], t="编辑器回到 hello / 5"),
        ],
    ),
    rows=[
        ("快照形态", "同构值结构", "<code>Memento</code> 私有字段", "C 直接复制，C++ 控制可见性"),
        ("谁能写快照", "编辑器", "编辑器（friend）", "调用方只传递，不修改"),
        ("恢复", "逐字段覆盖", "逐字段覆盖", "必须完整，不能只回滚一部分"),
        ("存储成本", "整份文本", "整份文本", "大对象要增量或压缩"),
    ],
    pitfalls=[
        ("快照存指针", "原对象继续改，快照跟着变；必须深拷贝值。"),
        ("恢复漏字段", "文本回去了、光标没回去，用户体验仍然错。"),
        ("快照无限保存", "每次按键一份会爆内存；按操作合并或限制数量。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/memento",
)

C["4.7"] = mk(
    desc="观察者：天气站发布气温，手机 App 和客厅大屏各自订阅。",
    lede="气温变化时，手机 App 要刷新，客厅大屏也要刷新。如果采样函数里直接调这两个界面，采样就被界面绑架了。观察者把“发布”和“订阅”分开：<b>发布者只遍历名单，订阅者各自处理</b>。",
    chips=["发布订阅解耦", "名单可增删", "C 用回调数组 · C++ 用虚接口"],
    s1="""
      <div class="prose">
        <p>坏写法是采样函数里写死通知：</p>
        <pre><code>void on_temp(int t) {
    phone_update(t);
    screen_update(t);   /* 加一个界面就要改这里 */
}</code></pre>
        <p>每加一个展示端就改采样；某个端暂时不想收，也只能改代码。</p>
        <p>观察者让发布者持有一份订阅名单：<code>subscribe(o)</code> 加入，<code>set_temp()</code> 遍历调用 <code>update</code>。采样不再认识具体界面。</p>
      </div>""",
    s2_sub="左边是天气站，中间是订阅名单，右边是两个订阅者。",
    fig_title="发布者只发事件，订阅者各自处理",
    boxes=[
        bx("st", "WeatherStation", "发布者", "setTemp(t)", "只负责产生事件和遍历名单。", *LEFT),
        bx("subs", "Subscribers", "订阅名单", "phone / screen", "名单决定谁收到，发布者不判断类型。", *MID),
        bx("phone", "PhoneApp", "订阅者 A", "update(t)", "手机 App 只关心自己的展示。", *TOP),
        bx("screen", "BigScreen", "订阅者 B", "update(t)", "大屏同理，互不影响。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "notify"), ar(440, 160, 520, 100, ""), ar(440, 200, 520, 242, "")],
    fig_note="发布者不知道订阅者是谁；订阅者不知道还有谁订阅。",
    s3="<p class='subh'>C 版订阅者是 <code>{name, callback}</code> 结构；C++ 版是抽象 <code>Observer</code>，发布者存指针。</p>",
    cfile="observer.c", cppfile="observer.cpp",
    demo=dict(
        title="气温变两次，两个订阅者都刷新",
        sub="21℃ 和 24℃ 两次发布。",
        nodes=[dict(id="st", label="天气站", sub="setTemp"), dict(id="ph", label="手机 App", sub="update"),
               dict(id="sc", label="客厅大屏", sub="update"), dict(id="l", label="名单", sub="2 人")],
        steps=[
            dict(hi=["st", "l"], t="气温 → 21℃，遍历名单"),
            dict(hi=["ph"], t="手机 App 显示 21℃"),
            dict(hi=["sc"], t="客厅大屏刷新 21℃"),
            dict(hi=["st"], t="气温 → 24℃，同一份名单"),
            dict(hi=["ph", "sc"], t="两个订阅者各自刷新 24℃"),
        ],
    ),
    rows=[
        ("订阅者形态", "<code>{name, update}</code>", "<code>Observer</code> 虚接口", "C 用回调，C++ 用多态"),
        ("名单", "固定数组", "<code>vector&lt;Observer*&gt;</code>", "真实实现要支持退订"),
        ("通知", "遍历数组调用", "遍历容器调用", "发布者不判断类型"),
        ("退订", "示例未做", "示例未做", "生产实现必须支持“通知中退订”"),
    ],
    pitfalls=[
        ("通知中退订", "遍历时删除元素会让迭代器失效；先拷贝名单或延迟删除。"),
        ("订阅者比发布者先死", "C++ 裸指针会悬空；需要弱引用或显式退订。"),
        ("更新顺序有依赖", "订阅者互相依赖时，观察者顺序会变成隐式契约；尽量不要让订阅者互相调用。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/observer",
)

C["4.8"] = mk(
    desc="状态：订单从新建到支付、发货、完成，非法事件被明确拒绝。",
    lede="订单有四个状态：新建、已支付、已发货、已完成。不是每个事件都能在任意状态发生：没付钱不能发货，付过钱不能再付。状态模式把<b>“当前状态 + 收到事件 → 下一个状态”</b>变成一张明确的转移表。",
    chips=["状态与转移显式", "非法事件被拒", "C 用枚举+函数 · C++ 用状态类"],
    s1="""
      <div class="prose">
        <p>坏写法是 <code>switch</code> 里再套 <code>if</code>：</p>
        <pre><code>switch (st) {
case NEW: if (e == PAY) st = PAID; break;
case PAID: if (e == SHIP) st = SHIPPED; break;
}</code></pre>
        <p>分支会随状态和事件相乘；某个组合忘了写，就默默保持原状态，调用方还以为成功了。</p>
        <p>状态模式把每个状态的合法事件写清楚：能转就返回新状态，不能转就明确拒绝。非法组合不再“静默通过”。</p>
      </div>""",
    s2_sub="左边是订单，中间是当前状态，右边是下一个状态。",
    fig_title="合法才转移，非法就拒绝",
    boxes=[
        bx("order", "Order", "上下文", "handle(event)", "订单只持有当前状态，不自己判断规则。", *LEFT),
        bx("cur", "New", "当前状态", "pay → Paid", "每个状态知道自己的合法事件。", *MID),
        bx("next", "Paid", "下一状态", "ship → Shipped", "转移由当前状态决定，不由调用方指定。", *TOP),
        bx("bad", "拒绝", "非法事件", "pay again", "已支付再支付：保持原状态并报错。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "事件"), ar(440, 160, 520, 100, "pay"), ar(440, 200, 520, 242, "非法")],
    fig_note="状态对象负责“我能接受什么”，上下文只负责转发。",
    s3="<p class='subh'>C 版状态是枚举，转移函数集中判断；C++ 版每个状态一个类，<code>next()</code> 返回下一个状态。</p>",
    cfile="state.c", cppfile="state.cpp",
    demo=dict(
        title="四个事件，看哪一步被拒",
        sub="pay → pay → ship → done。",
        nodes=[dict(id="o", label="Order", sub="新建"), dict(id="p", label="已支付", sub="Paid"),
               dict(id="s", label="已发货", sub="Shipped"), dict(id="d", label="已完成", sub="Done")],
        steps=[
            dict(hi=["o", "p"], t="新建 + pay → 已支付"),
            dict(hi=["p"], t="已支付 + pay：非法，拒绝", bad=True),
            dict(hi=["p", "s"], t="已支付 + ship → 已发货"),
            dict(hi=["s", "d"], t="已发货 + done → 已完成"),
            dict(hi=["d"], t="已完成后再来事件：保持原状态"),
        ],
    ),
    rows=[
        ("状态表示", "<code>enum state_t</code>", "状态类", "C 用枚举，C++ 用对象"),
        ("转移规则", "<code>next()</code> 集中判断", "每个状态类自己实现", "都只在一处"),
        ("非法事件", "返回原状态 + <code>ok=0</code>", "返回 <code>this</code>，上下文报错", "必须显式拒绝"),
        ("扩展状态", "加枚举 + 改转移函数", "加一个状态类 + 接线", "C 要改中心函数，C++ 更分散"),
    ],
    pitfalls=[
        ("非法事件静默通过", "调用方以为成功，订单却停在原地；必须返回明确的拒绝。"),
        ("状态里做业务", "状态只决定“能不能转”，不要在里面扣库存、发短信。"),
        ("状态对象可变", "C++ 状态类通常无状态、可共享；把每单数据放进上下文。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/state",
)

C["4.9"] = mk(
    desc="策略：同一组数据，分别用冒泡和插入排序，调用方代码不变。",
    lede="排序算法有好几种，选哪种取决于数据规模和是否近乎有序。如果把算法名写死在调用处，换算法就要改调用方。策略模式把算法变成参数：<b>上下文只持有一个“会排序”的函数/对象</b>。",
    chips=["算法即参数", "调用方不选分支", "C 用函数指针 · C++ 用策略对象"],
    s1="""
      <div class="prose">
        <p>坏写法是一个函数里堆所有算法：</p>
        <pre><code>if (mode == BUBBLE) bubble(a, n);
else if (mode == INSERT) insertion(a, n);
else if (mode == QUICK) quick(a, n);</code></pre>
        <p>算法越多分支越长；每个调用方都要知道 <code>mode</code> 的取值，测试也要覆盖所有分支。</p>
        <p>策略把算法抽成可传递的依赖：<code>sort(a, n, bubble)</code>。调用方只提供数据，选哪个算法由上层决定。</p>
      </div>""",
    s2_sub="左边是调用方，中间是策略参数，右边是两种排序实现。",
    fig_title="同一份数据，换一个排序函数",
    boxes=[
        bx("ctx", "Sorter", "上下文", "sort(data, strategy)", "上下文只调用策略，不判断算法名。", *LEFT),
        bx("st", "SortStrategy", "策略接口", "sort(a, n)", "接口只描述“把数组排好”。", *MID),
        bx("b", "Bubble", "实现 A", "冒泡", "冒泡按相邻交换，简单但慢。", *TOP),
        bx("i", "Insertion", "实现 B", "插入", "插入对近乎有序的数据更快。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "传入"), ar(440, 160, 520, 100, "调用"), ar(440, 200, 520, 242, "调用")],
    fig_note="上下文不认识具体算法；算法也不认识业务。",
    s3="<p class='subh'>C 版策略是函数指针，直接传函数名；C++ 版策略是对象，用 <code>unique_ptr</code> 注入。</p>",
    cfile="strategy.c", cppfile="strategy.cpp",
    demo=dict(
        title="同一组数，两种策略各排一次",
        sub="5 1 4 2 3 → 1 2 3 4 5。",
        nodes=[dict(id="c", label="Sorter", sub="同一段代码"), dict(id="s", label="策略", sub="bubble/insert"),
               dict(id="b", label="冒泡", sub="O(n²)"), dict(id="i", label="插入", sub="O(n²)")],
        steps=[
            dict(hi=["c", "s", "b"], t="传入冒泡策略，排 5 1 4 2 3"),
            dict(hi=["b"], t="冒泡结果：1 2 3 4 5"),
            dict(hi=["c", "s", "i"], t="换插入策略，调用方代码不改"),
            dict(hi=["i"], t="插入结果：1 2 3 4 5"),
            dict(hi=["c"], t="结果相同，过程不同：选择权在调用方"),
        ],
    ),
    rows=[
        ("策略形态", "函数指针", "策略对象", "C 最轻，C++ 可带状态"),
        ("注入方式", "参数传入", "构造/Setter 注入", "都在运行时决定"),
        ("调用方", "只给数据和策略", "只给数据和策略", "不写算法分支"),
        ("扩展算法", "加一个函数", "加一个策略子类", "都不改上下文"),
    ],
    pitfalls=[
        ("策略里藏业务规则", "策略只做算法；折扣、权限这类规则放别处。"),
        ("策略对象有状态还共享", "C++ 策略若被多个上下文共用，内部计数会互相干扰。"),
        ("为两个分支硬抽策略", "只有算法会独立演化、或需要运行时切换时才值得。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/strategy",
)

C["4.10"] = mk(
    desc="模板方法：报表骨架固定，CSV 与 HTML 只换表头、行、表尾三步。",
    lede="同一份数据要导出 CSV 和 HTML。两种格式的“取数—循环—收尾”顺序完全一样，只有表头、每行、表尾不同。模板方法把骨架写死在一个 <code>run()</code> 里，<b>把可变的三步留给子类实现</b>。",
    chips=["骨架只写一遍", "可变步骤下沉", "C 用函数表 · C++ 用虚函数"],
    s1="""
      <div class="prose">
        <p>坏写法是两套完整流程：</p>
        <pre><code>csv_report();    /* 自己循环 1..3 */
html_report();   /* 又抄一遍循环，顺序还可能不一样 */</code></pre>
        <p>循环次数、异常处理、空数据判断都抄了两遍；改一处忘另一处，两个报表行为就不一致。</p>
        <p>模板方法只保留一个 <code>run()</code>：先表头，再循环，再表尾。CSV 和 HTML 各自实现这三步，骨架不再重复。</p>
      </div>""",
    s2_sub="左边是报表骨架，中间是三个可变步骤，右边是两个格式。",
    fig_title="骨架固定，三步可换",
    boxes=[
        bx("run", "Report.run", "模板", "header → rows → footer", "顺序和循环次数只在这里。", *LEFT),
        bx("hooks", "三步钩子", "可变部分", "header/row/footer", "子类只实现这三步。", *MID),
        bx("csv", "CsvReport", "实现 A", "id,qty", "CSV 的表头和行格式。", *TOP),
        bx("html", "HtmlReport", "实现 B", "&lt;table&gt;", "HTML 的表头和行格式。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "调用"), ar(440, 160, 520, 100, "实现"), ar(440, 200, 520, 242, "实现")],
    fig_note="骨架方法不应被调用方覆盖；钩子方法才是扩展点。",
    s3="<p class='subh'>C 版报表是“名字 + 三个函数指针”的结构；C++ 版是抽象基类，<code>run()</code> 非虚，三步纯虚。</p>",
    cfile="template_method.c", cppfile="template_method.cpp",
    demo=dict(
        title="跑两种报表，骨架完全一样",
        sub="表头、三行、表尾。",
        nodes=[dict(id="run", label="run()", sub="骨架"), dict(id="h", label="header", sub="钩子"),
               dict(id="r", label="row", sub="钩子"), dict(id="f", label="footer", sub="钩子")],
        steps=[
            dict(hi=["run", "h"], t="run 先调 header：CSV 输出 id,qty"),
            dict(hi=["r"], t="循环 1..3，调 row：1,10 / 2,20 / 3,30"),
            dict(hi=["f"], t="调 footer：--"),
            dict(hi=["run"], t="换 HtmlReport，run 顺序不变"),
            dict(hi=["h", "r", "f"], t="只换三步实现：&lt;table&gt; / &lt;tr&gt; / &lt;/table&gt;"),
        ],
    ),
    rows=[
        ("骨架", "普通函数 <code>run(report)</code>", "非虚成员 <code>run()</code>", "都只写一遍"),
        ("可变步骤", "三个函数指针", "三个纯虚函数", "C 用数据注入，C++ 用继承"),
        ("扩展", "填一个新结构", "写一个子类", "都不改骨架"),
        ("顺序", "骨架里硬编码", "骨架里硬编码", "子类不能改顺序"),
    ],
    pitfalls=[
        ("把骨架也开放覆盖", "子类重写 <code>run()</code> 后，模板就名存实亡。"),
        ("钩子里做重活", "每一步应短小；复杂逻辑拆到辅助函数，别把模板变成大杂烩。"),
        ("C 版函数指针为空", "缺一个钩子就崩；构造时统一校验三个指针。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/template-method",
)

C["4.11"] = mk(
    desc="访问者：文件与目录节点只负责 accept，统计逻辑放在访问者里。",
    lede="目录树要做统计：文件数、总字节、最大文件、按扩展名分组……如果每加一种统计就改每个节点，节点会变成统计代码的垃圾场。访问者把统计搬出去：<b>节点只负责 accept，访问者决定访问时做什么</b>。",
    chips=["统计与节点解耦", "一次遍历多种统计", "C 用函数表 · C++ 用双重分派"],
    s1="""
      <div class="prose">
        <p>坏写法是节点里塞满统计字段：</p>
        <pre><code>struct node { int size; int file_count; int max_size; ... };
/* 每加一种统计，所有节点都要改 */</code></pre>
        <p>节点本该只描述“我是文件还是目录、我有多大”；统计是使用方的关注点，不该焊进数据结构。</p>
        <p>访问者把动作外置：节点调 <code>accept(v)</code>，访问者按节点类型分别处理。加统计只加访问者，节点不动。</p>
      </div>""",
    s2_sub="左边是节点，中间是 accept 分派，右边是访问者。",
    fig_title="节点只开门，访问者决定做什么",
    boxes=[
        bx("node", "Node", "节点", "accept(v)", "节点只知道自己是文件还是目录。", *LEFT),
        bx("acc", "accept", "双重分派", "file→visitFile", "先按节点类型，再按访问者类型分派。", *MID),
        bx("v", "Visitor", "访问者", "visitFile/visitDir", "统计逻辑集中在这里。", *TOP),
        bx("stat", "Counter", "统计结果", "2 文件 / 200B", "结果由访问者累计，节点不持有。", *BOT),
    ],
    arrows=[ar(174, 178, 250, 178, "accept"), ar(440, 160, 520, 100, "文件"), ar(440, 200, 520, 242, "目录")],
    fig_note="访问者模式把“遍历结构”和“对每个节点做什么”分开。",
    s3="<p class='subh'>C 版节点里放 <code>accept</code> 函数指针，访问者是一组回调；C++ 版用 <code>accept(Visitor&amp;)</code> + 虚函数实现双重分派。</p>",
    cfile="visitor.c", cppfile="visitor.cpp",
    demo=dict(
        title="两个文件一个目录，统计一次",
        sub="Counter 访问者累计文件数和字节。",
        nodes=[dict(id="root", label="root", sub="目录"), dict(id="src", label="src", sub="目录"),
               dict(id="a", label="a.c", sub="120B"), dict(id="b", label="b.c", sub="80B")],
        steps=[
            dict(hi=["root", "src"], t="根节点 accept：进入 root 目录"),
            dict(hi=["src"], t="src 目录 accept：进入 src"),
            dict(hi=["a"], t="a.c accept：Counter 记 1 个文件、120 字节"),
            dict(hi=["b"], t="b.c accept：再记 1 个文件、80 字节"),
            dict(hi=["root"], t="汇总：2 个文件，200 字节"),
        ],
    ),
    rows=[
        ("分派", "<code>accept</code> 函数指针 + 回调", "<code>accept(Visitor&amp;)</code> 虚函数", "C 手动，C++ 双重分派"),
        ("节点状态", "只存名字/类型/大小", "只存名字/类型/大小", "不塞统计字段"),
        ("加统计", "加一个访问者结构", "加一个 Visitor 子类", "节点完全不动"),
        ("遍历", "调用方按树结构递归", "调用方按树结构递归", "访问者不负责找孩子"),
    ],
    pitfalls=[
        ("节点类型判断漏分支", "访问者必须覆盖所有节点类型，否则统计会漏。"),
        ("访问者里改节点", "访问者应只读；要改结构就另开一次操作，别在遍历中改。"),
        ("双重分派成本", "每次访问两次虚调用；极热路径要考虑缓存或内联。"),
    ],
    ref="https://refactoringguru.cn/design-patterns/visitor",
)

