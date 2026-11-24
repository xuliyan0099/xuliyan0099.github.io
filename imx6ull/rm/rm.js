/* RM 逐章解读 · 目录渲染（依赖 rm-data.js）
   首页：renderRMToc('host')
   章节页：renderRMChapter('m1','c01.html')  —— 侧栏 + 上下章 */
(function () {
  var TAG = { read: '通读', table: '查表', opt: '选读' };

  function fmt(n) { return n < 10 ? '0' + n : '' + n; }
  function rmId(n) { return n === 'A' ? 'RM-A' : 'RM' + fmt(n); }
  function allChapters() {
    var out = [];
    for (var i = 0; i < window.RM.parts.length; i++) {
      var p = window.RM.parts[i];
      for (var j = 0; j < p.chapters.length; j++) {
        var c = p.chapters[j];
        c._pid = p.id;
        c._pno = p.no;
        c._ptitle = p.title;
        out.push(c);
      }
    }
    var a = window.RM.appendix;
    a._pid = 'm7'; a._pno = '七'; a._ptitle = '安全、调试与杂项';
    out.push(a);
    return out;
  }
  function fileOf(c) { return c.f || (typeof c.n === 'number' ? 'c' + fmt(c.n) + '.html' : 'ca.html'); }

  function row(c, showBatch) {
    var mark = '<span class="rmark ' + c.pri + '">' + TAG[c.pri] + '</span>';
    var meta = c.en + ' · p' + c.pp + ' · ' + c.pages + ' 页' + (showBatch && c.batch ? ' · 第' + c.batch + '批' : '');
    var inner =
      '<span class="rn">' + rmId(c.n) + '</span>' +
      '<span class="rt2"><b>' + c.zh + '</b>' +
      '<span class="ren">' + meta + '</span>' +
      '<span class="rline">' + c.line + '</span>' +
      (c.pts ? '<span class="rpts">' + c.pts.map(function (x) { return '· ' + x; }).join('<br>') + '</span>' : '') +
      '</span>' + mark;
    if (c.ready) return '<li class="rmrow"><a href="' + fileOf(c) + '">' + inner + '</a></li>';
    return '<li class="rmrow pending"><div>' + inner + '<span class="rst">筹备中</span></div></li>';
  }

  window.renderRMToc = function (hostId) {
    var host = document.getElementById(hostId);
    if (!host) return;
    var html = '', totalReady = 0, totalPages = 0;
    for (var i = 0; i < window.RM.parts.length; i++) {
      var p = window.RM.parts[i];
      var pages = 0, ready = 0;
      for (var j = 0; j < p.chapters.length; j++) {
        pages += p.chapters[j].pages;
        if (p.chapters[j].ready) ready++;
      }
      totalPages += pages; totalReady += ready;
      html += '<section class="rm-part" id="' + p.id + '">' +
        '<div class="rm-head"><span class="pk">第' + p.no + '篇</span><h2>' + p.title +
        '<small>' + p.en + '</small></h2><span class="pc">' + p.chapters.length + ' 章 · ' + pages +
        ' 页 · ' + ready + ' 已上线</span></div>' +
        '<p class="pl">' + p.intro + '</p><p class="psub">' + p.sub + '</p>' +
        '<ol class="rm-list">';
      for (var k = 0; k < p.chapters.length; k++) html += row(p.chapters[k], false);
      html += '</ol></section>';
    }
    var a = window.RM.appendix;
    totalPages += a.pages;
    html += '<section class="rm-part" id="rmA"><div class="rm-head"><span class="pk">附录</span>' +
      '<h2>附录 A<small>' + a.en + '</small></h2><span class="pc">' + a.pages + ' 页</span></div>' +
      '<ol class="rm-list">' + row(a, false) + '</ol></section>';
    host.innerHTML = html;

    var s;
    s = document.querySelectorAll('[data-rm-stat="chapters"]');
    for (var x = 0; x < s.length; x++) s[x].textContent = '60 + 附录 A';
    s = document.querySelectorAll('[data-rm-stat="pages"]');
    for (var y = 0; y < s.length; y++) s[y].textContent = totalPages + ' 页';
    s = document.querySelectorAll('[data-rm-stat="ready"]');
    for (var z = 0; z < s.length; z++) s[z].textContent = totalReady + ' / 60';
  };

  window.renderRMChapter = function (pid, curFile) {
    var p = null;
    for (var i = 0; i < window.RM.parts.length; i++) if (window.RM.parts[i].id === pid) p = window.RM.parts[i];
    if (!p) return;
    var list = document.getElementById('sideList');
    if (list) {
      var html = '';
      for (var j = 0; j < p.chapters.length; j++) {
        var c = p.chapters[j];
        var f = fileOf(c);
        if (!c.ready) {
          html += '<li class="pending"><span class="no">' + rmId(c.n) + '</span><span>' + c.zh +
            '<span class="sub">筹备中</span></span></li>';
        } else {
          html += '<li><a href="' + f + '"' + (f === curFile ? ' class="active"' : '') +
            '><span class="no">' + rmId(c.n) + '</span><span>' + c.zh +
            '<span class="sub">' + c.en + '</span></span></a></li>';
        }
      }
      list.innerHTML = html;
    }
    var all = allChapters(), iCur = -1, k;
    for (k = 0; k < all.length; k++) if (fileOf(all[k]) === curFile) iCur = k;
    var prev = null, next = null;
    for (k = iCur - 1; k >= 0; k--) if (all[k].ready) { prev = all[k]; break; }
    for (k = iCur + 1; k < all.length; k++) if (all[k].ready) { next = all[k]; break; }
    var nav = document.getElementById('volNav');
    if (nav) {
      nav.innerHTML =
        (prev ? '<a href="' + fileOf(prev) + '">← ' + rmId(prev.n) + ' ' + prev.zh + '</a>' : '<a href="index.html">☰ 计划目录</a>') +
        (next ? '<a href="' + fileOf(next) + '">' + rmId(next.n) + ' ' + next.zh + ' →</a>' : '<a href="index.html">☰ 计划目录</a>');
    }
    var cn = document.getElementById('chNavNext');
    if (cn) {
      if (next) { cn.href = fileOf(next); cn.innerHTML = '<span>下一章</span><b>' + rmId(next.n) + ' ' + next.zh + ' →</b>'; }
      else { cn.href = 'index.html'; cn.innerHTML = '<span>本卷完</span><b>返回计划目录 →</b>'; }
    }
  };
})();
