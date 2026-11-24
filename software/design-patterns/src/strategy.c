/* 策略模式 · C 实现：CAN 发送队列的调度策略
 * 编译：gcc -std=c11 -Wall -Wextra strategy.c -o strategy
 * 策略接口只有一个函数指针，上下文不关心是谁实现。
 */
#include <stdio.h>

typedef struct { int id; int due_ms; } frame_t;

/* 策略 = 一个签名固定的函数指针 */
typedef int (*pick_fn)(const frame_t *q, int n);

typedef struct {
    const char *name;
    pick_fn    pick;
} sched_t;

/* 三个具体策略：都返回「下一个该发哪一帧」的下标 */
static int pick_fifo(const frame_t *q, int n)
{
    (void)q;
    return n > 0 ? 0 : -1;
}

static int pick_edf(const frame_t *q, int n)          /* 最早截止优先 */
{
    int best = -1;
    for (int i = 0; i < n; i++)
        if (best < 0 || q[i].due_ms < q[best].due_ms)
            best = i;
    return best;
}

static int pick_prio(const frame_t *q, int n)         /* CAN ID 越小越优先 */
{
    int best = -1;
    for (int i = 0; i < n; i++)
        if (best < 0 || q[i].id < q[best].id)
            best = i;
    return best;
}

static const sched_t FIFO = { "FIFO", pick_fifo };
static const sched_t EDF  = { "EDF",  pick_edf  };
static const sched_t PRIO = { "PRIO", pick_prio };

/* 上下文：只持有 sched_t 的指针，换策略就是换指针 */
static void drain(const sched_t *s, frame_t *q, int n)
{
    printf("%-5s ->", s->name);
    int left = n;
    while (left > 0) {
        int i = s->pick(q, left);
        if (i < 0) break;
        printf(" %03X", q[i].id);
        for (int k = i; k < left - 1; k++)
            q[k] = q[k + 1];
        left--;
    }
    printf("\n");
}

int main(void)
{
    static const frame_t seed[5] = {
        { 0x210, 10 }, { 0x120, 4 }, { 0x305, 2 }, { 0x180, 8 }, { 0x0A0, 6 }
    };
    frame_t q[5];

    for (int i = 0; i < 5; i++) q[i] = seed[i];
    drain(&FIFO, q, 5);
    for (int i = 0; i < 5; i++) q[i] = seed[i];
    drain(&EDF, q, 5);
    for (int i = 0; i < 5; i++) q[i] = seed[i];
    drain(&PRIO, q, 5);

    printf("sizeof(sched_t)=%u  sizeof(pick_fn)=%u\n",
           (unsigned)sizeof(sched_t), (unsigned)sizeof(pick_fn));
    return 0;
}
