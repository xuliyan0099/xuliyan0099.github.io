/* 硬件篇导航渲染：侧栏 + 篇末上下章 + 总目录。依赖 parts.js。 */
(function () {
  function partById(id) {
    for (var i = 0; i < window.PARTS.length; i++) if (window.PARTS[i].id === id) return window.PARTS[i];
    return null;
  }

  window.renderPart = function (pid, curFile) {
    var p = partById(pid);
    if (!p) return;
    var list = document.getElementById('sideList');
    if (list) {
      var html = '';
      for (var i = 0; i < p.chapters.length; i++) {
        var c = p.chapters[i];
        if (!c.ready) {
          html += '<li class="pending"><span class="no">' + c.n + '</span><span>' + c.t +
            '<span class="sub">筹备中</span></span></li>';
        } else {
          html += '<li><a href="' + c.f + '"' + (c.f === curFile ? ' class="active"' : '') +
            '><span class="no">' + c.n + '</span><span>' + c.t +
            '<span class="sub">' + c.s + '</span></span></a></li>';
        }
      }
      list.innerHTML = html;
    }

    /* 篇末 / 侧栏底部：上一篇、下一篇（只在本篇已上线的章之间跳） */
    var iCur = -1;
    for (var k = 0; k < p.chapters.length; k++) if (p.chapters[k].f === curFile) iCur = k;
    var prev = null, next = null;
    if (iCur >= 0) {
      for (var a = iCur - 1; a >= 0; a--) if (p.chapters[a].ready) { prev = p.chapters[a]; break; }
      for (var b = iCur + 1; b < p.chapters.length; b++) if (p.chapters[b].ready) { next = p.chapters[b]; break; }
    }
    var nav = document.getElementById('volNav');
    if (nav) {
      nav.innerHTML =
        (prev ? '<a href="' + prev.f + '">← ' + prev.n + ' ' + prev.t + '</a>' : '<a href="../index.html">☰ 篇目录</a>') +
        (next ? '<a href="' + next.f + '">' + next.n + ' ' + next.t + ' →</a>' : '<a href="../index.html">☰ 篇目录</a>');
    }
    var cn = document.getElementById('chNavNext');
    if (cn) {
      if (next) { cn.href = next.f; cn.innerHTML = '<span>下一章</span><b>' + next.n + ' ' + next.t + ' →</b>'; }
      else { cn.href = '../index.html'; cn.innerHTML = '<span>本篇完</span><b>返回篇目录 →</b>'; }
    }
  };

  /* 总目录：hardware/index.html 用 */
  window.renderIndex = function (hostId) {
    var host = document.getElementById(hostId);
    if (!host) return;
    var html = '';
    for (var i = 0; i < window.PARTS.length; i++) {
      var p = window.PARTS[i];
      var readyN = 0;
      for (var j = 0; j < p.chapters.length; j++) if (p.chapters[j].ready) readyN++;
      html += '<section class="part-block" id="' + p.id + '">' +
        '<div class="part-head2"><span class="pk">第' + p.no + '篇</span>' +
        '<h2>' + p.title + '</h2><span class="pc">' + readyN + ' / ' + p.chapters.length + ' 章已上线</span></div>' +
        '<p class="pl">' + p.intro + '</p><ol class="chapters">';
      for (var k = 0; k < p.chapters.length; k++) {
        var c = p.chapters[k];
        var inner = '<span class="cn">' + c.n + '</span>' +
          '<span class="ct"><b>' + c.t + '</b><span>' + c.s + '</span></span>' +
          '<span class="cm">' + (c.ready ? '已上线' : '筹备中') + '</span>';
        html += c.ready
          ? '<li><a href="' + p.id + '/' + c.f + '">' + inner + '</a></li>'
          : '<li class="pending"><div>' + inner + '</div></li>';
      }
      html += '</ol></section>';
    }
    host.innerHTML = html;
  };
})();
