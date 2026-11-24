const fs=require('fs');
const html=fs.readFileSync('asm/index.html','utf8');
const m=html.match(/<script>([\s\S]*?)<\/script>/);
if(!m){console.log('NO SCRIPT');process.exit(1);}
try{ new Function(m[1]); console.log('JS OK, len='+m[1].length); }catch(e){ console.log('JS ERR: '+e.message); }
