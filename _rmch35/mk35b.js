const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 35,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const pts = [
  'CORE + PHY 分工、x16 DDR3L、400 MHz / 800 MT/s 与地址空间',
  '寄存器三组：core 0x0000、PHY 0x0800、debug 0x0410',
  '十三步上电序列与 CON_REQ/CON_ACK 握手',
  '时序换算：ns 换成时钟数，字段值为时钟数减一',
  '写均衡公式、1/8 周期粗调与 WL_CYC_DEL 补充',
  '读 DQS gating 与 read calibration 取窗口中点',
  'fly-by 拓扑、ODT/ZQ 端接与 memtester 压测层次'
];
const block = '{ "n": 35, "zh": "DDR 控制器 MMDC 与校准", "en": "Multi Mode DDR Controller", "pp": "\u0032\u0032\u0030\u0033\u2013\u0032\u0033\u0037\u0036", "pages": 174, "pri": "read", "batch": 3, "ready": true,\n' +
'          "line": "板子能不能亮的分水岭：DDR3L 初始化脚本与 write-leveling 校准。",\n' +
'          "pts": ' + JSON.stringify(pts) + ' }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');