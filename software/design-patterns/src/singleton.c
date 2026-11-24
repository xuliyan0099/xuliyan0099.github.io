/* 单例 · 全局配置
 * gcc -std=c11 -Wall -Wextra singleton.c -o singleton
 */
#include <stdio.h>
#include <string.h>

typedef struct {
    char theme[16];
    int  font_size;
} config_t;

static config_t *instance(void)
{
    static config_t cfg = { "light", 12 };
    static int inited = 0;
    if (!inited) {
        inited = 1;
        printf("  初始化配置（只发生一次）\n");
    }
    return &cfg;
}

int main(void)
{
    config_t *a = instance();
    config_t *b = instance();
    config_t *c = instance();

    printf("取三次实例：%p %p %p（同一个地址）\n", (void *)a, (void *)b, (void *)c);

    strcpy(a->theme, "dark");
    a->font_size = 16;
    printf("通过 a 改成 %s/%d，通过 c 读：%s/%d\n",
           a->theme, a->font_size, c->theme, c->font_size);
    return 0;
}
