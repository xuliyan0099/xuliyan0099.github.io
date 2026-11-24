/* 装饰器 · 给文本加粗、加斜体
 * gcc -std=c11 -Wall -Wextra decorator.c -o decorator
 */
#include <stdio.h>
#include <string.h>

typedef struct { char text[96]; } text_t;

static text_t bold(text_t t)
{
    text_t out;
    snprintf(out.text, sizeof out.text, "<b>%.*s</b>", (int)(sizeof out.text - 9), t.text);
    return out;
}

static text_t italic(text_t t)
{
    text_t out;
    snprintf(out.text, sizeof out.text, "<i>%.*s</i>", (int)(sizeof out.text - 9), t.text);
    return out;
}

int main(void)
{
    text_t t = { "hello" };
    printf("原始：%s\n", t.text);

    text_t b = bold(t);
    printf("加粗：%s\n", b.text);

    text_t bi = italic(b);
    printf("加粗+斜体：%s\n", bi.text);

    text_t ib = bold(italic(t));
    printf("顺序反过来：%s\n", ib.text);
    return 0;
}
