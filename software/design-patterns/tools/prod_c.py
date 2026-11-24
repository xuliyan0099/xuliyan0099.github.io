# -*- coding: utf-8 -*-
from prod_lib import PD

P = {}

P["4.1"] = PD(
"生产实例：报销审批链（风控 / 主管 / 总监 / CFO）",
"""<p>报销审批按金额分级：1000 以下主管，10000 以下总监，再往上 CFO。最先过的不是金额，而是<b>风控黑名单</b>：失信供应商、重复发票直接拒绝。职责链把每一关串起来，谁先命中谁负责，后级不再执行。</p>
<ul><li><b>顺序</li></b>：风控必须在金额审批之前，否则黑名单单据会先被批出去。</li>
<li><b>可跳过</li></b>：总监休假时由代理审批人接替，链结构不变，只换节点。</li>
<li><b>留痕</li></b>：每关记录通过/拒绝和耗时，出问题能定位卡在哪。</li></ul>""",
["最后一关必须兜底，不能把单据传丢", "同一关不能既处理又继续往下传", "链的顺序要在配置里校验，禁止成环"],
"""@startuml
autonumber
participant "Employee" as E
participant "RiskCheck" as R
participant "Supervisor" as S
participant "Director" as D
participant "CFO" as C

E -> R: submit(claim=6800, vendor="V-88")
R -> R: blacklist + invoice dedup
alt 命中黑名单
  R --> E: REJECTED(risk)
else 通过
  R -> S: handle(6800)
  alt <= 1000
    S --> E: APPROVED by Supervisor
  else 超过阈值
    S -> D: handle(6800)
    alt <= 10000
      D --> E: APPROVED by Director
    else 超过阈值
      D -> C: handle(6800)
      C --> E: APPROVED by CFO
    end
  end
end
@enduml""")

P["4.2"] = PD(
"生产实例：交易下单命令与撤销补偿",
"""<p>交易系统把“下单/撤单”封装成命令：命令带 clientOrderNo、幂等键、版本号，进持久化队列后由执行器消费。撤单不是删记录，而是产生一条<b>反向命令</b>，两条命令都留在账本里，审计可回放。</p>
<ul><li><b>幂等</li></b>：同一 clientOrderNo 重复投递只执行一次。</li>
<li><b>补偿</li></b>：撤单失败进入重试队列，超过 3 次转人工。</li>
<li><b>顺序</li></b>：同一订单的命令按版本号串行，禁止并发改状态。</li></ul>""",
["命令必须持久化后再执行，不能只存在内存队列", "执行与撤销要对称，撤单也要写账本", "重试不能生成新的幂等键"],
"""@startuml
autonumber
participant "Trader" as T
participant "CommandQueue" as Q
participant "Executor" as X
participant "MatchingEngine" as M
participant "Ledger" as L

T -> Q: PlaceOrder(clientOrderNo=O1, idem=K1, v=1)
Q -> X: consume(K1)
X -> L: check idem(K1)
alt 已执行
  X --> T: Duplicate(K1, orderId)
else 首次
  X -> M: submit(order)
  M --> X: accepted(orderId)
  X -> L: append(PlaceOrder, v=1)
end
T -> Q: CancelOrder(orderId, idem=K2, v=2)
Q -> X: consume(K2)
X -> M: cancel(orderId)
alt 撤单被拒
  M --> X: REJECT(late)
  X -> Q: retry(3) then manual
else 成功
  X -> L: append(CancelOrder, v=2)
  X --> T: Cancelled
end
@enduml""")

P["4.3"] = PD(
"生产实例：风控规则 DSL（年龄 / 金额 / 地区）",
"""<p>风控规则每天在变，不能每次改代码发版。规则写成表达式：<code>age &lt; 18 or (amount &gt; 5000 and region == "MO")</code>，解析成 AST 后缓存；每笔交易对同一棵树求值。新增规则只加节点，不改求值器。</p>
<ul><li><b>短路</li></b>：<code>or</code> 左边为真就不再求右边，降低延迟。</li>
<li><b>可解释</li></b>：命中时返回具体命中的子表达式，方便客服解释。</li>
<li><b>灰度</li></b>：新规则先影子运行，只记录不拦截。</li></ul>""",
["规则文本必须版本化，历史交易按当时版本解释", "求值器不能依赖外部 IO，否则规则不可重放", "节点类型要封闭，避免解析出未知节点导致放行"],
"""@startuml
abstract class RuleNode {
  +eval(ctx): bool
}
class And
class Or
class Not
class Compare {
  +field
  +op
  +value
}
class Value
RuleNode <|-- And
RuleNode <|-- Or
RuleNode <|-- Not
RuleNode <|-- Compare
Compare --> Value
note right of Compare: age < 18 / amount > 5000
note bottom of Or: 左真短路，不再求右
@enduml""")

