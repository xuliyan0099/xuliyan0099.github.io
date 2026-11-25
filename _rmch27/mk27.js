const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 27,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 27, "zh": "电源门控 GPC", "en": "General Power Controller", "pp": "1325–1342", "pages": 18, "pri": "opt", "batch": 6, "ready": true,\n' +
'          "line": "按域断电、按域唤醒；GPC 里还藏着一个中断控制器。",\n' +
'          "pts": ["GPC 与 CCM/SRC 的分工：pdn_req、时钟、复位", "GPC_CNTR 位域：L2_PGE、GPCIRQM、MEGA/DISPLAY 请求", "PGC 的 SW/SW2ISO/ISO/ISO2SW 四个时序参数", "硅版本 1.0/1.1 的 2048 与 64 倍快档", "IMR1–4/ISR1–4：128 个唤醒源的掩码与状态"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');
