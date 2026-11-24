/* 解释器 · 算术表达式 (2 + 3) * 4
 * gcc -std=c11 -Wall -Wextra interpreter.c -o interpreter
 */
#include <stdio.h>

typedef struct expr expr_t;
struct expr {
    int kind;          /* 0=数字 1=加法 2=乘法 */
    int value;
    expr_t *l, *r;
};

static int eval(const expr_t *e)
{
    switch (e->kind) {
    case 0: return e->value;
    case 1: return eval(e->l) + eval(e->r);
    case 2: return eval(e->l) * eval(e->r);
    }
    return 0;
}

int main(void)
{
    expr_t n2 = { 0, 2, NULL, NULL };
    expr_t n3 = { 0, 3, NULL, NULL };
    expr_t n4 = { 0, 4, NULL, NULL };
    expr_t add = { 1, 0, &n2, &n3 };
    expr_t mul = { 2, 0, &add, &n4 };

    printf("表达式： (2 + 3) * 4\n");
    printf("求值 = %d\n", eval(&mul));
    printf("换成 (2 + 3) * 5 只需换一个叶子，树结构不变\n");
    return 0;
}
