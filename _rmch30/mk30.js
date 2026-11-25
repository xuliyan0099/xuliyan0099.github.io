const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 30,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 30, "zh": "GPT：捕获、比较与自由计数", "en": "General Purpose Timer", "pp": "1421\u20131444", "pages": 24, "pri": "read", "batch": 2, "ready": true,\n' +
'          "line": "三种计数模式 + 输入捕获，测脉宽、做长延时都靠它。",\n' +
'          "pts": ["GPT 与 EPIT 的互补：加法器、捕获、三路比较", "六种 CLKSRC 与两级分频（PRESCALER24M/PRESCALER）", "CR 全位域：OM 四种引脚动作、IM 四种边沿、FO 强制比较", "restart/free-run 与 OCR1 写入清零计数器的副作用", "SR/IR 的六个位：ROV/IF1-2/OF1-3 全 w1c", "捕获测周期与占空比的公式、精度与溢出处理"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');