const fs=require("fs");
const s=fs.readFileSync("imx6ull/rm/rm-data.js","utf8");
const re=/\{\s*"n":\s*(\d+),([\s\S]*?)\}/g;
let m, ready=[];
while((m=re.exec(s))){ if(/"ready":\s*true/.test(m[2])) ready.push(+m[1]); }
console.log(ready.join(","));
