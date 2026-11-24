/* 观察者模式 · C 实现：采样总线 + 订阅者表
 * 编译：gcc -std=c11 -Wall -Wextra observer.c -o observer
 * 重点演示「在回调里退订」这一经典崩溃/漏发点。
 */
#include <stdio.h>
#include <string.h>

typedef void (*cb_fn)(void *ctx, const char *event);

typedef struct {
    int   id;            /* -1 表示墓碑：通知中被退订，等通知结束再压缩 */
    char  name[20];
    cb_fn fn;
    void *ctx;
} sub_t;

typedef struct {
    sub_t slot[8];
    int   n;
    int   depth;         /* 正在通知的层数 */
} bus_t;

typedef struct { bus_t *bus; int id; } peer_t;

static void bus_attach(bus_t *b, int id, const char *name, cb_fn fn, void *ctx)
{
    if (b->n >= 8) return;
    b->slot[b->n].id = id;
    snprintf(b->slot[b->n].name, sizeof b->slot[b->n].name, "%s", name);
    b->slot[b->n].fn = fn;
    b->slot[b->n].ctx = ctx;
    b->n++;
}

static void bus_compact(bus_t *b)
{
    int w = 0;
    for (int i = 0; i < b->n; i++)
        if (b->slot[i].id >= 0) b->slot[w++] = b->slot[i];
    b->n = w;
}

/* 朴素实现：立刻前移数组 */
static void bus_detach_raw(bus_t *b, int id)
{
    for (int i = 0; i < b->n; i++)
        if (b->slot[i].id == id) {
            for (int k = i; k < b->n - 1; k++) b->slot[k] = b->slot[k + 1];
            b->n--;                     /* 没有 i--，外层循环下一次就跳过了一个 */
            return;
        }
}

/* 朴素通知：边遍历边让 b->n 变化 */
static void bus_notify_raw(bus_t *b, const char *ev)
{
    for (int i = 0; i < b->n; i++)
        b->slot[i].fn(b->slot[i].ctx, ev);
}

/* 安全实现：通知中只打墓碑，不移动元素 */
static void bus_detach_safe(bus_t *b, int id)
{
    int i;
    for (i = 0; i < b->n; i++) if (b->slot[i].id == id) break;
    if (i == b->n) return;
    if (b->depth > 0) { b->slot[i].id = -1; return; }
    for (int k = i; k < b->n - 1; k++) b->slot[k] = b->slot[k + 1];
    b->n--;
}

/* 安全通知：先拍 id 快照，再按 id 找还活着的槽 */
static void bus_notify_safe(bus_t *b, const char *ev)
{
    int ids[8];
    int m = b->n;
    for (int i = 0; i < m; i++) ids[i] = b->slot[i].id;

    b->depth++;
    for (int i = 0; i < m; i++) {
        for (int k = 0; k < b->n; k++)
            if (b->slot[k].id == ids[i]) {
                b->slot[k].fn(b->slot[k].ctx, ev);
                break;
            }
    }
    b->depth--;
    if (b->depth == 0) bus_compact(b);
}

/* 三个订阅者 */
static void cb_gauge(void *ctx, const char *ev)
{
    (void)ctx;
    printf("  gauge    <- %s\n", ev);
}

static void cb_diag(void *ctx, const char *ev)
{
    (void)ctx;
    printf("  diag     <- %s\n", ev);
}

static void cb_recorder_raw(void *ctx, const char *ev)
{
    peer_t *p = ctx;
    printf("  recorder <- %s（收到后退订自己）\n", ev);
    bus_detach_raw(p->bus, p->id);
}

static void cb_recorder_safe(void *ctx, const char *ev)
{
    peer_t *p = ctx;
    printf("  recorder <- %s（收到后退订自己）\n", ev);
    bus_detach_safe(p->bus, p->id);
}

int main(void)
{
    bus_t raw = { .n = 0, .depth = 0 };
    bus_t safe = { .n = 0, .depth = 0 };
    peer_t r1 = { &raw, 2 }, r2 = { &safe, 2 };

    printf("朴素版本：\n");
    bus_attach(&raw, 1, "gauge", cb_gauge, NULL);
    bus_attach(&raw, 2, "recorder", cb_recorder_raw, &r1);
    bus_attach(&raw, 3, "diag", cb_diag, NULL);
    bus_notify_raw(&raw, "speed=62");
    printf("  剩余订阅者=%d（diag 被跳过）\n\n", raw.n);

    printf("安全版本：\n");
    bus_attach(&safe, 1, "gauge", cb_gauge, NULL);
    bus_attach(&safe, 2, "recorder", cb_recorder_safe, &r2);
    bus_attach(&safe, 3, "diag", cb_diag, NULL);
    bus_notify_safe(&safe, "speed=62");
    bus_notify_safe(&safe, "speed=63");
    printf("  剩余订阅者=%d\n", safe.n);
    return 0;
}
