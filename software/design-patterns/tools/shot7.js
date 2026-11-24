const { spawn } = require('child_process');
const fs = require('fs');
const edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const dir = 'C:/Users/xuliy/AppData/Local/Temp/dpbook3/shot7-' + Date.now();
const [url, out, w, h] = process.argv.slice(2);
const child = spawn(edge, ['--headless=new','--disable-gpu','--remote-debugging-port=9421','--user-data-dir='+dir,'--window-size='+w+','+h, url], {stdio:'ignore'});
setTimeout(async () => {
  const list = await (await fetch('http://127.0.0.1:9421/json/list')).json();
  const page = list.find(t=>t.type==='page' && t.url.includes('design-patterns')) || list.find(t=>t.type==='page'); const ws = new WebSocket(page.webSocketDebuggerUrl); let id=0;
  const call=(m,p={})=>new Promise(res=>{const cid=++id;const hh=e=>{const d=JSON.parse(e.data);if(d.id===cid){ws.removeEventListener('message',hh);res(d.result);}};ws.addEventListener('message',hh);ws.send(JSON.stringify({id:cid,method:m,params:p}));});
  ws.onopen = async () => {
    await call('Page.enable');
    await call('Emulation.setDeviceMetricsOverride',{width:+w,height:+h,deviceScaleFactor:1,mobile:false});
    await call('Page.reload'); await new Promise(r=>setTimeout(r,1200));
    for (let i=0;i<20;i++){ const r=await call('Runtime.evaluate',{expression:`(()=>{const im=document.querySelector('#s7 .puml-shot img');return im&&im.complete&&im.naturalWidth>0})()`,returnByValue:true}); if(r.result.value) break; await new Promise(r=>setTimeout(r,250)); }
    const m = await call('Runtime.evaluate',{expression:`(()=>{const im=document.querySelector('#s7 .puml-shot img');im.scrollIntoView({block:'start'});return JSON.stringify({nat:[im.naturalWidth,im.naturalHeight],dw:document.documentElement.scrollWidth,iw:innerWidth})})()`,returnByValue:true});
    console.log(m.result.value);
    await new Promise(r=>setTimeout(r,500));
    const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
    fs.writeFileSync(out, Buffer.from(shot.data,'base64')); child.kill(); process.exit(0);
  };
}, 2500);
