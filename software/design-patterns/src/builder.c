/* 建造者：把“拼一帧”拆成可检查的步骤，最后一次性交付 */
#include <stdio.h>
#include <stddef.h>

typedef struct {
    unsigned id;
    int dlc;
    unsigned char data[8];
    unsigned crc;
} frame_t;

typedef struct { frame_t f; } builder_t;

static void b_start(builder_t *b)          { b->f.id = 0; b->f.dlc = 0; b->f.crc = 0; }
static void b_id(builder_t *b, unsigned v) { b->f.id = v; }
static void b_data(builder_t *b, const unsigned char *d, int n)
{
    if (n > 8) n = 8;
    b->f.dlc = n;
    for (int i = 0; i < n; i++) b->f.data[i] = d[i];
}
static void b_crc(builder_t *b)
{
    unsigned sum = b->f.id;
    for (int i = 0; i < b->f.dlc; i++) sum += b->f.data[i];
    b->f.crc = sum & 0xFFu;
}
static frame_t b_build(const builder_t *b) { return b->f; }

static void dump(const frame_t *f)
{
    printf("id=0x%X dlc=%d data=[", f->id, f->dlc);
    for (int i = 0; i < f->dlc; i++) printf("%s%02X", i ? " " : "", f->data[i]);
    printf("] crc=0x%02X\n", f->crc);
}

int main(void)
{
    builder_t b;
    unsigned char payload[8] = { 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80 };

    b_start(&b);
    b_id(&b, 0x18FF50E5u);
    b_data(&b, payload, 3);
    b_crc(&b);
    frame_t f1 = b_build(&b);
    printf("frame1 ");
    dump(&f1);

    b_start(&b);                 /* 复用同一个 builder，不残留上一帧 */
    b_id(&b, 0x7DFu);
    b_data(&b, payload, 8);      /* 超长被截到 8 字节 */
    b_crc(&b);
    frame_t f2 = b_build(&b);
    printf("frame2 ");
    dump(&f2);
    printf("两次建造独立：frame1 dlc=%d, frame2 dlc=%d\n", f1.dlc, f2.dlc);
    return 0;
}
