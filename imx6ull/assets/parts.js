/* 硬件篇 · 全书目录数据。ready=true 表示该章已上线，其余显示“筹备中”。 */
window.PARTS = [
  {
    id: 'p1', no: '一', title: '电学与器件基础',
    sub: '先把每个值算出来，再谈电路',
    intro: '这一篇补的是最底层的账：电压电流怎么量、分压怎么算、功率会不会烧、电容电感各管什么。所有例子都取自这块板子上的真实元件。',
    chapters: [
      { n: '1.1', t: '三种基本量', s: '电压、电流、电阻在一块板上怎么量', f: 'c01.html', ready: true },
      { n: '1.2', t: '欧姆定律与分压', s: '上拉为什么是 10k，4.7k 又在管什么', f: 'c02.html', ready: true },
      { n: '1.3', t: '功率、发热与降额', s: '一颗 0402 到底能扛多少毫安', f: 'c03.html', ready: true },
      { n: '1.4', t: '电容', s: '充放电、RC 时间常数、两种容值为什么并存', f: 'c04.html', ready: true },
      { n: '1.5', t: '电感与磁珠', s: '储能和滤波不是一回事', f: 'c05.html', ready: true },
      { n: '1.6', t: '二极管家族', s: '整流、肖特基、齐纳、TVS、LED', f: 'c06.html', ready: true },
      { n: '1.7', t: '三极管与 MOS', s: '开关、放大、栅极电荷', f: 'c07.html', ready: true },
      { n: '1.8', t: '运放与比较器', s: '虚短虚断、跟随、迟滞', f: 'c08.html', ready: true },
      { n: '1.9', t: '数字电平', s: '3.3V 与 5V 能不能直连', f: 'c09.html', ready: true },
      { n: '1.10', t: '四种小电阻', s: '上拉、下拉、串阻、终端各治什么病', f: 'c10.html', ready: true }
    ]
  },
  {
    id: 'p2', no: '二', title: '元器件：从丝印读到规格书',
    sub: '认得出、读得懂、选得对',
    intro: '每一类元件单独一章：怎么在板上认出它、丝印代表什么、规格书只看哪几行、选错了板子会怎样。',
    chapters: [
      { n: '2.1', t: '电阻', s: '封装、精度、温漂、额定功率、排阻与 0Ω', f: 'c01.html', ready: true },
      { n: '2.2', t: '电容', s: 'MLCC 材质、直流偏压降容、钽与聚合物、ESR', f: 'c02.html', ready: true },
      { n: '2.3', t: '电感', s: '饱和电流、DCR、屏蔽、DCDC 电感怎么选', f: 'c03.html', ready: true },
      { n: '2.4', t: '二极管与 TVS', s: '正向压降、反向漏电、钳位电压、结电容', f: 'c04.html', ready: true },
      { n: '2.5', t: '三极管与 MOS', s: 'Vgs(th)、Rds(on)、Qg、热阻', f: 'c05.html', ready: true },
      { n: '2.6', t: '电源 IC', s: 'LDO 与 DCDC 规格书的关键页', f: 'c06.html', ready: true },
      { n: '2.7', t: '接口与逻辑 IC', s: '电平转换、缓冲、模拟开关、ESD 阵列', f: 'c07.html', ready: true },
      { n: '2.8', t: '怎么读数据手册', s: '绝对最大值、推荐条件、时序表、封装图', f: 'c08.html', ready: true }
    ]
  },
  {
    id: 'p3', no: '三', title: '逐页读这块板子的原理图',
    sub: '正点原子 MINI 底板 V2.2 + CORE V2.0 核心板',
    intro: '以这两份 PDF 原理图为教材，一页一章：列出这一页所有网络、逐个器件说出取值理由、点出最容易画错的地方。MINI 底板 4 页、核心板 8 页，全部拆开读。',
    chapters: [
      { n: '3.1', t: '图纸怎么读', s: '页序、网络命名、位号、跨页连接', f: 'c01.html', ready: true },
      { n: '3.2', t: '核心板第 1 页：六路电源逐个算', s: 'SNVS / CSI / ARM-SOC / VDD_HIGH / LVDDR3 / SD 可切', f: 'c02.html', ready: true },
      { n: '3.3', t: '核心板第 2 页：SoC 电源脚', s: 'VDD_ARM_CAP、VDD_SOC_CAP、SNVS 常电', f: 'c03.html', ready: true },
      { n: '3.4', t: '核心板第 3 页：DDR3L', s: '拓扑、VREF 1.5k 分压、端接、等长', f: 'c04.html', ready: true },
      { n: '3.5', t: '核心板第 4 页：eMMC 与 NAND', s: '10k 上拉、双存储位号、NVCC_SD 切换', f: 'c05.html', ready: true },
      { n: '3.6', t: '核心板第 5 页：LCD、以太网、GPIO、USB', s: '24 位 RGB、RMII 七根线、时钟串阻、VBUS 电容', f: 'c06.html', ready: true },
      { n: '3.7', t: '核心板第 6 页：ONOFF、复位与两颗晶振', s: 'POR_B、MAX809R、24MHz 18pF、RTC 32.768kHz', f: 'c07.html', ready: true },
      { n: '3.8', t: '核心板第 7 页：BOOT 配置的 47K 阵列', s: 'BT_CFG1/2/4 共 24 位、BMODE 表、4.7k 覆盖 47k', f: 'c08.html', ready: true },
      { n: '3.9', t: '核心板第 8 页：60pin 连接器与整板信号', s: 'J1/J2 定义、电源脚分布、连接器寄生的代价', f: 'c09.html', ready: true },
      { n: '3.10', t: 'MINI 第 1 页：连接器、启动拨码、I2C 与 JTAG', s: 'IMX1/IMX2、47k 上拉、8 位拨码、调试口', f: 'c10.html', ready: true },
      { n: '3.11', t: 'MINI 第 2 页：TF、CAN、RS485 与人机外设', s: 'TJA1050、SP3485 自动方向、屏与摄像头', f: 'c11.html', ready: true },
      { n: '3.12', t: 'MINI 第 3–4 页：以太网与电源树，一页看全板', s: 'SR8201F+变压器、DCJW5060 ×2、USB/CH340', f: 'c12.html', ready: true }
    ]
  },
  {
    id: 'p4', no: '四', title: '设计与计算',
    sub: '把“通常”“大概”全部换成公式和数字',
    intro: '第三篇里出现的每个值，在这里算一遍：电流预算、DCDC 外围、LDO 热、PDN、上下拉、复位与晶振、采样、测量与故障注入。',
    chapters: [
      { n: '4.1', t: '电流预算与选型', s: '一张表算出总功耗、峰值与余量', f: 'c01.html', ready: true },
      { n: '4.2', t: 'DCDC 外围计算', s: '电感、输出电容、反馈电阻、纹波', f: 'c02.html', ready: true },
      { n: '4.3', t: 'LDO 热设计', s: '结温、热阻、铜箔面积', f: 'c03.html', ready: true },
      { n: '4.4', t: '去耦与 PDN', s: '目标阻抗、容值组合、平面谐振', f: 'c04.html', ready: true },
      { n: '4.5', t: '上下拉与终端取值', s: 'I2C 4.7K、CAN 120Ω、DDR 470Ω 的推导', f: 'c05.html', ready: true },
      { n: '4.6', t: '复位与晶振计算', s: 'MAX809、18pF 负载电容、负阻裕度', f: 'c06.html', ready: true },
      { n: '4.7', t: '分压与采样', s: 'LSB、源阻抗、误差合成、抗混叠', f: 'c07.html', ready: true },
      { n: '4.8', t: '测量与故障注入', s: '五步上电、四种波形测法、十组注入', f: 'c08.html', ready: true }
    ]
  },
  {
    id: 'p5', no: '五', title: 'PCB 设计与制造',
    sub: '从网表到一块能上电的板',
    intro: '库与封装、叠层与阻抗、布局、布线、DDR 专题、电源平面、DFM、出图下单、贴片、首板点亮。',
    chapters: [
      { n: '5.1', t: '库与封装', s: '封装画错的六种后果', f: 'c01.html', ready: false },
      { n: '5.2', t: '叠层与阻抗', s: '4/6 层怎么定、怎么和板厂谈', f: 'c02.html', ready: false },
      { n: '5.3', t: '布局', s: '电源、SoC、DDR、接口、晶振的摆放顺序', f: 'c03.html', ready: false },
      { n: '5.4', t: '布线', s: '阻抗、回流、过孔、跨分割', f: 'c04.html', ready: false },
      { n: '5.5', t: 'DDR 布线专题', s: '拓扑、等长、VREF、地过孔', f: 'c05.html', ready: false },
      { n: '5.6', t: '电源平面与散热', s: '铜皮、散热焊盘、过孔阵列', f: 'c06.html', ready: false },
      { n: '5.7', t: 'DRC 与 DFM', s: '丝印、拼板、工艺边、测试点', f: 'c07.html', ready: false },
      { n: '5.8', t: '出图、贴片、首板点亮', s: 'Gerber、BOM/CPL、回流、十步法', f: 'c08.html', ready: false }
    ]
  },
  {
    id: 'p6', no: '六', title: '进阶：EMC、可靠性与量产',
    sub: '不只是能跑，还要跑得住',
    intro: 'ESD 与浪涌、EMI、信号完整性、热设计、降额与可靠性、量产测试与认证入门。',
    chapters: [
      { n: '6.1', t: 'ESD 与浪涌', s: 'TVS 选型、钳位、放哪儿才有用', f: 'c01.html', ready: false },
      { n: '6.2', t: 'EMI 与屏蔽', s: '辐射从哪来、地平面、磁珠与共模电感', f: 'c02.html', ready: false },
      { n: '6.3', t: '信号完整性基础', s: '反射、端接、眼图、TDR', f: 'c03.html', ready: false },
      { n: '6.4', t: '热设计', s: '结温、散热片、铜箔、风道', f: 'c04.html', ready: false },
      { n: '6.5', t: '降额与可靠性', s: '温度循环、MTBF、三防', f: 'c05.html', ready: false },
      { n: '6.6', t: '量产测试与认证', s: 'ICT/FCT、烧录工装、老化、CE/FCC', f: 'c06.html', ready: false }
    ]
  }
];

window.PART_OF = function (n) {
  var major = String(n).split('.')[0];
  var map = { '1': 'p1', '2': 'p2', '3': 'p3', '4': 'p4', '5': 'p5', '6': 'p6' };
  return map[major] || 'p1';
};



