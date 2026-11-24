/* 设计模式全书 · 左栏整书目录：四篇 25 章全部列出，当前章展开小节 */
(function () {
  'use strict';

  function curFile() {
    var seg = location.pathname.split('/');
    var f = seg[seg.length - 1];
    return f && f.indexOf('.html') > 0 ? f : 'index.html';
  }
  function curPart() {
    var seg = location.pathname.split('/');
    return seg.length > 1 ? seg[seg.length - 2] : '';
  }
  function hashPart() {
    var h = location.hash.replace('#', '');
    return h === 'p1' || h === 'p2' || h === 'p3' || h === 'p4' ? h : '';
  }

  window.dpNav = function (partId) {
    var parts = window.DP_PARTS || [];
    if (!parts.length) return;

    var file = curFile();
    var pid = partId || curPart() || hashPart();
    var active = null;
    parts.forEach(function (p) {
      p.chapters.forEach(function (c) { if (p.id === pid && c.f === file) active = c; });
    });

    var head = document.getElementById('sideHead');
    if (head) head.innerHTML = '设计模式全书 · 25 章<label for="navChk" class="nav-x" aria-label="收起目录">✕</label>';

    var list = document.getElementById('sideList');
    if (list) {
      list.innerHTML = '';
      parts.forEach(function (p) {
        var ph = document.createElement('li');
        ph.className = 'part-h';
        var pidx = 'index.html#' + p.id;
        ph.innerHTML = '<a href="' + (file === 'index.html' ? pidx : '../index.html#' + p.id) + '">' +
          '篇' + p.no + '<b>' + p.title + '</b><i>' + p.chapters.length + '</i></a>';
        list.appendChild(ph);

        p.chapters.forEach(function (c) {
          var li = document.createElement('li');
          var a = document.createElement('a');
          a.href = (p.id === pid && file !== 'index.html') ? c.f : '../' + p.id + '/' + c.f;
          if (file === 'index.html') a.href = p.id + '/' + c.f;
          a.innerHTML = '<span class="no">' + c.n + '</span><span>' + c.t +
            '<span class="sub">' + c.s + '</span></span>';
          var isActive = active && c === active;
          if (isActive) a.className = 'active';
          li.appendChild(a);
          if (isActive) {
            var sub = document.createElement('ol');
            sub.className = 'side-sub';
            c.sec.forEach(function (t, i) {
              var sli = document.createElement('li');
              var sa = document.createElement('a');
              sa.href = '#s' + (i + 1);
              sa.innerHTML = '<i>' + ('0' + (i + 1)).slice(-2) + '</i>' + t;
              sli.appendChild(sa);
              sub.appendChild(sli);
            });
            li.appendChild(sub);
          }
          list.appendChild(li);
        });
      });
    }

    var flat = [];
    parts.forEach(function (p) { p.chapters.forEach(function (c) { flat.push({ pid: p.id, n: c.n, f: c.f, t: c.t }); }); });
    var gi = -1;
    flat.forEach(function (c, i) { if (c.pid === pid && c.f === file) gi = i; });
    var prev = gi > 0 ? flat[gi - 1] : null;
    var next = gi > -1 && gi < flat.length - 1 ? flat[gi + 1] : null;

    var vol = document.getElementById('volNav');
    if (vol && gi > -1) {
      var base = '../';
      vol.innerHTML = (prev
        ? '<a href="' + base + prev.pid + '/' + prev.f + '">← ' + prev.n + '</a>'
        : '<a href="../index.html">← 目录</a>') +
        (next ? '<a class="nx" href="' + base + next.pid + '/' + next.f + '">' + next.n + ' →</a>'
              : '<a class="nx" href="../index.html">目录 →</a>');
    }

    var cn = document.getElementById('chNav');
    if (cn && gi > -1) {
      var bh = '';
      bh += '<a href="' + (prev ? '../' + prev.pid + '/' + prev.f : '../index.html') + '"><span>' +
        (prev ? '上一章' : '返回') + '</span><b>' + (prev ? '← ' + prev.n + ' ' + prev.t : '← 全书目录') + '</b></a>';
      bh += '<a class="nx" href="' + (next ? '../' + next.pid + '/' + next.f : '../index.html') + '"><span>' +
        (next ? '下一章' : 'END') + '</span><b>' + (next ? next.n + ' ' + next.t + ' →' : '读完 · 回到全书目录') + '</b></a>';
      cn.innerHTML = bh;
    }
  };

  window.dpToc = function () {
    var host = document.getElementById('toc');
    if (!host) return;
    var h = '';
    (window.DP_PARTS || []).forEach(function (p) {
      var total = p.chapters.reduce(function (a, c) { return a + c.min; }, 0);
      h += '<div class="part-block" id="' + p.id + '">' +
        '<div class="part-head2"><h2>' + p.no + '　' + p.title + '</h2>' +
        '<span class="pk">PART ' + p.no + '</span>' +
        '<span class="pc">' + p.chapters.length + ' 章 · 约 ' + total + ' 分钟</span></div>' +
        '<p class="pl">' + p.intro + '</p><div class="chlist">';
      p.chapters.forEach(function (c) {
        h += '<a class="chrow" href="' + p.id + '/' + c.f + '">' +
          '<span class="cn">' + c.n + '</span>' +
          '<span class="ct"><b>' + c.t + '</b><i>' + c.s + '</i></span>' +
          '<span class="cm">' + c.min + ' 分钟</span><span class="ca">→</span></a>';
      });
      h += '</div></div>';
    });
    host.innerHTML = h;
  };
})();
