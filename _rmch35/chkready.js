const fs=require('fs');
const s=fs.readFileSync('D:/Workspace/MainPage/imx6ull/rm/rm-data.js','utf8');
for (const p of s.split('{ "n": ').slice(1)) {
  const n=parseInt(p);
  if (n>=36 && n<=42 || n===60) {
    const head=p.slice(0, 120).replace(/\s+/g,' ');
    console.log(n, head.includes('ready') ? 'HAS-READY-FLAG' : 'no-ready', head.includes('"ready": true') ? 'TRUE' : '');
  }
}