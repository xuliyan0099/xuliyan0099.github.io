const { spawn } = require('child_process');
const edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const dir = 'C:/Users/xuliy/AppData/Local/Temp/dpbook3/of-' + Date.now();
const url = process.argv[2];
const child = spawn(edge, ['--headless=new','--disable-gpu','--remote-debugging-port=9420','--user-data-dir='+dir,'--window-size=390,844', url], {stdio:'ignore'});
setTimeout(async () => {
  const list = await (await fetch('http://127.0.0.1:9420/json/list')).json();
  const page = list.find(t=>t.type==='page');
  const ws = new WebSocket(page.webSocketDebuggerUrl); let id=0;
  const call=(m,p={})=>new Promise(res=>{const cid=++id;const hh=e=>{const d=JSON.parse(e.data);if(d.id===cid){ws.removeEventListener('message',hh);res(d.result);}};ws.addEventListener('message',hh);ws.send(JSON.stringify({id:cid,method:m,params:p}));});
  ws.onopen = async () => {
    await call('Page.enable');
    await call('Emulation.setDeviceMetricsOverride', {width:390,height:844,deviceScaleFactor:2,mobile:false});
    await call('Page.reload'); await new Promise(r=>setTimeout(r,1600));
    const r = await call('Runtime.evaluate', {expression:`JSON.stringify({iw:innerWidth,dw:document.documentElement.scrollWidth,bad:[...document.querySelectorAll('*')].map(e=>{const x=e.getBoundingClientRect();return {t:e.tagName,c:String(e.className).slice(0,30),r:Math.round(x.right),w:Math.round(x.width)}}).filter(o=>o.r>innerWidth+1).slice(0,12)})`, returnByValue:true});
    console.log(r.result.value); child.kill(); process.exit(0);
  };
}, 2500);
