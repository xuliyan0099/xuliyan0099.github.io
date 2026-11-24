/* 工厂方法 · 物流：卡车与轮船
 * gcc -std=c11 -Wall -Wextra factory.c -o factory
 */
#include <stdio.h>
#include <string.h>

typedef struct transport transport_t;
struct transport {
    const char *(*name)(transport_t *);
    void (*deliver)(transport_t *);
};

typedef transport_t *(*creator_t)(void);

typedef struct { transport_t base; } truck_t;
static const char *truck_name(transport_t *t) { (void)t; return "卡车"; }
static void truck_deliver(transport_t *t) { (void)t; puts("  卡车：陆运 200 箱"); }
static transport_t *truck_new(void) {
    static truck_t x = { { truck_name, truck_deliver } };
    return &x.base;
}

typedef struct { transport_t base; } ship_t;
static const char *ship_name(transport_t *t) { (void)t; return "轮船"; }
static void ship_deliver(transport_t *t) { (void)t; puts("  轮船：海运 800 箱"); }
static transport_t *ship_new(void) {
    static ship_t x = { { ship_name, ship_deliver } };
    return &x.base;
}

static const struct { const char *kind; creator_t create; } REG[] = {
    { "truck", truck_new },
    { "ship",  ship_new  },
};

static transport_t *create(const char *kind)
{
    for (unsigned i = 0; i < sizeof REG / sizeof REG[0]; i++)
        if (strcmp(kind, REG[i].kind) == 0)
            return REG[i].create();
    return NULL;
}

int main(void)
{
    const char *want[] = { "truck", "ship", "plane" };
    for (unsigned i = 0; i < 3; i++) {
        transport_t *t = create(want[i]);
        if (!t) { printf("create(\"%s\") -> 未知类型，返回 NULL\n", want[i]); continue; }
        printf("create(\"%s\") -> %s\n", want[i], t->name(t));
        t->deliver(t);
    }
    return 0;
}
