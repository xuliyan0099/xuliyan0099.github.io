const fs = require('fs');
const p = 'D:/Workspace/MainPage/imx6ull/rm/rm-data.js';
let s = fs.readFileSync(p, 'utf8');
const m = s.match(/\{ "n": 34,[\s\S]*?"pts": \[[^\]]*\] \}/);
if (!m) { console.error('no match'); process.exit(1); }
const block = '{ "n": 34, "zh": "RGB 屏接口 eLCDIF", "en": "Enhanced LCD Interface", "pp": "2131\u20132202", "pages": 72, "pri": "read", "batch": 4, "ready": true,\n' +
'          "line": "RGB 屏点不亮、花屏、偏移，都是这七八个时序参数没算对。",\n' +
'          "pts": ["四种接口（MPU/VSYNC/DOTCLK/DVI）与只有一套寄存器的关系", "寄存器地图 0x021C_8000 与 SET/CLR/TOG 别名，复位 C000_0000", "六个 porch 换算成 VDCTRL1/2/3/4：928\\u00d7525 的完整算例", "pix_clk 下限 = H_TOTAL\\u00d7V_TOTAL\\u00d7刷新，含消隐的带宽", "LFIFO 512 \\u4e2a 32bpp \\u4e0e underflow\\u3001panic \\u9608\\u503c\\u3001\\u53cc\\u7f13\\u51b2", "VDCTRL0 \\u5355\\u4f4d\\u4f4d\\u4e0e\\u6781\\u6027\\u3001BYPASS_COUNT\\u3001SYNC_SIGNALS_ON", "\\u9ed1\\u5c4f/\\u82b1\\u5c4f/\\u6eda\\u52a8/\\u6a2a\\u7eb9\\u7684\\u56db\\u5c42\\u5224\\u636e"] }';
s = s.replace(m[0], block);
fs.writeFileSync(p, s, 'utf8');
console.log('ok');