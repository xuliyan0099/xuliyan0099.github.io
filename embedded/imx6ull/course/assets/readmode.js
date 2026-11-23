/* 读法开关：📖 只读 / 🔧 实作
   只读模式把「动手 / 实作 / 实验 / 上机 / 作业 / 练习」这类段落折叠起来，
   折起来的内容原位保留，点一下就能展开；选择记在 localStorage。
   本文件只做展示层处理，不依赖正文里预先标记的 class。 */
(function () {
  'use strict';
  var KEY = 'imx6ull.readmode';
  var HIDE_RE = /^(?:\d+[.、]\s*)?(动手|实作|实验|上机|作业|练习|做实)/;
  var SOON_RE = /(动手|实作|实验|上机|作业|练习)/;

  var mode = 'full';
  try { mode = localStorage.getItem(KEY) || 'read'; } catch (e) { mode = 'read'; }

  var groups = [];   // { nodes:[], chip:Element }
  var bar, toast;

  function container() {
    return document.querySelector('main.doc') || document.querySelector('main') || document.body;
  }

  function collect() {
    var root = container();
    var kids = Array.prototype.slice.call(root.children);
    var cur = null;
    kids.forEach(function (el) {
      var tag = el.tagName;
      if (tag === 'H2' || tag === 'H3') {
        var txt = (el.textContent || '').trim();
        if (HIDE_RE.test(txt) || (tag === 'H2' && SOON_RE.test(txt))) {
          cur = { title: txt, nodes: [el], chip: null };
          groups.push(cur);
          return;
        }
        cur = null;
        return;
      }
      if (cur) cur.nodes.push(el);
    });
  }

  function buildChips() {
    groups.forEach(function (g) {
      var chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'rm-chip';
      chip.innerHTML = '<span class="rm-ico">🔧</span><span>实作段落已折叠：' +
        g.title.replace(/^\d+[.、]\s*/, '') + '</span><span class="rm-more">展开</span>';
      chip.addEventListener('click', function (ev) {
        ev.preventDefault();
        apply('full');
        if (g.nodes[0] && g.nodes[0].scrollIntoView) {
          g.nodes[0].scrollIntoView({ block: 'start', behavior: 'smooth' });
        }
        try { localStorage.setItem(KEY, 'full'); } catch (e) {}
        syncBar();
      });
      g.nodes[0].parentNode.insertBefore(chip, g.nodes[0]);
      g.chip = chip;
    });
  }

  function apply(m) {
    mode = m;
    groups.forEach(function (g) {
      var hide = (m === 'read');
      g.nodes.forEach(function (n) {
        if (n === g.nodes[0] && g.chip && g.chip.parentNode) { /* heading 本体 */ }
        n.style.display = hide ? 'none' : '';
      });
      if (g.chip) g.chip.style.display = hide ? '' : 'none';
    });
    try { localStorage.setItem(KEY, m); } catch (e) {}
    syncBar();
  }

  function syncBar() {
    if (!bar) return;
    var bRead = bar.querySelector('[data-m="read"]');
    var bFull = bar.querySelector('[data-m="full"]');
    if (bRead) bRead.classList.toggle('on', mode === 'read');
    if (bFull) bFull.classList.toggle('on', mode === 'full');
    var n = groups.length;
    var tip = bar.querySelector('.rm-tip');
    if (tip) {
      tip.textContent = n
        ? (mode === 'read' ? '已折叠 ' + n + ' 段操作内容' : '全部展开')
        : '本页没有操作段落';
    }
  }

  function buildBar() {
    bar = document.createElement('div');
    bar.className = 'rm-bar';
    bar.innerHTML =
      '<span class="rm-tip"></span>' +
      '<button type="button" data-m="read">📖 只读</button>' +
      '<button type="button" data-m="full">🔧 实作</button>';
    bar.addEventListener('click', function (ev) {
      var b = ev.target.closest ? ev.target.closest('button[data-m]') : null;
      if (!b) return;
      apply(b.getAttribute('data-m'));
      if (b.getAttribute('data-m') === 'read' && groups.length) brief('操作段落已折叠，点标题旁的「展开」可还原');
    });
    document.body.appendChild(bar);
  }

  function brief(msg) {
    if (toast) { toast.remove(); toast = null; }
    toast = document.createElement('div');
    toast.className = 'rm-toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(function () { if (toast) { toast.remove(); toast = null; } }, 2600);
  }

  function style() {
    var css = [
      '.rm-bar{position:fixed;right:18px;bottom:118px;z-index:70;display:flex;align-items:center;gap:6px;padding:6px 8px;border:1px solid rgba(110,168,254,.28);border-radius:12px;background:rgba(9,13,22,.92);backdrop-filter:blur(8px);box-shadow:0 8px 28px rgba(0,0,0,.45);font:12.5px/1.2 "Noto Sans SC","PingFang SC",system-ui,sans-serif}',
      '.rm-bar .rm-tip{color:#8b9cbb;padding:0 4px;max-width:190px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
      '.rm-bar button{cursor:pointer;padding:6px 10px;border-radius:9px;border:1px solid rgba(110,168,254,.24);background:rgba(15,21,34,.9);color:#b9cae6;font:inherit}',
      '.rm-bar button.on{border-color:#5ff1ef;color:#eafdff;background:rgba(95,241,239,.12);box-shadow:0 0 0 1px rgba(95,241,239,.25) inset}',
      '.rm-chip{display:flex;align-items:center;gap:8px;width:100%;margin:14px 0;padding:11px 14px;border:1px dashed rgba(110,168,254,.3);border-left:3px solid #8b5cf6;border-radius:10px;background:rgba(15,21,34,.75);color:#a9bbd8;font:13px/1.3 inherit;text-align:left;cursor:pointer}',
      '.rm-chip:hover{border-color:#5ff1ef;color:#e6ecfa}',
      '.rm-chip .rm-ico{flex:none}',
      '.rm-chip .rm-more{margin-left:auto;flex:none;color:#5ff1ef;font-size:12px}',
      '.rm-toast{position:fixed;right:18px;bottom:166px;z-index:71;max-width:270px;padding:10px 12px;border-radius:10px;border:1px solid rgba(95,241,239,.35);background:rgba(9,13,22,.95);color:#cfe6f7;font:12.5px/1.5 inherit;box-shadow:0 10px 30px rgba(0,0,0,.5)}',
      '@media(max-width:640px){.rm-bar .rm-tip{display:none}.rm-bar{right:10px;bottom:104px}.rm-toast{bottom:150px}}'
    ].join('');
    var s = document.createElement('style');
    s.textContent = css;
    document.head.appendChild(s);
  }

  function init() {
    style();
    collect();
    buildChips();
    buildBar();
    apply(mode);
    if (mode === 'read' && groups.length) {
      setTimeout(function () { brief('只读模式：已折叠 ' + groups.length + ' 段操作内容，右下角可切到「实作」'); }, 900);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
