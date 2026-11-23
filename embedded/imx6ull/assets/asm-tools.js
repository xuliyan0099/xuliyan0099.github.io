/* 汇编路口互动工具（单步台 / 立即数检查 / 条件码判断）
   页面里没有对应元素时自动跳过，可被多个章节共用。 */
(function(){
  function hx(v){ var s=(v>>>0).toString(16).toUpperCase(); while(s.length<8) s='0'+s; return '0x'+s; }
  function flagStr(s){ return 'N='+s.n+'  Z='+s.z+'  C='+s.c+'  V='+s.v; }
  function setNZ(s,res){ res=res>>>0; s.z=(res===0)?1:0; s.n=(res>>>31)&1; }
  function condOK(c,s){
    if(!c) return true;
    var n=s.n,z=s.z,cc=s.c,v=s.v;
    if(c==='eq') return z===1;
    if(c==='ne') return z===0;
    if(c==='cs') return cc===1;
    if(c==='cc') return cc===0;
    if(c==='mi') return n===1;
    if(c==='pl') return n===0;
    if(c==='vs') return v===1;
    if(c==='vc') return v===0;
    if(c==='hi') return cc===1&&z===0;
    if(c==='ls') return cc===0||z===1;
    if(c==='ge') return n===v;
    if(c==='lt') return n!==v;
    if(c==='gt') return z===0&&n===v;
    if(c==='le') return z===1||n!==v;
    return true;
  }
  function parseNum(str){
    str=(str||'').trim().replace(/_/g,'');
    var neg=false;
    if(str.charAt(0)==='-'){ neg=true; str=str.slice(1); }
    var v;
    if(/^0x/i.test(str)) v=parseInt(str.slice(2),16);
    else v=parseInt(str,10);
    if(isNaN(v)) return null;
    v = neg ? (-v) : v;
    return v>>>0;
  }

  /* ---------- 单步台 ---------- */
  var PROGS={
    a:{n:'A · 算术与标志位',mem:{},code:[
      {txt:'mov   r0, #5',       op:'mov',rd:0,imm:5},
      {txt:'mov   r1, #7',       op:'mov',rd:1,imm:7},
      {txt:'add   r0, r0, r1',   op:'add',rd:0,rn:0,rm:1},
      {txt:'sub   r2, r0, #12',  op:'sub',rd:2,rn:0,imm:12},
      {txt:'cmp   r2, #0',       op:'cmp',rn:2,imm:0},
      {txt:'addeq r3, r3, #1',   op:'add',cond:'eq',rd:3,rn:3,imm:1},
      {txt:'mov   r4, #0xFF',    op:'mov',rd:4,imm:255}
    ]},
    b:{n:'B · 循环 1+2+3+4+5',mem:{},code:[
      {txt:'mov  r0, #0        ; sum',  op:'mov',rd:0,imm:0},
      {txt:'mov  r1, #1        ; i',    op:'mov',rd:1,imm:1},
      {txt:'add  r0, r0, r1    ; loop:', op:'add',rd:0,rn:0,rm:1},
      {txt:'add  r1, r1, #1',           op:'add',rd:1,rn:1,imm:1},
      {txt:'cmp  r1, #6',               op:'cmp',rn:1,imm:6},
      {txt:'blt  loop',                 op:'b',cond:'lt',target:2},
      {txt:'; 循环结束，r0 = 15',       op:'halt'}
    ]},
    c:{n:'C · 函数调用与栈（lr 必须保）',mem:{},code:[
      {txt:'mov  r0, #3',       op:'mov',rd:0,imm:3},
      {txt:'mov  r1, #4',       op:'mov',rd:1,imm:4},
      {txt:'bl   add3',         op:'bl',target:4},
      {txt:'b    done',         op:'b',target:10},
      {txt:'add3:',             op:'nop'},
      {txt:'push {lr}',         op:'push',lst:[14]},
      {txt:'add  r0, r0, r1',   op:'add',rd:0,rn:0,rm:1},
      {txt:'mov  r2, r0',       op:'mov',rd:2,rn:0},
      {txt:'pop  {lr}',         op:'pop',lst:[14]},
      {txt:'bx   lr',           op:'bx'},
      {txt:'; 返回后 r0 = 7',   op:'halt'}
    ]},
    d:{n:'D · 内存读写（str / ldr）',mem:{256:0x12345678},code:[
      {txt:'mov  r0, #0x100',      op:'mov',rd:0,imm:256},
      {txt:'ldr  r1, [r0]',        op:'ldr',rd:1,rn:0,off:0},
      {txt:'add  r1, r1, #1',      op:'add',rd:1,rn:1,imm:1},
      {txt:'str  r1, [r0]',        op:'str',rd:1,rn:0,off:0},
      {txt:'mov  r2, #0x28',       op:'mov',rd:2,imm:40},
      {txt:'str  r2, [r0, #4]',    op:'str',rd:2,rn:0,off:4},
      {txt:'ldr  r3, [r0, #4]',    op:'ldr',rd:3,rn:0,off:4},
      {txt:'mov  r4, #0x10',       op:'mov',rd:4,imm:16},
      {txt:'bic  r4, r4, #0x10',   op:'bic',rd:4,rn:4,imm:16}
    ]},
    e:{n:'E · 位域：bfi / orr / bic',mem:{},code:[
      {txt:'mov  r0, #0',        op:'mov',rd:0,imm:0},
      {txt:'mov  r1, #5',        op:'mov',rd:1,imm:5},
      {txt:'bfi  r0, r1, #3, #3',op:'bfi',rd:0,rm:1,lsb:3,w:3},
      {txt:'orr  r0, r0, #0x80', op:'orr',rd:0,rn:0,imm:128},
      {txt:'bic  r0, r0, #0x08', op:'bic',rd:0,rn:0,imm:8},
      {txt:'and  r0, r0, #0xF0', op:'and',rd:0,rn:0,imm:240}
    ]},
    f:{n:'F · 有符号 vs 无符号（-1 与 1）',mem:{},code:[
      {txt:'mvn  r0, #0        ; r0 = -1', op:'mvn',rd:0,imm:0},
      {txt:'mov  r1, #1',      op:'mov',rd:1,imm:1},
      {txt:'cmp  r0, r1',      op:'cmp',rn:0,rm:1},
      {txt:'blt  L1            ; 有符号 -1 < 1 成立', op:'b',cond:'lt',target:6},
      {txt:'mov  r2, #0        ; 走这里说明判错了', op:'mov',rd:2,imm:0},
      {txt:'b    end',          op:'b',target:7},
      {txt:'L1: mov r2, #1',    op:'mov',rd:2,imm:1},
      {txt:'end: add r3, r2, #2',op:'add',rd:3,rn:2,imm:2}
    ]}
  };

  var selP=document.getElementById('simProg');
  if(selP){
    var codeEl=document.getElementById('simCode'),
        regsEl=document.getElementById('simRegs'),
        flagsEl=document.getElementById('simFlags'),
        memEl=document.getElementById('simMem'),
        noteEl=document.getElementById('simNote'),
        cur=null, st=null;

    function mk(p){
      var s={r:[],mem:{},n:0,z:0,c:0,v:0,halt:false,pc:0,chg:[]};
      for(var i=0;i<16;i++) s.r[i]=0;
      s.r[13]=0x2000;
      for(var k in p.mem) s.mem[k]=p.mem[k];
      return s;
    }

    function exec(s,ins){
      var r=s.r, chg=[], msg='', op=ins.op;
      if(op==='halt'){ s.halt=true; return {chg:[],msg:'<b>程序结束。</b>寄存器停在当前值不动了。'}; }
      if(!condOK(ins.cond,s)){ s.pc++; return {chg:[],msg:'条件 <b>'+ins.cond+'</b> 不成立 → 这条被<b>跳过</b>，标志位和寄存器都没动'}; }
      if(op==='nop'){ s.pc++; return {chg:[],msg:'标号行，不是指令，跳过'}; }
      if(op==='b'||op==='bl'){
        if(op==='bl'){ r[14]=(s.pc+1)*4; chg.push(14); }
        s.pc=ins.target;
        return {chg:chg, msg:(op==='bl'?'<b>bl</b>：返回地址 '+((ins.target)*4)+' 那一位写进 lr，然后跳过去':'<b>b</b>：无条件跳到第 '+(ins.target+1)+' 条')};
      }
      if(op==='bx'){ s.pc=r[14]/4; return {chg:[], msg:'<b>bx lr</b>：跳到 lr 存的地址，也就是 bl 的下一条'}; }
      if(op==='push'||op==='pop'){
        var sp=r[13];
        ins.lst.forEach(function(rg){
          if(op==='push'){ sp=sp-4; s.mem[sp]=r[rg]; }
          else { r[rg]=s.mem[sp]||0; sp=sp+4; chg.push(rg); }
        });
        r[13]=sp; chg.push(13); s.pc++;
        return {chg:chg, msg:(op==='push'?'<b>push</b>：sp 减 '+(4*ins.lst.length)+'，把 lr 存到栈上（sp = '+hx(sp)+'）':'<b>pop</b>：把栈里的值恢复到 lr，sp 加 '+(4*ins.lst.length))};
      }
      if(op==='ldr'||op==='str'){
        var addr=(r[ins.rn]+(ins.off||0))>>>0;
        if(op==='ldr'){ r[ins.rd]=s.mem[addr]||0; chg.push(ins.rd);
          msg='<b>ldr</b>：从 '+hx(addr)+' 读一个字 → r'+ins.rd+' = '+hx(r[ins.rd]); }
        else { s.mem[addr]=r[ins.rd];
          msg='<b>str</b>：把 r'+ins.rd+' = '+hx(r[ins.rd])+' 写进 '+hx(addr);
        }
        s.pc++; return {chg:chg, msg:msg};
      }

      var a = (ins.rn!=null)? r[ins.rn]>>>0 : 0;
      var b = (ins.rm!=null)? r[ins.rm]>>>0 : (ins.imm||0)>>>0;
      var res=0;
      if(op==='mov'){ res=b; setNZ(s,res); r[ins.rd]=res; chg.push(ins.rd); msg='<b>mov</b>：r'+ins.rd+' = '+hx(res); }
      else if(op==='mvn'){ res=(~b)>>>0; setNZ(s,res); r[ins.rd]=res; chg.push(ins.rd); msg='<b>mvn</b>：取反后放 r'+ins.rd+'，得到 '+hx(res)+'（这就是 -1 的写法）'; }
      else if(op==='add'){
        res=(a+b)>>>0; s.c=(res<a)?1:0; s.v=(((a^res)&(b^res))>>>31)&1; setNZ(s,res);
        r[ins.rd]=res; chg.push(ins.rd);
        msg='<b>add</b>：'+a+'+'+b+' = '+res+'（'+hx(res)+'）'+(ins.cond?'（条件 '+ins.cond+' 成立，所以真的执行了）':'');
      }
      else if(op==='sub'||op==='cmp'){
        res=(a-b)>>>0; s.c=(a>=b)?1:0; s.v=(((a^b)&(a^res))>>>31)&1; setNZ(s,res);
        if(op==='sub'){ r[ins.rd]=res; chg.push(ins.rd); msg='<b>sub</b>：'+a+'-'+b+' = '+res+'；'+flagStr(s); }
        else { msg='<b>cmp</b>：算 '+a+'−'+b+' 但<b>丢掉结果</b>，只更新标志：'+flagStr(s); }
      }
      else if(op==='and'||op==='orr'||op==='eor'||op==='bic'){
        if(op==='and') res=(a&b)>>>0;
        if(op==='orr') res=(a|b)>>>0;
        if(op==='eor') res=(a^b)>>>0;
        if(op==='bic') res=(a&(~b))>>>0;
        setNZ(s,res); r[ins.rd]=res; chg.push(ins.rd);
        msg='<b>'+op+'</b>：'+a+' 与 '+b+' → r'+ins.rd+' = '+hx(res)+(op==='bic'?'（把 '+b+' 对应的位清 0，其他位不动）':'');
      }
      else if(op==='lsl'||op==='lsr'||op==='asr'){
        var sh=ins.imm||0;
        if(op==='lsl') res=(a<<sh)>>>0;
        if(op==='lsr') res=(a>>>sh)>>>0;
        if(op==='asr') res=(a>>sh)>>>0;
        setNZ(s,res); r[ins.rd]=res; chg.push(ins.rd);
        msg='<b>'+op+'</b>：'+hx(a)+' 移 '+sh+' 位 → '+hx(res);
      }
      else if(op==='bfi'){
        var base=r[ins.rd]>>>0;
        var keep=(~(((1<<ins.w)-1)<<ins.lsb))>>>0;
        res=((base&keep)|((b&((1<<ins.w)-1))<<ins.lsb))>>>0;
        setNZ(s,res); r[ins.rd]=res; chg.push(ins.rd);
        msg='<b>bfi</b>：把 '+b+' 的低 '+ins.w+' 位放进 bit['+(ins.lsb+ins.w-1)+':'+ins.lsb+'] → r'+ins.rd+' = '+hx(res);
      }
      s.pc++;
      return {chg:chg, msg:msg};
    }

    function render(){
      if(!st) return;
      var html='';
      cur.code.forEach(function(ins,i){
        var cls = i===st.pc ? 'cur' : (i<st.pc?'done':'');
        var t=ins.txt;
        if(t.indexOf(';')>=0){ t=t.slice(0,t.indexOf(';'))+'<i>'+t.slice(t.indexOf(';'))+'</i>'; }
        html+='<div class="'+cls+'">'+(i+1<10?'&nbsp;':'')+(i+1)+'  '+t+'</div>';
      });
      codeEl.innerHTML=html;
      var names=['r0','r1','r2','r3','r4','r5','r6','r7','r8','r9','r10','r11','r12','sp','lr','pc'];
      var g='';
      for(var i=0;i<16;i++){
        var val = (i===15) ? st.pc*4 : st.r[i];
        var isCh = st.chg.indexOf(i)>=0;
        g+='<div class="'+(isCh?'ch':'')+'"><b>'+names[i]+'</b>'+hx(val)+'</div>';
      }
      regsEl.innerHTML=g;
      flagsEl.innerHTML='<span class="'+(st.n?'on':'')+'">N '+(st.n?'1':'0')+'</span>'+
        '<span class="'+(st.z?'on':'')+'">Z '+(st.z?'1':'0')+'</span>'+
        '<span class="'+(st.c?'on':'')+'">C '+(st.c?'1':'0')+'</span>'+
        '<span class="'+(st.v?'on':'')+'">V '+(st.v?'1':'0')+'</span>';
      var keys=[],km={};
      for(var k2 in st.mem){ if(!km[k2]){ km[k2]=1; keys.push(parseInt(k2,10)); } }
      keys.sort(function(x,y){return x-y});
      var m='';
      keys.slice(0,4).forEach(function(a){ m+='mem['+hx(a)+'] = <b>'+hx(st.mem[a])+'</b><br>'; });
      if(keys.length===0) m='<span style="color:#5d6c88">内存里还没有数据（栈上也空）</span>';
      memEl.innerHTML=m;
    }
    function load(k){
      cur=PROGS[k]; st=mk(cur); render();
      noteEl.innerHTML='已载入 <b>'+cur.n+'</b>。点「单步执行」开始。';
    }
    selP.innerHTML='';
    for(var k in PROGS){ var o=document.createElement('option'); o.value=k; o.textContent=PROGS[k].n; selP.appendChild(o); }
    selP.addEventListener('change',function(){ load(selP.value); });
    document.getElementById('simStep').addEventListener('click',function(){
      if(!st) return;
      var ins=cur.code[st.pc];
      if(!ins){ noteEl.innerHTML='<b>已到末尾。</b>点「重置」从头再来。'; return; }
      var e=exec(st,ins);
      st.chg=e.chg||[];
      noteEl.innerHTML=e.msg;
      render();
    });
    document.getElementById('simRun').addEventListener('click',function(){
      if(!st) return;
      var guard=0, last='';
      while(!st.halt && guard<200){
        var ins=cur.code[st.pc];
        if(!ins){ st.halt=true; break; }
        var e=exec(st,ins); st.chg=e.chg||[]; last=e.msg; guard++;
      }
      noteEl.innerHTML=(last||'')+'　<b>执行到底了。</b>';
      render();
    });
    document.getElementById('simReset').addEventListener('click',function(){ load(selP.value); });
    load('a');
  }

  /* ---------- 立即数检查 ---------- */
  var immIn=document.getElementById('immIn');
  if(immIn){
    var immOut=document.getElementById('immOut');
    function encImm(v){
      for(var rot=0;rot<16;rot++){
        var n=2*rot;
        var x = n===0 ? v : (((v<<n)|(v>>>(32-n)))>>>0);
        if(x<256) return {imm8:x,rot:rot};
      }
      return null;
    }
    function paintImm(){
      var v=parseNum(immIn.value);
      if(v===null){ immOut.innerHTML='<span class="no">输入不合法</span>　十进制或 0x 十六进制都行'; return; }
      var e=encImm(v);
      var lines=['常数 = '+hx(v)+'（十进制 '+(v>2147483647? v-4294967296 : v)+'）'];
      if(e){
        lines.push('<span class="ok">✓ 能直接编进 mov</span>');
        lines.push('编码 = imm8 0x'+e.imm8.toString(16).toUpperCase()+' 循环右移 '+(2*e.rot)+' 位（rot 字段 = '+e.rot+'）');
        lines.push('写法：<b>mov r0, #'+hx(v)+'</b>');
      }else{
        lines.push('<span class="no">✗ 编不进 mov 的 12 位立即数</span>　8 位值 + 偶数位循环右移，只有 4096 种组合');
        var hi=(v>>>16)&0xFFFF, lo=v&0xFFFF;
        lines.push('可行写法一：<b>movw r0, #'+hx(lo)+'</b>　<b>movt r0, #'+hx(hi)+'</b>　（两条，16 位立即数，无需常量池）');
        lines.push('可行写法二：<b>ldr r0, ='+hx(v)+'</b>　（伪指令，汇编器把常数放进常量池，用 PC 相对 ldr 取）');
      }
      immOut.innerHTML=lines.join('<br>');
    }
    immIn.addEventListener('input',paintImm);
    document.getElementById('immGo').addEventListener('click',paintImm);
    Array.prototype.forEach.call(document.querySelectorAll('.im'),function(b){
      b.addEventListener('click',function(){ immIn.value=b.dataset.v; paintImm(); });
    });
    paintImm();
  }

  /* ---------- 条件码 ---------- */
  var cA=document.getElementById('cndA');
  if(cA){
    var cB=document.getElementById('cndB'),
        cOut=document.getElementById('cndOut'),
        cTab=document.getElementById('cndTab');
    var CONDS=[
      ['eq','Z=1','相等'],['ne','Z=0','不等'],
      ['cs','C=1','无符号 ≥（有进位）'],['cc','C=0','无符号 <（无进位）'],
      ['mi','N=1','结果为负'],['pl','N=0','结果非负'],
      ['vs','V=1','有符号溢出'],['vc','V=0','无溢出'],
      ['hi','C=1 且 Z=0','无符号 >'],['ls','C=0 或 Z=1','无符号 ≤'],
      ['ge','N=V','有符号 ≥'],['lt','N≠V','有符号 <'],
      ['gt','Z=0 且 N=V','有符号 >'],['le','Z=1 或 N≠V','有符号 ≤']
    ];
    function paintCond(){
      var a=parseNum(cA.value), b=parseNum(cB.value);
      if(a===null||b===null){ cOut.innerHTML='<span class="no">输入不合法</span>'; cTab.innerHTML=''; return; }
      var res=(a-b)>>>0;
      var s={n:(res>>>31)&1, z:res===0?1:0, c:(a>=b)?1:0, v:(((a^b)&(a^res))>>>31)&1};
      var sa=(a>2147483647)?a-4294967296:a, sb=(b>2147483647)?b-4294967296:b;
      var same = condOK('eq',s)?'相等':((condOK('lt',s)?'有符号：前者更小':'有符号：前者更大')+'；'+(condOK('hi',s)?'无符号：前者更大':'无符号：前者更小'));
      cOut.innerHTML='A = '+hx(a)+'（有符号 '+sa+'）　B = '+hx(b)+'（有符号 '+sb+'）<br>'+
        'cmp 结果（a−b，丢弃）= '+hx(res)+'<br>'+
        '<b>标志：</b>'+flagStr(s)+'<br>'+
        '<b>结论：</b>'+same;
      var rows=CONDS.map(function(c){
        var ok=condOK(c[0],s);
        var cls = ok?'t':'f';
        var ul = (c[0]==='hi'||c[0]==='ls'||c[0]==='cs'||c[0]==='cc') ? ' ul' : '';
        return '<tr><td class="'+cls+'">'+c[0]+'</td><td class="'+cls+ul+'">'+(ok?'✓ 成立':'✗ 不成立')+'</td><td>'+c[1]+'</td><td style="color:#8fa3c4">'+c[2]+'</td></tr>';
      }).join('');
      cTab.innerHTML='<table class="condtab"><thead><tr><th>后缀</th><th>此时</th><th>条件</th><th>含义</th></tr></thead><tbody>'+rows+'</tbody></table>';
    }
    cA.addEventListener('input',paintCond); cB.addEventListener('input',paintCond);
    document.getElementById('cndGo').addEventListener('click',paintCond);
    Array.prototype.forEach.call(document.querySelectorAll('.ct'),function(b){
      b.addEventListener('click',function(){ cA.value=b.dataset.a; cB.value=b.dataset.b; paintCond(); });
    });
    paintCond();
  }

  /* ---------- 位域解码（手册研读 4 篇） ---------- */
  var decVal=document.getElementById('decVal');
  if(decVal){
    var decSpec=document.getElementById('decSpec'), decOut=document.getElementById('decOut');
    function paintDec(){
      var v=parseNum(decVal.value);
      if(v===null){ decOut.innerHTML='<span class="no">值不合法</span>'; return; }
      var groups=decSpec.value.split(','), rows=[];
      for(var i=0;i<groups.length;i++){
        var g=groups[i].trim(); if(!g) continue;
        var m=g.match(/^(\d+)(?:-(\d+))?\s*:\s*(.+)$/);
        if(!m){ decOut.innerHTML='<span class="no">字段表格式不对：应写成 起始位-结束位:名称，多段用逗号分隔</span>'; return; }
        var lo=parseInt(m[1],10), hi=(m[2]!==undefined?parseInt(m[2],10):lo);
        if(hi<lo){ var tmp=hi; hi=lo; lo=tmp; }
        var width=hi-lo+1;
        var mask=width>=32?0xFFFFFFFF:(((1<<width)-1)<<lo);
        var raw=((v>>>lo)&(width>=32?0xFFFFFFFF:(1<<width)-1))>>>0;
        rows.push({lo:lo,hi:hi,name:m[3].trim(),mask:mask,raw:raw});
      }
      rows.sort(function(a,b){ return a.lo-b.lo; });
      var covered=0;
      rows.forEach(function(r){ covered |= r.mask; });
      var rest=(v & ~covered)>>>0;
      var html='<b>值 = '+hx(v)+'</b><br>';
      html+='<table class="condtab"><thead><tr><th>位</th><th>掩码</th><th>字段</th><th>取出值</th></tr></thead><tbody>';
      rows.forEach(function(r){
        html+='<tr><td>['+r.hi+(r.hi===r.lo?'':':'+r.lo)+']</td><td style="color:#8fa3c4">'+hx(r.mask)+
          '</td><td>'+hx(r.raw)+'（'+(r.hi-r.lo+1)+' 位，十进制 '+r.raw+'）</td><td style="color:#8fa3c4">'+r.name+'</td></tr>';
      });
      html+='</tbody></table>';
      if(rest) html+='<span class="no">字段表没覆盖到的位：'+hx(rest)+'　—— 这些位在真实寄存器里通常是 Reserved，保持复位值不动。</span>';
      else html+='<span class="ok">字段表覆盖了所有非零位。</span>';
      decOut.innerHTML=html;
    }
    decVal.addEventListener('input',paintDec); decSpec.addEventListener('input',paintDec);
    document.getElementById('decGo').addEventListener('click',paintDec);
    Array.prototype.forEach.call(document.querySelectorAll('.dv'),function(b){
      b.addEventListener('click',function(){ decVal.value=b.dataset.v; if(b.dataset.s) decSpec.value=b.dataset.s; paintDec(); });
    });
    paintDec();
  }
})();
