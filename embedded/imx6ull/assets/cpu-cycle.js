(function(){
  var PROG=[
    {a:'0x00',b:'0001 0010',t:'LOAD R0, [0x02]'},
    {a:'0x01',b:'0010 0001',t:'ADD  R0, R1'},
    {a:'0x02',b:'0000 0011',t:'数据 3'},
    {a:'0x03',b:'0000 0100',t:'数据 4'},
    {a:'0x04',b:'0000 0000',t:'空槽，等结果'}
  ];
  var STEPS=[
    {n:'① 取指', pc:'0x01', ir:'0001 0010', r0:'0', r1:'4', hl:[0], dt:[], pcRow:1,
     t:'按 PC = 0x00 去内存读 8 位：0001 0010，塞进 IR。PC 顺手加一，指向 0x01——它永远记着「下一条」在哪。'},
    {n:'② 译码', pc:'0x01', ir:'0001 0010', r0:'0', r1:'4', hl:[0], dt:[], pcRow:1,
     t:'把 IR 切两半：0001 是动作（LOAD 装载），0010 是地址 0x02。CPU 不认识「LOAD」这个字，它只认 0001 这个编号。'},
    {n:'③ 执行', pc:'0x01', ir:'0001 0010', r0:'0', r1:'4', hl:[], dt:[], pcRow:1,
     t:'LOAD 的「执行」就是算地址：把 0010 当成 0x02，准备去这个格子取数。这一步还没有碰内存。'},
    {n:'④ 访存', pc:'0x01', ir:'0001 0010', r0:'0', r1:'4', hl:[], dt:[2], pcRow:1,
     t:'读内存 0x02，拿到 0000 0011，也就是十进制的 3。这 3 本来就是「数据」，和指令躺在同一片内存里。'},
    {n:'⑤ 写回', pc:'0x01', ir:'0001 0010', r0:'3', r1:'4', hl:[], dt:[], pcRow:1, on:['rR0'],
     t:'把 3 放进 R0。一圈走完，PC 已经是 0x01，下一轮从头再来——只是换成 ADD 那条指令。这五步重复上亿次，就是我们说的「程序在跑」。'}
  ];
  var rows=document.getElementById('ccRows');
  if(!rows) return;
  PROG.forEach(function(p,i){
    var li=document.createElement('li');
    li.innerHTML='<span class="a">'+p.a+'</span><span class="b">'+p.b+'</span><span class="t">'+p.t+'</span><span class="pc">PC</span>';
    li.dataset.i=i;
    rows.appendChild(li);
  });
  var rPC=document.getElementById('rPC'), rIR=document.getElementById('rIR'),
      rR0=document.getElementById('rR0'), rR1=document.getElementById('rR1');
  var ccNo=document.getElementById('ccNo'), ccTxt=document.getElementById('ccTxt'),
      ccProg=document.getElementById('ccProg'), pcTag=document.getElementById('ccPcTag'),
      play=document.getElementById('ccPlay');
  var idx=0, timer=null;

  function set(id,val,on){ id.querySelector('b').textContent=val; id.classList.toggle('on',!!on); }
  function render(){
    Array.prototype.forEach.call(rows.children,function(li){
      li.classList.remove('hl','dt','ispc');
    });
    if(idx===0){
      rPC.querySelector('b').textContent='0x00';
      rIR.querySelector('b').textContent='—';
      rR0.querySelector('b').textContent='0';
      rR1.querySelector('b').textContent='4';
      [rPC,rIR,rR0,rR1].forEach(function(x){x.classList.remove('on')});
      ccNo.textContent='待机';
      ccTxt.textContent='点「下一步」，从取指开始走。';
      ccProg.textContent='第 0 / 5 步';
      pcTag.textContent='PC 指向 0x00';
      rows.children[0].classList.add('ispc');
      return;
    }
    var s=STEPS[idx-1];
    set(rPC,s.pc); set(rIR,s.ir,true); set(rR0,s.r0,s.on&&idx===5); set(rR1,s.r1);
    s.hl.forEach(function(i){ rows.children[i].classList.add('hl'); });
    s.dt.forEach(function(i){ rows.children[i].classList.add('dt'); });
    rows.children[s.pcRow].classList.add('ispc');
    ccNo.textContent=s.n;
    ccTxt.textContent=s.t;
    ccProg.textContent='第 '+idx+' / 5 步';
    pcTag.textContent='PC 指向 '+s.pc;
  }
  function stop(){ if(timer){clearInterval(timer);timer=null;} play.classList.remove('on'); play.textContent='▶ 播放'; }
  function go(n){ idx=Math.max(0,Math.min(STEPS.length,n)); render(); if(idx>=STEPS.length) stop(); }
  document.querySelector('.cc-ctl').addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    var a=b.dataset.a;
    if(a==='next'){ stop(); go(idx+1); }
    else if(a==='prev'){ stop(); go(idx-1); }
    else if(a==='reset'){ stop(); go(0); }
    else if(a==='play'){
      if(timer){ stop(); return; }
      if(idx>=STEPS.length) go(0);
      play.classList.add('on'); play.textContent='❚❚ 暂停';
      timer=setInterval(function(){ go(idx+1); }, 1800);
    }
  });
  var q=location.search.match(/cc=(\d)/); if(q) go(Math.min(+q[1],5));
  render();
})();