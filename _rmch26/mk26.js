const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 26,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 26, "zh": "CAN 控制器 FLEXCAN", "en": "Flexible Controller Area Network", "pp": "1245–1324", "pages": 80, "pri": "read", "batch": 2, "ready": true,\n' +
'          "line": "邮箱、Rx FIFO、位时序三件事，车载开发绕不过去。",\n' +
'          "pts": ["MCR/CTRL1 全位域与 Freeze 配置法", "邮箱 16 字节结构与 CODE 收发状态机", "位时序三段与 500k/250k/1M 波特率算例", "RXIMR 个体掩码、Rx FIFO 六帧深与过滤", "ECR/ESR1 错误计数、Bus-Off 与 128×11 位恢复", "板级 CAN 引脚、收发器与 120 Ω 终端"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');
