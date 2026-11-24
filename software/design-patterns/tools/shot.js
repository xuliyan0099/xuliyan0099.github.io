const { spawn } = require('child_process');
const fs = require('fs');
const edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const dir = 'C:/Users/xuliy/AppData/Local/Temp/dpbook3/shot-' + Date.now();
const [url, out, w, h] = process.argv.slice(2);
const child = spawn(edge, ['--headless=new','--disable-gpu','--remote-debugging-port=9417','--user-data-dir='+dir,'--window-size='+w+','+h, url], {stdio:'ignore'});
setTimeout(async () => {
  const list = await (await fetch('http://127.0.0.1:9417/json/list')).json();
  const page = list.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0;
  const call = (m, p={}) => new Promise(res => { const cid = ++id; const hh = e => { const d = JSON.parse(e.data); if (d.id === cid) { ws.removeEventListener('message', hh); res(d.result); } }; ws.addEventListener('message', hh); ws.send(JSON.stringify({id:cid, method:m, params:p})); });
  ws.onopen = async () => {
    await call('Page.enable');
    await call('Emulation.setDeviceMetricsOverride', {width:+w, height:+h, deviceScaleFactor:1, mobile:false});
    await call('Page.reload'); await new Promise(r=>setTimeout(r,1500));
    await call('Runtime.evaluate', {expression: `document.getElementById('s7').scrollIntoView();JSON.stringify({iw:innerWidth,dw:document.documentElement.scrollWidth,secs:document.querySelectorAll('section.sec').length})`, returnByValue:true}).then(r=>console.log(r.result.value));
    await new Promise(r=>setTimeout(r,400));
    const shot = await call('Page.captureScreenshot', {format:'png', captureBeyondViewport:false});
    fs.writeFileSync(out, Buffer.from(shot.data,'base64'));
    child.kill(); process.exit(0);
  };
}, 2500);
