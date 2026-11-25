const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 33,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 33, "zh": "矩阵键盘 KPP", "en": "Keypad Port", "pp": "2111\u20132130", "pages": 20, "pri": "opt", "batch": 2, "ready": true,\n' +
'          "line": "只有二十页、四个寄存器，却是练「开漏 + 上拉 + 同步 + 去抖」的最佳小外设。",\n' +
'          "pts": ["8\u00d78 矩阵与 16 根 ENET/NAND 复用脚，COL0 与 ROW2 同脚", "四个寄存器地图：KPCR/KPSR/KDDR/KPDR 与复位值 0x0400", "KPSR 低 4 位：KPKD/KPKR 的 w1c 与 KRSS/KDSC 两个自清位", "扫描时序：待机列全 0，扫描逐列拉 0，推挽充电再切开漏", "硬件 122 \u00b5s 同步 + 软件 3\u20134 遍比对，两层时间常数对齐", "ghost key 与二极矩阵、3-point 接法、低功耗唤醒与故障判据"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');