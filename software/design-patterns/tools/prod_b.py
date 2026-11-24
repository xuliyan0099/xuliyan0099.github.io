# -*- coding: utf-8 -*-
from prod_lib import PD

P = {}

P["3.1"] = PD(
"生产实例：支付核心适配银行老 SOAP 接口",
"""<p>新支付核心内部是 JSON + REST，但几家地方银行只提供十年前的 SOAP 接口：字段名不同、签名算法不同、错误码是一串数字。适配器把 <code>transfer(req)</code> 翻译成 SOAP 信封，负责签名、超时和错误码映射，支付核心完全看不到 SOAP。</p>
<ul><li><b>字段映射</b>：金额单位从元转分，收款行行号补零到 12 位。</li>
<li><b>签名</li></b>：私钥按银行要求做 SHA1-RSA，适配器内部完成。</li>
<li><b>错误码</li></b>：银行 1003 映射为 <code>INSUFFICIENT_FUNDS</code>，上层只认领域错误。</li></ul>""",
["适配器只做协议翻译，不承担重试与对账", "签名失败要快速失败，不能把明文请求打出去", "错误码映射表要可配置，新增银行不改核心"],
"""@startuml
autonumber
participant "PaymentCore" as P
participant "BankAdapter" as A
participant "SOAPClient" as S
participant "BankHost" as B

P -> A: transfer(req{amount=199.00, bank="ICBC"})
A -> A: map fields (yuan->fen, pad bankCode)
A -> A: sign(SHA1-RSA, privateKey)
A -> S: send(envelope, timeout=8s)
S -> B: HTTPS POST /bank/transfer
alt 银行返回 1003
  B --> S: fault(1003)
  S --> A: fault
  A --> P: INSUFFICIENT_FUNDS
else 成功
  B --> S: response(tradeNo)
  A --> P: TransferResult(tradeNo)
end
note over A: 支付核心从未出现 SOAP 字段
@enduml""")

P["3.2"] = PD(
"生产实例：消息平台 × 序列化协议",
"""<p>消息平台要支持 Kafka 和 RabbitMQ，还要支持 JSON 与 Protobuf。按“通道+协议”建子类就是四种实现，再加 Pulsar 或 Avro 立刻翻倍。桥接把两维拆开：通道只管收发，编解码器只管字节，生产者持有“通道 + 编解码器”两个引用。</p>
<ul><li><b>协议演进</li></b>：同一通道可以从 JSON 切到 Protobuf，消费者按 header 里的 codec 选择解码器。</li>
<li><b>兼容性</li></b>：Protobuf 保留旧字段编号，JSON 保留未知字段。</li>
<li><b>性能</li></b>：编解码器无状态、可复用，避免每条消息新建。</li></ul>""",
["通道和编解码器不能互相知道对方实现类名", "消息头必须带 codec 标识，否则无法渐进迁移", "编解码失败要进死信队列，不能阻塞分区"],
"""@startuml
autonumber
participant "Producer" as P
participant "KafkaChannel" as K
participant "ProtoCodec" as C
participant "Broker" as B
participant "Consumer" as S

P -> K: publish(topic="orders", event, codec=protobuf)
K -> C: encode(event)
C --> K: bytes + schemaId
K -> B: send(partitionKey=orderId, headers{codec})
B --> S: consume(batch)
S -> C: decode(bytes, schemaId)
alt schema 不兼容
  C --> S: DecodeError
  S -> B: send(DLQ, raw)
else 成功
  C --> S: OrderEvent
end
note over K,C: 换 RabbitMQ 只换通道；换 Avro 只换编解码器
@enduml""")

P["3.3"] = PD(
"生产实例：RBAC 权限树（部门 / 角色 / 菜单）",
"""<p>后台权限是树：部门下有子部门，角色挂在部门，菜单挂在角色；鉴权要回答“这个用户能不能看这张报表”。如果每个层级各写一套遍历，加一层“数据权限”就要改所有调用方。组合模式让部门和菜单实现同一个 <code>check()</code>：部门递归孩子，菜单返回自身是否命中。</p>
<ul><li><b>缓存</li></b>：整棵权限树按 userId 缓存 5 分钟，角色变更时按部门失效。</li>
<li><b>默认拒绝</b>：没有命中的路径一律拒绝，避免“漏配即放行”。</li>
<li><b>审计</b>：每次拒绝记录命中路径，方便定位是哪个角色缺权限。</li></ul>""",
["枝和叶必须共用 check 接口，调用方不能判断节点类型", "空部门要返回拒绝，不能返回未初始化值", "缓存失效要精确到部门，不能全量清空"],
"""@startuml
interface PermissionNode {
  +check(userId, resource): Decision
}
class Department {
  +children: PermissionNode[]
  +check(userId, resource)
}
class Role {
  +menus: PermissionNode[]
  +check(userId, resource)
}
class Menu {
  +resourceId
  +check(userId, resource)
}
Department --> PermissionNode : children
Role --> PermissionNode : menus
Department --> Role : contains
Role --> Menu : grants
note right of Menu: 命中返回 ALLOW，否则 DENY
@enduml""")

