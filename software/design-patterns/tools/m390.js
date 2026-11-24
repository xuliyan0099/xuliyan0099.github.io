const { spawn } = require('child_process');
const edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const dir = 'C:/Users/xuliy/AppData/Local/Temp/dpbook2/m390-' + Date.now();
const url = 'http://192.168.1.52:8090/software/design-patterns/p2/c01.html';
const child = spawn(edge, ['--headless=new','--disable-gpu','--remote-debugging-port=9416','--user-data-dir='+dir,'--window-size=600,900', url], {stdio:'ignore'});
setTimeout(async () => {
  const list = await (await fetch('http://127.0.0.1:9416/json/list')).json();
  const page = list.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0;
  const call = (m, p={}) => new Promise(res => { const cid = ++id; const h = e => { const d = JSON.parse(e.data); if (d.id === cid) { ws.removeEventListener('message', h); res(d.result); } }; ws.addEventListener('message', h); ws.send(JSON.stringify({id:cid, method:m, params:p})); });
  ws.onopen = async () => {
    await call('Page.enable');
    await call('Emulation.setDeviceMetricsOverride', {width:390, height:844, deviceScaleFactor:2, mobile:false});
    await call('Page.reload'); await new Promise(r=>setTimeout(r,1800));
    const r = await call('Runtime.evaluate', {expression: `JSON.stringify({iw:innerWidth, dw:document.documentElement.scrollWidth, wide:[...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,8).map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().right))})`, returnByValue:true});
    console.log(r.result.value);
    const shot = await call('Page.captureScreenshot', {format:'png', captureBeyondViewport:false});
    require('fs').writeFileSync('C:/Users/xuliy/AppData/Local/Temp/dpcheck/m390.png', Buffer.from(shot.data,'base64'));
    child.kill(); process.exit(0);
  };
}, 2500);
