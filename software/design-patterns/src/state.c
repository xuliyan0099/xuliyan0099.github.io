/* 状态 · 订单状态流转
 * gcc -std=c11 -Wall -Wextra state.c -o state
 */
#include <stdio.h>

typedef enum { NEW, PAID, SHIPPED, DONE } state_t;

static const char *name(state_t s)
{
    static const char *N[] = { "新建", "已支付", "已发货", "已完成" };
    return N[s];
}

static state_t next(state_t s, const char *event, int *ok)
{
    *ok = 1;
    if (s == NEW     && event[0] == 'p') return PAID;
    if (s == PAID    && event[0] == 's') return SHIPPED;
    if (s == SHIPPED && event[0] == 'd') return DONE;
    *ok = 0;
    return s;
}

int main(void)
{
    state_t s = NEW;
    const char *events[] = { "pay", "pay", "ship", "done" };
    for (unsigned i = 0; i < 4; i++) {
        int ok;
        state_t n = next(s, events[i], &ok);
        if (!ok) printf("%s 状态下 %s 被拒绝\n", name(s), events[i]);
        else     printf("%s -> %s（%s）\n", name(s), name(n), events[i]);
        s = n;
    }
    return 0;
}
