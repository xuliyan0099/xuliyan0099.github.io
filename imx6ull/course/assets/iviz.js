/* ===== 交互组件库 iviz.js ===== */
(function () {
  'use strict';
  function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; }
  function num(v, d) { var n = parseFloat(v); return isNaN(n) ? d : n; }
  function head(n, cfg) {
    var t = cfg.title || n.getAttribute('data-title') || '动手试一下';
    var hint = cfg.hint || n.getAttribute('data-hint') || '';
    var h = el('div', 'it', '<i></i><span>' + t + '</span>' + (hint ? '<em>' + hint + '</em>' : ''));
    n.appendChild(h);
    return n;
  }
  function bin(x, w) {
    w = w || 8;
    var m = 1;
    for (var i = 0; i < w; i++) m *= 2;
    var n = ((Math.floor(x) % m) + m) % m, s = '';
    for (var k = w - 1; k >= 0; k--) s += (Math.floor(n / Math.pow(2, k)) % 2);
    return s;
  }
  function hex(x, w) {
    w = w || 2;
    return bin(x, w * 4).replace(/[01]{4}/g, function (g) {
      return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'][parseInt(g, 2)];
    });
  }
  function calc(expr, v) {
    try { return Function('v', 'bin', 'hex', 'return (' + expr + ');')(v, bin, hex); } catch (e) { return '—'; }
  }
  function fmt(x) {
    if (typeof x !== 'number' || !isFinite(x)) return String(x);
    if (Math.abs(x) >= 1000) return String(Math.round(x));
    if (Number.isInteger(x)) return String(x);
    return x.toFixed(2);
  }

  /* ---------- 单步推进 ---------- */
  function renderSteps(n, cfg) {
    head(n, cfg);
    n.classList.add('ivz-steps');
    var steps = cfg.steps || [], i = 0;
    var track = el('div', 'track');
    var card = el('div', 'card');
    var ctl = el('div', 'ctl');
    var prev = el('button', 'ivb', '← 上一步');
    var next = el('button', 'ivb', '下一步 →');
    var cnt = el('span', 'cnt');
    prev.type = next.type = 'button';
    var dots = [];
    steps.forEach(function (s, k) {
      var d = el('div', 'dot');
      d.addEventListener('click', function () { i = k; paint(); });
      track.appendChild(d); dots.push(d);
    });
    n.appendChild(track); n.appendChild(card);
    ctl.appendChild(prev); ctl.appendChild(next); ctl.appendChild(cnt);
    n.appendChild(ctl);
    if (cfg.note) n.appendChild(el('div', 'hint', cfg.note));
    function paint() {
      var s = steps[i] || {};
      card.innerHTML = '<b>' + (s.t || '') + '</b><p>' + (s.d || '') + '</p>';
      dots.forEach(function (d, k) { d.classList.toggle('on', k <= i); });
      cnt.textContent = (i + 1) + ' / ' + steps.length;
      prev.disabled = i === 0;
      next.disabled = i === steps.length - 1;
    }
    prev.addEventListener('click', function () { if (i > 0) { i--; paint(); } });
    next.addEventListener('click', function () { if (i < steps.length - 1) { i++; paint(); } });
    paint();
  }

  /* ---------- 点选查看 ---------- */
  function renderPick(n, cfg) {
    head(n, cfg);
    n.classList.add('ivz-pick');
    var chips = el('div', 'chips');
    var desc = el('div', 'desc');
    var items = cfg.items || [], cur = -1;
    var cps = [];
    items.forEach(function (it, k) {
      var b = el('button', 'chip', it.b);
      b.type = 'button';
      b.addEventListener('click', function () { cur = (cur === k ? -1 : k); paint(); });
      chips.appendChild(b); cps.push(b);
    });
    n.appendChild(chips); n.appendChild(desc);
    function paint() {
      cps.forEach(function (b, k) { b.classList.toggle('on', k === cur); });
      if (cur < 0) desc.innerHTML = '<em>' + (cfg.note || '点上面任意一项，看它到底干什么。') + '</em>';
      else desc.innerHTML = items[cur].d;
    }
    paint();
  }

  /* ---------- 视图切换 ---------- */
  function renderSwitch(n, cfg) {
    head(n, cfg);
    n.classList.add('ivz-sw');
    var chips = el('div', 'chips');
    var list = el('div', 'list');
    var views = cfg.views || [], cur = 0;
    var bs = [];
    views.forEach(function (v, k) {
      var b = el('button', 'ivb', v.b);
      b.type = 'button';
      b.addEventListener('click', function () { cur = k; paint(); });
      chips.appendChild(b); bs.push(b);
    });
    n.appendChild(chips); n.appendChild(list);
    function paint() {
      bs.forEach(function (b, k) { b.classList.toggle('on', k === cur); });
      var v = views[cur] || { items: [] };
      list.innerHTML = '';
      (v.items || []).forEach(function (it) {
        var r = el('div', 'row');
        r.innerHTML = '<b>' + (it.t || '') + '</b>' + (it.d ? '<s>' + it.d + '</s>' : '');
        list.appendChild(r);
      });
    }
    paint();
  }

  /* ---------- 滑块联动 ---------- */
  function renderSlider(n, cfg) {
    head(n, cfg);
    n.classList.add('ivz-sl');
    var min = num(cfg.min, 0), max = num(cfg.max, 100), step = num(cfg.step, 1);
    var v = num(cfg.value, min);
    var top = el('div', 'head');
    var lab = el('span', 'lab', cfg.label || '拖动滑块');
    var val = el('span', 'val');
    var unit = el('span', 'unit', cfg.unit || '');
    top.appendChild(lab); top.appendChild(val); top.appendChild(unit);
    var range = el('input', 'ivrange');
    range.type = 'range';
    range.min = min; range.max = max; range.step = step; range.value = v;
    range.setAttribute('aria-label', (cfg.label || '') + ' 调节滑块');
    var bar = el('div', 'bar', '<i></i>');
    var out = el('div', 'ivz-out');
    n.appendChild(top); n.appendChild(range); n.appendChild(bar);
    if (cfg.out && cfg.out.length) n.appendChild(out);
    var presets = null;
    if (cfg.presets && cfg.presets.length) {
      presets = el('div', 'ivz-presets');
      cfg.presets.forEach(function (p) {
        var b = el('button', 'ivb', p.t);
        b.type = 'button';
        b.addEventListener('click', function () { v = p.v; range.value = p.v; paint(); });
        presets.appendChild(b);
      });
      n.appendChild(presets);
    }
    if (cfg.note) { var hintEl = el('div', 'hint', cfg.note); n.appendChild(hintEl); }
    function paint() {
      v = num(range.value, min);
      val.textContent = fmt(v);
      var p = max === min ? 0 : (v - min) / (max - min);
      bar.firstChild.style.width = (p * 100).toFixed(1) + '%';
      if (out) {
        out.innerHTML = '';
        (cfg.out || []).forEach(function (o) {
          var d = el('div');
          var res = o.expr ? calc(o.expr, v) : v;
          d.innerHTML = '<s>' + (o.k || '') + '</s><b>' + fmt(res) + (o.unit || '') + '</b>';
          out.appendChild(d);
        });
      }
    }
    range.addEventListener('input', paint);
    range.addEventListener('change', paint);
    paint();
  }

  /* ---------- 点选答题 ---------- */
  function renderGuess(n, cfg) {
    head(n, cfg);
    n.classList.add('ivz-g');
    var q = el('p', 'q', cfg.q || '');
    n.appendChild(q);
    var opts = cfg.options || [], answered = false;
    var why = el('div', 'why', '');
    var bs = [];
    opts.forEach(function (o) {
      var b = el('button', 'ivb opt', o.t);
      b.type = 'button';
      b.addEventListener('click', function () {
        if (answered) return;
        answered = true;
        bs.forEach(function (x, k) {
          if (opts[k].ok) x.classList.add('ok');
          else if (k === bs.indexOf(b)) x.classList.add('no');
          x.disabled = true;
        });
        why.innerHTML = (o.ok ? '<b style="color:#5ce1a0">对。</b> ' : '<b style="color:#ff6b81">不对。</b> ') + (o.why || '') +
          (cfg.explain ? '<br><em style="color:#93a1bd">' + cfg.explain + '</em>' : '');
      });
      n.appendChild(b); bs.push(b);
    });
    n.appendChild(why);
  }

  function boot() {
    var nodes = document.querySelectorAll('.iviz[data-kind]');
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.getAttribute('data-built') === '1') continue;
      var cfg = null;
      try { cfg = JSON.parse(n.getAttribute('data-json') || '{}'); } catch (e) { cfg = null; }
      if (!cfg) { n.innerHTML = '<div class="it"><i></i><span>组件数据有误</span></div>'; continue; }
      var kind = n.getAttribute('data-kind');
      try {
        if (kind === 'steps') renderSteps(n, cfg);
        else if (kind === 'pick') renderPick(n, cfg);
        else if (kind === 'switch') renderSwitch(n, cfg);
        else if (kind === 'slider') renderSlider(n, cfg);
        else if (kind === 'guess') renderGuess(n, cfg);
        else n.innerHTML = '<div class="it"><i></i><span>未知组件：' + kind + '</span></div>';
      } catch (e) {
        n.innerHTML = '<div class="it"><i></i><span>渲染失败</span></div>';
      }
      n.setAttribute('data-built', '1');
    }
  }
  window.ivizRender = boot;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
