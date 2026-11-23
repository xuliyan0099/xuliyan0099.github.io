/* ===== 可视化组件库 · viz.js =====
   用法：页面里写一个空 div，带 data-kind 与 data-json 即可自动渲染。
   <div class="viz" data-kind="bits" data-title="CCM_CCGR1 位域" data-json='{...}'></div>
   支持 kind：bits / flow / tree / seq / map / stack / bars
*/
(function () {
  'use strict';

  var COLOR = { cy:'vz-c-cy', vi:'vz-c-vi', or:'vz-c-or', gr:'vz-c-gr', rd:'vz-c-rd', gray:'vz-c-gray' };
  var FILL = {
    cy:'linear-gradient(180deg,rgba(61,219,217,.45),rgba(61,219,217,.20))',
    vi:'linear-gradient(180deg,rgba(139,123,255,.45),rgba(139,123,255,.20))',
    or:'linear-gradient(180deg,rgba(255,179,92,.45),rgba(255,179,92,.20))',
    gr:'linear-gradient(180deg,rgba(92,225,160,.45),rgba(92,225,160,.20))',
    rd:'linear-gradient(180deg,rgba(255,107,129,.45),rgba(255,107,129,.20))',
    gray:'rgba(255,255,255,.10)'
  };

  function mk(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  /* ---------- 外壳 ---------- */
  function shell(host, title, sub) {
    var head = mk('div', 'vz-t');
    head.appendChild(mk('i'));
    var t = mk('span', null, title || '');
    head.appendChild(t);
    if (sub) head.appendChild(mk('em', null, sub));
    host.appendChild(head);
    var body = mk('div', 'vz-body');
    host.appendChild(body);
    return body;
  }

  function note(host, text) {
    if (text) host.appendChild(mk('p', 'vz-note', text));
  }

  /* ---------- bits：寄存器位域 ---------- */
  function renderBits(host, d) {
    var wrap = mk('div', 'vz-bits');
    var row = mk('div', 'vz-bitrow');
    var fields = d.fields || [];
    var w = d.w || 32;
    /* 按 lo 从高到低排（MSB 在左） */
    var parts = fields.slice().sort(function (a, b) { return b.hi - a.hi; });
    var cursor = w - 1;
    parts.forEach(function (f, fi) {
      if (f.hi < cursor) {
        /* 补空缺 */
        var gapBits = cursor - f.hi;
        var g = mk('div', 'seg vz-c-gray');
        g.style.flex = gapBits + ' 0 0';
        g.appendChild(mk('b', null, '—'));
        g.appendChild(mk('s', null, '保留'));
        row.appendChild(g);
      }
      var bits = f.hi - f.lo + 1;
      var seg = mk('div', 'seg ' + (COLOR[f.c] || 'vz-c-gray'));
      seg.style.flex = bits + ' 0 0';
      seg.style.animationDelay = (fi * 0.42) + 's';
      seg.title = (f.n || '') + ' 位 ' + f.hi + ':' + f.lo + (f.t ? ' — ' + f.t : '');
      seg.appendChild(mk('b', null, f.n || ''));
      var range = (f.hi === f.lo) ? ('bit ' + f.hi) : (f.hi + ':' + f.lo);
      seg.appendChild(mk('s', null, range));
      row.appendChild(seg);
      cursor = f.lo - 1;
    });
    if (cursor >= 0) {
      var tail = mk('div', 'seg vz-c-gray');
      tail.style.flex = (cursor + 1) + ' 0 0';
      tail.appendChild(mk('b', null, '—'));
      tail.appendChild(mk('s', null, '保留'));
      row.appendChild(tail);
    }
    wrap.appendChild(row);

    var scale = mk('div', 'vz-scale');
    scale.appendChild(mk('span', null, 'bit ' + (w - 1)));
    scale.appendChild(mk('span', null, 'bit 0'));
    wrap.appendChild(scale);
    host.appendChild(wrap);

    if (d.note) note(host, d.note);
  }

  /* ---------- flow：流程条 ---------- */
  function renderFlow(host, d) {
    var wrap = mk('div', 'vz-flow' + (d.still ? '' : ' vz-play'));
    (d.steps || []).forEach(function (s, i) {
      if (i > 0) wrap.appendChild(mk('span', 'arw', '→'));
      var st = mk('div', 'st');
      st.style.animationDelay = (i * 0.45) + 's';
      st.appendChild(mk('b', null, s.n || ''));
      if (s.d) st.appendChild(mk('s', null, s.d));
      wrap.appendChild(st);
    });
    host.appendChild(wrap);
    if (d.note) note(host, d.note);
  }

  /* ---------- tree：层级树 ---------- */
  function renderTree(host, d) {
    var root = mk('div', 'vz-tree');
    var ul = mk('ul');
    (d.nodes || []).forEach(function (nd) { ul.appendChild(treeItem(nd)); });
    root.appendChild(ul);
    host.appendChild(root);
    if (d.note) note(host, d.note);
  }

  function treeItem(nd) {
    var li = mk('li');
    var box = mk('span', 'nd ' + (COLOR[nd.c] || ''));
    box.appendChild(mk('b', null, nd.n || ''));
    if (nd.d) box.appendChild(mk('s', null, nd.d));
    li.appendChild(box);
    if (nd.ch && nd.ch.length) {
      var ul = mk('ul');
      nd.ch.forEach(function (c) { ul.appendChild(treeItem(c)); });
      li.appendChild(ul);
    }
    return li;
  }

  /* ---------- seq：时序波形 ---------- */
  function expand(w) {
    /* '1' 高，'0' 低，'.' 表示沿用上一个值 */
    var out = '', prev = '0';
    for (var i = 0; i < w.length; i++) {
      var c = w[i];
      if (c === '.') c = prev;
      out += c; prev = c;
    }
    return out;
  }

  function renderSeq(host, d) {
    var wrap = mk('div', 'vz-seq');
    var slots = d.slots || 24;
    var sigs = d.sigs || [];
    sigs.forEach(function (s) {
      var rowWrap = mk('div');
      rowWrap.appendChild(mk('div', 'lbl', s.n || ''));
      var wave = mk('div', 'vz-wave');
      var str = expand(s.w || '');
      if (str.length < slots) {
        /* 循环填充到 slots */
        var rep = '';
        while (rep.length < slots) rep += str;
        str = rep.slice(0, slots);
      } else {
        str = str.slice(0, slots);
      }
      var i = 0;
      while (i < str.length) {
        var v = str[i], j = i;
        while (j < str.length && str[j] === v) j++;
        var seg = mk('div', 'hi');
        seg.style.left = (i / slots * 100) + '%';
        seg.style.width = ((j - i) / slots * 100) + '%';
        if (v === '1') {
          seg.style.background = FILL[s.c || 'cy'];
          seg.style.top = '7px';
          seg.style.height = '20px';
        } else {
          seg.style.background = 'rgba(255,255,255,.10)';
          seg.style.top = '26px';
          seg.style.height = '4px';
        }
        wave.appendChild(seg);
        i = j;
      }
      if (s.note) {
        var t = mk('span', 'tx', s.note);
        wave.appendChild(t);
      }
      if (d.scan !== false) {
        var sc = mk('div', 'vz-scan');
        wave.appendChild(sc);
      }
      if (d.marker != null && d.marker >= 0) {
        var cu = mk('div', 'vz-cursor');
        cu.style.left = (d.marker / slots * 100) + '%';
        wave.appendChild(cu);
      }
      rowWrap.appendChild(wave);
      wrap.appendChild(rowWrap);
    });
    host.appendChild(wrap);
    if (d.note) note(host, d.note);
  }

  /* ---------- map：地址 / 内存映射 ---------- */
  function renderMap(host, d) {
    var wrap = mk('div', 'vz-map');
    (d.rows || []).forEach(function (r) {
      var row = mk('div', 'vz-maprow');
      var total = 0;
      r.segs.forEach(function (s) { total += (s.size || 1); });
      r.segs.forEach(function (s) {
        var seg = mk('div', 'mseg ' + (COLOR[s.c] || 'vz-c-gray'));
        seg.style.flex = (s.size || 1) + ' 0 0';
        seg.appendChild(mk('b', null, s.n || ''));
        if (s.d) seg.appendChild(mk('s', null, s.d));
        row.appendChild(seg);
      });
      if (r.ptr != null && total > 0) {
        var ptr = mk('div', 'vz-ptr');
        ptr.style.left = (r.ptr * 100) + '%';
        row.appendChild(ptr);
      }
      wrap.appendChild(row);
      if (r.from && r.to) {
        var ad = mk('div', 'vz-addr');
        ad.appendChild(mk('span', null, r.from));
        ad.appendChild(mk('span', null, r.to));
        wrap.appendChild(ad);
      }
    });
    host.appendChild(wrap);
    if (d.note) note(host, d.note);
  }

  /* ---------- stack：栈帧 ---------- */
  function renderStack(host, d) {
    var wrap = mk('div', 'vz-stack');
    (d.frames || []).forEach(function (f, i) {
      var row = mk('div', 'vz-frame');
      row.style.animationDelay = (i * 0.12) + 's';
      row.appendChild(mk('b', null, (i + 1) + '. ' + (f.n || '')));
      if (f.d) row.appendChild(mk('s', null, f.d));
      if (f.sp) row.appendChild(mk('span', 'sp', f.sp));
      wrap.appendChild(row);
    });
    host.appendChild(wrap);
    if (d.spHint) host.appendChild(mk('div', 'vz-sp-arrow', d.spHint));
    if (d.note) note(host, d.note);
  }

  /* ---------- bars：柱状对比 ---------- */
  function renderBars(host, d) {
    var wrap = mk('div', 'vz-bars');
    var max = d.max || 0;
    var items = d.items || [];
    if (!max) items.forEach(function (it) { if (it.v > max) max = it.v; });
    items.forEach(function (it) {
      var row = mk('div', 'vz-bar');
      row.appendChild(mk('span', 'nm', it.n || ''));
      var track = mk('div', 'track');
      var fill = mk('div', 'fill');
      if (it.c && FILL[it.c]) fill.style.background = FILL[it.c];
      track.appendChild(fill);
      row.appendChild(track);
      row.appendChild(mk('span', 'v', (it.v || 0) + (it.unit || '')));
      wrap.appendChild(row);
      setTimeout(function () {
        fill.style.width = (max ? Math.max(2, (it.v / max) * 100) : 0) + '%';
      }, 60);
    });
    host.appendChild(wrap);
    if (d.note) note(host, d.note);
  }

  /* ---------- timeline：横向时间线（流光自动跑） ---------- */
  var STROKE = {
    cy: '#3ddbd9', vi: '#8b7bff', or: '#ffb35c', gr: '#5ce1a0', rd: '#ff6b81', gray: '#8894ad'
  };
  function renderTimeline(host, d) {
    var wrap = mk('div', 'vz-tl');
    wrap.appendChild(mk('div', 'vz-tl-line'));
    var run = mk('div', 'vz-tl-run');
    wrap.appendChild(run);
    (d.items || []).forEach(function (it, i) {
      var node = mk('div', 'vz-tln ' + (i % 2 ? 'down' : 'up'));
      node.style.animationDelay = (i * 0.22) + 's';
      var dot = mk('div', 'vz-tl-dot');
      dot.style.background = STROKE[it.c] || STROKE.cy;
      dot.style.boxShadow = '0 0 14px ' + (STROKE[it.c] || STROKE.cy);
      node.appendChild(dot);
      var box = mk('div', 'vz-tl-box');
      box.appendChild(mk('b', null, it.t || ''));
      if (it.n) box.appendChild(mk('span', null, it.n));
      if (it.d) box.appendChild(mk('s', null, it.d));
      node.appendChild(box);
      wrap.appendChild(node);
    });
    host.appendChild(wrap);
    if (d.note) note(host, d.note);
  }

  /* ---------- compare：错误 / 正确两列对照 ---------- */
  function renderCompare(host, d) {
    var wrap = mk('div', 'vz-cmp');
    [['bad', d.bad, '✗ 常见误解'], ['good', d.good, '✓ 实际情况']].forEach(function (p) {
      var col = mk('div', 'vz-cmp-col ' + p[0]);
      var head = mk('div', 'vz-cmp-h');
      head.textContent = (p[1] && p[1].t) ? ((p[0] === 'bad' ? '✗ ' : '✓ ') + p[1].t) : p[2];
      col.appendChild(head);
      var ul = mk('ul');
      ((p[1] && p[1].items) || []).forEach(function (s) { ul.appendChild(mk('li', null, s)); });
      col.appendChild(ul);
      wrap.appendChild(col);
    });
    host.appendChild(wrap);
    if (d.note) note(host, d.note);
  }

  /* ---------- matrix：网格矩阵（可高亮单元） ---------- */
  function renderMatrix(host, d) {
    var wrap = mk('div', 'vz-mx');
    var cols = d.cols || [];
    var head = mk('div', 'vz-mx-row head');
    head.appendChild(mk('span', 'nm', d.corner || ''));
    cols.forEach(function (c) { head.appendChild(mk('span', 'cell', c)); });
    wrap.appendChild(head);
    var hl = d.hi || [];
    (d.rows || []).forEach(function (r, ri) {
      var row = mk('div', 'vz-mx-row');
      row.appendChild(mk('span', 'nm', r.n || ''));
      (r.cells || []).forEach(function (c, ci) {
        var cell = mk('span', 'cell ' + (COLOR[(c && c.c) || r.c] || 'vz-c-gray'));
        cell.textContent = (c && c.v != null) ? c.v : (c == null ? '' : c);
        if (hl.length && hl.some(function (p) { return p[0] === ri && p[1] === ci; })) {
          cell.className += ' hit';
        }
        row.appendChild(cell);
      });
      wrap.appendChild(row);
    });
    host.appendChild(wrap);
    if (d.note) note(host, d.note);
  }

  /* ---------- donut：环形占比（描边动画） ---------- */
  function renderDonut(host, d) {
    var items = d.items || [];
    var total = 0;
    items.forEach(function (i) { total += (i.v || 0); });
    var ns = 'http://www.w3.org/2000/svg';
    var wrap = mk('div', 'vz-donut');
    var svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 120 120');
    var R = 46, C = 2 * Math.PI * R, off = 0;
    var t = document.createElementNS(ns, 'circle');
    t.setAttribute('cx', 60); t.setAttribute('cy', 60); t.setAttribute('r', R);
    t.setAttribute('fill', 'none'); t.setAttribute('stroke', 'rgba(255,255,255,.07)');
    t.setAttribute('stroke-width', 15);
    svg.appendChild(t);
    items.forEach(function (it) {
      var v = it.v || 0;
      var seg = document.createElementNS(ns, 'circle');
      seg.setAttribute('cx', 60); seg.setAttribute('cy', 60); seg.setAttribute('r', R);
      seg.setAttribute('fill', 'none');
      seg.setAttribute('stroke', STROKE[it.c] || STROKE.cy);
      seg.setAttribute('stroke-width', 15);
      seg.setAttribute('stroke-dasharray', (C * v / (total || 1)) + ' ' + C);
      seg.setAttribute('stroke-dashoffset', -C * off / (total || 1));
      seg.setAttribute('transform', 'rotate(-90 60 60)');
      svg.appendChild(seg);
      off += v;
    });
    wrap.appendChild(svg);
    var ctr = mk('div', 'vz-donut-c');
    ctr.appendChild(mk('b', null, d.center != null ? d.center : total));
    if (d.unit) ctr.appendChild(mk('s', null, d.unit));
    wrap.appendChild(ctr);
    host.appendChild(wrap);
    var lg = mk('div', 'vz-legend');
    (d.items || []).forEach(function (it) {
      var sp = mk('span');
      var ic = mk('i');
      ic.style.background = STROKE[it.c] || STROKE.cy;
      sp.appendChild(ic);
      sp.appendChild(document.createTextNode((it.n || '') + ' ' + (it.v || 0) + (d.unit || '')));
      lg.appendChild(sp);
    });
    host.appendChild(lg);
    if (d.note) note(host, d.note);
  }

  /* ---------- pipe：流水线（光点循环跑） ---------- */
  function renderPipe(host, d) {
    var wrap = mk('div', 'vz-pipe');
    (d.stages || []).forEach(function (s, i) {
      if (i > 0) wrap.appendChild(mk('span', 'vz-pipe-arw', '▶'));
      var st = mk('div', 'vz-pipe-st ' + (COLOR[s.c] || ''));
      st.appendChild(mk('b', null, s.n || ''));
      if (s.d) st.appendChild(mk('s', null, s.d));
      wrap.appendChild(st);
    });
    wrap.appendChild(mk('div', 'vz-pipe-dot'));
    host.appendChild(wrap);
    if (d.note) note(host, d.note);
  }

  /* ---------- layers：分层堆叠（自底向上浮入） ---------- */
  function renderLayers(host, d) {
    var wrap = mk('div', 'vz-layers');
    (d.items || []).forEach(function (it, i) {
      var row = mk('div', 'vz-layer ' + (COLOR[it.c] || ''));
      row.style.animationDelay = (i * 0.12) + 's';
      row.appendChild(mk('b', null, it.n || ''));
      if (it.d) row.appendChild(mk('s', null, it.d));
      wrap.appendChild(row);
    });
    host.appendChild(wrap);
    if (d.note) note(host, d.note);
  }

  /* ---------- 渲染入口 ---------- */
  var RENDER = {
    bits: renderBits, flow: renderFlow, tree: renderTree,
    seq: renderSeq, map: renderMap, stack: renderStack, bars: renderBars,
    timeline: renderTimeline, compare: renderCompare, matrix: renderMatrix,
    donut: renderDonut, pipe: renderPipe, layers: renderLayers
  };

  function renderAll() {
    var nodes = document.querySelectorAll('.viz[data-kind]');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.dataset.rendered) continue;
      var kind = el.dataset.kind;
      var fn = RENDER[kind];
      if (!fn) continue;
      var data = {};
      try {
        data = JSON.parse(el.dataset.json || '{}');
      } catch (e) {
        el.appendChild(mk('p', 'vz-note', '数据解析失败：' + e.message));
        continue;
      }
      var body = shell(el, el.dataset.title || '', el.dataset.sub || '');
      fn(body, data);
      el.dataset.rendered = '1';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderAll);
  } else {
    renderAll();
  }
  window.vizRender = renderAll;
})();
