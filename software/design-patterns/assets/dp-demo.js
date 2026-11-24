/* 通用演示引擎：一串步骤点亮结构里的节点，并写日志 */
(function () {
  'use strict';
  window.dpDemo = function (cfg) {
    var box = document.getElementById('demo');
    if (!box) return;
    var flow = document.getElementById('dflow');
    var log = document.getElementById('dlog');
    var bar = document.getElementById('dbar');
    var idx = -1;
    var timer = null;

    (cfg.nodes || []).forEach(function (n) {
      var d = document.createElement('button');
      d.type = 'button';
      d.className = 'dchip';
      d.id = 'chip-' + n.id;
      d.innerHTML = '<b>' + n.label + '</b>' + (n.sub ? '<i>' + n.sub + '</i>' : '');
      if (n.note) {
        d.title = n.note;
        d.addEventListener('click', function () {
          var t = document.getElementById('dnote');
          if (t) t.textContent = n.note;
        });
      }
      flow.appendChild(d);
    });

    function paint() {
      (cfg.nodes || []).forEach(function (n) {
        var el = document.getElementById('chip-' + n.id);
        if (el) el.classList.remove('on');
      });
      var st = cfg.steps[Math.max(0, idx)];
      if (!st) return;
      (st.hi || []).forEach(function (id) {
        var el = document.getElementById('chip-' + id);
        if (el) el.classList.add('on');
      });
      if (bar) {
        bar.textContent = (idx + 1) + ' / ' + cfg.steps.length + '　' + st.t;
        bar.className = 'dbar' + (st.bad ? ' bad' : '');
      }
    }
    function step() {
      if (idx >= cfg.steps.length - 1) return false;
      idx++;
      paint();
      var st = cfg.steps[idx];
      var d = document.createElement('div');
      if (st.bad) d.className = 'bad';
      d.innerHTML = '<em>' + ('0' + (idx + 1)).slice(-2) + '</em>' + st.t;
      log.appendChild(d);
      log.scrollTop = log.scrollHeight;
      return true;
    }
    function reset() {
      stop();
      idx = -1; log.innerHTML = '';
      (cfg.nodes || []).forEach(function (n) {
        var el = document.getElementById('chip-' + n.id);
        if (el) el.classList.remove('on');
      });
      if (bar) { bar.textContent = '未开始'; bar.className = 'dbar'; }
    }
    function play() {
      if (timer) { stop(); return; }
      timer = setInterval(function () { if (!step()) stop(); }, 900);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }

    var bPrev = document.getElementById('dPrev');
    var bNext = document.getElementById('dNext');
    var bPlay = document.getElementById('dPlay');
    var bReset = document.getElementById('dReset');
    if (bPrev) bPrev.onclick = function () { reset(); for (var i = 0; i <= idx; i++) { } };
    if (bNext) bNext.onclick = function () { stop(); step(); };
    if (bPlay) bPlay.onclick = play;
    if (bReset) bReset.onclick = reset;
    reset();
  };
})();
