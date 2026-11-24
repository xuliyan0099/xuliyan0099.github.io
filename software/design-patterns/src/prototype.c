/* 原型：配置先登记，用的时候按名字复制一份，改副本不动原版 */
#include <stdio.h>
#include <string.h>
#include <stddef.h>

typedef struct {
    char name[16];
    int timeout_ms;
    int retry;
} config_t;

typedef struct {
    const char *key;
    config_t proto;
} proto_t;

static proto_t PROTOS[] = {
    { "default", { "default", 500, 3 } },
    { "fast",    { "fast",    120, 1 } },
};

static const proto_t *find_proto(const char *key)
{
    for (size_t i = 0; i < sizeof PROTOS / sizeof PROTOS[0]; i++)
        if (strcmp(PROTOS[i].key, key) == 0) return &PROTOS[i];
    return NULL;
}

static config_t clone(const proto_t *p)
{
    config_t c = p->proto;          /* 结构体整体复制 = 深拷贝（这里没有指针成员） */
    return c;
}

static void dump(const char *tag, const config_t *c)
{
    printf("%-8s name=%-8s timeout=%d retry=%d\n", tag, c->name, c->timeout_ms, c->retry);
}

int main(void)
{
    const proto_t *p = find_proto("fast");
    if (!p) { printf("no prototype\n"); return 1; }

    config_t a = clone(p);
    config_t b = clone(p);
    dump("original", &p->proto);

    b.timeout_ms = 90;              /* 只改副本 */
    strcpy(b.name, "fast-tuned");
    dump("clone-a", &a);
    dump("clone-b", &b);
    dump("original", &p->proto);

    const proto_t *miss = find_proto("slow");
    printf("lookup slow: %s\n", miss ? "found" : "miss");
    printf("克隆 2 份，原型仍 timeout=%d\n", p->proto.timeout_ms);
    return 0;
}
