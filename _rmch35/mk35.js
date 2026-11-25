const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 35,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 35, "zh": "DDR 控制器 MMDC 与校准", "en": "Multi Mode DDR Controller", "pp": "2203\u20132376", "pages": 174, "pri": "read", "batch": 3, "ready": true,\n' +
'          "line": "板子能不能亮的分水岭：DDR3L 初始化脚本与 write-leveling 校准。",\n' +
'          "pts": ["CORE + PHY 分工、x16 DDR3L、400 MHz/800 MT/s 与地址空间", "寄存器三组：core 0x0000、PHY 0x0800、debug 0x0410", "十三步上电序列与 CON_REQ/CON_ACK 握手", "时序换算：ns \u2192 \u65cb\u8f6a\u6570 \u2192 \u5b57\u6bb5\u503c-\u2013 \u7b2c\u8fc0" , "写均衡公式与 1/8 cycle、WL_CYC_DEL \u4f2f\u6577", "读 DQS gating + read calibration \u53d6\u7a97\u53e1\u4e2d\u70b9", "fly-by 拓扑\u3001ODT/ZQ\u3001memtester \u4e0e\u5b9c\u8e29\u5c42\u6b21"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');