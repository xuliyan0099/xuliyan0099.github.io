/* 迭代器 · 遍历数组集合
 * gcc -std=c11 -Wall -Wextra iterator.c -o iterator
 */
#include <stdio.h>

typedef struct {
    const int *data;
    int n;
    int i;
} iter_t;

static void iter_init(iter_t *it, const int *data, int n)
{
    it->data = data; it->n = n; it->i = 0;
}

static const int *iter_next(iter_t *it)
{
    if (it->i >= it->n) return NULL;
    return &it->data[it->i++];
}

int main(void)
{
    int nums[] = { 10, 20, 30, 40, 50 };
    iter_t it;
    iter_init(&it, nums, 5);

    const int *p;
    int sum = 0;
    while ((p = iter_next(&it)) != NULL) {
        printf("  取到 %d\n", *p);
        sum += *p;
    }
    printf("总和 = %d\n", sum);
    printf("调用方没有用到下标，换链表也不用改这里\n");
    return 0;
}
