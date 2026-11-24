const { spawn } = require('child_process');
const edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const dir = 'C:/Users/xuliy/AppData/Local/Temp/dpbook3/mt-' + Date.now();
const [url, w, h] = process.argv.slice(2);
const child = spawn(edge, ['--headless=new','--disable-gpu','--remote-debugging-port=9418','--user-data-dir='+dir,'--window-size='+w+','+h, url], {stdio:'ignore'});
setTimeout(async () => {
  const list = await (await fetch('http://127.0.0.1:9418/json/list')).json();
  const page = list.find(t => t.type === 'page' && t.url.includes('design-patterns')) || list.find(t=>t.type==='page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0;
  const call = (m, p={}) => new Promise(res => { const cid = ++id; const hh = e => { const d = JSON.parse(e.data); if (d.id === cid) { ws.removeEventListener('message', hh); res(d.result); } }; ws.addEventListener('message', hh); ws.send(JSON.stringify({id:cid, method:m, params:p})); });
  ws.onopen = async () => {
    await call('Page.enable');
    await call('Emulation.setDeviceMetricsOverride', {width:+w, height:+h, deviceScaleFactor:1, mobile:false});
    await call('Page.reload'); await new Promise(r=>setTimeout(r,1600));
    const expr = `(()=>{const s=document.getElementById('s7'),im=s.querySelector('.puml-shot img'),b=s.querySelector('.puml-box'),sh=s.querySelector('.puml-shot');const r=e=>{const x=e.getBoundingClientRect();return {w:Math.round(x.width),h:Math.round(x.height),l:Math.round(x.left),t:Math.round(x.top)}};return JSON.stringify({iw:innerWidth,dw:document.documentElement.scrollWidth,sec:r(s),shot:r(sh),img:r(im),nat:[im.naturalWidth,im.naturalHeight],complete:im.complete,dets:r(b),side:r(document.querySelector('aside')),fonts:document.querySelectorAll('.side-sub li').length})})()`;
    const r = await call('Runtime.evaluate', {expression: expr, returnByValue:true});
    console.log(r.result.value || JSON.stringify(r));
    child.kill(); process.exit(0);
  };
}, 2500);
