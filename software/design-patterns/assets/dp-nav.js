/* 设计模式全书：按篇渲染侧栏、篇目录页的章列表。依赖 assets/dp-data.js。 */
(function () {
  function partById(id) {
    var list = window.DP_PARTS || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }
  function curFile() {
    var seg = location.pathname.split('/');
    var f = seg[seg.length - 1];
    return f && f.indexOf('.html') > 0 ? f : 'c01.html';
  }

  window.dpNav = function (partId) {
    var part = partById(partId);
    if (!part) return;
    var file = curFile();

    var head = document.querySelector('#sidebar .vol-h');
    if (head) {
      head.innerHTML = '篇' + part.no + ' · ' + part.title +
        '<label for="navChk" class="nav-x" aria-label="收起目录">✕</label>';
    }

    var list = document.getElementById('sideList');
    if (list) {
      list.innerHTML = '';
      part.chapters.forEach(function (c) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = '../' + part.id + '/' + c.f;
        a.innerHTML = '<span class="no">' + c.n + '</span><span>' + c.t +
          '<span class="sub">' + c.s + '</span></span>';
        li.appendChild(a);
        if (c.f === file) {
          a.className = 'active';
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
    }

    var nav = document.getElementById('volNav');
    if (nav) {
      var flat = [];
      (window.DP_PARTS || []).forEach(function (p) {
        p.chapters.forEach(function (c) { flat.push({ pid: p.id, n: c.n, f: c.f }); });
      });
      var gi = -1;
      flat.forEach(function (c, i) { if (c.pid === partId && c.f === file) gi = i; });
      var prev = gi > 0 ? flat[gi - 1] : null;
      var next = gi > -1 && gi < flat.length - 1 ? flat[gi + 1] : null;
      var html = prev
        ? '<a href="../' + prev.pid + '/' + prev.f + '">← ' + prev.n + '</a>'
        : '<a href="../index.html">← 目录</a>';
      html += next
        ? '<a class="nx" href="../' + next.pid + '/' + next.f + '">' + next.n + ' →</a>'
        : '<a class="nx" href="../index.html">目录 →</a>';
      nav.innerHTML = html;
    }
  };

  window.dpToc = function () {
    var host = document.getElementById('toc');
    if (!host) return;
    var html = '';
    (window.DP_PARTS || []).forEach(function (p) {
      var total = p.chapters.reduce(function (a, c) { return a + c.min; }, 0);
      html += '<div class="part-block" id="' + p.id + '">' +
        '<div class="part-head2"><h2>' + p.no + '　' + p.title + '</h2>' +
        '<span class="pk">篇' + p.no + '</span>' +
        '<span class="pc">' + p.chapters.length + ' 章 · 约 ' + total + ' 分钟</span></div>' +
        '<p class="pl">' + p.intro + '</p><div class="chlist">';
      p.chapters.forEach(function (c) {
        html += '<a class="chrow" href="' + p.id + '/' + c.f + '">' +
          '<span class="cn">' + c.n + '</span>' +
          '<span class="ct"><b>' + c.t + '</b><i>' + c.s + '</i></span>' +
          '<span class="cm">' + c.min + ' 分钟</span><span class="ca">→</span></a>';
      });
      html += '</div></div>';
    });
    host.innerHTML = html;
  };
})();
