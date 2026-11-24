/* 解释器：把 "TEMP>90 AND RPM<800" 变成小语法树，换环境就能重算 */
#include <stdio.h>

typedef struct ctx { int temp; int rpm; } ctx_t;

typedef struct expr expr_t;
typedef enum { E_CMP, E_AND, E_OR } kind_t;

struct expr {
    kind_t kind;
    int var;        /* 0=temp 1=rpm，仅 CMP 用 */
    int op;         /* 0='>' 1='<' */
    int value;
    const expr_t *l;
    const expr_t *r;
};

static int eval(const expr_t *e, const ctx_t *c)
{
    switch (e->kind) {
        case E_CMP: {
            int v = e->var == 0 ? c->temp : c->rpm;
            return e->op == 0 ? v > e->value : v < e->value;
        }
        case E_AND: return eval(e->l, c) && eval(e->r, c);
        case E_OR:  return eval(e->l, c) || eval(e->r, c);
    }
    return 0;
}

int main(void)
{
    /* 等价于 TEMP>90 AND RPM<800 */
    const expr_t t90  = { .kind = E_CMP, .var = 0, .op = 0, .value = 90 };
    const expr_t r800 = { .kind = E_CMP, .var = 1, .op = 1, .value = 800 };
    const expr_t all  = { .kind = E_AND, .l = &t90, .r = &r800 };

    ctx_t hot  = { 105, 700 };   /* 超温且转速没上来 */
    ctx_t idle = { 88,  650 };
    ctx_t fast = { 95,  900 };

    printf("hot  temp=%d rpm=%d -> %s\n", hot.temp, hot.rpm, eval(&all, &hot) ? "报警" : "正常");
    printf("idle temp=%d rpm=%d -> %s\n", idle.temp, idle.rpm, eval(&all, &idle) ? "报警" : "正常");
    printf("fast temp=%d rpm=%d -> %s\n", fast.temp, fast.rpm, eval(&all, &fast) ? "报警" : "正常");
    printf("同一棵树，三组输入，不需要重新解析\n");
    return 0;
}
