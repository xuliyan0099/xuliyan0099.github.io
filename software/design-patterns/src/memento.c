/* 备忘录 · 撤销快照
 * gcc -std=c11 -Wall -Wextra memento.c -o memento
 */
#include <stdio.h>
#include <string.h>

typedef struct { char text[64]; int cursor; } editor_t;
typedef struct { char text[64]; int cursor; } memento_t;

static memento_t save(const editor_t *e)
{
    memento_t m;
    strcpy(m.text, e->text);
    m.cursor = e->cursor;
    return m;
}

static void restore(editor_t *e, const memento_t *m)
{
    strcpy(e->text, m->text);
    e->cursor = m->cursor;
}

int main(void)
{
    editor_t e = { "hello", 5 };
    printf("初始：\"%s\" cursor=%d\n", e.text, e.cursor);

    memento_t snap = save(&e);

    strcpy(e.text, "hello world");
    e.cursor = 11;
    printf("编辑后：\"%s\" cursor=%d\n", e.text, e.cursor);

    restore(&e, &snap);
    printf("恢复后：\"%s\" cursor=%d\n", e.text, e.cursor);
    printf("快照是值拷贝，编辑过程不会污染它\n");
    return 0;
}
