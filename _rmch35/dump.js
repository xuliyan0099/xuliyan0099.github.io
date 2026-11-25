const fs=require('fs');
const s=fs.readFileSync('D:/Workspace/MainPage/imx6ull/rm/rm-data.js','utf8');
const parts=s.split('{ "n": ');
for(const p of parts.slice(1)){
  const n=parseInt(p);
  if(((n>=36&&n<=48)||(n>=55&&n<=60))){
    const obj=p.slice(0,p.indexOf('] }')+3);
    console.log('-----', n);
    console.log(obj.replace(/\s+/g,' '));
  }
}