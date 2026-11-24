/* 备忘录：改标定之前先存一份，出事能原样退回 */
#include <stdio.h>

typedef struct {
    int gain;
    int offset;
    int mode;
} calib_t;

typedef struct { calib_t snap; } memento_t;

static memento_t save(const calib_t *c)
{
    memento_t m = { *c };
    return m;
}
static void restore(calib_t *c, const memento_t *m)
{
    *c = m->snap;
}

static void dump(const char *tag, const calib_t *c)
{
    printf("%-9s gain=%d offset=%d mode=%d\n", tag, c->gain, c->offset, c->mode);
}

int main(void)
{
    calib_t ecu = { 12, 0, 1 };
    dump("before", &ecu);

    memento_t m = save(&ecu);

    ecu.gain = 30;          /* 现场调参，调坏了 */
    ecu.offset = -8;
    ecu.mode = 3;
    dump("tuned", &ecu);

    restore(&ecu, &m);
    dump("restored", &ecu);
    printf("快照是值拷贝：之后改 ecu 不会污染 memento\n");
    return 0;
}
