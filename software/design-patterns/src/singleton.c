/* 单例模式 · C 实现：进程内唯一的配置对象
 * 编译：gcc -std=c11 -Wall -Wextra singleton.c -o singleton
 * 注意：这段只保证「唯一」，不保证「多线程安全」，线程版见页面说明。
 */
#include <stdio.h>

typedef struct { int timeout_ms; int log_level; } config_t;

static config_t g_cfg;
static int      g_ready = 0;
static unsigned g_calls = 0;
static unsigned g_inits = 0;

config_t *config_instance(void)
{
    g_calls++;
    if (!g_ready) {
        g_cfg.timeout_ms = 500;
        g_cfg.log_level  = 2;
        g_ready = 1;
        g_inits++;
    }
    return &g_cfg;
}

void config_reset_for_test(void)
{
    g_ready = 0;
    printf("  reset：下次访问会重新初始化\n");
}

unsigned config_calls(void) { return g_calls; }
unsigned config_inits(void) { return g_inits; }

int main(void)
{
    config_t *a = config_instance();
    config_t *b = config_instance();
    config_t *c = config_instance();

    printf("三次取实例是同一个对象：%s\n", (a == b && b == c) ? "是" : "否");
    printf("访问 %u 次，只初始化 %u 次\n", config_calls(), config_inits());

    a->timeout_ms = 800;
    printf("通过 a 改，通过 b 读：timeout=%d\n", b->timeout_ms);

    config_reset_for_test();
    printf("reset 后 timeout=%d（测试用例之间互相污染）\n", config_instance()->timeout_ms);
    printf("reset 后初始化次数=%u\n", config_inits());
    return 0;
}
