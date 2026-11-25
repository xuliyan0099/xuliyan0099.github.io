const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 32,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 32, "zh": "IOMUXC：复用、电气属性与 daisy chain", "en": "IOMUX Controller", "pp": "1469\u20132110", "pages": 642, "pri": "table", "batch": 1, "ready": true,\n' +
'          "line": "全片最常查的 642 页：MUX_MODE 选功能，PAD_CTL 定电气，SELECT_INPUT 接输入。",\n' +
'          "pts": ["IOMUXC/IOMUX/IORING 三层结构与 ALT0\u20137、ALT6/7 优先级", "MUX_CTL 的 MUX_MODE 与 SION：GPIO 脚复位为何是 ALT5", "PAD_CTL 位域与 0x10B0 解码：keeper、PUS 四档、DSE 阻抗表", "SPEED 四档与 SRE：为什么不能一律拉满", "SELECT_INPUT 的 daisy chain：焊盘 + ALT 成对配置", "板级冲突图谱（NAND/CSI/I2C/ENET）与读回校验流程"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');