P["4.4"] = PD(
"生产实例：千万行数据导出（游标分页）",
"""<p>导出报表不能一次性 <code>SELECT</code> 全表，也不能用 <code>OFFSET</code> 翻页：越往后越慢，还会重复/漏行。迭代器封装游标：每次取一批，记住最后一条主键，调用方只写 <code>while (next())</code>，内存里最多一批。</p>
<ul><li><b>稳定性</li></b>：按主键升序，批次之间不重不漏。</li>
<li><b>背压</li></b>：下游写得慢时暂停拉取，避免内存堆积。</li>
<li><b>续传</li></b>：任务失败后从最后位点继续，不从头扫。</li></ul>""",
["迭代器要暴露“还有没有下一批”，不能靠异常结束", "游标字段必须唯一且有索引，否则仍会漏行", "连接和游标要确保关闭，失败路径也要释放"],
"""@startuml
autonumber
participant "Exporter" as E
participant "CursorIterator" as I
participant "Database" as D
participant "S3Writer" as W

E -> I: open(table="orders", batch=1000)
loop 直到没有下一批
  I -> D: SELECT ... WHERE id > :lastId ORDER BY id LIMIT 1000
  D --> I: rows[1000] + lastId
  I --> E: batch
  E -> W: write(part-000N.csv)
end
I --> E: EOF
note over I: 内存里最多一批；失败从 lastId 续传
@enduml""")

P["4.5"] = PD(
"生产实例：订单事件总线（订单 / 库存 / 积分 / 通知）",
"""<p>下单后要扣库存、加积分、发通知。四个模块两两直连就是 6 条线，每加一个模块再翻一倍。中介者做成事件总线：订单只发 <code>OrderPlaced</code>，总线按订阅关系投递，模块之间互不持有。</p>
<ul><li><b>至少一次</li></b>：投递失败重试，消费者按 eventId 去重。</li>
<li><b>顺序</li></b>：同一订单的事件按分区键保序。</li>
<li><b>隔离</li></b>：通知失败不影响库存与积分。</li></ul>""",
["总线只做路由，不做业务编排", "消费者必须幂等，重试是常态", "死信要可查询，不能静默丢弃"],
"""@startuml
autonumber
participant "OrderService" as O
participant "EventBus" as B
participant "InventorySvc" as I
participant "PointsSvc" as P
participant "NotifySvc" as N

O -> B: publish(OrderPlaced, key=orderId)
B -> I: deliver(eventId=E1)
I --> B: ack
B -> P: deliver(eventId=E1)
P --> B: ack
B -> N: deliver(eventId=E1)
alt 通知超时
  N --> B: nack
  B -> B: retry(backoff) 5 次后进 DLQ
else 成功
  N --> B: ack
end
note over O,I,P,N: 四个模块互不持有，只认识总线
@enduml""")

P["4.6"] = PD(
"生产实例：长流程工作流的回滚快照",
"""<p>开户流程有七步：实名、绑卡、风控、授信、签约、激活、通知。第三步失败时，前两步已经落库，不能简单重跑。备忘录在每步成功后保存一个<b>可恢复快照</b>（业务主键 + 状态 + 外部资源 ID），失败时按快照逆序补偿。</p>
<ul><li><b>持久化</li></b>：快照写数据库，进程崩溃也能恢复。</li>
<li><b>幂等</li></b>：补偿操作重复执行结果一致。</li>
<li><b>保留期</li></b>：快照保留 7 天，过期归档，避免无限膨胀。</li></ul>""",
["快照要包含外部系统 ID，否则无法撤销远程资源", "恢复只能回到已提交的步骤，不能回到半提交状态", "快照不能存大对象，存引用和版本"],
"""@startuml
autonumber
participant "Workflow" as W
participant "StepRunner" as R
participant "SnapshotStore" as S
participant "BankAPI" as B

W -> R: run(step=实名)
R -> B: verifyIdentity
B --> R: ok
R -> S: save(snapshot{step=1, userId, bankRef})
W -> R: run(step=绑卡)
R -> B: bindCard
B --> R: ok
R -> S: save(snapshot{step=2, cardRef})
W -> R: run(step=风控)
alt 风控拒绝
  R -> S: load(step=2)
  R -> B: unbindCard(cardRef)
  R -> S: load(step=1)
  R --> W: Failed(rolledBackTo=1)
else 通过
  R -> S: save(step=3)
  R --> W: Continue
end
@enduml""")

