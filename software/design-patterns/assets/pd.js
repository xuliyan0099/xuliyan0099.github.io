/* 设计模式 · 全节共用脚本：语法着色、复制、结构图点选、演示日志小工具 */
(function () {
  'use strict';

  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  var RE = /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|^[ \t]*#[^\n]*)|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b(?:alignas|auto|bool|break|case|catch|char|class|const|constexpr|continue|default|delete|do|double|else|enum|explicit|extern|false|final|float|for|friend|goto|if|inline|int|long|mutable|namespace|new|noexcept|nullptr|operator|override|private|protected|public|register|return|short|signed|sizeof|static|struct|switch|template|this|throw|true|try|typedef|typename|union|unsigned|using|virtual|void|volatile|while|size_t|std|string|vector|unique_ptr|shared_ptr|make_shared|make_unique|const_cast|static_cast|dynamic_cast|stdin|stdout)\b)|\b(0x[0-9A-Fa-f]+|\d+(?:\.\d+)?[uUlLfF]?)\b/g;

  function highlight(code) {
    var out = '', last = 0, m;
    RE.lastIndex = 0;
    while ((m = RE.exec(code)) !== null) {
      out += esc(code.slice(last, m.index));
      var cls = m[1] ? 'cmt' : m[2] ? 'str' : m[3] ? 'kw' : 'num';
      out += '<span class="' + cls + '">' + esc(m[0]) + '</span>';
      last = m.index + m[0].length;
    }
    return out + esc(code.slice(last));
  }

  document.querySelectorAll('.codecard').forEach(function (card) {
    var codeEl = card.querySelector('pre code');
    var pre = card.querySelector('pre');
    if (!codeEl) return;
    var raw = codeEl.textContent.replace(/\s+$/, '');
    codeEl.innerHTML = highlight(raw);
    var lines = raw.split('\n').length;
    var fn = card.querySelector('.fn');
    if (fn && lines) fn.textContent = fn.textContent.replace(/\s*·.*$/, '') + ' · ' + lines + ' 行';

    var btn = card.querySelector('.copy');
    if (btn) {
      btn.addEventListener('click', function () {
        var done = function () {
          var old = btn.textContent;
          btn.textContent = '已复制';
          setTimeout(function () { btn.textContent = old; }, 1400);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(raw).then(done, function () { fallback(); });
        } else { fallback(); }
        function fallback() {
          var t = document.createElement('textarea');
          t.value = raw;
          document.body.appendChild(t);
          t.select();
          try { document.execCommand('copy'); done(); } catch (e) { /* 无剪贴板权限 */ }
          t.remove();
        }
      });
    }
  });

  // 结构图：点方框，右侧/下方说明栏显示这个角色在做什么
  document.querySelectorAll('.diagram').forEach(function (d) {
    d.querySelectorAll('[data-role]').forEach(function (g) {
      g.addEventListener('click', function () {
        d.querySelectorAll('[data-role]').forEach(function (x) { x.classList.remove('is-on'); });
        g.classList.add('is-on');
        var fig = d.closest('.fig');
        var t = fig ? fig.querySelector('.rb-t') : null;
        if (t && g.getAttribute('data-note')) {
          t.textContent = g.getAttribute('data-note');
          t.classList.remove('flash');
          void t.offsetWidth;
          t.classList.add('flash');
        }
      });
    });
  });

  var PD = {
    esc: esc,
    log: function (el, html, cls) {
      if (!el) return;
      var d = document.createElement('div');
      if (cls) d.className = cls;
      d.innerHTML = html;
      el.appendChild(d);
      el.scrollTop = el.scrollHeight;
    },
    clear: function (el) { if (el) el.innerHTML = ''; },
    setClass: function (el, nameOn, nameOff) {
      if (!el) return;
      el.classList.remove(nameOn, nameOff);
      el.classList.add(nameOff || '');
    }
  };
  window.PD = PD;
})();
