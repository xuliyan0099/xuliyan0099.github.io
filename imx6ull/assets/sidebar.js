/* =====================================================================
   sidebar.js · 左栏唯一渲染器
   读 assets/catalog.js，把 <aside id="sidebar"> 的内容全部生成出来。
   页面里只需：<aside id="sidebar" data-root="../" data-page="docs/xxx.html"></aside>
   卷页用 data-vol="07"。加一条新篇 = 改 catalog.js，不动任何页面。
   ===================================================================== */
(function () {
  'use strict';

  var C = window.CATALOG;
  if (!C) { console.warn('[sidebar] catalog.js 未加载，左栏为空'); return; }

  var GN = {};                       /* 体裁 key -> 定义 */
  C.groups.forEach(function (g) { GN[g.key] = g; });

  var aside = document.getElementById('sidebar');
  if (!aside) return;

  var page = aside.getAttribute('data-page') || '';
  var root = aside.getAttribute('data-root') || '../';
  var volHint = aside.getAttribute('data-vol') || '';

  /* ---------- 模式 A：卷清单（juan/index.html） ---------- */
  if ((aside.getAttribute('data-mode') || '') === 'vols') {
    var rows = ['<div class="vol-h">十四卷 · 逐卷进入</div>'];
    C.volumes.forEach(function (v) {
      var n = 0;
      v.groups.forEach(function (g) { n += g.items.length; });
      rows.push('<li><a href="j' + v.id + '.html">' +
        '<span class="no">' + v.id + '</span>' +
        '<span>' + v.title + '<span class="sub">' + n + ' 篇 · 读 ' + v.read + 'h · 做 ' + v.work + 'h</span></span></a></li>');
    });
    aside.innerHTML = rows[0] + '<ol>' + rows.slice(1).join('\n') + '</ol>' +
      '<div class="vol-nav"><a href="../index.html">⌂ 学习站入口</a>' +
      '<a href="../sitemap.html">全部页面</a></div>';
    return;
  }

  /* ---------- 定位当前卷 / 当前篇 ---------- */
  var volIdx = -1, itemIdx = 0, allIdx = -1, nRun = 0;

  C.volumes.forEach(function (v, vi) {
    var inVol = 0;
    v.groups.forEach(function (g) {
      g.items.forEach(function (it) {
        nRun++; inVol++;
        if (page && it.f === page) { volIdx = vi; itemIdx = inVol; allIdx = nRun; }
      });
    });
  });

  if (volIdx < 0) {
    /* 卷页：按 data-vol 找，找不到就按文件名 jNN.html 推 */
    var m = /j(\d\d)\.html$/i.exec(location.pathname);
    var want = volHint || (m ? m[1] : '');
    C.volumes.forEach(function (v, vi) { if (v.id === want) volIdx = vi; });
  }
  if (volIdx < 0) volIdx = 0;

  var V = C.volumes[volIdx];

  /* ---------- 小工具 ---------- */
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function sumH(items) { var s = 0; items.forEach(function (i) { s += i.h; }); return s; }
  function pagesOf(v) { var n = 0; v.groups.forEach(function (g) { n += g.items.length; }); return n; }

  /* ---------- 组内容 ---------- */
  var parts = [];

  parts.push('<div class="vol-h">卷 ' + V.id + ' · ' + esc(V.title) + '</div>');
  parts.push('<div class="vol-stat">' + pagesOf(V) + ' 篇 · 读 ' + V.read + 'h · 做 ' + V.work + 'h</div>');

  if (allIdx > 0) {
    parts.push('<div class="vol-stat now">第 ' + itemIdx + ' 篇 · 全站 ' + allIdx + ' / ' + C.total + '</div>');
  }

  V.groups.forEach(function (g) {
    var items = g.items, meta = GN[g.key] || { name: g.key };
    parts.push('<div class="grp grp-' + g.key + '">');
    parts.push('<div class="grp-h">' + esc(meta.name) +
      '<em>' + items.length + ' 篇 · 约 ' + sumH(items) + ' 小时</em></div>');
    parts.push('<ol>');

    items.forEach(function (it) {
      var active = page && it.f === page;
      var cls = it.p ? ' class="pair"' : '';
      var link = root + it.f;
      var sub = '约 ' + it.h + ' 小时';

      /* 配对项：把「补 XX.XX」写进 sub，标题不再重复 */
      if (it.p) sub = '↳ 补 ' + it.p;
      if (active) sub += ' · 当前';

      parts.push('<li' + cls + '><a href="' + esc(link) + '"' +
        (active ? ' class="active"' : '') + '>' +
        '<span class="no">' + it.n + '</span>' +
        '<span>' + esc(it.t) + '<span class="sub">' + esc(sub) + '</span></span></a></li>');
    });

    parts.push('</ol></div>');
  });

  /* ---------- 卷间跳转 ---------- */
  var prev = C.volumes[volIdx - 1], next = C.volumes[volIdx + 1];
  parts.push('<div class="vol-nav">');
  if (prev) {
    parts.push('<a href="' + root + 'juan/j' + prev.id + '.html">← 卷 ' + prev.id + '</a>');
  } else {
    parts.push('<a href="' + root + 'juan/index.html">☰ 总览</a>');
  }
  parts.push('<a href="' + root + 'juan/j' + V.id + '.html">本卷</a>');
  if (next) {
    parts.push('<a href="' + root + 'juan/j' + next.id + '.html">卷 ' + next.id + ' →</a>');
  } else {
    parts.push('<a href="' + root + 'juan/index.html">总览</a>');
  }
  parts.push('</div>');

  aside.innerHTML = parts.join('\n');
})();