P["4.7"] = PD(
"生产实例：领域事件 + Outbox 表",
"""<p>订单服务要在同一个数据库事务里改订单状态并通知下游。直接发 MQ 会有“事务回滚了消息已发”的问题。观察者在这里落成 <b>outbox</b>：业务表和 outbox 同事务写入，后台投递器读取 outbox 发消息，下游按 eventId 幂等消费。</p>
<ul><li><b>至少一次</li></b>：投递器失败重试，消费者去重。</li>
<li><b>不阻塞主链</li></b>：投递异步，订单接口不被 MQ 抖动拖慢。</li>
<li><b>可回放</li></b>：outbox 保留 3 天，故障后可重放。</li></ul>""",
["业务写入和 outbox 必须同一事务", "投递器要支持多实例，避免重复并发发送", "消费者按 eventId 去重，不能只靠消息顺序"],
"""@startuml
autonumber
participant "OrderTx" as T
participant "OrderDB" as D
participant "OutboxPoller" as P
participant "Kafka" as K
participant "PointsConsumer" as C

T -> D: BEGIN
T -> D: UPDATE order SET status=PAID
T -> D: INSERT outbox(eventId=E9, type=OrderPaid)
T -> D: COMMIT
P -> D: SELECT unpublished outbox
P -> K: publish(E9, key=orderId)
alt 发送成功
  K --> C: consume(E9)
  C -> C: if seen(E9) skip else addPoints
  P -> D: mark published
else 发送失败
  P -> P: retry(backoff)
  note right: 不丢事件；最多重复，消费端幂等
end
@enduml""")

P["4.8"] = PD(
"生产实例：支付单状态机（重复回调 / 超时关单）",
"""<p>支付单状态：<code>INIT → PAYING → SUCCESS / FAILED / CLOSED</code>。渠道回调会重复、会乱序，用户还会重复点支付。状态模式把“当前状态能接受哪些事件”写死：已成功的单再收到支付回调只返回成功，不再扣款；超时未支付由定时器关单。</p>
<ul><li><b>幂等</li></b>：同一 tradeNo 的回调重复到达，只认第一次。</li>
<li><b>乱序</li></b>：FAILED 之后到达的 SUCCESS 进入人工复核，不直接覆盖。</li>
<li><b>超时</li></b>：创建后 15 分钟未支付自动 CLOSED，并释放库存。</li></ul>""",
["非法事件必须显式拒绝并记录，不能静默忽略", "状态转移要落库带版本号，防并发覆盖", "回调验签在进入状态机之前完成"],
"""@startuml
[*] --> INIT : createPayment
INIT --> PAYING : payRequested
PAYING --> SUCCESS : callbackSuccess(验签通过)
PAYING --> FAILED : callbackFail
PAYING --> CLOSED : timeout(15min)
SUCCESS --> [*]
FAILED --> [*]
CLOSED --> [*]
PAYING --> PAYING : duplicateCallback(幂等返回)
SUCCESS --> SUCCESS : duplicateCallback(不再扣款)
note right of SUCCESS: 重复/迟到回调只记录，不改金额
@enduml""")

P["4.9"] = PD(
"生产实例：网关路由与限流策略",
"""<p>网关按租户选择路由策略：小租户轮询、大租户加权、缓存型租户一致性哈希；限流也分令牌桶与滑动窗口。策略在运行时按配置切换，业务代码只调 <code>pick()</code> 和 <code>allow()</code>，不写算法分支。</p>
<ul><li><b>热切换</li></b>：策略变更走配置推送，连接不断。</li>
<li><b>降权</li></b>：节点连续失败时权重临时降为 0，恢复后缓慢回升。</li>
<li><b>可观测</li></b>：每次决策记录策略名和命中节点。</li></ul>""",
["策略对象要无状态或线程安全，不能共享可变计数", "切换过程中允许新旧策略并存一个短暂窗口", "限流拒绝要返回明确的重试时间"],
"""@startuml
autonumber
participant "Gateway" as G
participant "Router" as R
participant "Strategy" as S
participant "Limiter" as L
participant "Upstream" as U

G -> R: pick(tenant=42, path=/api/order)
R -> S: select(tenant)
alt 大租户
  S --> R: WeightedRoundRobin
else 缓存型
  S --> R: ConsistentHash
end
R -> S: choose(nodes, key)
S --> R: node-3
G -> L: allow(tenant, qps=200)
alt 超限
  L --> G: 429 retryAfter=1s
else 放行
  L --> G: ok
  G -> U: proxy(node-3)
  U --> G: 200
end
note over R,S: 策略名随 trace 上报，便于回放
@enduml""")

