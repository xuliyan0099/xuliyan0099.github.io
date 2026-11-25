const fs = require('fs');
const vm = require('vm');
const src = fs.readFileSync('D:/Workspace/MainPage/imx6ull/rm/rm-data.js', 'utf8');
const ctx = { window: {} };
vm.createContext(ctx);
vm.runInContext(src, ctx);
const RM = ctx.window.RM || [];
console.log('entries', RM.length, 'ready', RM.filter(x => x.ready).length);
for (const x of RM) if ([15, 16, 17, 18].includes(x.n)) console.log(x.n, x.ready, (x.pts || []).length);
