/* 建造者 · 一步步盖房子
 * gcc -std=c11 -Wall -Wextra builder.c -o builder
 */
#include <stdio.h>

typedef struct {
    int walls, doors, windows;
    int has_roof;
} house_t;

static void add_walls(house_t *h, int n)   { h->walls = n;   printf("  砌 %d 面墙\n", n); }
static void add_doors(house_t *h, int n)   { h->doors = n;   printf("  装 %d 扇门\n", n); }
static void add_windows(house_t *h, int n) { h->windows = n; printf("  装 %d 扇窗\n", n); }
static void add_roof(house_t *h)           { h->has_roof = 1; printf("  封顶\n"); }

static int build(const house_t *h)
{
    if (h->walls < 4 || h->doors < 1 || h->windows < 1 || !h->has_roof) {
        printf("  校验失败：房子还不完整\n");
        return -1;
    }
    printf("  交付：%d 墙 / %d 门 / %d 窗 / 有屋顶\n",
           h->walls, h->doors, h->windows);
    return 0;
}

int main(void)
{
    house_t h = { 0, 0, 0, 0 };
    printf("普通小屋：\n");
    add_walls(&h, 4); add_doors(&h, 1); add_windows(&h, 2); add_roof(&h);
    build(&h);

    house_t v = { 0, 0, 0, 0 };
    printf("缺步骤的房子：\n");
    add_walls(&v, 4); add_doors(&v, 1);
    build(&v);
    return 0;
}
