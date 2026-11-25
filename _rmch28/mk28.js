const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 28,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 28, "zh": "GPIO：数据、方向与中断", "en": "General Purpose Input/Output", "pp": "1343\u20131370", "pages": 28, "pri": "read", "batch": 1, "ready": true,\n' +
'          "line": "五个 bank 的七个寄存器，点灯、读键、边沿中断全在这一页表里。",\n' +
'          "pts": ["五个 bank 基址与 8 个偏移：DR/GDIR/PSR/ICR1/ICR2/IMR/ISR/EDGE_SEL", "读 DR 的四种组合：非 GPIO 且输入时恒为 0", "PAD 六个旋钮：PKE/PUS/ODE/DSE/SRE/HYS", "ICR 四种触发条件与 IMR 的 1=使能极性", "ISR 写 1 清零、与 IMR 无关，电平触发易中断风暴", "板级 LED0/KEY0/BEEP 的点灯与读键流程"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');