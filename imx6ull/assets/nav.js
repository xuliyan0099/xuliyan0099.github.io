/* 手册导航：统一生成顶栏、左侧目录、上下章翻页 */
const HANDBOOK = [
  { group: '入口', id: 'index', file: 'index.html', no: '00', title: '学习规划手册', sub: '路线图 · 时间表 · 验收标准' },
  { group: '入口', id: 'roadmap', file: 'roadmap.html', no: '01', title: '学习路线图：比特到板子', sub: '六阶段 · 双螺旋 · 软硬件对账表' },

  { group: '理论卷', id: 'th01', file: 'th01.html', no: 'T01', title: '操作系统与 Linux 的分层', sub: '用户态 / 内核态 / 子系统' },
  { group: '理论卷', id: 'th02', file: 'th02.html', no: 'T02', title: '进程、线程与调度', sub: 'task_struct / 状态机 / CFS' },
  { group: '理论卷', id: 'th03', file: 'th03.html', no: 'T03', title: '虚拟内存与地址翻译', sub: 'MMU / 页表 / 分配器' },
  { group: '理论卷', id: 'th04', file: 'th04.html', no: 'T04', title: '文件系统与 VFS', sub: 'inode / 页缓存 / 日志' },
  { group: '理论卷', id: 'th05', file: 'th05.html', no: 'T05', title: '设备模型与驱动框架', sub: '三类设备 / bus-driver' },
  { group: '理论卷', id: 'th06', file: 'th06.html', no: 'T06', title: '中断、并发与同步', sub: '上下半部 / 锁 / 死锁' },
  { group: '理论卷', id: 'th07', file: 'th07.html', no: 'T07', title: 'ARM 架构与 Cortex-A7', sub: '特权级 / 异常向量 / Cache' },
  { group: '理论卷', id: 'th08', file: 'th08.html', no: 'T08', title: '从第一个字节开始', sub: 'BootROM / IVT / DCD / SPL' },
  { group: '理论卷', id: 'th09', file: 'th09.html', no: 'T09', title: '内核怎么起来', sub: 'head.S / start_kernel / init' },
  { group: '理论卷', id: 'th10', file: 'th10.html', no: 'T10', title: '总线体系', sub: 'AXI / AHB / APB / I2C' },
  { group: '理论卷', id: 'th11', file: 'th11.html', no: 'T11', title: '时钟树、复位与电源域', sub: 'PLL / CCGR / SRC / RTC / 看门狗' },
  { group: '理论卷', id: 'th12', file: 'th12.html', no: 'T12', title: '最小系统外设（上）', sub: 'DDR / 中断控制器 / 定时器 / GPIO / UART' },
  { group: '理论卷', id: 'th13', file: 'th13.html', no: 'T13', title: '最小系统外设（下）', sub: '存储 / DMA / 以太网 / USB' },
  { group: '理论卷', id: 'th14', file: 'th14.html', no: 'T14', title: '内存管理进阶', sub: '分页 / 缺页 / 回收 / OOM' },
  { group: '理论卷', id: 'th15', file: 'th15.html', no: 'T15', title: '内核全貌：子系统协作', sub: 'read 全链路 / 可观测性 / 裁剪' },
  { group: '理论卷', id: 'th16', file: 'th16.html', no: 'T16', title: 'BSP 与设备树原理', sub: 'dts / compatible / 移植清单' },
  { group: '理论卷', id: 'th17', file: 'th17.html', no: 'T17', title: '交叉编译与工具链原理', sub: 'ABI / ELF / 静态与动态' },
  { group: '理论卷', id: 'th18', file: 'th18.html', no: 'T18', title: 'CPU 是怎么执行代码的', sub: '机器码 / 流水线 / 中断 / 切换' },

  { group: '实践卷', id: 'ch01', file: 'ch01.html', no: '01', title: 'Linux 全景认知', sub: '内核 / 发行版 / 嵌入式三条线' },
  { group: '实践卷', id: 'ch02', file: 'ch02.html', no: '02', title: '搭好实验台', sub: '虚拟机 / Ubuntu / 串口 / SSH' },
  { group: '实践卷', id: 'ch03', file: 'ch03.html', no: '03', title: '命令行与文件系统', sub: '一切皆文件 · 核心命令' },
  { group: '实践卷', id: 'ch04', file: 'ch04.html', no: '04', title: '系统管理四件事', sub: '权限 / 软件 / 进程 / 日志' },
  { group: '实践卷', id: 'ch05', file: 'ch05.html', no: '05', title: 'Vim 与 Shell 脚本', sub: '效率工具 · 自动化' },
  { group: '实践卷', id: 'ch06', file: 'ch06.html', no: '06', title: '网络与远程开发', sub: 'IP / SSH / NFS / TFTP' },
  { group: '实践卷', id: 'ch07', file: 'ch07.html', no: '07', title: '交叉编译与工程构建', sub: '工具链 / Makefile / gdb' },
  { group: '实践卷', id: 'ch08', file: 'ch08.html', no: '08', title: 'i.MX6ULL 与启动链路', sub: 'BootROM → U-Boot → 内核' },
  { group: '实践卷', id: 'ch09', file: 'ch09.html', no: '09', title: 'U-Boot 与烧写', sub: '命令 / 启动参数 / 固化' },
  { group: '实践卷', id: 'ch10', file: 'ch10.html', no: '10', title: '内核裁剪与设备树', sub: 'menuconfig / DTS 语法' },
  { group: '实践卷', id: 'ch11', file: 'ch11.html', no: '11', title: '根文件系统构建', sub: 'BusyBox / Buildroot' },
  { group: '实践卷', id: 'ch12', file: 'ch12.html', no: '12', title: '驱动开发入门', sub: '字符设备 / GPIO / 设备树' },
  { group: '实践卷', id: 'ch13', file: 'ch13.html', no: '13', title: '调试与排障工具箱', sub: '日志 / strace / gdb / ftrace' },
  { group: '实践卷', id: 'ch14', file: 'ch14.html', no: '14', title: '综合实战项目', sub: '从零做出能跑的系统' }
];