P["3.4"] = PD(
"生产实例：API 网关中间件链（Trace / Auth / 限流 / 重试）",
"""<p>网关每个请求都要过：生成 traceId、校验 JWT、按租户限流、失败重试。把这些写进一个 handler，任何一步调整都要改整段。装饰器把每层做成独立中间件：<b>持有下一个 handler，进入前做事，必要时短路</b>。顺序由配置决定，不改业务代码。</p>
<ul><li><b>短路</li></b>：鉴权失败直接返回 401，不再进限流和业务。</li>
<li><b>可观测</li></b>：traceId 在最外层生成，后续日志统一带上。</li>
<li><b>顺序敏感</li></b>：限流必须在鉴权之后，否则匿名请求会打满配额。</li></ul>""",
["每层只做一件事，禁止在装饰器里写业务逻辑", "短路要显式返回，不能继续调用 next", "顺序由配置校验，错误顺序在启动时拒绝"],
"""@startuml
autonumber
participant "Client" as C
participant "TraceMiddleware" as T
participant "AuthMiddleware" as A
participant "RateLimitMiddleware" as R
participant "OrderHandler" as H

C -> T: POST /orders (no traceId)
T -> T: traceId = uuid()
T -> A: next(req + traceId)
A -> A: verify JWT
alt token 过期
  A --> T: 401 TOKEN_EXPIRED
  T --> C: 401 + traceId
else 通过
  A -> R: next(req + userId)
  R -> R: check quota(tenant)
  alt 超限
    R --> C: 429 + Retry-After
  else 放行
    R -> H: handle(req)
    H --> R: 201 Created
  end
end
@enduml""")

P["3.5"] = PD(
"生产实例：下单履约外观（库存 / 运费 / 支付 / 通知）",
"""<p>下单不是一次数据库写入：锁库存、算运费、建支付单、发履约消息，四步各有超时和失败模式。让每个入口自己排这四步，迟早漏补偿。外观提供 <code>placeOrder()</code> 一个入口，内部按顺序调用，<b>任一步失败按逆序补偿</b>。</p>
<ul><li><b>补偿</b>：支付单创建失败要释放库存；消息发送失败不回滚已支付订单，转而进重试表。</li>
<li><b>超时</b>：每步独立超时，总预算 3s，超时即失败。</li>
<li><b>幂等</li></b>：入口接收 clientOrderNo，重复请求返回同一结果。</li></ul>""",
["外观只编排，不实现库存/支付细节", "补偿操作必须自身幂等，允许重复执行", "通知失败不应回滚交易，改为异步重试"],
"""@startuml
autonumber
participant "API" as A
participant "OrderFacade" as F
participant "Inventory" as I
participant "Payment" as P
participant "Notifier" as N

A -> F: placeOrder(clientOrderNo, sku, qty)
F -> I: reserve(sku, qty)
I --> F: reservationId
F -> P: createPayment(orderNo, amount)
alt 支付单创建失败
  P --> F: TIMEOUT
  F -> I: release(reservationId)
  F --> A: 503 PAYMENT_UNAVAILABLE
else 成功
  P --> F: paymentId
  F -> N: send(OrderPlaced) (异步)
  F --> A: 201 {orderNo, paymentId}
end
note over F: 每步独立超时，总预算 3s；补偿幂等
@enduml""")

P["3.6"] = PD(
"生产实例：千万商品的类目 / 品牌 / 税率共享",
"""<p>商品库有上千万 SKU，但类目只有几千个，每个类目带名称、税率、展示模板。如果每个 SKU 都复制一份类目描述，内存和 GC 都受不了。享元把类目做成共享对象，SKU 只留类目 ID、价格、库存这些<b>外部状态</b>。</p>
<ul><li><b>不可变</li></b>：类目对象发布后只读，税率调整走新版本。</li>
<li><b>预热</li></b>：启动时加载热点类目，避免首屏抖动。</li>
<li><b>失效</li></b>：类目下架只从池里摘引用，不修改共享对象。</li></ul>""",
["共享对象必须不可变；任何 set 方法都应去掉", "池要有上限和淘汰，不能随用户输入无限增长", "外部状态（价格、库存）绝不能进共享对象"],
"""@startuml
class CategoryFlyweight {
  +categoryId
  +name
  +taxRate
  +templateId
}
class CategoryFactory {
  -cache: Map<Long, CategoryFlyweight>
  +get(categoryId): CategoryFlyweight
}
class Sku {
  +skuId
  +categoryId
  +price
  +stock
}
CategoryFactory --> CategoryFlyweight : caches
Sku --> CategoryFlyweight : shares
note right of CategoryFlyweight: 只读；税率变更生成新版本
note bottom of Sku: 每 SKU 只多存 ID/价格/库存
@enduml""")

P["3.7"] = PD(
"生产实例：商品目录远程服务代理（缓存 + 熔断）",
"""<p>商品目录是独立微服务，首页每秒几千次查询。直接调用会让下游抖动直接传到前端。代理站在真实客户端前面：<b>先查本地缓存，未命中再走远程；连续失败触发熔断，返回上一次的 stale 数据</b>。调用方仍然只调 <code>getSku()</code>。</p>
<ul><li><b>缓存</li></b>：按 SKU 缓存 60s，热点 key 加随机抖动防雪崩。</li>
<li><b>熔断</li></b>：10s 内错误率 > 50% 打开断路器，30s 后半开探测。</li>
<li><b>降级</li></b>：断路器打开时返回 stale 并标记 <code>degraded=true</code>。</li></ul>""",
["代理和真实客户端接口必须一致，调用方不能感知降级", "缓存要有失效与穿透保护，空值也要短缓存", "熔断状态要可观测，不能悄悄一直返回旧数据"],
"""@startuml
autonumber
participant "Web" as W
participant "CatalogProxy" as P
participant "LocalCache" as L
participant "CatalogService" as S

W -> P: getSku("A100")
P -> L: get("A100")
alt 命中
  L --> P: sku(version=7)
  P --> W: sku
else 未命中且断路器关闭
  P -> S: GET /sku/A100 (timeout=300ms)
  alt 成功
    S --> P: sku
    P -> L: put(ttl=60s + jitter)
    P --> W: sku
  else 连续失败
    S --> P: 5xx
    P -> P: openCircuit(30s)
    P --> W: stale + degraded=true
  end
else 断路器打开
  P --> W: stale + degraded=true
end
@enduml""")