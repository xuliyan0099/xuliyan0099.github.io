const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 31,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 31, "zh": "I2C 控制器", "en": "I2C Controller", "pp": "1445\u20131468", "pages": 24, "pri": "read", "batch": 2, "ready": true,\n' +
'          "line": "START/重复 START、ACK、仲裁与分频，全在一个状态机里。",\n' +
'          "pts": ["开漏线与、上拉与时钟拉伸的电气基础", "四路 I2C 的焊盘与 ALT3，板上 I2C1/I2C2 接口", "五个 16 位寄存器与只允许半字访问", "IFDR 的 64 个固定分频：49.5 MHz 下 400k/100k 怎么选", "I2CR/I2SR 的位义与「写 0 清 IIF」等清除规则", "主发/主收流程（dummy read）与三层判据、9 脉冲救总线"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');