const fs = require('fs'), vm = require('vm');
const c = { window: {} };
vm.createContext(c);
vm.runInContext(fs.readFileSync('D:/Workspace/MainPage/imx6ull/rm/rm-data.js', 'utf8'), c);
const R = c.window.RM;
let chs = [];
if (Array.isArray(R.chapters)) chs = R.chapters;
else if (Array.isArray(R)) chs = R;
else {
  for (const k of Object.keys(R)) {
    const v = R[k];
    if (Array.isArray(v)) chs = chs.concat(v);
    else if (v && Array.isArray(v.chapters)) chs = chs.concat(v.chapters);
  }
}
const flat = chs.filter(x => x && typeof x === 'object' && 'n' in x);
console.log('total', flat.length, 'ready', flat.filter(x => x.ready).length);
for (const x of flat) if ([15, 16, 17, 18].includes(x.n)) console.log(x.n, x.ready, (x.pts || []).length);
