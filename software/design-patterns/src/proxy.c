/* 代理：在真 NVRAM 前加缓存和写穿，读两次只打一次底层 */
#include <stdio.h>

typedef struct {
    int (*read)(int addr);
    void (*write)(int addr, int value);
} nv_t;

static int REAL[16];

static int real_read(int addr)
{
    printf("[NVRAM] read  [%d] = %d\n", addr, REAL[addr]);
    return REAL[addr];
}
static void real_write(int addr, int value)
{
    REAL[addr] = value;
    printf("[NVRAM] write [%d] = %d\n", addr, value);
}

typedef struct {
    nv_t real;
    int cache[16];
    int valid[16];
} proxy_t;

static int proxy_read(nv_t *self, int addr)
{
    proxy_t *p = (proxy_t *)self;      /* nv_t 是 proxy_t 的第一个成员 */
    if (!p->valid[addr]) {
        p->cache[addr] = p->real.read(addr);
        p->valid[addr] = 1;
        printf("[PROXY] cache miss [%d]\n", addr);
    } else {
        printf("[PROXY] cache hit  [%d] = %d\n", addr, p->cache[addr]);
    }
    return p->cache[addr];
}
static void proxy_write(nv_t *self, int addr, int value)
{
    proxy_t *p = (proxy_t *)self;
    p->real.write(addr, value);        /* 写穿：底层一定更新 */
    p->cache[addr] = value;
    p->valid[addr] = 1;
    printf("[PROXY] write-through [%d]\n", addr);
}

int main(void)
{
    proxy_t p = { .real = { real_read, real_write }, .valid = { 0 } };
    REAL[3] = 11;

    printf("read1 = %d\n", proxy_read(&p.real, 3));
    printf("read2 = %d\n", proxy_read(&p.real, 3));
    proxy_write(&p.real, 3, 25);
    printf("read3 = %d\n", proxy_read(&p.real, 3));
    printf("真实存储 [3] = %d\n", REAL[3]);
    return 0;
}
