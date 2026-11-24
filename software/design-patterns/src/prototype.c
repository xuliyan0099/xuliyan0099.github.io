/* 原型 · 克隆图形
 * gcc -std=c11 -Wall -Wextra prototype.c -o prototype
 */
#include <stdio.h>
#include <string.h>

typedef struct shape shape_t;
struct shape {
    const char *kind;
    int size;
    void (*clone)(const shape_t *, shape_t *out);
};

static void circle_clone(const shape_t *s, shape_t *out) { *out = *s; }
static void square_clone(const shape_t *s, shape_t *out) { *out = *s; }

static shape_t CIRCLE = { "圆", 10, circle_clone };
static shape_t SQUARE = { "方", 10, square_clone };

static shape_t *registry(const char *kind)
{
    if (strcmp(kind, "circle") == 0) return &CIRCLE;
    if (strcmp(kind, "square") == 0) return &SQUARE;
    return NULL;
}

int main(void)
{
    shape_t a, b;
    registry("circle")->clone(&CIRCLE, &a);
    registry("circle")->clone(&CIRCLE, &b);
    printf("克隆两份圆：a.size=%d  b.size=%d\n", a.size, b.size);

    b.size = 25;
    printf("改 b 之后：a.size=%d  b.size=%d（互不影响）\n", a.size, b.size);
    printf("原型仍是 size=%d\n", CIRCLE.size);
    return 0;
}
