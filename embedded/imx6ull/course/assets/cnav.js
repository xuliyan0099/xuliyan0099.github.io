/* 课程导航 · 从零学计算机（45 章 / 9 部） */
const COURSE = [
  { part: 'P0 起点：计算机是什么', id: '00', file: '00.html', t: '计算机只是一台会照抄指令的机器', s: '冯诺依曼 / 五件事 / 它的极限', h: 2 },
  { part: 'P0 起点：计算机是什么', id: '01', file: '01.html', t: '为什么偏偏是二进制', s: '电平 / 噪声容限 / 两个状态就够了', h: 2 },
  { part: 'P0 起点：计算机是什么', id: '02', file: '02.html', t: '一个字节能装什么', s: '位 / 字节 / 补码 / 溢出', h: 2 },
  { part: 'P0 起点：计算机是什么', id: '03', file: '03.html', t: '从按键到屏幕', s: '端到端 / 一次 I/O 的完整路径', h: 2 },

  { part: 'P1 从开关到加法器', id: '04', file: '04.html', t: '一个开关能做什么', s: 'MOS / 上拉下拉 / 反相器', h: 3 },
  { part: 'P1 从开关到加法器', id: '05', file: '05.html', t: '与或非：布尔代数变成电路', s: '真值表 / 卡诺图 / 门电路', h: 3 },
  { part: 'P1 从开关到加法器', id: '06', file: '06.html', t: '从半加器到全加器', s: '进位链 / 4 位加法器', h: 3 },
  { part: 'P1 从开关到加法器', id: '07', file: '07.html', t: '补码与减法器', s: '取反加一 / 溢出标志', h: 3 },
  { part: 'P1 从开关到加法器', id: '08', file: '08.html', t: '时钟与触发器', s: 'D 触发器 / 寄存器 / 状态机', h: 4 },

  { part: 'P2 CPU 骨架', id: '09', file: '09.html', t: '冯诺依曼的五件事', s: '取指 / 译码 / 执行 / 访存 / 写回', h: 3 },
  { part: 'P2 CPU 骨架', id: '10', file: '10.html', t: 'PC 与指令寄存器', s: '程序是一串地址 / 跳转的本质', h: 3 },
  { part: 'P2 CPU 骨架', id: '11', file: '11.html', t: 'ALU 与标志位', s: 'N/Z/C/V / 接回 CPSR', h: 3 },
  { part: 'P2 CPU 骨架', id: '12', file: '12.html', t: '一条指令的完整旅程', s: '单周期模型 / 数据通路', h: 4 },
  { part: 'P2 CPU 骨架', id: '13', file: '13.html', t: '流水线', s: '8 级 / 冒险 / 前递 / 分支预测', h: 4 },

  { part: 'P3 指令集与语言的落差', id: '14', file: '14.html', t: '机器码的位段', s: 'cond / opcode / Rd / imm', h: 3 },
  { part: 'P3 指令集与语言的落差', id: '15', file: '15.html', t: '九种寻址方式', s: 'ldr / str / 前后索引 / 多寄存器', h: 3 },
  { part: 'P3 指令集与语言的落差', id: '16', file: '16.html', t: '汇编只有四类动作', s: '搬 / 算 / 跳 / 特权', h: 3 },
  { part: 'P3 指令集与语言的落差', id: '17', file: '17.html', t: '函数调用与 ABI', s: 'bl / lr / 栈帧 / r0–r3', h: 4 },
  { part: 'P3 指令集与语言的落差', id: '18', file: '18.html', t: '从 C 到汇编', s: '表达式 / 循环 / 结构体 / 优化', h: 4 },
  { part: 'P3 指令集与语言的落差', id: '19', file: '19.html', t: '从源码到可执行', s: '四步编译 / 链接 / ELF / 加载', h: 4 },

  { part: 'P4 存储与性能', id: '20', file: '20.html', t: '存储层次', s: '1 周期到 1 毫秒的四层', h: 3 },
  { part: 'P4 存储与性能', id: '21', file: '21.html', t: 'Cache 三参数', s: 'line / 组相联 / 写回', h: 4 },
  { part: 'P4 存储与性能', id: '22', file: '22.html', t: '内存墙与局部性', s: '遍历顺序实验', h: 3 },
  { part: 'P4 存储与性能', id: '23', file: '23.html', t: '用 perf 量化', s: '七条命令看懂性能', h: 4 },

  { part: 'P5 地址空间与进程', id: '24', file: '24.html', t: '虚拟地址是什么', s: '为什么不能直摸物理内存', h: 3 },
  { part: 'P5 地址空间与进程', id: '25', file: '25.html', t: '页表与 MMU', s: '两级表 / TLB / 页表遍历', h: 4 },
  { part: 'P5 地址空间与进程', id: '26', file: '26.html', t: '缺页与换页', s: '一次 page fault 的全链路', h: 4 },
  { part: 'P5 地址空间与进程', id: '27', file: '27.html', t: '进程、线程与 task_struct', s: '隔离靠的是页表', h: 4 },
  { part: 'P5 地址空间与进程', id: '28', file: '28.html', t: 'fork 与 exec', s: 'COW / 新进程怎么诞生', h: 4 },

  { part: 'P6 内核机制', id: '29', file: '29.html', t: '特权级与异常', s: 'svc 三步 / CPSR 模式位', h: 3 },
  { part: 'P6 内核机制', id: '30', file: '30.html', t: '中断', s: 'GIC → handler / 上下半部', h: 4 },
  { part: 'P6 内核机制', id: '31', file: '31.html', t: '调度', s: 'CFS / vruntime / 时间片', h: 4 },
  { part: 'P6 内核机制', id: '32', file: '32.html', t: '上下文切换', s: 'switch_to 五行汇编', h: 4 },
  { part: 'P6 内核机制', id: '33', file: '33.html', t: '同步', s: '原子 / 自旋 / 信号量 / 屏障', h: 4 },
  { part: 'P6 内核机制', id: '34', file: '34.html', t: '文件与设备', s: 'VFS / inode / 字符设备', h: 4 },

  { part: 'P7 上板', id: '35', file: '35.html', t: 'i.MX6ULL 最小系统', s: '电源 / 时钟 / 复位 / DDR', h: 3 },
  { part: 'P7 上板', id: '36', file: '36.html', t: '启动链', s: 'BootROM / IVT / DCD / SPL / U-Boot', h: 4 },
  { part: 'P7 上板', id: '37', file: '37.html', t: '设备树', s: 'dts / dtb / compatible / pinctrl', h: 4 },
  { part: 'P7 上板', id: '38', file: '38.html', t: '总线', s: 'AXI / AHB / APB / 时序', h: 3 },
  { part: 'P7 上板', id: '39', file: '39.html', t: 'GIC 与定时器', s: '中断号 / GPT / tick', h: 3 },
  { part: 'P7 上板', id: '40', file: '40.html', t: '存储与外设', s: 'eMMC / UART / I2C / SPI', h: 4 },
  { part: 'P7 上板', id: '41', file: '41.html', t: '根文件系统', s: 'BusyBox / Buildroot / 启动参数', h: 3 },

  { part: 'P8 综合与验收', id: '42', file: '42.html', t: '从零做出一个能跑的系统', s: '十步综合实战', h: 4 },
  { part: 'P8 综合与验收', id: '43', file: '43.html', t: '排障方法论', s: '五级日志 / 三件套证据链', h: 3 },
  { part: 'P8 综合与验收', id: '44', file: '44.html', t: '总复盘：一条从头到尾的链', s: '全链地图 / 十条结论 / 三条路线', h: 2 },

  { part: 'P9 驱动实操', id: '45', file: '45.html', t: '写一个字符设备', s: 'register_chrdev / cdev / copy_to_user', h: 4 },
  { part: 'P9 驱动实操', id: '46', file: '46.html', t: 'pinctrl 与 GPIO', s: 'pinmux / pinconf / gpiod', h: 4 },
  { part: 'P9 驱动实操', id: '47', file: '47.html', t: 'I2C 设备驱动', s: 'i2c_client / regmap / i2cdetect', h: 4 },
  { part: 'P9 驱动实操', id: '48', file: '48.html', t: '中断的上半部与下半部', s: 'request_irq / tasklet / 防抖', h: 4 }
];