document.addEventListener('DOMContentLoaded', function () {
  const cur = document.body.dataset.page || 'index';
  const siteTitle = 'i.MX6ULL · Linux 从零到驱动';

  /* ---------- 顶栏 ---------- */
  const tb = document.getElementById('topbar');
  if (tb) {
    tb.innerHTML =
      '<div class="brand"><span class="dot"></span>' + siteTitle +
      '<small>理论 + 实践</small></div><div class="spacer"></div>' +
      (cur === 'index' ? '' : '<a class="home" href="index.html"><span class="lg">☰ 参考卷目录</span><span class="sm">☰ 参考卷</span></a>') +
      '<a class="home" href="../index.html"><span class="lg">⌂ 学习站入口</span><span class="sm">⌂ 学习站</span></a>' +
      '<a class="home" href="../../index.html"><span class="lg">⌂ 个人知识库</span><span class="sm">⌂ 知识库</span></a>';
  }

  /* ---------- 侧栏（按卷分组） ---------- */
  const sb = document.getElementById('sidebar');
  if (sb) {
    let html = '';
    let lastGroup = null;
    let open = false;
    HANDBOOK.forEach(function (c) {
      if (c.group !== lastGroup) {
        if (open) { html += '</ol>'; }
        html += '<p class="side-t">' + c.group + '</p><ol>';
        lastGroup = c.group;
        open = true;
      }
      const act = c.id === cur ? ' class="active"' : '';
      html += '<li><a' + act + ' href="' + c.file + '">' +
        '<span class="no">' + c.no + '</span><span>' + c.title +
        '<span class="sub">' + c.sub + '</span></span></a></li>';
    });
    if (open) { html += '</ol>'; }
    sb.innerHTML = html;

    if (window.innerWidth <= 900) {
      sb.classList.add('collapsed');
      const tg = document.createElement('button');
      tg.type = 'button';
      tg.className = 'side-tg';
      tg.textContent = '☰ 目录（' + HANDBOOK.length + ' 条）';
      tg.addEventListener('click', function () {
        const on = sb.classList.toggle('collapsed');
        tg.textContent = on ? '☰ 目录（' + HANDBOOK.length + ' 条）' : '✕ 收起目录';
      });
      sb.insertBefore(tg, sb.firstChild);
    }
  }

  /* ---------- 翻页 ---------- */
  const pg = document.getElementById('pager');
  if (pg) {
    const i = HANDBOOK.findIndex(function (c) { return c.id === cur; });
    let html = '';
    if (i > 0) {
      const p = HANDBOOK[i - 1];
      html += '<a class="prev" href="' + p.file + '"><span class="dir">← 上一章</span>' +
        '<span class="tt">' + p.no + ' · ' + p.title + '</span></a>';
    } else { html += '<span></span>'; }
    if (i > -1 && i < HANDBOOK.length - 1) {
      const n = HANDBOOK[i + 1];
      html += '<a class="next" href="' + n.file + '"><span class="dir">下一章 →</span>' +
        '<span class="tt">' + n.no + ' · ' + n.title + '</span></a>';
    }
    pg.innerHTML = html;
  }

  /* ---------- 回到目录 / 回顶部 ---------- */
  const fl = document.createElement('div');
  fl.className = 'floats';
  fl.innerHTML = (cur === 'index' ? '' : '<a class="fb" href="index.html">☰ 总目录</a>') +
    '<button class="fb" type="button" id="toTopBtn">↑ 顶部</button>';
  document.body.appendChild(fl);
  fl.querySelector('#toTopBtn').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  window.addEventListener('scroll', function () {
    if (window.scrollY > 320) { fl.classList.add('show'); } else { fl.classList.remove('show'); }
  }, { passive: true });
});
