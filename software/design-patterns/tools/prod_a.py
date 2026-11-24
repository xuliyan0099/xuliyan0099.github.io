# -*- coding: utf-8 -*-
from prod_lib import PD

P = {}

P["2.1"] = PD(
"生产实例：支付渠道工厂（Alipay / WeChat / Stripe）",
"""<p>支付网关不可能只接一家渠道。线上常见做法是<b>渠道注册表 + 工厂</b>：下单主流程只说 <code>channel="wechat"</code>，工厂按名字取出 provider，同时校验该渠道的开关、限额、密钥版本。新增 Stripe 只注册一个 provider，不改下单代码。</p>
<ul><li><b>密钥轮换</b>：provider 构造时绑定密钥版本，旧版本在宽限期内仍可退款。</li>
<li><b>渠道降级</b>：主渠道超时后由工厂返回备用 provider，但订单号与幂等键保持不变。</li>
<li><b>可观测</b>：每次 create 记录 channel、keyVersion、耗时，便于按渠道看错误率。</li></ul>""",
["渠道名拼错必须显式失败，不能默认落到第一家", "provider 无状态或只读，回调并发时不能共享可变字段", "工厂不负责重试；重试策略放在上层，避免重复扣款"],
"""@startuml
autonumber
participant "OrderService" as O
participant "PaymentFactory" as F
participant "ProviderRegistry" as R
participant "WeChatProvider" as W
participant "AlipayProvider" as A

O -> F: create("wechat", merchant, keyVer=3)
F -> R: lookup("wechat")
R --> F: WeChatProvider
F -> W: new(merchant, keyVer)
F --> O: provider
O -> W: pay(orderNo, idemKey, 199.00)
alt 渠道超时
  O -> F: create("alipay", merchant, keyVer=7)
  F --> O: AlipayProvider
  O -> A: pay(同一 idemKey)
  note right of A: 幂等键不变，避免重复扣款
else 成功
  W --> O: tradeNo + SUCCESS
end
@enduml""")

P["2.2"] = PD(
"生产实例：多云部署的整族资源（AWS / GCP）",
"""<p>一家公司同时跑 AWS 和 GCP：计算、对象存储、消息队列必须落在<b>同一云、同一区域</b>，否则跨云出网费和合规审计都会失控。抽象工厂按 <code>cloud=aws, region=ap-southeast-1</code> 一次交付三件资源，部署器拿不到“单独换一件”的机会。</p>
<ul><li><b>区域合规</b>：欧洲租户只能拿 eu-central-1 的整族资源，工厂在入口校验。</li>
<li><b>成本标签</b>：每个资源带 costCenter，账单按族聚合。</li>
<li><b>失败回滚</b>：第三件创建失败时，前两件必须按创建逆序销毁。</li></ul>""",
["工厂返回的资源必须属于同一 region，不能只校验云厂商", "资源创建失败要回滚，禁止留下半套基础设施", "族内资源数量会增长，但不要塞进与部署无关的产品（如 CDN）"],
"""@startuml
autonumber
participant "Deployer" as D
participant "CloudFactory(AWS)" as F
participant "EC2" as C
participant "S3" as S
participant "SQS" as Q

D -> F: provision(region="ap-southeast-1")
F -> C: createInstance(vpc, ami)
C --> F: i-0abc
F -> S: createBucket(region, kmsKey)
S --> F: bucket-xyz
F -> Q: createQueue(region)
alt 队列创建失败
  F -> S: deleteBucket(bucket-xyz)
  F -> C: terminate(i-0abc)
  F --> D: ProvisionFailed(rolledBack=true)
else 成功
  Q --> F: queue-url
  F --> D: ResourceSet{compute, storage, queue}
end
note over D: 三件资源同云同区，账单按 costCenter 聚合
@enduml""")

