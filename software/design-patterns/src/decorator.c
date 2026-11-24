/* 装饰：一条读数流水线，每层只加一件事，顺序可换 */
#include <stdio.h>

typedef struct stage stage_t;
struct stage {
    int (*apply)(stage_t *self, int raw);
    stage_t *inner;   /* 下一层；最底层为 NULL */
    int arg;
};

static int raw_apply(stage_t *self, int raw) { (void)self; return raw; }

static int offset_apply(stage_t *self, int raw)
{
    int v = self->inner->apply(self->inner, raw);
    return v + self->arg;
}
static int clamp_apply(stage_t *self, int raw)
{
    int v = self->inner->apply(self->inner, raw);
    if (v < 0) v = 0;
    if (v > self->arg) v = self->arg;
    return v;
}

int main(void)
{
    stage_t raw   = { raw_apply,   NULL, 0 };
    stage_t off   = { offset_apply, &raw, 5 };
    stage_t clamp = { clamp_apply,  &off, 40 };

    printf("raw       = %d\n", raw.apply(&raw, 42));
    printf("+offset5  = %d\n", off.apply(&off, 42));
    printf("+clamp40  = %d\n", clamp.apply(&clamp, 42));

    stage_t off2   = { offset_apply, &raw, -60 };
    stage_t clamp2 = { clamp_apply,  &off2, 40 };
    printf("负值路径  = %d\n", clamp2.apply(&clamp2, 42));
    printf("三层顺序：raw -> offset -> clamp，换顺序结果会变\n");
    return 0;
}
