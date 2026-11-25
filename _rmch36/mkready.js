const fs = require('fs');
const path = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(path, 'utf8');

const data = {
  36: ["IOMUXC_GPR2 四个位域与 mclk 公式", "MQS 引脚复用与外部 RC 滤波", "音质边界：SNR 与 44.1k 跑调"],
  37: ["512×8 熔丝与影子寄存器映射", "解锁码 0x3E77 与写时序", "读锁返回 0xBADABADA 的判据"],
  38: ["128 KB 四 bank 64 位交错", "四个等待/流水旋钮 GPR3", "cache 与 DMA 一致性"],
  39: ["七路 LDO 与 TARGET 编码", "复位默认电压与 DVFS 调压", "弱稳压器三步与 USB LDO"],
  40: ["时钟源、分频与频率公式", "占空比、FIFO 与立即生效", "背光 BLT_PWM 的调光实践"],
  41: ["PS/AS/OUT 三级引擎与数据流", "CSC、LUT、dither 与 alpha", "摄像头→旋转缩放→LCD 的配置顺序"],
  42: ["IP 命令与 AHB 映射两条通道", "LUT 序列引擎与 IPCR 触发", "DDR/DQS 采样与擦写判据"],
  60: ["24MHz 起振电路与负载电容反推", "MISC0 与 LOWPWR_CTRL 逐位", "RC 自校准与实测判据"]
};

for (const n of Object.keys(data)) {
  const num = parseInt(n, 10);
  const re = new RegExp('\\{ "n": ' + num + ',[\\s\\S]*?"pts": \\[[^\\]]*\\] \\}', 'g');
  const m = s.match(re);
  if (!m || !m.length) { console.log(n + ' MISS'); continue; }
  let block = m[0];
  block = block.replace(/"pts": \[[^\]]*\]/, '"pts": ' + JSON.stringify(data[n]));
  if (!block.includes('"ready"')) {
    block = block.replace(/"batch": (\d+)/, '"batch": $1, "ready": true');
  }
  s = s.replace(m[0], block);
  console.log(n + ' ok ready=' + block.includes('"ready": true'));
}
fs.writeFileSync(path, s, 'utf8');
