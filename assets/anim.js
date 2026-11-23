/* ===== 动画演示引擎 anim.js ===== */
(function () {
  'use strict';
  function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; }

  function build(n, cfg) {
    var nodes = cfg.nodes || [], frames = cfg.frames || [];
    if (!nodes.length || !frames.length) { n.innerHTML = '<div class="an-h"><i></i><span>动画数据缺失</span></div>'; return; }
    var speed = cfg.speed || 2200;

    n.classList.add('an-wrap');
    var head = el('div', 'an-h', '<i></i><span>' + (cfg.title || '动画演示') + '</span>' + (cfg.hint ? '<em>' + cfg.hint + '</em>' : ''));
    n.appendChild(head);

    var track = el('div', 'an-track');
    var nodeEls = [], linkEls = [];
    nodes.forEach(function (nd, k) {
      var box = el('div', 'an-n', '<b>' + (nd.k || '') + '</b>' + (nd.s ? '<s>' + nd.s + '</s>' : ''));
      track.appendChild(box); nodeEls.push(box);
      if (k < nodes.length - 1) { var lk = el('span', 'an-link'); track.appendChild(lk); linkEls.push(lk); }
    });
    n.appendChild(track);

    var msg = el('div', 'an-msg');
    var ctl = el('div', 'an-ctl');
    var playB = el('button', 'an-b pri', '⏸ 暂停');
    var prevB = el('button', 'an-b', '← 上一帧');
    var nextB = el('button', 'an-b', '下一帧 →');
    var againB = el('button', 'an-b', '↻ 重播');
    var cnt = el('span', 'an-cnt');
    playB.type = prevB.type = nextB.type = againB.type = 'button';
    ctl.appendChild(playB); ctl.appendChild(prevB); ctl.appendChild(nextB); ctl.appendChild(againB); ctl.appendChild(cnt);
    n.appendChild(msg); n.appendChild(ctl);

    var bar = el('div', 'an-bar', '<i></i>');
    n.appendChild(bar);

    var i = -1, timer = null, playing = true;

    function paint() {
      var f = frames[i] || {};
      nodeEls.forEach(function (b, k) {
        b.classList.toggle('on', k === (f.i == null ? i : f.i));
        b.classList.toggle('done', k < (f.i == null ? i : f.i));
      });
      linkEls.forEach(function (l, k) { l.classList.toggle('on', k === (f.i == null ? i : f.i)); });
      msg.innerHTML = (f.n != null ? '<b>' + nodes[f.n].k + '</b> · ' : '') + (f.d || '');
      cnt.textContent = (i + 1) + ' / ' + frames.length;
      bar.firstChild.style.width = ((i + 1) / frames.length * 100).toFixed(1) + '%';
      prevB.disabled = i <= 0;
      nextB.disabled = i >= frames.length - 1;
    }
    function step(dir) {
      var k = i + dir;
      if (k < 0) k = 0;
      if (k > frames.length - 1) k = 0;
      i = k; paint();
    }
    function tick() { if (i >= frames.length - 1) { i = 0; } else { i++; } paint(); }
    function start() {
      stop();
      playing = true; playB.textContent = '⏸ 暂停';
      timer = setInterval(tick, speed);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    playB.addEventListener('click', function () {
      if (playing) { stop(); playing = false; playB.textContent = '▶ 播放'; }
      else { start(); }
    });
    prevB.addEventListener('click', function () { stop(); playing = false; playB.textContent = '▶ 播放'; step(-1); });
    nextB.addEventListener('click', function () { stop(); playing = false; playB.textContent = '▶ 播放'; step(1); });
    againB.addEventListener('click', function () { i = 0; paint(); start(); });

    paint.call(null);
    i = 0; paint(); start();

    n.setAttribute('data-built', '1');
  }

  function boot() {
    var list = document.querySelectorAll('.anim[data-anim]');
    for (var k = 0; k < list.length; k++) {
      var n = list[k];
      if (n.getAttribute('data-built') === '1') continue;
      var cfg = null;
      try { cfg = JSON.parse(n.getAttribute('data-json') || '{}'); } catch (e) { cfg = null; }
      if (!cfg) { n.innerHTML = '<div class="an-h"><i></i><span>动画数据有误</span></div>'; continue; }
      try { build(n, cfg); } catch (e) { n.innerHTML = '<div class="an-h"><i></i><span>动画渲染失败</span></div>'; }
    }
  }
  window.animRender = boot;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
