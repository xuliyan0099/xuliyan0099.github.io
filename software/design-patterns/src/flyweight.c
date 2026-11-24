/* 享元：1000 个信号共用 8 份单位描述，只存指针 */
#include <stdio.h>
#include <string.h>
#include <stddef.h>

typedef struct {
    const char *unit;
    double scale;
} sig_t;

typedef struct {
    sig_t pool[8];
    int n;
} registry_t;

static const sig_t *intern(registry_t *r, const char *unit, double scale)
{
    for (int i = 0; i < r->n; i++)
        if (strcmp(r->pool[i].unit, unit) == 0) return &r->pool[i];
    if (r->n >= 8) return NULL;
    r->pool[r->n].unit = unit;
    r->pool[r->n].scale = scale;
    return &r->pool[r->n++];
}

int main(void)
{
    static const char *UNITS[] = { "C", "kPa", "rpm", "%", "V", "A", "km/h", "deg" };
    registry_t reg = { .n = 0 };
    const sig_t *signals[1000];

    size_t nu = sizeof UNITS / sizeof UNITS[0];
    for (size_t i = 0; i < 1000; i++)
        signals[i] = intern(&reg, UNITS[i % nu], 1.0 + (double)(i % nu) / 10.0);

    printf("信号 1000 个，描述池 %d 份\n", reg.n);
    printf("sig[0]   unit=%-4s scale=%.1f\n", signals[0]->unit, signals[0]->scale);
    printf("sig[7]   unit=%-4s scale=%.1f\n", signals[7]->unit, signals[7]->scale);
    printf("sig[999] unit=%-4s scale=%.1f\n", signals[999]->unit, signals[999]->scale);
    printf("指针相同：sig[0]==sig[8] -> %s\n", signals[0] == signals[8] ? "yes" : "no");
    return 0;
}
