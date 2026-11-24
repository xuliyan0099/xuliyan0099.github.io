/* 策略 · 排序策略
 * gcc -std=c11 -Wall -Wextra strategy.c -o strategy
 */
#include <stdio.h>

typedef void (*sort_fn)(int *, int);

static void bubble(int *a, int n)
{
    for (int i = 0; i < n; i++)
        for (int j = 0; j + 1 < n - i; j++)
            if (a[j] > a[j + 1]) { int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; }
}

static void insertion(int *a, int n)
{
    for (int i = 1; i < n; i++) {
        int key = a[i], j = i - 1;
        while (j >= 0 && a[j] > key) { a[j + 1] = a[j]; j--; }
        a[j + 1] = key;
    }
}

static void run(const char *name, sort_fn fn, int *src, int n)
{
    int a[8];
    for (int i = 0; i < n; i++) a[i] = src[i];
    fn(a, n);
    printf("%s：", name);
    for (int i = 0; i < n; i++) printf(" %d", a[i]);
    printf("\n");
}

int main(void)
{
    int src[] = { 5, 1, 4, 2, 3 };
    run("冒泡", bubble, src, 5);
    run("插入", insertion, src, 5);
    printf("排序函数是参数，换策略不改调用方\n");
    return 0;
}