P["2.3"] = PD(
"生产实例：履约单组装（仓、承运商、保价、发票）",
"""<p>履约单有二十多个字段，来自库存、承运商、关税、发票四个系统。直接写一个巨型构造函数，调用方靠位置参数记忆，线上就出现过“保价传成了发票类型”的事故。建造者把每一步变成具名方法，<b>build() 时统一校验</b>：没有保价、没有报关单、地址缺邮编，一律拒绝交付。</p>
<ul><li><b>部分失败</b>：承运商报价失败时保留已选仓库，允许换承运商重试。</li>
<li><b>不可变成品</b>：交付后的履约单禁止再改，防止后续步骤偷改运费。</li>
<li><b>审计</b>：每步记录操作人和时间，出问题能还原拼装过程。</li></ul>""",
["build() 之前允许重试某一步，build() 之后成品只读", "校验规则要版本化，历史订单按当时规则解释", "不要把外部调用塞进建造者，网络失败会让半成品长期占用内存"],
"""@startuml
autonumber
participant "OrderService" as O
participant "FulfillmentBuilder" as B
participant "Inventory" as I
participant "Carrier" as C

O -> B: new(orderId)
O -> B: warehouse("SHA-01")
B -> I: lockStock(sku, qty)
I --> B: reserved
O -> B: carrier("SF", insured=true)
B -> C: quote(address, weight)
alt 报价失败
  C --> B: TIMEOUT
  B --> O: Retryable("换承运商")
  O -> B: carrier("JD", insured=true)
  B -> C: quote(address, weight)
end
O -> B: invoice(taxNo, type="VAT")
O -> B: build()
B -> B: validate()
alt 缺报关单
  B --> O: Invalid("CUSTOMS_DOC_MISSING")
else 校验通过
  B --> O: Fulfillment(只读)
end
@enduml""")

P["2.4"] = PD(
"生产实例：多租户报表模板克隆",
"""<p>SaaS 报表平台给每个租户一份模板：列顺序、公式、时区、币种。模板对象内部有公式 AST 和样式表指针，直接赋值会让所有租户共享同一份，某租户改列就污染全体。原型模式让登记表 <code>clone()</code> 出<b>深拷贝</b>，租户只改自己的副本。</p>
<ul><li><b>模板升级</b>：平台升级只影响之后创建的租户，存量租户保持旧版可回滚。</li>
<li><b>内存</b>：公式 AST 不可变，可共享；样式表按引用计数复制。</li>
<li><b>一致性</b>：克隆时校验必填列，缺列直接失败而不是运行时报错。</li></ul>""",
["含指针/容器的对象必须深拷贝，浅拷贝会让租户互相污染", "原型只读；任何“原地改模板”的接口都应删除", "克隆要带版本号，升级与回滚才有依据"],
"""@startuml
autonumber
participant "TenantService" as T
participant "TemplateRegistry" as R
participant "MonthlyTemplate" as M
participant "TenantCopy" as C

T -> R: clone("monthly", tenant=42)
R -> M: deepCopy()
M -> M: copy formula AST (immutable, shared)
M -> M: copy style table (refcount++)
M --> R: new template
R -> R: validateRequiredColumns()
alt 缺“税额”列
  R --> T: InvalidTemplate
else 通过
  R --> T: TenantCopy(version=7)
end
T -> C: setTimezone("Asia/Shanghai")
note right: 只改副本，原型仍为 UTC
@enduml""")

P["2.5"] = PD(
"生产实例：配置中心客户端单例",
"""<p>每个进程只需要一个配置中心客户端：它维护长轮询、本地缓存、版本号。如果每个模块各 new 一个，长连接数翻倍，配置变更还会出现“同一进程内两个版本”。单例把初始化和长轮询收在一个入口后面，首次调用时注册监听。</p>
<ul><li><b>并发首次初始化</b>：多线程同时 get，只允许一个线程建连。</li>
<li><b>测试隔离</li></b>：提供 <code>resetForTest()</code>，生产代码不暴露。</li>
<li><b>fork 安全</li></b>：子进程继承锁会死锁，fork 后重置。</li></ul>""",
["不要用裸双重检查；C++ 用局部静态，C 用 pthread_once", "单例只放“进程级唯一”的东西，业务缓存不要塞进来", "首次初始化失败要允许重试，不能永久卡在坏状态"],
"""@startuml
autonumber
participant "Thread-A" as A
participant "Thread-B" as B
participant "ConfigClient" as C
participant "ConfigServer" as S

A -> C: get()
C -> C: lock(once)
C -> S: connect + longPoll(version=0)
S --> C: snapshot(v=41)
C --> A: instance(v=41)
B -> C: get()
alt 初始化未完成
  B -> B: wait(once)
else 已完成
  C --> B: 同一实例(v=41)
end
S -> C: push(v=42)
C -> C: update cache, notify listeners
note over A,B: 全进程只有一个长连接、一个版本号
@enduml""")