P["4.10"] = PD(
"生产实例：数据同步 Job 的固定骨架",
"""<p>每个同步任务都长一个样：抢锁、读位点、抽取、转换、校验、写入、提交位点、释放锁。区别只在抽取源和转换规则。模板方法把骨架写在 <code>run()</code>，子类只实现 <code>extract/transform</code>，避免每个 Job 各写一套锁和位点逻辑。</p>
<ul><li><b>恰好一次</li></b>：位点与目标写入同事务提交。</li>
<li><b>可重入</li></b>：失败重跑从上次位点开始。</li>
<li><b>可观测</li></b>：每阶段耗时和行数上报。</li></ul>""",
["骨架方法不能被覆盖，否则位点逻辑会丢", "钩子只做数据变换，不要在里面抢锁", "空批次要正常提交位点，避免死循环"],
"""@startuml
autonumber
participant "Scheduler" as S
participant "SyncJob" as J
participant "Source" as R
participant "Sink" as W
participant "MetaDB" as M

S -> J: run(jobId)
J -> M: acquireLock(jobId)
J -> M: loadOffset()
J -> R: extract(offset)
R --> J: batch
J -> J: transform(batch)
alt 校验失败
  J -> M: releaseLock()
  J --> S: Failed(offset unchanged)
else 通过
  J -> W: write(batch, txn)
  J -> M: commitOffset(next) in same txn
  J -> M: releaseLock()
  J --> S: Success(rows=N, nextOffset)
end
note over J: run() 顺序固定；子类只换 extract/transform
@enduml""")

P["4.11"] = PD(
"生产实例：SQL 审核里的 AST 访问者",
"""<p>SQL 上线前要审：是否全表扫描、有没有越权表、是否写了笛卡尔积。解析器产出 AST，节点成千上万；如果每种规则都写一遍递归，AST 一升级全崩。访问者把规则搬出节点：解析器只负责 <code>accept</code>，审核规则各自实现 <code>visit</code>。</p>
<ul><li><b>只读</li></b>：访问者不改 AST，多个规则可并行跑。</li>
<li><b>覆盖</li></b>：未知节点类型默认报错，避免漏审。</li>
<li><b>性能</li></b>：一次遍历可组合多个访问者，减少重复递归。</li></ul>""",
["节点不要内置审核规则，否则加规则就要改 AST", "访问者要覆盖所有节点类型，未知类型不能放行", "遍历中禁止修改树结构"],
"""@startuml
abstract class SqlNode {
  +accept(v: Visitor)
}
class Select
class Join
class TableRef
class BinaryExpr
SqlNode <|-- Select
SqlNode <|-- Join
SqlNode <|-- TableRef
SqlNode <|-- BinaryExpr
interface Visitor {
  +visitSelect(n)
  +visitJoin(n)
  +visitTable(n)
}
class PermissionAudit
class FullScanAudit
Visitor <|-- PermissionAudit
Visitor <|-- FullScanAudit
Select --> Visitor : accept
note right of PermissionAudit: 越权表 -> BLOCK
note right of FullScanAudit: 无索引扫描 -> WARN
@enduml""")

P["4.5"]["puml"] = """@startuml
autonumber
participant "OrderService" as O
participant "EventBus" as B
participant "InventorySvc" as I
participant "PointsSvc" as P
participant "NotifySvc" as N

O -> B: publish(OrderPlaced, key=orderId)
B -> I: deliver(eventId=E1)
I --> B: ack
B -> P: deliver(eventId=E1)
P --> B: ack
B -> N: deliver(eventId=E1)
N --> B: timeout
B -> B: retry(backoff)
B -> N: redeliver(E1)
N --> B: ack
note over B: 最多重复；消费端按 eventId 去重
@enduml"""