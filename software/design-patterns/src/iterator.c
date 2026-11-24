/* 迭代器：调用方只拿 next()，看不到故障表是数组还是链表 */
#include <stdio.h>
#include <stddef.h>

typedef struct {
    int code;
    const char *name;
} fault_t;

static const fault_t FAULTS[] = {
    { 0,  "none" },
    { 17, "O2 heater" },
    { 0,  "none" },
    { 42, "misfire" },
    { 91, "CAN bus off" },
};

typedef struct {
    const fault_t *arr;
    int n;
    int i;
} fault_iter_t;

static void iter_init(fault_iter_t *it, const fault_t *arr, int n)
{
    it->arr = arr; it->n = n; it->i = 0;
}

/* 只返回有效故障；返回 NULL 表示遍历结束 */
static const fault_t *iter_next(fault_iter_t *it)
{
    while (it->i < it->n) {
        const fault_t *f = &it->arr[it->i++];
        if (f->code != 0) return f;
    }
    return NULL;
}

int main(void)
{
    fault_iter_t it;
    iter_init(&it, FAULTS, (int)(sizeof FAULTS / sizeof FAULTS[0]));

    const fault_t *f;
    int count = 0;
    while ((f = iter_next(&it)) != NULL) {
        printf("fault #%d code=%d %s\n", ++count, f->code, f->name);
    }
    printf("有效故障 %d 条，全部遍历完\n", count);
    return 0;
}
