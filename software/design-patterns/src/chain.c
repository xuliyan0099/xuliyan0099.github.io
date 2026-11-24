/* 责任链模式 · C 实现：报文过滤管道
 * 编译：gcc -std=c11 -Wall -Wextra chain.c -o chain
 * 每个处理器返回 0 = 放行给下一个，1 = 就地终止。
 */
#include <stdio.h>

typedef struct { int id; int len; unsigned char crc; } frame_t;

typedef struct handler handler_t;
typedef struct {
    int (*handle)(handler_t *self, const frame_t *f);
} handler_ops_t;

struct handler {
    const handler_ops_t *ops;
    handler_t           *next;
    const char          *name;
};

/* ① 长度检查 */
static int len_handle(handler_t *h, const frame_t *f)
{
    if (f->len != 8) {
        printf("  [%s] 丢弃 0x%03X：长度 %d != 8\n", h->name, f->id, f->len);
        return 1;
    }
    printf("  [%s] 通过\n", h->name);
    return h->next ? h->next->ops->handle(h->next, f) : 0;
}

/* ② CRC：约定 crc = 高字节 ^ 低字节 ^ 长度 */
static int crc_handle(handler_t *h, const frame_t *f)
{
    unsigned char want = (unsigned char)(((f->id >> 8) & 0xFF) ^ (f->id & 0xFF) ^ f->len);
    if (f->crc != want) {
        printf("  [%s] 丢弃 0x%03X：crc=%02X，应为 %02X\n", h->name, f->id, f->crc, want);
        return 1;
    }
    printf("  [%s] 通过\n", h->name);
    return h->next ? h->next->ops->handle(h->next, f) : 0;
}

/* ③ 白名单：只收 0x100 / 0x2A0 */
static int white_handle(handler_t *h, const frame_t *f)
{
    if (!(f->id == 0x100 || f->id == 0x2A0)) {
        printf("  [%s] 丢弃 0x%03X：不在白名单\n", h->name, f->id);
        return 1;
    }
    printf("  [%s] 通过\n", h->name);
    return h->next ? h->next->ops->handle(h->next, f) : 0;
}

/* ④ 业务处理：链尾 */
static int app_handle(handler_t *h, const frame_t *f)
{
    printf("  [%s] 已消费 0x%03X\n", h->name, f->id);
    return 1;
}

static const handler_ops_t LEN_OPS   = { len_handle };
static const handler_ops_t CRC_OPS   = { crc_handle };
static const handler_ops_t WHITE_OPS = { white_handle };
static const handler_ops_t APP_OPS   = { app_handle };

int main(void)
{
    handler_t h_app   = { &APP_OPS,   NULL, "app"   };
    handler_t h_white = { &WHITE_OPS, &h_app, "white" };
    handler_t h_crc   = { &CRC_OPS,   &h_white, "crc" };
    handler_t h_len   = { &LEN_OPS,   &h_crc, "len" };

    static const frame_t frames[] = {
        { 0x100, 7, 0x09 },   /* 长度错 */
        { 0x100, 8, 0x00 },   /* crc 错 */
        { 0x500, 8, 0x0D },   /* 不在白名单 */
        { 0x100, 8, 0x09 }    /* 全部通过 */
    };

    for (unsigned i = 0; i < sizeof frames / sizeof frames[0]; i++) {
        printf("frame 0x%03X len=%d crc=%02X\n", frames[i].id, frames[i].len, frames[i].crc);
        h_len.ops->handle(&h_len, &frames[i]);
    }
    return 0;
}
