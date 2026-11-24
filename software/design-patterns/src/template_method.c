/* 模板方法：自检顺序固定，每一步换成具体实现 */
#include <stdio.h>

typedef struct {
    const char *name;
    int (*power)(void);
    int (*comm)(void);
    int (*sensor)(void);
} selftest_t;

/* 骨架：顺序不可改，任何一步失败立即中止 */
static int run(const selftest_t *t)
{
    printf("== %s ==\n", t->name);
    printf("step1 power  ... ");
    if (!t->power())  { printf("FAIL\n"); return 0; }
    printf("OK\n");

    printf("step2 comm   ... ");
    if (!t->comm())   { printf("FAIL\n"); return 0; }
    printf("OK\n");

    printf("step3 sensor ... ");
    if (!t->sensor()) { printf("FAIL\n"); return 0; }
    printf("OK\n");

    printf("result PASS\n");
    return 1;
}

static int p_ok(void)  { return 1; }
static int c_ok(void)  { return 1; }
static int s_ok(void)  { return 1; }
static int s_bad(void) { return 0; }

int main(void)
{
    const selftest_t bench = { "bench",  p_ok, c_ok, s_ok };
    const selftest_t field = { "field",  p_ok, c_ok, s_bad };

    run(&bench);
    run(&field);
    printf("两个变体共用同一套顺序与日志\n");
    return 0;
}
