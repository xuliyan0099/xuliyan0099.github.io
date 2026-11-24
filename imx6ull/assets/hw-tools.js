/* 硬件基础课互动工具（LED 限流 / 门电路真值表 / RC 充放电）
   页面里没有对应元素时自动跳过。 */
(function(){
  function num(s){ var v=parseFloat(s); return isNaN(v)?null:v; }

  /* ---------- LED 限流 ---------- */
  var ledV=document.getElementById('ledV');
  if(ledV){
    var ledVf=document.getElementById('ledVf'), ledI=document.getElementById('ledI'), ledOut=document.getElementById('ledOut');
    var E24=[1.0,1.2,1.5,1.8,2.0,2.2,2.4,2.7,3.0,3.3,3.6,3.9,4.3,4.7,5.1,5.6,6.2,6.8,7.5,8.2,9.1];
    function e24(x){
      if(x<=0) return null;
      var dec=Math.pow(10,Math.floor(Math.log10(x))-1), best=null, bd=1e9;
      [1,10,100].forEach(function(m){
        E24.forEach(function(b){
          var v=b*dec*m, d=Math.abs(v-x);
          if(d<bd){ bd=d; best=v; }
        });
      });
      return best;
    }
    function paintLed(){
      var v=num(ledV.value), vf=num(ledVf.value), ma=num(ledI.value);
      if(v===null||vf===null||ma===null){ ledOut.innerHTML='<span class="no">输入不合法</span>'; return; }
      if(v<=vf){ ledOut.innerHTML='<span class="no">电源电压必须大于 LED 的正向压降，否则它根本不亮。</span>'; return; }
      var r=(v-vf)/(ma/1000);
      var std=e24(r);
      var p=(v-vf)*(ma/1000);
      var lines=[];
      lines.push('理想电阻 R = (V − Vf) / I = ('+v+' − '+vf+') / '+(ma/1000)+' = <b>'+r.toFixed(1)+' Ω</b>');
      if(std) lines.push('E24 就近取值：<b>'+std.toFixed(1)+' Ω</b>（实际电流 '+( (v-vf)/std*1000 ).toFixed(1)+' mA）');
      lines.push('电阻功耗 P = U·I = '+(v-vf).toFixed(2)+' V × '+(ma/1000)+' A = <b>'+p.toFixed(3)+' W</b>（选 1/4W 电阻足够时余量 ≥ 2 倍）');
      lines.push('判定：'+(ma<1?'<span class="no">电流太小，几乎看不见</span>':(ma>20?'<span class="no">超过常见指示 LED 的 20mA 上限，会衰减甚至烧</span>':'<span class="ok">1–20 mA 区间，正常指示亮度</span>')));
      ledOut.innerHTML=lines.join('<br>');
    }
    ['input','change'].forEach(function(ev){
      ledV.addEventListener(ev,paintLed); ledVf.addEventListener(ev,paintLed); ledI.addEventListener(ev,paintLed);
    });
    document.getElementById('ledGo').addEventListener('click',paintLed);
    paintLed();
  }

  /* ---------- 门电路真值表 ---------- */
  var gSel=document.getElementById('gateSel');
  if(gSel){
    var gOut=document.getElementById('gateOut');
    var GATES={
      and:{n:'AND 与',f:function(a,b){return a&&b?1:0;},sym:'a · b'},
      or:{n:'OR 或',f:function(a,b){return a||b?1:0;},sym:'a + b'},
      not:{n:'NOT 非',f:function(a){return a?0:1;},sym:'ā（单输入）'},
      nand:{n:'NAND 与非',f:function(a,b){return a&&b?0:1;},sym:'a · b 取反'},
      nor:{n:'NOR 或非',f:function(a,b){return a||b?0:1;},sym:'a + b 取反'},
      xor:{n:'XOR 异或',f:function(a,b){return (a?1:0)^(b?1:0);},sym:'a ⊕ b'}
    };
    function paintGate(){
      var g=GATES[gSel.value];
      var rows, single=(gSel.value==='not');
      if(single){
        rows=[[0],[1]].map(function(r){ return '<tr><td>'+r[0]+'</td><td>'+g.f(r[0])+'</td></tr>'; }).join('');
      }else{
        rows=[[0,0],[0,1],[1,0],[1,1]].map(function(r){ return '<tr><td>'+r[0]+'</td><td>'+r[1]+'</td><td>'+g.f(r[0],r[1])+'</td></tr>'; }).join('');
      }
      var head=single?'<tr><th>a</th><th>y</th></tr>':'<tr><th>a</th><th>b</th><th>y</th></tr>';
      gOut.innerHTML='<b>'+g.n+'</b>　布尔式：'+g.sym+
        '<table class="condtab" style="margin-top:10px"><thead>'+head+'</thead><tbody>'+rows+'</tbody></table>';
    }
    gSel.addEventListener('change',paintGate);
    paintGate();
  }

  /* ---------- RC 充放电 ---------- */
  var rcR=document.getElementById('rcR');
  if(rcR){
    var rcC=document.getElementById('rcC'), rcT=document.getElementById('rcT'), rcOut=document.getElementById('rcOut'), rcCv=document.getElementById('rcCv');
    function paintRC(){
      var r=num(rcR.value)*1000, c=num(rcC.value)*1e-6, th=num(rcT.value);
      if(!r||!c||th===null){ rcOut.innerHTML='<span class="no">输入不合法</span>'; return; }
      var tau=r*c;
      var t=(th>=1)?null:(-tau*Math.log(1-th));
      var lines=[];
      lines.push('时间常数 τ = R·C = '+(r/1000)+' kΩ × '+num(rcC.value)+' µF = <b>'+(tau*1000).toFixed(2)+' ms</b>');
      if(t===null) lines.push('阈值已达满幅，理论上无穷时间。');
      else lines.push('到达 '+(th*100)+'% 满幅所需时间 t = −τ·ln(1−'+th+') = <b>'+(t*1000).toFixed(2)+' ms</b>');
      lines.push('经验值：1τ→63.2%、2τ→86.5%、3τ→95.0%、5τ→99.3%');
      rcOut.innerHTML=lines.join('<br>');
      /* 画曲线 */
      var cv=rcCv, ctx=cv.getContext('2d');
      var W=cv.width, H=cv.height;
      ctx.clearRect(0,0,W,H);
      ctx.strokeStyle='rgba(255,255,255,.18)'; ctx.lineWidth=1;
      ctx.beginPath(); ctx.moveTo(40,10); ctx.lineTo(40,H-30); ctx.lineTo(W-10,H-30); ctx.stroke();
      ctx.strokeStyle='#ffb545'; ctx.lineWidth=2; ctx.beginPath();
      var span=tau*5;
      for(var i=0;i<=200;i++){
        var tt=span*i/200;
        var y=1-Math.exp(-tt/tau);
        var px=40+(W-50)*(i/200);
        var py=(H-30)-(H-40)*y;
        if(i===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);
      }
      ctx.stroke();
      if(t!==null){
        var px2=40+(W-50)*(t/span), py2=(H-30)-(H-40)*th;
        ctx.strokeStyle='#03d6b4'; ctx.beginPath(); ctx.moveTo(px2,H-30); ctx.lineTo(px2,py2); ctx.stroke();
        ctx.fillStyle='#03d6b4'; ctx.fillText((th*100)+'% @ '+(t*1000).toFixed(1)+'ms', Math.min(px2+6,W-110), py2-6);
      }
      ctx.fillStyle='rgba(255,255,255,.55)'; ctx.font='11px sans-serif';
      ctx.fillText('0',36,H-16); ctx.fillText('5τ = '+(span*1000).toFixed(0)+' ms',W-110,H-16);
      ctx.save(); ctx.translate(14,H/2); ctx.rotate(-Math.PI/2); ctx.fillText('电压（满幅比例）',-60,0); ctx.restore();
    }
    ['input','change'].forEach(function(ev){ rcR.addEventListener(ev,paintRC); rcC.addEventListener(ev,paintRC); rcT.addEventListener(ev,paintRC); });
    paintRC();
  }
})();
