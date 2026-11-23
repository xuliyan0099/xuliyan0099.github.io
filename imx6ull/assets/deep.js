/* deep.js —— 阅读进度、目录高亮、代码复制。依赖：无。 */
(function () {
  var bar = document.querySelector('.dp-prog i');
  function onScroll() {
    if (!bar) return;
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // 目录高亮
  var links = [].slice.call(document.querySelectorAll('.dp-toc a'));
  var heads = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  if (links.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var i = heads.indexOf(e.target);
        if (i < 0) return;
        links.forEach(function (a) { a.classList.remove('on'); });
        links[i].classList.add('on');
      });
    }, { rootMargin: '-15% 0px -70% 0px', threshold: 0 });
    heads.forEach(function (h) { if (h) io.observe(h); });
  }

  // 代码块加复制按钮
  [].slice.call(document.querySelectorAll('.dp-main pre')).forEach(function (pre) {
    if (!pre.querySelector('code')) return;
    var b = document.createElement('button');
    b.textContent = '复制';
    b.className = 'dp-copy';
    b.onclick = function () {
      var t = pre.querySelector('code').textContent;
      if (navigator.clipboard) navigator.clipboard.writeText(t);
      b.textContent = '已复制';
      setTimeout(function () { b.textContent = '复制'; }, 1200);
    };
    pre.appendChild(b);
  });
  var st = document.createElement('style');
  st.textContent = '.dp-main pre .dp-copy{position:absolute;right:8px;top:7px;font-size:11px;padding:3px 8px;' +
    'border-radius:6px;border:1px solid rgba(110,168,254,.3);background:rgba(10,15,24,.92);color:#93a5c2;cursor:pointer}' +
    '.dp-main pre .dp-copy:hover{color:#eafdff;border-color:#5ff1ef}' +
    '.dp-main pre[data-lang]:before{right:58px}';
  document.head.appendChild(st);
})();
