/* 命令 · 编辑器撤销
 * gcc -std=c11 -Wall -Wextra command.c -o command
 */
#include <stdio.h>
#include <string.h>

typedef struct { char text[64]; int len; } editor_t;

typedef struct { int kind; char ch; } cmd_t;   /* 0=追加 1=删除 */

static void apply(editor_t *e, cmd_t c)
{
    if (c.kind == 0 && e->len < 63) e->text[e->len++] = c.ch, e->text[e->len] = 0;
    else if (c.kind == 1 && e->len > 0) e->text[--e->len] = 0;
}

static void undo(editor_t *e, cmd_t c)
{
    if (c.kind == 0) { if (e->len > 0) e->text[--e->len] = 0; }
    else             { if (e->len < 63) e->text[e->len++] = c.ch, e->text[e->len] = 0; }
}

int main(void)
{
    editor_t e = { "", 0 };
    cmd_t history[16];
    int n = 0;

    cmd_t a = { 0, 'H' }, b = { 0, 'i' }, c = { 0, '!' };
    apply(&e, history[n++] = a);
    apply(&e, history[n++] = b);
    apply(&e, history[n++] = c);
    printf("输入三个命令后：\"%s\"（len=%d）\n", e.text, e.len);

    for (int i = 0; i < 2; i++) {
        undo(&e, history[--n]);
        printf("撤销一步：\"%s\"\n", e.text);
    }
    return 0;
}
