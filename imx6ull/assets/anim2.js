/* ============================================================
   anim2.js · 章节机制动画（anime.js v4 编排 + SVG 结构化演出）
   数据契约：
   <div class="anim2" data-json='{
     "title":"…","hint":"…","kind":"flow|stack|chain|split",
     "nodes":[{"k":"节点名","s":"一句话"}],
     "frames":[{"i":0,"d":"这一帧发生了什么"}]
   }'></div>
   ============================================================ */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';

  function mk(t, a) {
    const e = document.createElementNS(NS, t);
    if (a) { for (const k in a) e.setAttribute(k, a[k]); }
    return e;
  }
  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function cut(s, n) {
    s = String(s || '');
    return s.length > n ? s.slice(0, n - 1) + '…' : s;
  }
  function anim() { return (window.anime && typeof window.anime.animate === 'function') ? window.anime : null; }

  /* 量文字宽度，节点宽度跟着文字走，避免大框里漂着四个字 */
  var _mc = null;
  function tw(s) {
    if (!_mc) { _mc = document.createElement('canvas').getContext('2d'); }
    _mc.font = '600 14.5px "Noto Sans SC", "PingFang SC", system-ui, sans-serif';
    return _mc.measureText(String(s || '')).width;
  }

  /* 节点坐标：wide 单行/两行蛇形；narrow 单列纵向；stack 宽屏也纵向堆叠 */
  function positions(n, W, narrow, kind, ww) {
    const items = [];
    if (narrow || (kind === 'stack' && !narrow)) {
      const gap = narrow ? 84 : (kind === 'stack' ? 88 : 68), top = narrow ? 36 : 32;
      for (let i = 0; i < n; i++) items.push({ x: W / 2, y: top + i * gap, row: i });
      return { items: items, H: top + n * gap + 12, narrow: true, per: 1 };
    }
    const rows = ((kind === 'split' && n > 1) || n > 4) ? 2 : 1;
    const per = rows === 1 ? n : Math.ceil(n / 2);
    const H = rows === 1 ? 216 : 252;
    const cnt = rows === 1 ? n : per;
    const gap = cnt > 1 ? Math.min(96, Math.max(44, (W - 120 - cnt * ww) / (cnt - 1))) : 0;
    const span = cnt * ww + (cnt - 1) * gap;
    const x0 = (W - span) / 2 + ww / 2;
    for (let i = 0; i < n; i++) {
      if (rows === 1) { items.push({ x: x0 + i * (ww + gap), y: H / 2, row: 0 }); }
      else {
        const row = i < per ? 0 : 1;
        const col = row === 0 ? i : (kind === 'chain' ? (n - 1 - i) : (i - per));
        const rowCnt = row === 0 ? per : n - per;
        const rGap = rowCnt > 1 ? Math.min(96, Math.max(44, (W - 120 - rowCnt * ww) / (rowCnt - 1))) : 0;
        const rSpan = rowCnt * ww + (rowCnt - 1) * rGap;
        const rx0 = (W - rSpan) / 2 + ww / 2;
        items.push({ x: rx0 + col * (ww + rGap), y: row === 0 ? 84 : 172, row: row });
      }
    }
    return { items: items, H: H, narrow: false, per: per, rows: rows };
  }

  function build(root) {
    let d;
    try { d = JSON.parse(root.getAttribute('data-json')); } catch (e) { return; }
    if (!d || !d.nodes || !d.nodes.length) return;

    root.classList.add('an2');
    root.setAttribute('tabindex', '0');
    root.innerHTML =
      '<div class="an2-head"><span class="an2-badge">动画演示</span>' +
      '<b class="an2-title">' + (d.title || '机制走向') + '</b>' +
      '<span class="an2-hint">' + (d.hint || '') + '</span></div>' +
      '<div class="an2-stage"></div>' +
      '<div class="an2-cap"><span class="an2-step"></span><p class="an2-desc"></p></div>' +
      '<div class="an2-ctl">' +
      '<button class="an2-btn" type="button" data-a="prev">◀ 上一帧</button>' +
      '<button class="an2-btn pri" type="button" data-a="play">▶ 播放</button>' +
      '<button class="an2-btn" type="button" data-a="next">下一帧 ▶</button>' +
      '<button class="an2-btn" type="button" data-a="replay">↺ 重播</button>' +
      '<span class="an2-speed">速度<select data-a="speed"><option value="0.7">0.7×</option>' +
      '<option value="1" selected>1×</option><option value="1.5">1.5×</option></select></span>' +
      '<div class="an2-dots"></div></div>';

    const stage = root.querySelector('.an2-stage');
    const descEl = root.querySelector('.an2-desc');
    const stepEl = root.querySelector('.an2-step');
    const dotsEl = root.querySelector('.an2-dots');
    const svg = mk('svg', { class: 'an2-svg', preserveAspectRatio: 'xMidYMid meet' });
    const pkt = mk('circle', { r: '5', class: 'an2-pkt' });
    stage.appendChild(svg);

    const n = d.nodes.length, frames = d.frames || [];
    let nodes = [], edges = [], an = null, narrow = false, W = 1000;
    const state = { i: 0, playing: false, speed: 1, timer: null, pktAnim: null };

    dotsEl.innerHTML = frames.map(function (_, k) {
      return '<button class="an2-dot" type="button" data-k="' + k + '" title="跳到第 ' + (k + 1) + ' 帧"></button>';
    }).join('');

    function draw(withFade) {
      narrow = window.innerWidth <= 900;
      W = narrow ? 520 : 1000;
      const h = narrow ? 54 : 50;
      const isStack = d.kind === 'stack' && !narrow;
      let wMax = 0;
      d.nodes.forEach(function (nd) { wMax = Math.max(wMax, tw(nd.k) + 46); });
      const wNode = isStack ? Math.min(440, W - 320)
        : (narrow ? Math.min(300, W - 60) : clamp(wMax, 104, 172));
      const P = positions(n, W, narrow, d.kind, wNode);
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + P.H);
      svg.innerHTML = '';
      nodes = []; edges = [];

      const gE = mk('g'), gN = mk('g'), gP = mk('g');
      for (let i = 0; i < n - 1; i++) {
        const a = P.items[i], b = P.items[i + 1];
        let path;
        if (a.x === b.x) {
          /* 同一列：直接竖线 */
          path = 'M ' + a.x + ' ' + (a.y + h / 2) + ' L ' + b.x + ' ' + (b.y - h / 2);
        } else if (a.row === b.row) {
          /* 同一行：直接横线 */
          const ax = b.x > a.x ? a.x + wNode / 2 : a.x - wNode / 2;
          const bx = b.x > a.x ? b.x - wNode / 2 : b.x + wNode / 2;
          path = 'M ' + ax + ' ' + a.y + ' L ' + bx + ' ' + b.y;
        } else {
          /* 换行：竖—横—竖的正交折线，像工程图的水管 */
          const sx = a.x, sy = a.y + h / 2, tx = b.x, ty = b.y - h / 2, my = (sy + ty) / 2;
          path = 'M ' + sx + ' ' + sy + ' L ' + sx + ' ' + my + ' L ' + tx + ' ' + my + ' L ' + tx + ' ' + ty;
        }
        const p = mk('path', { d: path, class: 'an2-edge', 'stroke-linecap': 'round' });
        gE.appendChild(p);
        edges.push(p);
      }

      P.items.forEach(function (a, i) {
        const nd = d.nodes[i];
        const g = mk('g', { class: 'an2-node' });
        g.style.transformBox = 'fill-box';
        g.style.transformOrigin = 'center';
        const r = mk('rect', {
          x: a.x - wNode / 2, y: a.y - h / 2, width: wNode, height: h, rx: '13'
        });
        const t1 = mk('text', {
          x: a.x, y: a.y, 'text-anchor': 'middle', class: 'an2-k'
        });
        t1.setAttribute('dominant-baseline', 'middle');
        t1.textContent = nd.k;
        g.appendChild(r); g.appendChild(t1);
        gN.appendChild(g);
        nodes.push({ g: g, r: r });
      });

      gP.appendChild(pkt);
      svg.appendChild(gE); svg.appendChild(gN); svg.appendChild(gP);

      if (d.kind === 'chain' && !narrow) {
        const axY = P.H - 24;
        const axis = mk('line', { x1: '52', y1: axY, x2: W - 52, y2: axY, class: 'an2-axis' });
        gE.insertBefore(axis, gE.firstChild);
        P.items.forEach(function (a, i) {
          if (a.row !== 0) return;
          const tk = mk('line', { x1: a.x, y1: a.y + h / 2 + 6, x2: a.x, y2: axY, class: 'an2-tick' });
          const tx = mk('text', { x: a.x, y: axY + 15, 'text-anchor': 'middle', class: 'an2-tno' });
          tx.textContent = ('0' + (i + 1)).slice(-2);
          gE.appendChild(tk); gE.appendChild(tx);
        });
      }

      edges.forEach(function (p) {
        const len = p.getTotalLength();
        p.style.setProperty('--len', len.toFixed(1) + 'px');
      });

      an = anim();
      if (an && nodes.length && withFade !== false) {
        try {
          an.animate(nodes.map(function (o) { return o.g; }), {
            opacity: [0, 1], translateY: [8, 0], delay: an.stagger(55), duration: 420, ease: 'out(3)'
          });
        } catch (e1) { }
      }
      applyFrame(state.i, false);
    }

    function dwell() {
      const d0 = (frames[state.i] && frames[state.i].d) || '';
      return clamp(1500 + d0.length * 30, 2100, 4300) / state.speed;
    }

    function runPkt(path, dur) {
      if (!path) return;
      if (state.pktAnim && state.pktAnim.cancel) { try { state.pktAnim.cancel(); } catch (e) { } }
      const len = path.getTotalLength();
      const an2 = anim();
      const place = function (t) {
        const p = path.getPointAtLength(t * len);
        pkt.setAttribute('cx', p.x.toFixed(1));
        pkt.setAttribute('cy', p.y.toFixed(1));
        pkt.style.opacity = t < 0.1 ? (t / 0.1) : (t > 0.9 ? ((1 - t) / 0.1) : 0.95);
      };
      if (an2) {
        const o = { t: 0 };
        try {
          state.pktAnim = an2.animate(o, {
            t: 1, duration: dur, ease: 'inOutSine',
            onUpdate: function () { place(o.t); },
            onComplete: function () { pkt.style.opacity = 0; }
          });
          return;
        } catch (e) { }
      }
      const t0 = performance.now();
      (function loop(now) {
        const t = Math.min(1, (now - t0) / dur);
        place(t);
        if (t < 1) requestAnimationFrame(loop); else pkt.style.opacity = 0;
      })(t0);
    }

    function applyFrame(i, withPkt) {
      i = clamp(i, 0, frames.length ? frames.length - 1 : 0);
      state.i = i;
      nodes.forEach(function (o, k) {
        o.g.classList.toggle('on', k === i);
        o.g.classList.toggle('done', k < i);
      });
      edges.forEach(function (p, k) { p.classList.toggle('on', k < i); });

      const f = frames[i] || {};
      stepEl.innerHTML = '第 <b>' + (i + 1) + '</b> / ' + frames.length + ' 帧';
      descEl.style.opacity = '0';
      descEl.textContent = f.d || '';
      const an2 = anim();
      if (an2) { try { an2.animate(descEl, { opacity: [0, 1], translateY: [6, 0], duration: 260, ease: 'out(2)' }); } catch (e) { descEl.style.opacity = '1'; } }
      else { descEl.style.opacity = '1'; }

      root.style.setProperty('--p', (((frames.length ? i + 1 : 0) / frames.length) * 100).toFixed(1) + '%');
      Array.prototype.forEach.call(dotsEl.children, function (b, k) {
        b.classList.toggle('on', k === i);
        b.classList.toggle('done', k < i);
      });

      pkt.style.opacity = 0;
      if (withPkt && i > 0 && edges[i - 1]) runPkt(edges[i - 1], 640 / state.speed);

      if (withPkt && i === frames.length - 1 && state.playing) { /* 末帧停一拍再循环，由 tick 处理 */ }
      updBtn();
    }

    function updBtn() {
      const b = root.querySelector('[data-a="play"]');
      b.textContent = state.playing ? '⏸ 暂停' : '▶ 播放';
      b.classList.toggle('is-pause', state.playing);
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
      const b = e.target.closest('[data-a],[data-k]');
      if (!b) return;
      const a = b.getAttribute('data-a');
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

    var t = 0, lastW = window.innerWidth;
    window.addEventListener('resize', function () {
      clearTimeout(t);
      t = setTimeout(function () {
        var w = window.innerWidth;
        /* 只有断点真的翻转、且宽度变化足够大才重建，避免平板地址栏抖动反复重绘 */
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

    /* 切到后台就停表，回前台再续，避免平板上切 app 回来重排一次闪屏 */
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { if (state.playing) { stop(); state._hidden = true; } }
      else if (state._hidden) { state._hidden = false; if (state.playing) tick(); }
    });

    draw(true);
    updBtn();
  }

  window.animRender = function () {
    Array.prototype.forEach.call(document.querySelectorAll('.anim2[data-json]'), function (r) {
      if (r.dataset.built === '1') return;
      /* 单页版里只构建当前可见的那一页，避免一次性创建几十个 SVG 拖垮平板 */
      var sec = r.closest && r.closest('section.lesson');
      if (sec && sec.hasAttribute('hidden')) return;
      build(r);
      r.dataset.built = '1';
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', window.animRender);
  else window.animRender();
})();