document.addEventListener('DOMContentLoaded', function () {
  const cur = document.body.dataset.page || 'index';
  const top = document.getElementById('topbar');
  if (top) {
    top.innerHTML = '<button class="nav-toggle" id="navBtn" type="button" aria-label="打开目录" aria-expanded="false">☰</button>' +
      '<div class="brand"><span class="dot"></span>从零学计算机' +
      '<small>比特 → 电路 → CPU → 内核 → 板子</small></div><div class="spacer"></div>' +
      '<a class="home" href="index.html"><span class="lg">⌂ 课程总览</span><span class="sm">☰ 目录</span></a>' +
      '<a class="home" href="../juan/index.html"><span class="lg">📚 卷总览</span><span class="sm">📚</span></a>' +
      '<a class="home" href="../index.html"><span class="lg">⌂ 手册总入口</span><span class="sm">⌂ 入口</span></a>';
  }

  const sb = document.getElementById('sidebar');
  if (sb) {
    let html = '';
    let last = null;
    let open = false;
    COURSE.forEach(function (c) {
      if (c.part !== last) {
        if (open) html += '</ol>';
        html += '<p class="side-t">' + c.part + '</p><ol>';
        last = c.part;
        open = true;
      }
      const act = c.id === cur ? ' class="active"' : '';
      html += '<li><a' + act + ' href="' + c.file + '"><span class="no">' + c.id +
        '</span><span>' + c.t + '<span class="sub">' + c.s + '</span></span></a></li>';
    });
    if (open) html += '</ol>';
    sb.innerHTML = '<div class="nav-head"><b>课程目录</b><button type="button" id="navClose" aria-label="关闭目录">✕</button></div>' + html;

    /* ---- 手机 / 平板抽屉 ---- */
    const btn = document.getElementById('navBtn');
    let mask = document.getElementById('navmask');
    if (!mask) { mask = document.createElement('div'); mask.id = 'navmask'; document.body.appendChild(mask); }
    function setNav(on) {
      sb.classList.toggle('open', on);
      mask.classList.toggle('show', on);
      document.body.classList.toggle('nav-open', on);
      if (btn) btn.setAttribute('aria-expanded', on ? 'true' : 'false');
    }
    if (btn) btn.addEventListener('click', function () { setNav(!sb.classList.contains('open')); });
    const cbtn = document.getElementById('navClose');
    if (cbtn) cbtn.addEventListener('click', function () { setNav(false); });
    mask.addEventListener('click', function () { setNav(false); });
    sb.addEventListener('click', function (e) {
      if (e.target && e.target.closest && e.target.closest('a')) setNav(false);
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 900) setNav(false); });
  }

  const pg = document.getElementById('pager');
  if (pg) {
    const i = COURSE.findIndex(function (c) { return c.id === cur; });
    let html = '';
    if (i > 0) {
      const p = COURSE[i - 1];
      html += '<a class="prev" href="' + p.file + '"><span class="dir">← 上一课</span>' +
        '<span class="tt">' + p.id + ' · ' + p.t + '</span></a>';
    } else { html += '<span></span>'; }
    if (i > -1 && i < COURSE.length - 1) {
      const n = COURSE[i + 1];
      html += '<a class="next" href="' + n.file + '"><span class="dir">下一课 →</span>' +
        '<span class="tt">' + n.id + ' · ' + n.t + '</span></a>';
    }
    pg.innerHTML = html;
  }

  /* ---- 回到课程总览 / 回顶部 ---- */
  const fl = document.createElement('div');
  fl.className = 'floats';
  fl.innerHTML = '<a class="fb" href="index.html">☰ 课程总览</a>' +
    '<button class="fb" type="button" id="toTopBtn">↑ 顶部</button>';
  document.body.appendChild(fl);
  fl.querySelector('#toTopBtn').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  window.addEventListener('scroll', function () {
    if (window.scrollY > 320) { fl.classList.add('show'); } else { fl.classList.remove('show'); }
  }, { passive: true });
});
