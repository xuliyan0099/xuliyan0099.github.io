/* =====================================================================
   catalog.js · i.MX6ULL 学习手册「唯一目录源」
   生成于 2026-11-26 · 数据取自 docs/ 113 个页面的真实左栏（标题、时长、链接）
   规则见文件末尾注释；此后左栏、卷页表格、上下篇都由这份数据渲染。
   ===================================================================== */
window.CATALOG = {
  site: 'i.MX6ULL · 从裸机到 Linux 驱动',
  built: '2026-11-26',
  total: 113,
  hours: 406,          /* 逐篇相加 */
  hoursClaimed: 120,   /* 总览页现在写的「通读 120h」 */

  /* 组 = 体裁。顺序即左栏里的显示顺序；空组不渲染。 */
  groups: [
    { key: 'core',     name: '核心',   tip: '先跑通 · 每篇约 1 小时' },
    { key: 'detail',   name: '详解',   tip: '补原理 · 3–8 小时' },
    { key: 'practice', name: '实战',   tip: '动手 · 10–20 小时' },
    { key: 'deep',     name: '深读',   tip: '选读 · 专题' },
    { key: 'lab',      name: '互动台', tip: '改参数即时看结果' }
  ],

  volumes: [
  /* ---------------------------------------------------------------- 卷 00 */
  { id:'00', title:'起步 · Linux 与实验台', oldHours:8, sum:70,
    groups:[
      { key:'practice', items:[
        { n:'00.01', o:'01', t:'Linux 全景认知', h:4,  f:'docs/course-ch01.html' },
        { n:'00.02', o:'02', t:'搭好实验台', h:10, f:'docs/course-ch02.html' },
        { n:'00.03', o:'03', t:'命令行与文件系统', h:16, f:'docs/course-ch03.html' },
        { n:'00.04', o:'04', t:'系统管理四件事', h:16, f:'docs/course-ch04.html' },
        { n:'00.05', o:'05', t:'Vim 与 Shell 脚本', h:14, f:'docs/course-ch05.html' },
        { n:'00.06', o:'06', t:'网络与远程开发', h:10, f:'docs/course-ch06.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 01 */
  { id:'01', title:'机器与指令', oldHours:24, sum:22,
    groups:[
      { key:'core', items:[
        { n:'01.01', o:'01', t:'计算机只是一台会照抄指令的机器', h:1, f:'docs/course-00.html' },
        { n:'01.02', o:'02', t:'为什么偏偏是二进制', h:1, f:'docs/course-01.html' },
        { n:'01.03', o:'03', t:'一个字节能装什么', h:1, f:'docs/course-02.html' },
        { n:'01.04', o:'04', t:'从按键到屏幕', h:1, f:'docs/course-03.html' },
        { n:'01.05', o:'05', t:'一个开关能做什么', h:1, f:'docs/course-04.html' },
        { n:'01.06', o:'06', t:'与、或、非', h:1, f:'docs/course-05.html' },
        { n:'01.07', o:'07', t:'从半加器到全加器', h:1, f:'docs/course-06.html' },
        { n:'01.08', o:'08', t:'补码与减法器', h:1, f:'docs/course-07.html' },
        { n:'01.09', o:'09', t:'时钟与触发器', h:1, f:'docs/course-08.html' },
        { n:'01.10', o:'10', t:'冯诺依曼五件事', h:1, f:'docs/course-09.html' },
        { n:'01.11', o:'11', t:'PC 与指令寄存器', h:1, f:'docs/course-10.html' },
        { n:'01.12', o:'12', t:'ALU 与标志位', h:1, f:'docs/course-11.html' },
        { n:'01.13', o:'13', t:'一条指令的完整旅程', h:1, f:'docs/course-12.html' },
        { n:'01.14', o:'14', t:'流水线', h:1, f:'docs/course-13.html' },
        { n:'01.15', o:'15', t:'机器码的位段', h:1, f:'docs/course-14.html' },
        { n:'01.16', o:'16', t:'九种寻址方式', h:1, f:'docs/course-15.html' },
        { n:'01.17', o:'17', t:'汇编只有四类动作', h:1, f:'docs/course-16.html' },
        { n:'01.18', o:'18', t:'函数调用与 ABI', h:1, f:'docs/course-17.html' },
        { n:'01.19', o:'19', t:'从 C 到汇编', h:1, f:'docs/course-18.html' }
      ]},
      { key:'detail', items:[
        { n:'01.20', o:'20', t:'CPU 是怎么执行一行代码的（详解）', h:3, f:'docs/course-th18.html', p:'01.13' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 02 */
  { id:'02', title:'编译与运行', oldHours:4, sum:25,
    groups:[
      { key:'core', items:[
        { n:'02.01', o:'01', t:'从源码到可执行', h:1, f:'docs/course-19.html' }
      ]},
      { key:'detail', items:[
        { n:'02.02', o:'03', t:'交叉编译与工具链原理', h:4, f:'docs/course-th17.html', p:'02.03' }
      ]},
      { key:'practice', items:[
        { n:'02.03', o:'02', t:'交叉编译与工程构建', h:12, f:'docs/course-ch07.html' }
      ]},
      { key:'deep', items:[
        { n:'02.04', o:'04', t:'ELF 与链接重定位：从符号表到 .rel.text', h:3, f:'docs/d02-01.html' },
        { n:'02.05', o:'05', t:'静态库与动态链接：PLT / GOT / PIC 全链路', h:3, f:'docs/d02-02.html' },
        { n:'02.06', o:'06', t:'程序加载与内存布局：段、栈、堆、core dump', h:2, f:'docs/d02-03.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 03 */
  { id:'03', title:'存储与地址', oldHours:12, sum:18,
    groups:[
      { key:'core', items:[
        { n:'03.01', o:'01', t:'存储层次', h:1, f:'docs/course-20.html' },
        { n:'03.02', o:'02', t:'Cache 三参数', h:1, f:'docs/course-21.html' },
        { n:'03.03', o:'03', t:'内存墙与局部性', h:1, f:'docs/course-22.html' },
        { n:'03.04', o:'04', t:'用 perf 量化', h:1, f:'docs/course-23.html' },
        { n:'03.05', o:'05', t:'虚拟地址是什么', h:1, f:'docs/course-24.html' },
        { n:'03.06', o:'06', t:'页表与 MMU', h:1, f:'docs/course-25.html' },
        { n:'03.07', o:'07', t:'缺页与换页', h:1, f:'docs/course-26.html' }
      ]},
      { key:'detail', items:[
        { n:'03.08', o:'08', t:'虚拟内存与地址翻译（详解）', h:4, f:'docs/course-th03.html', p:'03.06' },
        { n:'03.09', o:'09', t:'内存管理进阶：分页、回收与 OOM', h:5, f:'docs/course-th14.html', p:'03.07' }
      ]},
      { key:'lab', items:[
        { n:'03.10', o:'10', t:'互动台：MMU 页表翻译', h:1, f:'docs/viz-mmu.html' },
        { n:'03.11', o:'11', t:'互动台：Cache 层次与命中', h:1, f:'docs/viz-cache.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 04 */
  { id:'04', title:'操作系统', oldHours:13, sum:23,
    groups:[
      { key:'core', items:[
        { n:'04.01', o:'02', t:'进程、线程与 task_struct', h:1, f:'docs/course-27.html' },
        { n:'04.02', o:'03', t:'fork 与 exec', h:1, f:'docs/course-28.html' },
        { n:'04.03', o:'04', t:'特权级与异常', h:1, f:'docs/course-29.html' },
        { n:'04.04', o:'05', t:'中断', h:1, f:'docs/course-30.html' },
        { n:'04.05', o:'06', t:'调度', h:1, f:'docs/course-31.html' },
        { n:'04.06', o:'07', t:'上下文切换', h:1, f:'docs/course-32.html' },
        { n:'04.07', o:'08', t:'同步', h:1, f:'docs/course-33.html' }
      ]},
      { key:'detail', items:[
        { n:'04.08', o:'01', t:'操作系统与 Linux 的分层', h:3, f:'docs/course-th01.html' },
        { n:'04.09', o:'09', t:'进程、线程与调度（详解）', h:4, f:'docs/course-th02.html', p:'04.01' },
        { n:'04.10', o:'10', t:'中断、并发与同步（详解）', h:5, f:'docs/course-th06.html', p:'04.04' },
        { n:'04.11', o:'11', t:'内核全貌：子系统如何协作', h:4, f:'docs/course-th15.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 05 */
  { id:'05', title:'文件与设备', oldHours:3, sum:9,
    groups:[
      { key:'core', items:[
        { n:'05.01', o:'01', t:'文件与设备', h:1, f:'docs/course-34.html' }
      ]},
      { key:'detail', items:[
        { n:'05.02', o:'02', t:'文件系统与 VFS（详解）', h:4, f:'docs/course-th04.html', p:'05.01' }
      ]},
      { key:'deep', items:[
        { n:'05.03', o:'03', t:'ext4 磁盘布局：超级块、块组、inode 表、目录项与日志', h:4, f:'docs/d05-01.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 06 */
  { id:'06', title:'网络栈', oldHours:6, sum:6,
    groups:[
      { key:'deep', items:[
        { n:'06.01', o:'01', t:'从 socket 到协议栈：套接字、sock、传输层入口', h:2, f:'docs/d06-01.html' },
        { n:'06.02', o:'02', t:'TCP 状态机与 sk_buff：一次数据往返的完整路径', h:2, f:'docs/d06-02.html' },
        { n:'06.03', o:'03', t:'IP、路由与网卡驱动：包怎么出了门又回来', h:2, f:'docs/d06-03.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 07 */
  { id:'07', title:'芯片与硬件底座', oldHours:15, sum:39,
    groups:[
      { key:'core', items:[
        { n:'07.01', o:'02', t:'i.MX6ULL 最小系统', h:1, f:'docs/course-35.html' },
        { n:'07.02', o:'09', t:'总线', h:1, f:'docs/course-38.html' },
        { n:'07.03', o:'10', t:'GIC 与定时器', h:1, f:'docs/course-39.html' },
        { n:'07.04', o:'11', t:'存储与外设', h:1, f:'docs/course-40.html' },
        { n:'07.05', o:'07', t:'设备树', h:1, f:'docs/course-37.html' }
      ]},
      { key:'detail', items:[
        { n:'07.06', o:'01', t:'ARM 架构与 Cortex-A7', h:5, f:'docs/course-th07.html', p:'07.01' },
        { n:'07.07', o:'03', t:'总线体系：AXI / AHB / APB 与 I2C / SPI / CAN', h:4, f:'docs/course-th10.html', p:'07.02' },
        { n:'07.08', o:'04', t:'时钟树、复位、电源域、RTC 与看门狗', h:5, f:'docs/course-th11.html' },
        { n:'07.09', o:'05', t:'最小系统必需外设（上）：DDR、中断、定时器、GPIO、UART', h:6, f:'docs/course-th12.html', p:'07.03' },
        { n:'07.10', o:'06', t:'最小系统必需外设（下）：存储、DMA、以太网、USB', h:5, f:'docs/course-th13.html', p:'07.04' },
        { n:'07.11', o:'08', t:'BSP 与设备树原理', h:6, f:'docs/course-th16.html', p:'07.05' }
      ]},
      { key:'lab', items:[
        { n:'07.12', o:'12', t:'互动台：时钟树与门控', h:1, f:'docs/viz-clock-tree.html' },
        { n:'07.13', o:'13', t:'互动台：GPIO 与 IOMUX 配置', h:1, f:'docs/viz-gpio.html' },
        { n:'07.14', o:'14', t:'互动台：中断优先级与抢占', h:1, f:'docs/viz-nvic.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 08 */
  { id:'08', title:'启动链', oldHours:13, sum:68,
    groups:[
      { key:'core', items:[
        { n:'08.01', o:'02', t:'启动链', h:1, f:'docs/course-36.html' },
        { n:'08.02', o:'07', t:'根文件系统', h:1, f:'docs/course-41.html' },
        { n:'08.03', o:'09', t:'做出一块能跑的系统', h:1, f:'docs/course-42.html' }
      ]},
      { key:'detail', items:[
        { n:'08.04', o:'01', t:'从第一个字节开始：BootROM → SPL → U-Boot', h:5, f:'docs/course-th08.html', p:'08.01' },
        { n:'08.05', o:'04', t:'内核怎么起来：head.S → start_kernel → init', h:5, f:'docs/course-th09.html' }
      ]},
      { key:'practice', items:[
        { n:'08.06', o:'03', t:'i.MX6ULL 与启动链路', h:10, f:'docs/course-ch08.html' },
        { n:'08.07', o:'05', t:'U-Boot 与烧写', h:12, f:'docs/course-ch09.html' },
        { n:'08.08', o:'06', t:'内核裁剪与设备树', h:18, f:'docs/course-ch10.html' },
        { n:'08.09', o:'08', t:'根文件系统构建', h:14, f:'docs/course-ch11.html', p:'08.02' }
      ]},
      { key:'lab', items:[
        { n:'08.10', o:'10', t:'互动台：启动链路逐级点亮', h:1, f:'docs/viz-boot.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 09 */
  { id:'09', title:'驱动体系', oldHours:8, sum:45,
    groups:[
      { key:'core', items:[
        { n:'09.01', o:'02', t:'写一个字符设备', h:1, f:'docs/course-45.html' },
        { n:'09.02', o:'03', t:'pinctrl 与 GPIO', h:1, f:'docs/course-46.html' },
        { n:'09.03', o:'04', t:'I2C 设备驱动', h:1, f:'docs/course-47.html' },
        { n:'09.04', o:'05', t:'中断的上半部与下半部', h:1, f:'docs/course-48.html' }
      ]},
      { key:'detail', items:[
        { n:'09.05', o:'01', t:'设备模型与驱动框架', h:4, f:'docs/course-th05.html', p:'09.01' }
      ]},
      { key:'practice', items:[
        { n:'09.06', o:'06', t:'驱动开发入门', h:20, f:'docs/course-ch12.html' }
      ]},
      { key:'deep', items:[
        { n:'09.07', o:'07', t:'platform 总线模型：probe、匹配、资源与设备树', h:4, f:'docs/d09-01.html' },
        { n:'09.08', o:'08', t:'阻塞 IO 与等待队列：poll / select / epoll 的驱动侧', h:3, f:'docs/d09-02.html' },
        { n:'09.09', o:'09', t:'SPI 子系统：控制器驱动与设备驱动', h:3, f:'docs/d09-03.html' },
        { n:'09.10', o:'10', t:'块设备与 eMMC：gendisk、请求队列与分区', h:4, f:'docs/d09-04.html' },
        { n:'09.11', o:'11', t:'DMA 与 Cache 一致性：谁负责 flush，谁负责 invalidate', h:3, f:'docs/d09-05.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 10 */
  { id:'10', title:'用户态', oldHours:8, sum:8,
    groups:[
      { key:'deep', items:[
        { n:'10.01', o:'01', t:'文件 IO 与 mmap：从 read 到直接映射寄存器', h:2, f:'docs/d10-01.html' },
        { n:'10.02', o:'02', t:'多线程与锁：pthread、条件变量、常见死锁', h:2, f:'docs/d10-02.html' },
        { n:'10.03', o:'03', t:'socket 与 epoll：一个能扛住千连接的事件循环', h:2, f:'docs/d10-03.html' },
        { n:'10.04', o:'04', t:'进程间通信：管道、共享内存、消息队列、信号', h:2, f:'docs/d10-04.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 11 */
  { id:'11', title:'调试与可观测', oldHours:3, sum:20,
    groups:[
      { key:'core', items:[
        { n:'11.01', o:'01', t:'排障方法论', h:1, f:'docs/course-43.html' }
      ]},
      { key:'practice', items:[
        { n:'11.02', o:'02', t:'调试与排障工具箱', h:8, f:'docs/course-ch13.html' }
      ]},
      { key:'deep', items:[
        { n:'11.03', o:'03', t:'oops 现场还原：寄存器、栈回溯、反汇编定位到行', h:3, f:'docs/d11-01.html' },
        { n:'11.04', o:'04', t:'JTAG 与 Ozone：停核、看页表、单步走启动链', h:4, f:'docs/d11-02.html' },
        { n:'11.05', o:'05', t:'ftrace / perf / eBPF：内核里的可观测四件套', h:4, f:'docs/d11-03.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 12 */
  { id:'12', title:'产品化', oldHours:2, sum:36,
    groups:[
      { key:'practice', items:[
        { n:'12.01', o:'01', t:'综合实战项目', h:16, f:'docs/course-ch14.html' }
      ]},
      { key:'deep', items:[
        { n:'12.02', o:'02', t:'Buildroot 到 Yocto：定制镜像、裁剪包、产出固件', h:6, f:'docs/d12-01.html' },
        { n:'12.03', o:'03', t:'分区与双 Bank OTA：A/B 切换、回滚与校验', h:6, f:'docs/d12-02.html' },
        { n:'12.04', o:'04', t:'HAB 安全启动：签名、验签、失败现象', h:4, f:'docs/d12-03.html' },
        { n:'12.05', o:'05', t:'看门狗、电源管理与长时间稳定性测试', h:4, f:'docs/d12-04.html' }
      ]}
    ]},

  /* ---------------------------------------------------------------- 卷 13 */
  { id:'13', title:'拔高', oldHours:1, sum:17,
    groups:[
      { key:'core', items:[
        { n:'13.01', o:'01', t:'总复盘', h:1, f:'docs/course-44.html' }
      ]},
      { key:'deep', items:[
        { n:'13.02', o:'02', t:'AArch64 / RISC-V / x86：三套体系横向对照', h:4, f:'docs/d13-01.html' },
        { n:'13.03', o:'03', t:'xv6 或自制一个最小 OS：把操作系统造一遍', h:8, f:'docs/d13-02.html' },
        { n:'13.04', o:'04', t:'虚拟化与 KVM：ARM 上的 EL2 与 stage-2 页表', h:4, f:'docs/d13-03.html' }
      ]}
    ]}
  ]
};

/* ---------------------------------------------------------------------
   编号规则   n = 卷号 + '.' + 组内顺序，按左栏显示顺序连续编号（07.01 → 07.14）
             o = 旧编号（本卷内的 01..N），仅用于对照，不再显示
   p         同主题配对：详解 → 它所补的那条主线（左栏里缩进挂在主线下面）
   f         真实 PDF 之外的正文地址，docs/ 为唯一真身；course/、ref/ 两个旧目录只保留跳转
   时长 h    来自左侧目录数据里的「约 X 小时」，为阅读时间，不含动手
   --------------------------------------------------------------------- */
