/* ============================================================
   ikit.js —— 互动讲义组件（无依赖，单文件）
   用法：
     <div class="ikit" data-type="seq" data-json='{"title":"...","actors":[...],"steps":[...]}'></div>
   约定：data-json 用单引号包住，JSON 内部不要出现单引号。
   组件类型：seq / machine / stack / walk / param / drag / mem / queue / hop / code
   ============================================================ */
(function () {
  'use strict';

  var R = {}; // 类型注册表

  /* ---------------- 工具 ---------------- */
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function num(v, d) { var n = Number(v); return isFinite(n) ? n : d; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  function shell(cfg, opts) {
    var box = el('div', 'ikit ' + (opts.cls || ''));
    var head = el('div', 'ik-head');
    head.appendChild(el('span', 'ik-title', esc(cfg.title || '互动演示')));
    if (cfg.hint) head.appendChild(el('span', 'ik-hint', esc(cfg.hint)));
    if (cfg.badge) head.appendChild(el('span', 'ik-badge', esc(cfg.badge)));
    box.appendChild(head);
    var body = el('div', 'ik-body');
    box.appendChild(body);
    var note = el('div', 'ik-note', cfg.note || '');
    box.appendChild(note);
    var ctl = el('div', 'ik-ctl');
    box.appendChild(ctl);
    return { box: box, body: body, note: note, ctl: ctl };
  }

  function btn(label, fn, cls) {
    var b = el('button', cls || '', esc(label));
    if (fn) b.addEventListener('click', fn);
    return b;
  }

  function speedPicker(onChange) {
    var speeds = [0.5, 1, 2];
    var cur = 1;
    var wrap = el('span', 'ik-step', '速度');
    var b = el('button', 'on', '1×');
    b.addEventListener('click', function () {
      cur = speeds[(speeds.indexOf(cur) + 1) % speeds.length];
      b.textContent = cur + '×';
      onChange(cur);
    });
    wrap.appendChild(b);
    return { node: wrap, get: function () { return cur; } };
  }

  /* ============ 1. seq 双端时序 ============ */
  R.seq = function (cfg, box) {
    var actors = cfg.actors || [{ name: '客户端' }, { name: '服务端' }];
    var steps = cfg.steps || [];
    var s = shell(cfg, { cls: 'ik-seq' });
    var stage = el('div', 'ik-stage');
    stage.appendChild(el('div', 'ik-actor-row', actors.map(function (a, i) {
      return '<div class="ik-actor"><span class="nm">' + esc(a.name) + '</span>' +
        '<span class="st" data-a="' + i + '">' + esc(a.start || '—') + '</span></div>';
    }).join('')));
    var lanes = el('div', 'ik-lanes');
    steps.forEach(function (st, i) {
      var row = el('div', 'ik-msg' + (st.dir === 'l' ? ' rev' : ''));
      row.innerHTML = '<div class="bar"><div class="line"></div><div class="head"></div>' +
        '<span class="lb">' + esc(st.label) + '</span></div>';
      row.dataset.i = i;
      lanes.appendChild(row);
    });
    stage.appendChild(lanes);
    s.body.appendChild(stage);

    var i = -1, timer = null, sp = 1;
    function render() {
      Array.prototype.forEach.call(lanes.children, function (row, k) {
        row.classList.toggle('on', k <= i);
      });
      Array.prototype.forEach.call(stage.querySelectorAll('.st'), function (st, k) {
        var v = '—';
        for (var m = 0; m <= i; m++) {
          var sv = steps[m] && steps[m].states && steps[m].states[k];
          if (sv != null) v = sv;
        }
        st.textContent = v;
        st.classList.toggle('on', i >= 0 && v !== '—');
      });
      s.note.innerHTML = i >= 0 && steps[i].note
        ? '<b style="color:#a78bfa">第 ' + (i + 1) + ' 步</b>　' + esc(steps[i].note)
        : (cfg.note || '点「下一步」开始，或点「自动播放」看完整过程。');
      st.textContent = (i + 1) + ' / ' + steps.length;
      prev.classList.toggle('dim', i < 0);
      next.classList.toggle('dim', i >= steps.length - 1);
      play.classList.toggle('on', !!timer);
    }
    var prev = btn('← 上一步', function () { stop(); i = Math.max(-1, i - 1); render(); });
    var next = btn('下一步 →', function () { stop(); i = Math.min(steps.length - 1, i + 1); render(); });
    var play = btn('▶ 自动播放', function toggle() {
      if (timer) return stop();
      play.classList.add('on');
      play.textContent = '⏸ 暂停';
      timer = setInterval(function () {
        if (i >= steps.length - 1) return stop();
        i++; render();
      }, 1400 / sp);
      render();
    });
    function stop() {
      if (timer) { clearInterval(timer); timer = null; play.textContent = '▶ 自动播放'; play.classList.remove('on'); }
    }
    var st = el('span', 'ik-step', '0 / ' + steps.length);
    var spd = speedPicker(function (v) { sp = v; if (timer) { stop(); play.click(); } });
    s.ctl.appendChild(prev); s.ctl.appendChild(next); s.ctl.appendChild(play);
    s.ctl.appendChild(el('span', 'ik-sp')); s.ctl.appendChild(st); s.ctl.appendChild(spd.node);
    box.appendChild(s.box);
    render();
    if (false) setTimeout(function () { play.click(); }, 500);
  };

  /* ============ 2. machine 状态机 ============ */
  R.machine = function (cfg, box) {
    var states = cfg.states || [];
    var edges = cfg.edges || [];
    var s = shell(cfg, { cls: 'ik-mac' });
    var stage = el('div', 'ik-stage');
    var W = 640, H = 380;
    var svg = '<svg class="ik-svg" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="xMidYMid meet">';
    svg += '<defs><marker id="ikarrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">' +
      '<path d="M0,0 L8,4.5 L0,9 z" fill="rgba(167,139,250,.9)"/></marker></defs>';
    var NW = 96, NH = 34;
    states.forEach(function (st) {
      var x = (st.x || 50) / 100 * W, y = (st.y || 50) / 100 * H;
      st._x = x; st._y = y;
      svg += '<g class="node" data-id="' + esc(st.id) + '">' +
        '<rect x="' + (x - NW / 2) + '" y="' + (y - NH / 2) + '" width="' + NW + '" height="' + NH +
        '" rx="9" fill="rgba(18,26,42,.92)" stroke="rgba(110,168,254,.35)"/>' +
        '<text x="' + x + '" y="' + (y + 4) + '" text-anchor="middle">' + esc(st.label || st.id) + '</text></g>';
    });
    edges.forEach(function (e, k) {
      var a = states.find(function (s2) { return s2.id === e.from; });
      var b = states.find(function (s2) { return s2.id === e.to; });
      if (!a || !b) return;
      var dx = b._x - a._x, dy = b._y - a._y;
      var len = Math.sqrt(dx * dx + dy * dy) || 1;
      var ux = dx / len, uy = dy / len;
      var sx = a._x + ux * (NW / 2 + 3), sy = a._y + uy * (NH / 2 + 3);
      var ex = b._x - ux * (NW / 2 + 10), ey = b._y - uy * (NH / 2 + 10);
      var mx = (sx + ex) / 2 - uy * 26, my = (sy + ey) / 2 + ux * 26;
      // 标签位置：lt=曲线上取点比例(默认 .5)，lp=垂直偏移(默认 32)，可单独调开重叠
      var lt = e.lt === undefined ? 0.5 : e.lt;
      var lp = e.lp === undefined ? 32 : e.lp;
      var lx = (1 - lt) * (1 - lt) * sx + 2 * (1 - lt) * lt * mx + lt * lt * ex;
      var ly = (1 - lt) * (1 - lt) * sy + 2 * (1 - lt) * lt * my + lt * lt * ey;
      svg += '<g class="edge" data-k="' + k + '"><path d="M' + sx + ',' + sy + ' Q' + mx + ',' + my + ' ' + ex + ',' + ey +
        '" marker-end="url(#ikarrow)"/>' +
        '<text x="' + (lx - uy * lp) + '" y="' + (ly + ux * lp) + '" text-anchor="middle">' +
        esc(e.label || '') + '</text></g>';
      e._path = { sx: sx, sy: sy, mx: mx, my: my, ex: ex, ey: ey };
    });
    svg += '</svg>';
    stage.innerHTML = svg;
    var token = el('div', 'token');
    stage.appendChild(token);
    s.body.appendChild(stage);

    var cur = cfg.start || (states[0] && states[0].id);
    var auto = null, autoIdx = 0, sp = 1;

    function paint() {
      Array.prototype.forEach.call(stage.querySelectorAll('.node'), function (n) {
        n.classList.toggle('active', n.dataset.id === cur);
      });
      Array.prototype.forEach.call(s.ctl.querySelectorAll('[data-edge]'), function (b) {
        var e = edges[+b.dataset.edge];
        b.classList.toggle('dim', e.from !== cur);
      });
      s.note.innerHTML = '<b style="color:#5ff1ef">当前状态</b>　' + esc(cur) +
        (cfg.stateNotes && cfg.stateNotes[cur] ? '　' + esc(cfg.stateNotes[cur]) : '');
    }

    function fire(k, done) {
      var e = edges[k];
      if (!e || e.from !== cur) return;
      var g = stage.querySelector('.edge[data-k="' + k + '"]');
      if (g) g.classList.add('fire');
      var p = e._path;
      var t0 = performance.now(), dur = 600 / sp;
      token.style.opacity = '1';
      (function step(now) {
        var t = clamp((now - t0) / dur, 0, 1);
        var x = (1 - t) * (1 - t) * p.sx + 2 * (1 - t) * t * p.mx + t * t * p.ex;
        var y = (1 - t) * (1 - t) * p.sy + 2 * (1 - t) * t * p.my + t * t * p.ey;
        token.style.left = (x / W * stage.clientWidth) + 'px';
        token.style.top = (y / H * stage.clientHeight) + 'px';
        token.style.transform = 'translate(-50%,-50%)';
        if (t < 1) requestAnimationFrame(step);
        else {
          token.style.opacity = '0';
          cur = e.to;
          if (g) setTimeout(function () { g.classList.remove('fire'); }, 260);
          paint();
          if (done) done();
        }
      })(t0);
    }

    var ctlBtns = [];
    edges.forEach(function (e, k) {
      if (cfg.events === false) return;
      var b = btn((e.event || e.label || ('事件' + (k + 1))), function () {
        if (e.from === cur) { stopAuto(); fire(k); }
        else shake();
      });
      b.dataset.edge = k;
      ctlBtns.push(b);
    });
    function shake() {
      s.box.animate ? s.box.animate([{ transform: 'none' }, { transform: 'translateX(-3px)' }, { transform: 'none' }], { duration: 260 }) : 0;
    }
    var sa = btn('▶ 按剧本巡演', function () {
      if (auto) return stopAuto();
      if (!cfg.script || !cfg.script.length) return;
      autoIdx = 0;
      auto = setInterval(function () {
        var k = cfg.script[autoIdx++];
        if (k == null || autoIdx > cfg.script.length) return stopAuto();
        var e = edges[k];
        if (!e) return;
        cur = e.from; paint();
        setTimeout(function () { fire(k); }, 120);
      }, 1200 / sp);
      sa.classList.add('on');
    });
    function stopAuto() {
      if (auto) { clearInterval(auto); auto = null; sa.classList.remove('on'); }
    }
    var rs = btn('↺ 重置', function () { stopAuto(); cur = cfg.start || states[0].id; paint(); });
    var spd = speedPicker(function (v) { sp = v; });
    s.ctl.appendChild(rs);
    if (cfg.script && cfg.script.length) s.ctl.appendChild(sa);
    s.ctl.appendChild(el('span', 'ik-sp'));
    ctlBtns.forEach(function (b) { s.ctl.appendChild(b); });
    box.appendChild(s.box);
    paint();
    if (false && cfg.script) setTimeout(function () { sa.click(); }, 700);
  };

  /* ============ 3. stack 分层封装 ============ */
  R.stack = function (cfg, box) {
    var layers = cfg.layers || [];
    var s = shell(cfg, { cls: 'ik-st' });
    var stage = el('div', 'ik-stage');
    var pkt = el('div', 'ik-packet');
    var list = el('div', '');
    var depth = 0; // 0 = 只有数据；每 +1 加一层头
    var order = layers.slice();

    function paint() {
      pkt.innerHTML = '';
      var segs = [];
      for (var i = depth - 1; i >= 0; i--) {
        var L = order[i];
        segs.push('<span class="seg" style="border-color:' + (L.color || '#5ff1ef') + '55;background:' + (L.color || '#5ff1ef') + '22">' + esc(L.header || L.name) + '</span>');
      }
      segs.push('<span class="seg" style="border-color:rgba(251,191,36,.5);background:rgba(251,191,36,.16)">' + esc(cfg.payload || 'DATA') + '</span>');
      pkt.innerHTML = segs.join('');
      Array.prototype.forEach.call(list.children, function (row, i) {
        row.classList.toggle('on', i < depth);
        var hd = row.querySelector('.hdr');
        if (hd) hd.classList.toggle('show', i < depth);
      });
      s.note.innerHTML = depth === 0
        ? (cfg.note0 || '还没有任何协议头：这就是应用写进缓冲区的那串字节。')
        : ('已' + (cfg.word || '封装') + ' <b style="color:#5ff1ef">' + depth + '</b> 层：' +
           esc(order.slice(0, depth).map(function (L) { return L.header || L.name; }).join(' + ') + ' + DATA') +
           (cfg.notes && cfg.notes[depth - 1] ? '<br>' + esc(cfg.notes[depth - 1]) : ''));
      st.textContent = depth + ' / ' + order.length;
      btnDn.classList.toggle('dim', depth >= order.length);
      btnUp.classList.toggle('dim', depth <= 0);
    }
    order.forEach(function (L, i) {
      var row = el('div', 'ik-layer');
      row.innerHTML = '<span class="ln" style="color:' + (L.color || '#5ff1ef') + '">' + esc(L.name) + '</span>' +
        '<span class="hdr">' + esc(L.header || '') + '</span>' +
        '<span class="pl">' + esc(L.hint || '') + '</span>';
      row.addEventListener('click', function () { depth = i + 1; paint(); });
      list.appendChild(row);
    });
    stage.appendChild(pkt);
    stage.appendChild(list);
    s.body.appendChild(stage);

    var btnDn = btn('↓ 封装一层', function () { depth = Math.min(order.length, depth + 1); paint(); });
    var btnUp = btn('↑ 解封装', function () { depth = Math.max(0, depth - 1); paint(); });
    var auto = btn('▶ 自动', function () {
      var t = 0;
      var id = setInterval(function () {
        t++;
        if (t <= order.length) { depth = t; paint(); }
        else if (t <= order.length * 2) { depth = order.length * 2 - t; paint(); }
        else clearInterval(id);
      }, 900);
    });
    var st = el('span', 'ik-step', '0 / ' + order.length);
    s.ctl.appendChild(btnDn); s.ctl.appendChild(btnUp); s.ctl.appendChild(auto);
    s.ctl.appendChild(el('span', 'ik-sp')); s.ctl.appendChild(st);
    box.appendChild(s.box);
    paint();
  };

  /* ============ 4. walk 拆位查表 ============ */
  R.walk = function (cfg, box) {
    var bits = cfg.bits || [];
    var levels = cfg.levels || [];
    var s = shell(cfg, { cls: 'ik-wk' });
    var body = el('div', '');
    var inputWrap = el('div', 'ik-in');
    var inp = el('input'); inp.type = 'text'; inp.value = cfg.addr || '0x0000';
    inputWrap.appendChild(el('span', '', '地址'));
    inputWrap.appendChild(inp);
    var rnd = btn('随机', function () {
      var n = Math.floor(Math.random() * Math.pow(2, bits.reduce(function (a, b) { return a + b.n; }, 0)));
      inp.value = '0x' + n.toString(16).toUpperCase();
      run();
    });
    inputWrap.appendChild(rnd);
    var tlbWrap = el('span', '', '');
    var tlbOn = false;
    var tlbBtn = btn('TLB：未命中', function () {
      tlbOn = !tlbOn;
      tlbBtn.textContent = tlbOn ? 'TLB：命中（跳过查表）' : 'TLB：未命中';
      tlbBtn.classList.toggle('on', tlbOn);
      run();
    });
    inputWrap.appendChild(tlbBtn);
    body.appendChild(inputWrap);

    var bitsBar = el('div', 'ik-bits');
    body.appendChild(bitsBar);
    var tblWrap = el('div', 'ik-tbl');
    body.appendChild(tblWrap);
    var out = el('div', 'ik-out');
    body.appendChild(out);
    s.body.appendChild(body);

    function parse() {
      var t = inp.value.trim().replace(/_/g, '');
      var n = /^0x/i.test(t) ? parseInt(t.slice(2), 16) : parseInt(t, 10);
      var total = bits.reduce(function (a, b) { return a + b.n; }, 0);
      if (!isFinite(n)) n = 0;
      n = n % Math.pow(2, total);
      return n;
    }

    function split(n) {
      var out2 = [], total = bits.reduce(function (a, b) { return a + b.n; }, 0);
      var shift = total;
      bits.forEach(function (b) {
        shift -= b.n;
        var mask = (1 << b.n) - 1;
        out2.push({ v: (n >> shift) & mask, k: b.k, n: b.n });
      });
      return out2;
    }

    function run() {
      var n = parse(), parts = split(n);
      bitsBar.innerHTML = parts.map(function (p, i) {
        return '<div class="ik-bit" data-i="' + i + '"><div class="v">0x' + p.v.toString(16).toUpperCase() + '</div>' +
          '<div class="k">' + esc(p.k) + ' · ' + p.n + 'b</div></div>';
      }).join('');

      // 表：每层用对应位段做索引，高亮该行
      var html = '';
      levels.forEach(function (lv, li) {
        var pi = Math.min(lv.idx === undefined ? li : lv.idx, parts.length - 1);
        var idx = parts[pi] ? parts[pi].v : 0;
        var rows = lv.rows || [];
        var win = lv.window || rows.length;
        var start = Math.min(Math.max(0, idx - 3), Math.max(0, rows.length - win));
        html += '<div style="margin:10px 0 4px;color:#a78bfa;font-size:11.5px">' + esc(lv.name) +
          '　<span style="color:#64789a">索引 = 0x' + idx.toString(16).toUpperCase() + '</span></div>';
        html += '<table><thead><tr><th style="width:52px">项</th><th>表项内容</th></tr></thead><tbody>';
        for (var k = start; k < Math.min(rows.length, start + win); k++) {
          var isHit = k === idx;
          html += '<tr class="' + (isHit ? 'hit' : '') + '"><td>0x' + k.toString(16).toUpperCase() + '</td><td>' +
            esc(rows[k]) + (isHit ? '　<span style="color:#5ff1ef">← 命中</span>' : '') + '</td></tr>';
        }
        html += '</tbody></table>';
      });
      tblWrap.innerHTML = html;

      var o = [];
      o.push('拆分：' + parts.map(function (p) { return p.k + '=0x' + p.v.toString(16).toUpperCase(); }).join(' ｜ '));
      if (tlbOn) {
        o.push('TLB 命中 → 直接得到物理地址，跳过 ' + levels.length + ' 次查表（省掉 ' + (levels.length * 2) + ' 次内存访问）');
        o.push('物理地址 = ' + (cfg.tlbPA || '（由 TLB 输出）'));
      } else {
        o.push('查表：' + levels.map(function (lv, i) { return '第 ' + (i + 1) + ' 级用 ' + esc(lv.name); }).join(' → '));
        var last = levels[levels.length - 1];
        var lp = last && last.idx !== undefined ? Math.min(last.idx, parts.length - 1) : Math.min(levels.length - 1, parts.length - 1);
        var v = (last && last.rows && last.rows[parts[lp].v]) || '（表项）';
        o.push('命中表项 = ' + v);
        o.push('物理地址 = 表项里的页基址 + 偏移 0x' + parts[parts.length - 1].v.toString(16).toUpperCase());
      }
      out.textContent = o.join('\n');
      s.note.innerHTML = cfg.note
        ? esc(cfg.note)
        : '改地址看位段怎么变；开 TLB 看缓存命中和查表的差别。';
      // 顺序点亮位段
      Array.prototype.forEach.call(bitsBar.children, function (b, i) {
        setTimeout(function () { b.classList.add('on'); }, 120 * i);
      });
    }
    inp.addEventListener('input', run);
    s.ctl.appendChild(el('span', 'ik-sp'));
    s.ctl.appendChild(btn('重新走一遍', function () { Array.prototype.forEach.call(bitsBar.children, function (b) { b.classList.remove('on'); }); setTimeout(run, 60); }));
    box.appendChild(s.box);
    run();
  };

  /* ============ 5. param 参数联动 ============ */
  R.param = function (cfg, box) {
    var fields = cfg.fields || [];
    var s = shell(cfg, { cls: 'ik-pm' });
    var body = el('div', '');
    var wrap = el('div', 'ik-fields');
    var vals = {};
    fields.forEach(function (f) {
      vals[f.k] = num(f.val, f.min || 0);
      var row = el('div', 'ik-f');
      row.appendChild(el('label', '', esc(f.label)));
      var r = el('input'); r.type = 'range';
      r.min = f.min; r.max = f.max; r.step = f.step || 1; r.value = vals[f.k];
      var uv = el('span', 'uv', vals[f.k] + (f.unit || ''));
      r.addEventListener('input', function () {
        vals[f.k] = +r.value;
        uv.textContent = vals[f.k] + (f.unit || '');
        compute();
      });
      row.appendChild(r); row.appendChild(uv);
      wrap.appendChild(row);
    });
    body.appendChild(wrap);
    var outWrap = el('div', 'ik-out');
    body.appendChild(outWrap);
    s.body.appendChild(body);

    function fmt(v) {
      if (typeof v !== 'number' || !isFinite(v)) return String(v);
      if (Math.abs(v) >= 1e9) return (v / 1e9).toFixed(2) + 'G';
      if (Math.abs(v) >= 1e6) return (v / 1e6).toFixed(2) + 'M';
      if (Math.abs(v) >= 1e3) return v.toLocaleString('zh-CN', { maximumFractionDigits: 2 });
      return String(+v.toFixed(3));
    }
    function compute() {
      outWrap.innerHTML = '';
      (cfg.outs || []).forEach(function (o) {
        var v;
        try {
          v = new Function('V', 'with(Math){return (' + o.expr + ')}')(vals);
        } catch (e) { v = '?'; }
        outWrap.appendChild(el('div', 'ik-o',
          '<span class="k">' + esc(o.label) + '</span><b>' + esc(fmt(v)) + esc(o.unit || '') + '</b>'));
      });
      if (cfg.bar) {
        var pct = 0;
        try { pct = clamp(new Function('V', 'with(Math){return (' + cfg.bar.expr + ')}')(vals), 0, 100); } catch (e) {}
        if (!outWrap.querySelector('.ik-bar')) {
          outWrap.appendChild(el('div', 'ik-bar', '<i></i>'));
        }
        outWrap.querySelector('.ik-bar i').style.width = pct + '%';
      }
      if (cfg.verdict) {
        var txt, cls = '';
        try {
          var r = new Function('V', 'with(Math){return (' + cfg.verdict.expr + ')}')(vals);
          txt = r ? cfg.verdict.ok : cfg.verdict.bad;
          cls = r ? 'ok' : 'warn';
        } catch (e) { txt = ''; }
        var vd = outWrap.querySelector('.vd');
        if (!vd) { vd = el('div', 'ik-o vd'); outWrap.appendChild(vd); }
        vd.innerHTML = '<span class="k">判断</span><b style="color:' + (cls === 'ok' ? '#34d399' : '#fb7185') + '">' + esc(txt) + '</b>';
      }
      s.note.innerHTML = cfg.note ? esc(cfg.note) : '拖动滑块，下面的数字实时跟着变。';
    }
    compute();
    box.appendChild(s.box);
  };

  /* ============ 6. drag 拖拽排序 ============ */
  R.drag = function (cfg, box) {
    var items = (cfg.items || []).slice();
    var answer = cfg.answer || items.map(function (it) { return it.id; });
    var s = shell(cfg, { cls: 'ik-dr' });
    var pool = el('div', 'ik-pool');
    var slots = el('div', 'ik-slots');
    s.body.appendChild(el('div', '', '<span style="color:#8b9cbb;font-size:11.5px">把下面的卡片放进正确顺序（可拖动，也可先点卡片再点空位）</span>'));
    s.body.appendChild(pool);
    s.body.appendChild(el('div', '', '<span style="color:#8b9cbb;font-size:11.5px">顺序</span>'));
    s.body.appendChild(slots);

    var picked = null;
    items.forEach(function (it) {
      var c = el('div', 'ik-chip', esc(it.text));
      c.draggable = true; c.dataset.id = it.id;
      c.addEventListener('dragstart', function (ev) { ev.dataTransfer.setData('text/plain', it.id); c.classList.add('dragging'); });
      c.addEventListener('dragend', function () { c.classList.remove('dragging'); });
      c.addEventListener('click', function () {
        picked = it.id;
        Array.prototype.forEach.call(pool.querySelectorAll('.ik-chip'), function (x) { x.style.borderColor = ''; });
        c.style.borderColor = '#5ff1ef';
      });
      pool.appendChild(c);
    });
    answer.forEach(function (_, i) {
      var sl = el('div', 'ik-slot', '<span class="no">' + (i + 1) + '</span><span class="fill"></span>');
      sl.dataset.i = i;
      sl.addEventListener('dragover', function (ev) { ev.preventDefault(); sl.classList.add('over'); });
      sl.addEventListener('dragleave', function () { sl.classList.remove('over'); });
      sl.addEventListener('drop', function (ev) {
        ev.preventDefault(); sl.classList.remove('over');
        place(ev.dataTransfer.getData('text/plain'), sl);
      });
      sl.addEventListener('click', function () {
        if (picked) { place(picked, sl); picked = null; }
        else if (sl.querySelector('.ik-chip')) { // 取回
          var c = sl.querySelector('.ik-chip');
          pool.appendChild(c); c.style.borderColor = '';
          sl.classList.remove('ok', 'bad');
        }
      });
      slots.appendChild(sl);
    });
    function place(id, sl) {
      if (!id) return;
      var chip = pool.querySelector('[data-id="' + id + '"]');
      if (!chip) return;
      var occupied = sl.querySelector('.ik-chip');
      if (occupied) pool.appendChild(occupied);
      sl.querySelector('.fill').appendChild(chip);
      chip.style.borderColor = '';
      sl.classList.remove('ok', 'bad');
    }
    var msg;
    function check() {
      var okAll = true;
      Array.prototype.forEach.call(slots.children, function (sl, i) {
        var c = sl.querySelector('.ik-chip');
        var good = c && c.dataset.id === answer[i];
        sl.classList.toggle('ok', !!good);
        sl.classList.toggle('bad', !good && !!c);
        if (!good) okAll = false;
      });
      if (msg) msg.remove();
      msg = el('div', okAll ? 'ik-ok' : 'ik-warn',
        okAll ? ('全部正确。' + esc(cfg.explain || '')) : '还有位置不对：红色的是错的。点卡片可取回重放，或看答案。');
      s.body.appendChild(msg);
      if (okAll && cfg.explain) s.note.innerHTML = esc(cfg.explain);
    }
    s.ctl.appendChild(btn('✓ 校验顺序', check));
    s.ctl.appendChild(btn('看答案', function () {
      Array.prototype.forEach.call(slots.children, function (sl, i) {
        var c = sl.querySelector('.ik-chip'); if (c) pool.appendChild(c);
      });
      Array.prototype.forEach.call(slots.children, function (sl, i) {
        var chip = pool.querySelector('[data-id="' + answer[i] + '"]');
        sl.querySelector('.fill').appendChild(chip);
        sl.classList.add('ok');
      });
      s.note.innerHTML = esc(cfg.explain || '');
    }));
    s.ctl.appendChild(el('span', 'ik-sp'));
    s.ctl.appendChild(btn('↺ 全部取回', function () {
      Array.prototype.forEach.call(slots.querySelectorAll('.ik-chip'), function (c) { pool.appendChild(c); });
      Array.prototype.forEach.call(slots.children, function (sl) { sl.classList.remove('ok', 'bad'); });
      if (msg) { msg.remove(); msg = null; }
    }));
    box.appendChild(s.box);
  };

  /* ============ 7. mem 布局条 ============ */
  R.mem = function (cfg, box) {
    var segs = cfg.segments || [];
    var s = shell(cfg, { cls: 'ik-mm' });
    var bar = el('div', 'ik-bar');
    var ptr = el('div', 'ik-ptr');
    var detail = el('div', 'ik-detail', cfg.note || '鼠标在条上移动，看每一段装的是什么。');
    var sum = segs.reduce(function (a, x) { return a + num(x.len, 1); }, 0);
    segs.forEach(function (g, i) {
      var d = el('div', 'seg', esc(g.name));
      d.style.flex = num(g.len, 1) + ' 0 0%';
      d.style.background = g.color || 'rgba(95,241,239,.3)';
      d.dataset.i = i;
      bar.appendChild(d);
    });
    bar.appendChild(ptr);
    s.body.appendChild(bar);
    if (cfg.legend) s.body.appendChild(el('div', 'ik-legend', cfg.legend));
    s.body.appendChild(detail);

    function show(i, pct) {
      Array.prototype.forEach.call(bar.querySelectorAll('.seg'), function (x) { x.classList.toggle('on', +x.dataset.i === i); });
      var g = segs[i];
      if (!g) return;
      detail.innerHTML = '<b style="color:' + (g.color || '#5ff1ef') + '">' + esc(g.name) + '</b>' +
        (g.addr ? '　<span style="font-family:monospace;color:#8b9cbb">' + esc(g.addr) + '</span>' : '') +
        (g.note ? '<br>' + esc(g.note) : '');
    }
    function fromX(clientX) {
      var r = bar.getBoundingClientRect();
      var p = clamp((clientX - r.left) / r.width, 0, 0.9999);
      ptr.style.left = (p * 100) + '%';
      var acc = 0;
      for (var i = 0; i < segs.length; i++) {
        acc += num(segs[i].len, 1);
        if (p * sum <= acc) return show(i, p);
      }
    }
    bar.addEventListener('pointermove', function (ev) { fromX(ev.clientX); });
    bar.addEventListener('click', function (ev) { fromX(ev.clientX); });
    box.appendChild(s.box);
  };

  /* ============ 8. queue 环形缓冲 ============ */
  R.queue = function (cfg, box) {
    var n = cfg.size || 8;
    var s = shell(cfg, { cls: 'ik-qu' });
    var ring = el('div', 'ik-ring');
    var cells = [];
    for (var i = 0; i < n; i++) {
      var ang = (i / n) * Math.PI * 2 - Math.PI / 2;
      var cx = 95 + Math.cos(ang) * 72 - 20, cy = 95 + Math.sin(ang) * 72 - 20;
      var c = el('div', 'cell', String(i));
      c.style.left = cx + 'px'; c.style.top = cy + 'px';
      ring.appendChild(c); cells.push(c);
    }
    s.body.appendChild(ring);
    var label = el('div', 'ik-label', 'head=0　tail=0　空');
    s.body.appendChild(label);
    var head = 0, tail = 0, count = 0, data = [];

    function paint(msg) {
      cells.forEach(function (c, i) {
        c.classList.toggle('filled', data.some(function (d) { return d.i === i; }));
        c.textContent = data.some(function (d) { return d.i === i; }) ? String(i) : String(i);
      });
      label.textContent = 'head=' + head + '　tail=' + tail + '　' + (count === 0 ? '空' : count === n ? '满' : count + '/' + n);
      s.note.innerHTML = msg || (cfg.note || '');
    }
    function push() {
      if (count === n) {
        s.note.innerHTML = '<b style="color:#fb7185">缓冲区满</b>　tail 追上 head：写端必须阻塞或丢掉这段数据。';
        return;
      }
      data.push({ i: tail }); count++;
      cells[tail].classList.add('flash');
      tail = (tail + 1) % n;
      paint();
    }
    function pop() {
      if (!count) { s.note.innerHTML = '<b style="color:#fbbf24">缓冲区空</b>　读端阻塞，等写端写入或收到 EOF。'; return; }
      var d = data.shift(); count--;
      cells[d.i].classList.add('flash');
      head = (head + 1) % n;
      paint();
    }
    s.ctl.appendChild(btn('写入一块 →', push));
    s.ctl.appendChild(btn('← 读出一块', pop));
    s.ctl.appendChild(btn('▶ 自动', function () {
      var k = 0;
      var id = setInterval(function () {
        k++;
        if (k % 3 === 0) pop(); else push();
        if (k > 14) clearInterval(id);
      }, 700);
    }));
    s.ctl.appendChild(el('span', 'ik-sp'));
    s.ctl.appendChild(btn('↺ 清空', function () { data = []; head = tail = count = 0; paint(''); }));
    box.appendChild(s.box);
    paint();
  };

  /* ============ 9. hop 逐跳 ============ */
  R.hop = function (cfg, box) {
    var nodes = cfg.nodes || [];
    var hops = cfg.hops || [];
    var s = shell(cfg, { cls: 'ik-hp' });
    var row = el('div', 'ik-nodes');
    nodes.forEach(function (nd, i) {
      row.appendChild(el('div', 'ik-node', '<div class="n">' + esc(nd.n) + '</div><div class="s">' + esc(nd.s || '') + '</div>'));
    });
    s.body.appendChild(row);
    var track = el('div', 'ik-track');
    var pkt = el('div', 'ik-pkt', esc(cfg.packet || '数据包'));
    track.appendChild(pkt);
    s.body.appendChild(track);
    var log = el('div', 'ik-hops', cfg.note || '点「下一步」，看包怎么一跳一跳走过去。');
    s.body.appendChild(log);
    var i = 0, timer = null;

    function pos(idx) {
      var nd = row.children[idx];
      if (!nd) return;
      var r = nd.getBoundingClientRect(), pr = track.getBoundingClientRect();
      pkt.style.left = ((r.left - pr.left + r.width / 2) / pr.width * 100) + '%';
    }
    function paint() {
      Array.prototype.forEach.call(row.children, function (n2, k) { n2.classList.toggle('on', k <= i); });
      pos(i);
      var h = hops[i];
      log.innerHTML = h ? ('<b style="color:#5ff1ef">第 ' + (i + 1) + ' 跳 · ' + esc(h.at || nodes[i] && nodes[i].n || '') + '</b>　' + esc(h.label || '') +
        (h.note ? '<br>' + esc(h.note) : '')) : (cfg.note || '');
      if (h && h.pkt) pkt.textContent = h.pkt;
      st.textContent = (i + 1) + ' / ' + hops.length;
    }
    var st = el('span', 'ik-step', '0 / ' + hops.length);
    var next = btn('下一步 →', function () { stop(); i = Math.min(hops.length - 1, i + 1); paint(); });
    var prev = btn('← 上一步', function () { stop(); i = Math.max(0, i - 1); paint(); });
    var auto = btn('▶ 自动', function () {
      if (timer) return stop();
      timer = setInterval(function () {
        if (i >= hops.length - 1) return stop();
        i++; paint();
      }, 1200);
      auto.textContent = '⏸ 暂停';
    });
    function stop() { if (timer) { clearInterval(timer); timer = null; } auto.textContent = '▶ 自动'; }
    s.ctl.appendChild(prev); s.ctl.appendChild(next); s.ctl.appendChild(auto);
    s.ctl.appendChild(el('span', 'ik-sp')); s.ctl.appendChild(st);
    box.appendChild(s.box);
    paint();
    window.addEventListener('resize', function () { pos(i); });
  };

  /* ============ 10. code 代码 / 寄存器联动 ============ */
  R.code = function (cfg, box) {
    var lines = cfg.lines || [];
    var s = shell(cfg, { cls: 'ik-code' });
    var grid = el('div', 'ik-cd');
    var left = el('div', 'ik-lines');
    var right = el('div', 'ik-regs');
    grid.appendChild(left); grid.appendChild(right);
    s.body.appendChild(grid);

    var regs = {};
    (cfg.regs || []).forEach(function (r) { regs[r.n] = r.v; });

    lines.forEach(function (L, i) {
      var row = el('div', 'ik-line');
      row.innerHTML = '<span class="ln">' + (i + 1) + '</span><span class="cd">' + esc(L.c) + '</span>';
      row.addEventListener('click', function () { go(i); });
      left.appendChild(row);
    });
    function paintRegs(changed) {
      right.innerHTML = '';
      Object.keys(regs).forEach(function (k) {
        var r = el('div', 'ik-reg' + (changed && changed[k] != null ? ' chg' : ''),
          '<span class="rn">' + esc(k) + '</span><span class="rv">' + esc(regs[k]) + '</span>');
        right.appendChild(r);
      });
    }
    var i = -1;
    function go(idx) {
      i = idx;
      Array.prototype.forEach.call(left.children, function (r, k) { r.classList.toggle('cur', k === i); });
      var changed = {};
      var L = lines[i];
      if (L && L.set) Object.keys(L.set).forEach(function (k) { regs[k] = L.set[k]; changed[k] = 1; });
      paintRegs(changed);
      s.note.innerHTML = L && L.note ? ('<b style="color:#fbbf24">第 ' + (i + 1) + ' 行</b>　' + esc(L.note)) : (cfg.note || '');
      st.textContent = (i + 1) + ' / ' + lines.length;
    }
    var st = el('span', 'ik-step', '0 / ' + lines.length);
    s.ctl.appendChild(btn('← 上一步', function () { go(Math.max(0, i - 1)); }));
    s.ctl.appendChild(btn('单步 →', function () { go(Math.min(lines.length - 1, i + 1)); }));
    s.ctl.appendChild(btn('▶ 自动', function () {
      var k = i < 0 ? 0 : i;
      var id = setInterval(function () { k++; if (k >= lines.length) clearInterval(id); else go(k); }, 900);
    }));
    s.ctl.appendChild(btn('↺ 重置', function () {
      (cfg.regs || []).forEach(function (r) { regs[r.n] = r.v; });
      i = -1; paintRegs(); s.note.innerHTML = cfg.note || '';
    }));
    s.ctl.appendChild(el('span', 'ik-sp')); s.ctl.appendChild(st);
    box.appendChild(s.box);
    paintRegs();
    if (false) setTimeout(function () { go(Math.min(lines.length - 1, 1)); }, 600);
  };

  /* ---------------- 启动 ---------------- */
  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('.ikit[data-type]'), function (box) {
      if (box.dataset.ready) return;
      var type = box.dataset.type;
      var fn = R[type];
      if (!fn) { box.innerHTML = '<div class="ik-note">未实现的组件类型：' + type + '</div>'; return; }
      var cfg = {};
      try { cfg = JSON.parse(box.dataset.json || '{}'); } catch (e) { cfg = {}; }
      try { fn(cfg, box); box.dataset.ready = '1'; } catch (e) {
        box.innerHTML = '<div class="ik-note">组件渲染失败：' + esc(e.message) + '</div>';
      }
    });
  }

  window.IKit = { init: init, types: R };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
