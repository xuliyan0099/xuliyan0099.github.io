/* ============================================================
   cpu3.js · CPU 执行循环动画（anime.js v4）
   演示：Flash 里的代码 → 向量表 → 取指 → 译码 → 执行 → 写回
   数据契约（可选）：
   <div class="cpu3" data-json='{"title":"","hint":"","flash":[{a,h,n}],"frames":[{...}]}'></div>
   不传 data-json 时使用内置 i.MX6ULL / Cortex-A7 小段程序
   ============================================================ */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';

  function mk(t, a) {
    var e = document.createElementNS(NS, t);
    if (a) { for (var k in a) e.setAttribute(k, a[k]); }
    return e;
  }
  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function anim() { return (window.anime && typeof window.anime.animate === 'function') ? window.anime : null; }

  var DEMO = {
    title: 'CPU 怎么跑一条指令：取指 → 译码 → 执行 → 写回',
    hint: '代码在 Flash 里，PC 指着它，四个阶段一圈一圈转',
    flash: [
      { a: '0x08000000', h: '2000 1F00', n: 'SP 初值', k: 'vec' },
      { a: '0x08000004', h: '0800 0100', n: '复位向量', k: 'vec' },
      { a: '0x08000100', h: 'E3A00005', n: 'mov r0,#5', k: 'c' },
      { a: '0x08000104', h: 'E2800003', n: 'add r0,#3', k: 'c' },
      { a: '0x08000108', h: 'E3500008', n: 'cmp r0,#8', k: 'c' },
      { a: '0x0800010C', h: '1AFFFFFC', n: 'bne 0x104', k: 'c' },
      { a: '0x08000110', h: 'E5810000', n: 'str r0,[r1]', k: 'c' },
      { a: '0x08000114', h: 'EAFFFFFE', n: 'b .', k: 'c' }
    ],
    frames: [
      { d: '上电那一刻。代码还没跑，CPU 只知道一件事：Flash 挂在 0x08000000，硬件把 PC 强行指过去。', pc: '0x08000000', sp: '—', ir: '—', alu: '—', regs: ['—', '—', '—', '—'], flags: '—', mem: '—', hi: ['f0', 'f1'], do: 'addr' },
      { d: 'Flash 开头 8 个字节不是代码，是向量表：第一格给 SP 初值，第二格给复位入口地址。硬件读它，SP 与 PC 才有值。', pc: '0x08000000', sp: '0x20001F00', ir: '—', alu: '—', regs: ['—', '—', '—', '—'], flags: '—', mem: '—', hi: ['f0', 'f1', 'sp'], do: 'vec' },
      { d: 'PC 现在 = 0x08000100，指向 _start 的第一条指令。这个地址不是 CPU 算出来的，是刚才从向量表第二格读出来的。', pc: '0x08000100', sp: '0x20001F00', ir: '—', alu: '—', regs: ['—', '—', '—', '—'], flags: '—', mem: '—', hi: ['f2', 'pc'], do: 'addr' },
      { d: '取指：按 PC 的地址从 Flash 里拿 4 个字节放进 IR，同时 PC 自己加 4，指向下一条。这一步跟指令内容无关。', pc: '0x08000104', sp: '0x20001F00', ir: 'E3A00005', alu: '—', regs: ['—', '—', '—', '—'], flags: '—', mem: '—', hi: ['f2', 'ir', 'pc'], do: 'fetch' },
      { d: '译码看出这是 mov：目标寄存器 Rd=r0，立即数就直接藏在指令的低 12 位里（5）。执行：把 5 写进 R0。', pc: '0x08000104', sp: '0x20001F00', ir: 'E3A00005', alu: 'imm 5 → R0', regs: ['5', '—', '—', '—'], flags: '—', mem: '—', hi: ['ir', 'dec', 'r0'], do: 'wb' },
      { d: '取指：Flash[0x08000104] 是 add，4 个字节进 IR，PC 变成 0x08000108。', pc: '0x08000108', sp: '0x20001F00', ir: 'E2800003', alu: '—', regs: ['5', '—', '—', '—'], flags: '—', mem: '—', hi: ['f3', 'ir', 'pc'], do: 'fetch' },
      { d: '译码要读 R0，执行把 R0=5 和立即数 3 送进 ALU，算出 8，再写回 R0。这条指令改的是寄存器。', pc: '0x08000108', sp: '0x20001F00', ir: 'E2800003', alu: '5 + 3 = 8', regs: ['8', '—', '—', '—'], flags: '—', mem: '—', hi: ['ir', 'alu', 'r0'], do: 'wb' },
      { d: '取指 cmp：这条不写寄存器，只让 ALU 做一次减法，把结果丢掉、只留标志位。', pc: '0x0800010C', sp: '0x20001F00', ir: 'E3500008', alu: '—', regs: ['8', '—', '—', '—'], flags: 'Z=0', mem: '—', hi: ['f4', 'ir', 'pc'], do: 'fetch' },
      { d: '执行 cmp：8 − 8 = 0，于是 Z=1。R0 一个字节都没变——cmp 的产物是标志位，不是数据。', pc: '0x0800010C', sp: '0x20001F00', ir: 'E3500008', alu: '8 − 8 = 0', regs: ['8', '—', '—', '—'], flags: 'Z=1', mem: '—', hi: ['alu', 'flags'], do: 'alu' },
      { d: '取指 bne：条件跳转也是普通 4 个字节，PC 照例先加 4，跳不跳要等执行阶段才决定。', pc: '0x08000110', sp: '0x20001F00', ir: '1AFFFFFC', alu: '—', regs: ['8', '—', '—', '—'], flags: 'Z=1', mem: '—', hi: ['f5', 'ir', 'pc'], do: 'fetch' },
      { d: '执行 bne：条件是 NE（Z==0），现在 Z=1，条件不成立，PC 不动，于是继续往下走 0x08000110。', pc: '0x08000110', sp: '0x20001F00', ir: '1AFFFFFC', alu: 'NE? Z=1 → 不跳', regs: ['8', '—', '—', '—'], flags: 'Z=1', mem: '—', hi: ['ir', 'dec'], do: 'alu' },
      { d: '取指 str：这条要把寄存器里的值写到内存/外设，地址在 R1（0x02000000），数据在 R0。', pc: '0x08000114', sp: '0x20001F00', ir: 'E5810000', alu: '—', regs: ['8', '0x02000000', '—', '—'], flags: 'Z=1', mem: '—', hi: ['f6', 'ir', 'r1'], do: 'fetch' },
      { d: '执行 str：地址总线送出 0x02000000，数据总线送出 8，写进那个位置。到这里一条完整的「读—算—写」就走完了。', pc: '0x08000114', sp: '0x20001F00', ir: 'E5810000', alu: 'R0 → [R1]', regs: ['8', '0x02000000', '—', '—'], flags: 'Z=1', mem: '8 @ 0x02000000', hi: ['mem', 'alu'], do: 'bus' },
      { d: '最后是 b .：跳到自己的地址，等于原地死循环。程序就是这样一条接一条跑下去，直到断电或异常打断。', pc: '0x08000114', sp: '0x20001F00', ir: 'EAFFFFFE', alu: 'PC ← 自己', regs: ['8', '0x02000000', '—', '—'], flags: 'Z=1', mem: '8 @ 0x02000000', hi: ['f7', 'pc', 'ir'], do: 'fetch' }
    ]
  };

  /* 宽屏：Flash 横排 8 格在上，CPU 核（上排四个框 + 左寄存器 / 右 ALU）在左下 */
  function layWide() {
    var fw = 115, fx0 = 40, fy = 56, fh = 60, gap = 3;
    var fl = [];
    for (var i = 0; i < 8; i++) fl.push({ x: fx0 + i * (fw + gap), y: fy, w: fw, h: fh });
    return {
      W: 1000, H: 420,
      flash: fl,
      flashLabel: { x: 40, y: 44 },
      cpuBox: { x: 40, y: 152, w: 660, h: 246 },
      pc: { x: 60, y: 182, w: 140, h: 44 },
      sp: { x: 214, y: 182, w: 140, h: 44 },
      ir: { x: 368, y: 182, w: 150, h: 44 },
      dec: { x: 532, y: 182, w: 148, h: 44 },
      regs: { x: 60, y: 248, w: 270, rh: 26 },
      alu: { x: 530, y: 254, w: 150, h: 46 },
      mem: { x: 742, y: 262, w: 228, h: 70 },
      memLabel: { x: 742, y: 250 }
    };
  }
  /* 窄屏：Flash 两列四行在上，CPU 各框往下排 */
  function layNarrow() {
    var cw = 236, ch = 52, x0 = 14, x1 = 266, y0 = 56, rg = 8;
    var fl = [];
    for (var i = 0; i < 8; i++) {
      var r = Math.floor(i / 2), c = i % 2;
      fl.push({ x: c ? x1 : x0, y: y0 + r * (ch + rg), w: cw, h: ch });
    }
    return {
      W: 520, H: 684,
      flash: fl,
      flashLabel: { x: 14, y: 44 },
      cpuBox: { x: 8, y: 322, w: 504, h: 352 },
      pc: { x: 22, y: 348, w: 150, h: 46 },
      sp: { x: 182, y: 348, w: 148, h: 46 },
      ir: { x: 340, y: 348, w: 156, h: 46 },
      dec: { x: 22, y: 404, w: 474, h: 38 },
      regs: { x: 22, y: 452, w: 474, rh: 30 },
      alu: { x: 22, y: 588, w: 216, h: 46 },
      mem: { x: 266, y: 592, w: 230, h: 60 },
      memLabel: { x: 266, y: 582 }
    };
  }

  function build(root) {
    var d = DEMO;
    try {
      var o = JSON.parse(root.getAttribute('data-json') || 'null');
      if (o && (o.flash || o.frames || o.title)) {
        d = {
          title: o.title || DEMO.title,
          hint: o.hint || DEMO.hint,
          flash: o.flash || DEMO.flash,
          frames: o.frames || DEMO.frames
        };
      }
    } catch (e) { }

    root.classList.add('c3');
    root.setAttribute('tabindex', '0');
    root.innerHTML =
      '<div class="c3-head"><span class="c3-badge">执行循环</span>' +
      '<b class="c3-title">' + (d.title || '') + '</b>' +
      '<span class="c3-hint">' + (d.hint || '') + '</span></div>' +
      '<div class="c3-stage"></div>' +
      '<div class="c3-cap"><span class="an2-step c3-step"></span><p class="an2-desc c3-desc"></p></div>' +
      '<div class="an2-ctl c3-ctl">' +
      '<button class="an2-btn" type="button" data-a="prev">◀ 上一帧</button>' +
      '<button class="an2-btn pri" type="button" data-a="play">▶ 播放</button>' +
      '<button class="an2-btn" type="button" data-a="next">下一帧 ▶</button>' +
      '<button class="an2-btn" type="button" data-a="replay">↺ 重播</button>' +
      '<span class="an2-speed">速度<select data-a="speed"><option value="0.7">0.7×</option>' +
      '<option value="1" selected>1×</option><option value="1.5">1.5×</option></select></span>' +
      '<div class="an2-dots c3-dots"></div></div>';

    var stage = root.querySelector('.c3-stage');
    var descEl = root.querySelector('.c3-desc');
    var stepEl = root.querySelector('.c3-step');
    var dotsEl = root.querySelector('.c3-dots');
    var svg = mk('svg', { class: 'c3-svg', preserveAspectRatio: 'xMidYMid meet' });
    stage.appendChild(svg);

    var frames = d.frames || [];
    var state = { i: 0, playing: false, speed: 1, timer: null, pkt: null };
    var els = {}, edges = {}, pkt = null, narrow = false, geo = null;

    dotsEl.innerHTML = frames.map(function (_, k) {
      return '<button class="an2-dot" type="button" data-k="' + k + '" title="跳到第 ' + (k + 1) + ' 帧"></button>';
    }).join('');

    function box(g, o, cls, label) {
      var r = mk('rect', { x: o.x, y: o.y, width: o.w, height: o.h, rx: '10', class: cls + '-r' });
      var l = mk('text', { x: o.x + 10, y: o.y + 15, class: 'c3-cap2' });
      l.textContent = label || '';
      var tx = mk('text', { x: o.x + o.w / 2, y: o.y + o.h - 12, 'text-anchor': 'middle', class: cls + '-t' });
      tx.textContent = '';
      g.appendChild(r); g.appendChild(l); g.appendChild(tx);
      return { r: r, t: tx, l: l };
    }

    function draw(withFade) {
      narrow = window.innerWidth <= 900;
      geo = narrow ? layNarrow() : layWide();
      svg.setAttribute('viewBox', '0 0 ' + geo.W + ' ' + geo.H);
      svg.innerHTML = '';
      els = {}; edges = {};

      var gE = mk('g'), gN = mk('g'), gP = mk('g');

      /* Flash 区块 */
      var flTitle = mk('text', { x: geo.flashLabel.x, y: geo.flashLabel.y, class: 'c3-lbl' });
      flTitle.textContent = 'Flash 0x08000000（代码就住在这里）';
      gN.appendChild(flTitle);
      d.flash.forEach(function (f, i) {
        var o = geo.flash[i];
        var g = mk('g');
        var r = mk('rect', { x: o.x, y: o.y, width: o.w, height: o.h, rx: '8', class: 'c3-fr' + (i < 2 ? ' vec' : '') });
        var a = mk('text', { x: o.x + 8, y: o.y + 14, class: 'c3-fa' });
        a.textContent = f.a;
        var h = mk('text', { x: o.x + 8, y: o.y + (narrow ? 31 : 35), class: 'c3-fh' });
        h.textContent = f.h;
        var n = mk('text', { x: o.x + 8, y: o.y + (narrow ? 45 : 52), class: 'c3-fn' });
        n.textContent = f.n;
        g.appendChild(r); g.appendChild(a); g.appendChild(h); g.appendChild(n);
        gN.appendChild(g);
        els['f' + i] = { g: g, r: r };
      });

      /* CPU 外框 */
      var cb = mk('rect', { x: geo.cpuBox.x, y: geo.cpuBox.y, width: geo.cpuBox.w, height: geo.cpuBox.h, rx: '14', class: 'c3-core' });
      gN.appendChild(cb);
      var ct = mk('text', { x: geo.cpuBox.x + 12, y: geo.cpuBox.y + 20, class: 'c3-lbl' });
      ct.textContent = 'CPU 核（Cortex-A7）';
      gN.appendChild(ct);

      els.pc = box(gN, geo.pc, 'c3-pc', 'PC 程序计数器');
      els.sp = box(gN, geo.sp, 'c3-sp', 'SP 栈指针');
      els.ir = box(gN, geo.ir, 'c3-ir', 'IR 指令寄存器');
      els.dec = box(gN, geo.dec, 'c3-dec', '译码器');
      els.dec.t.setAttribute('class', 'c3-dec-t tiny');
      els.dec.t.textContent = 'cond · opcode · Rd · imm';

      /* 寄存器堆 */
      var rgT = mk('text', { x: geo.regs.x, y: geo.regs.y - 8, class: 'c3-cap2' });
      rgT.textContent = '寄存器堆（通用寄存器）';
      gN.appendChild(rgT);
      var names = ['R0', 'R1', 'R2', 'R3'];
      for (var i = 0; i < 4; i++) {
        var ro = { x: geo.regs.x, y: geo.regs.y + i * geo.regs.rh, w: geo.regs.w, h: geo.regs.rh - 4 };
        var rr = mk('rect', { x: ro.x, y: ro.y, width: ro.w, height: ro.h, rx: '7', class: 'c3-rg' });
        var rn = mk('text', { x: ro.x + 12, y: ro.y + ro.h / 2, 'dominant-baseline': 'middle', class: 'c3-rgn' });
        rn.textContent = names[i];
        var rv = mk('text', { x: ro.x + ro.w - 12, y: ro.y + ro.h / 2, 'text-anchor': 'end', 'dominant-baseline': 'middle', class: 'c3-rgv' });
        rv.textContent = '—';
        gN.appendChild(rr); gN.appendChild(rn); gN.appendChild(rv);
        els['r' + i] = { r: rr, t: rv };
      }

      els.alu = box(gN, geo.alu, 'c3-alu', 'ALU 运算单元');

      /* 内存 / 外设 */
      var ml = mk('text', { x: geo.memLabel.x, y: geo.memLabel.y, class: 'c3-lbl' });
      ml.textContent = '内存 / 外设';
      gN.appendChild(ml);
      var mm = mk('rect', { x: geo.mem.x, y: geo.mem.y, width: geo.mem.w, height: geo.mem.h, rx: '10', class: 'c3-mem-r' });
      var mt = mk('text', { x: geo.mem.x + geo.mem.w / 2, y: geo.mem.y + geo.mem.h / 2, 'text-anchor': 'middle', 'dominant-baseline': 'middle', class: 'c3-memt' });
      mt.textContent = '0x02000000 · 外设';
      gN.appendChild(mm); gN.appendChild(mt);
      els.mem = { r: mm, t: mt };

      /* flags */
      var fl2 = mk('text', { x: geo.alu.x, y: geo.alu.y + geo.alu.h + 18, class: 'c3-flags' });
      fl2.textContent = '标志: —';
      gN.appendChild(fl2);
      els.flags = fl2;

      /* 连线：地址（PC→Flash，虚线）/ 取指（Flash→IR）/ 译码 / 执行 / 写回 / 总线 */
      function line(d, cls) {
        var p = mk('path', { d: d, class: 'c3-edge ' + (cls || ''), 'stroke-linecap': 'round' });
        gE.appendChild(p);
        return p;
      }
      var f0 = geo.flash[0];
      var fx = f0.x + f0.w / 2;
      var fBot = f0.y + f0.h;

      if (!narrow) {
        edges.addr = line('M ' + (geo.pc.x + 34) + ' ' + geo.pc.y + ' L ' + (geo.pc.x + 34) + ' 132 L ' + fx + ' 132 L ' + fx + ' ' + fBot, 'addr');
        edges.fetch = line('M ' + fx + ' ' + fBot + ' L ' + fx + ' 146 L ' + (geo.ir.x + 44) + ' 146 L ' + (geo.ir.x + 44) + ' ' + geo.ir.y, 'fetch');
        edges.dec = line('M ' + (geo.ir.x + geo.ir.w) + ' ' + (geo.ir.y + geo.ir.h / 2) + ' L ' + geo.dec.x + ' ' + (geo.dec.y + geo.dec.h / 2), 'dec');
        edges.dec2 = line('M ' + (geo.dec.x + geo.dec.w / 2) + ' ' + (geo.dec.y + geo.dec.h) + ' L ' + (geo.dec.x + geo.dec.w / 2) + ' 240' +
          ' L ' + (geo.alu.x + geo.alu.w / 2) + ' 240 L ' + (geo.alu.x + geo.alu.w / 2) + ' ' + geo.alu.y, 'exec');
        edges.wb = line('M ' + geo.alu.x + ' ' + (geo.alu.y + geo.alu.h / 2) + ' L ' + (geo.regs.x + geo.regs.w) + ' ' + (geo.alu.y + geo.alu.h / 2), 'wb');
        edges.bus = line('M ' + (geo.alu.x + geo.alu.w) + ' ' + (geo.alu.y + geo.alu.h / 2) + ' L ' + geo.mem.x + ' ' + (geo.mem.y + geo.mem.h / 2), 'bus');
      } else {
        var fBotN = geo.flash[7].y + geo.flash[7].h;
        edges.addr = line('M ' + (geo.pc.x + 24) + ' ' + geo.pc.y + ' L ' + (geo.pc.x + 24) + ' 304 L ' + fx + ' 304 L ' + fx + ' ' + fBotN, 'addr');
        edges.fetch = line('M ' + fx + ' ' + fBotN + ' L ' + fx + ' 312 L ' + (geo.ir.x + 30) + ' 312 L ' + (geo.ir.x + 30) + ' ' + geo.ir.y, 'fetch');
        edges.dec = line('M ' + (geo.ir.x + geo.ir.w / 2) + ' ' + (geo.ir.y + geo.ir.h) + ' L ' + (geo.ir.x + geo.ir.w / 2) + ' ' + geo.dec.y, 'dec');
        edges.dec2 = line('M ' + geo.dec.x + ' ' + (geo.dec.y + geo.dec.h / 2) + ' L 8 ' + (geo.dec.y + geo.dec.h / 2) + ' L 8 ' + (geo.alu.y + geo.alu.h / 2) + ' L ' + geo.alu.x + ' ' + (geo.alu.y + geo.alu.h / 2), 'exec');
        edges.wb = line('M ' + (geo.alu.x + 26) + ' ' + geo.alu.y + ' L ' + (geo.alu.x + 26) + ' ' + (geo.regs.y + 4 * geo.regs.rh + 2) + ' L ' + (geo.regs.x + 26) + ' ' + (geo.regs.y + 4 * geo.regs.rh + 2), 'wb');
        edges.bus = line('M ' + (geo.alu.x + geo.alu.w) + ' ' + (geo.alu.y + geo.alu.h / 2) + ' L ' + geo.mem.x + ' ' + (geo.mem.y + geo.mem.h / 2), 'bus');
      }

      pkt = mk('circle', { r: '5', class: 'c3-pkt' });
      gP.appendChild(pkt);

      svg.appendChild(gE); svg.appendChild(gN); svg.appendChild(gP);

      applyFrame(state.i, false, withFade);
    }

    function runPkt(path, dur, cls) {
      if (!path) return;
      if (state.pkt && state.pkt.cancel) { try { state.pkt.cancel(); } catch (e) { } }
      pkt.setAttribute('r', '5');
      pkt.className.baseVal = 'c3-pkt ' + (cls || '');
      var len = path.getTotalLength();
      var place = function (t) {
        var p = path.getPointAtLength(t * len);
        pkt.setAttribute('cx', p.x.toFixed(1));
        pkt.setAttribute('cy', p.y.toFixed(1));
        pkt.style.opacity = t < 0.08 ? (t / 0.08) : (t > 0.92 ? ((1 - t) / 0.08) : 0.95);
      };
      var an2 = anim();
      if (an2) {
        var o = { t: 0 };
        try {
          state.pkt = an2.animate(o, {
            t: 1, duration: dur, ease: 'inOutSine',
            onUpdate: function () { place(o.t); },
            onComplete: function () { pkt.style.opacity = 0; }
          });
          return;
        } catch (e) { }
      }
      var t0 = performance.now();
      (function loop(now) {
        var t = Math.min(1, (now - t0) / dur);
        place(t);
        if (t < 1) requestAnimationFrame(loop); else pkt.style.opacity = 0;
      })(t0);
    }

    function setBox(b, txt) { if (b) { b.t.textContent = txt; } }

    function fetchPath(idx) {
      var g = geo.flash[idx] || geo.flash[0];
      var sx = g.x + g.w / 2, sy = g.y + g.h;
      var tx = narrow ? geo.ir.x + 30 : geo.ir.x + 44;
      if (narrow) {
        var chN = 312;
        return 'M ' + sx + ' ' + sy + ' L ' + sx + ' ' + chN + ' L ' + tx + ' ' + chN + ' L ' + tx + ' ' + geo.ir.y;
      }
      return 'M ' + sx + ' ' + sy + ' L ' + sx + ' 146 L ' + tx + ' 146 L ' + tx + ' ' + geo.ir.y;
    }
    function addrPath(idx) {
      var g = geo.flash[idx] || geo.flash[0];
      var gx = g.x + g.w / 2, gy = g.y + g.h;
      var px = geo.pc.x + (narrow ? 24 : 34), py = geo.pc.y;
      var ch = narrow ? 300 : 132;
      return 'M ' + px + ' ' + py + ' L ' + px + ' ' + ch + ' L ' + gx + ' ' + ch + ' L ' + gx + ' ' + gy;
    }

    function applyFrame(i, withPkt, fade) {
      i = clamp(i, 0, frames.length ? frames.length - 1 : 0);
      state.i = i;
      var f = frames[i] || {};

      setBox(els.pc, f.pc || '—');
      setBox(els.sp, f.sp || '—');
      setBox(els.ir, f.ir || '—');
      setBox(els.alu, f.alu || 'ALU');
      setBox(els.mem, f.mem || '—');
      if (els.flags) els.flags.textContent = '标志: ' + (f.flags || '—');
      (f.regs || []).forEach(function (v, k) { setBox(els['r' + k], v); });

      /* 高亮 */
      Object.keys(els).forEach(function (k) {
        if (els[k] && els[k].r) els[k].r.classList.remove('on');
      });
      Object.keys(edges).forEach(function (k) { edges[k].classList.remove('on'); });
      var hi = f.hi || [];
      hi.forEach(function (h) {
        var e = els[h];
        if (e && e.r) e.r.classList.add('on');
      });
      if (f.alu && f.alu !== '—') { if (els.alu && hi.indexOf('alu') >= 0) els.alu.r.classList.add('on'); }
      if (f.mem && f.mem !== '—') { if (els.mem && hi.indexOf('mem') >= 0) els.mem.r.classList.add('on'); }
      ['r0', 'r1', 'r2', 'r3'].forEach(function (k) {
        if (hi.indexOf(k) >= 0 && els[k]) { els[k].r.classList.add('on'); els[k].t.classList.add('on'); }
        else if (els[k]) { els[k].t.classList.remove('on'); }
      });

      /* 帧文字 */
      stepEl.innerHTML = '第 <b>' + (i + 1) + '</b> / ' + frames.length + ' 帧';
      descEl.textContent = f.d || '';
      var an = anim();
      if (an && fade !== false) {
        descEl.style.opacity = '0';
        try { an.animate(descEl, { opacity: [0, 1], translateY: [6, 0], duration: 240, ease: 'out(2)' }); } catch (e) { descEl.style.opacity = '1'; }
      } else { descEl.style.opacity = '1'; }

      Array.prototype.forEach.call(dotsEl.children, function (b, k) {
        b.classList.toggle('on', k === i);
        b.classList.toggle('done', k < i);
      });

      pkt.style.opacity = 0;
      var fi = -1;
      hi.forEach(function (h) {
        if (fi < 0 && h.charAt(0) === 'f') { var nn = parseInt(h.slice(1), 10); if (!isNaN(nn)) fi = nn; }
      });
      if (fi >= 0) {
        if (edges.fetch) edges.fetch.setAttribute('d', fetchPath(fi));
        if (edges.addr) edges.addr.setAttribute('d', addrPath(fi));
      }
      if (withPkt) {
        var to = f.do;
        if (to === 'fetch' && edges.fetch) { edges.fetch.classList.add('on'); runPkt(edges.fetch, 560 / state.speed, 'p-fetch'); }
        else if (to === 'addr' || to === 'vec') { edges.addr.classList.add('on'); runPkt(edges.addr, 620 / state.speed, 'p-addr'); }
        else if (to === 'wb' && edges.wb) { edges.wb.classList.add('on'); runPkt(edges.wb, 520 / state.speed, 'p-wb'); }
        else if (to === 'bus' && edges.bus) { edges.bus.classList.add('on'); runPkt(edges.bus, 560 / state.speed, 'p-bus'); }
        else if (to === 'alu' && edges.dec2) { edges.dec2.classList.add('on'); runPkt(edges.dec2, 420 / state.speed, 'p-alu'); }
        else if (to === 'alu' && edges.dec) { edges.dec.classList.add('on'); runPkt(edges.dec, 420 / state.speed, 'p-alu'); }
      }
      updBtn();
    }

    function dwell() {
      var d0 = (frames[state.i] && frames[state.i].d) || '';
      return clamp(1700 + d0.length * 26, 2400, 4600) / state.speed;
    }
    function updBtn() {
      var b = root.querySelector('[data-a="play"]');
      b.textContent = state.playing ? '⏸ 暂停' : '▶ 播放';
    }
    function stop() { clearTimeout(state.timer); state.timer = null; }
    function tick() {
      stop();
      if (!state.playing) return;
      state.timer = setTimeout(function () {
        if (!state.playing) return;
        applyFrame((state.i + 1) % frames.length, true);
        tick();
      }, dwell());
    }
    function play() { state.playing = true; updBtn(); tick(); }
    function pause() { state.playing = false; stop(); updBtn(); }

    root.addEventListener('click', function (e) {
      var b = e.target.closest('[data-a],[data-k]');
      if (!b) return;
      var a = b.getAttribute('data-a');
      if (a === 'play') { state.playing ? pause() : play(); }
      else if (a === 'prev') { pause(); applyFrame(state.i - 1, false); }
      else if (a === 'next') { pause(); applyFrame(state.i + 1, true); }
      else if (a === 'replay') { applyFrame(0, false); play(); }
      else if (b.hasAttribute('data-k')) { pause(); applyFrame(+b.getAttribute('data-k'), true); }
    });
    root.addEventListener('change', function (e) {
      if (e.target.getAttribute('data-a') === 'speed') {
        state.speed = parseFloat(e.target.value) || 1;
        if (state.playing) tick();
      }
    });
    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); pause(); applyFrame(state.i - 1, false); }
      else if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); pause(); applyFrame(state.i + 1, true); }
    });

    var rt = 0, lastW = window.innerWidth;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () {
        var w = window.innerWidth;
        if ((w <= 900) !== narrow && Math.abs(w - lastW) > 80) { lastW = w; draw(false); }
        lastW = w;
      }, 260);
    });
    if (window.matchMedia) {
      var mq = window.matchMedia('(max-width: 900px)');
      var onMq = function () { if (mq.matches !== narrow) draw(false); };
      if (mq.addEventListener) mq.addEventListener('change', onMq);
      else if (mq.addListener) mq.addListener(onMq);
    }

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting && state.playing) { stop(); state._auto = true; }
          else if (en.isIntersecting && state._auto && state.playing) { state._auto = false; tick(); }
        });
      }, { threshold: 0.12 }).observe(root);
    }

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { if (state.playing) { stop(); state._hidden = true; } }
      else if (state._hidden) { state._hidden = false; if (state.playing) tick(); }
    });

    draw();
    var pb = root.querySelector('[data-a="play"]'); if (pb) pb.textContent = '▶ 播放';
  }

  window.cpu3Render = function () {
    Array.prototype.forEach.call(document.querySelectorAll('.cpu3'), function (r) {
      if (r.dataset.built === '1') return;
      var sec = r.closest && r.closest('section.lesson');
      if (sec && sec.hasAttribute('hidden')) return;
      build(r);
      r.dataset.built = '1';
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', window.cpu3Render);
  else window.cpu3Render();
})();
