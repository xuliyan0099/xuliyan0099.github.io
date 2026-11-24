/* 职责链 · 客服逐级升级
 * gcc -std=c11 -Wall -Wextra chain.c -o chain
 */
#include <stdio.h>

typedef struct handler handler_t;
typedef int (*handle_fn)(int level, const char *msg);

struct handler {
    const char *name;
    int max_level;
    handle_fn fn;
    handler_t *next;
};

static int faq(int level, const char *msg) {
    if (level <= 1) { printf("  FAQ：%s\n", msg); return 1; }
    return 0;
}
static int tech(int level, const char *msg) {
    if (level <= 2) { printf("  技术支持：%s\n", msg); return 1; }
    return 0;
}
static int engineer(int level, const char *msg) {
    printf("  工程师：%s\n", msg); return 1; (void)level;
}

static void dispatch(handler_t *h, int level, const char *msg)
{
    printf("工单 L%d「%s」\n", level, msg);
    for (; h; h = h->next)
        if (h->fn(level, msg)) { printf("  -> %s 接手\n", h->name); return; }
    printf("  没人处理\n");
}

int main(void)
{
    handler_t eng  = { "工程师", 9, engineer, NULL };
    handler_t techh= { "技术支持", 2, tech, &eng };
    handler_t faqh = { "FAQ", 1, faq, &techh };

    dispatch(&faqh, 1, "怎么改密码");
    dispatch(&faqh, 2, "客户端连不上");
    dispatch(&faqh, 3, "服务器 500");
    return 0;
}
