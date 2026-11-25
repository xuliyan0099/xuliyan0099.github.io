const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 29,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 29, "zh": "NAND 控制器 GPMI", "en": "General Purpose Media Interface", "pp": "1371\u20131420", "pages": 50, "pri": "read", "batch": 3, "ready": true,\n' +
'          "line": "NAND 的时序、命令与数据搬运，和 BCH 一起构成一条 ECC 流水线。",\n' +
'          "pts": ["GPMI + APBH DMA + BCH 的分工与 50/200 MB/s 上限", "CTRL0 全位域：COMMAND_MODE/ADDRESS/CLE-ALE/XFER_COUNT", "TIMING0 的 tAS/tDS/tDH 与写 0 即 256 的陷阱", "EDO 采样窗：DELAY = tREA+4ns-tRP，RDN_DELAY 与 HALF_PERIOD", "ECCCTRL/ECCCOUNT 与 BUFFER_MASK 0x1FF 整页规则", "初始化六步与三层判据（模块/器件/数据）"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');