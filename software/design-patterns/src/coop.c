/* C 的面向对象地基：vtable + 结构体内嵌 + 指针还原
 * 编译：gcc -std=c11 -Wall -Wextra coop.c -o coop
 * 这段是所有 C 版设计模式的地基。
 */
#include <stddef.h>
#include <stdio.h>

typedef struct shape shape_t;

/* 虚函数表：一个结构体，里面全是函数指针 */
typedef struct {
    double      (*area)(const shape_t *self);
    const char *(*name)(const shape_t *self);
} shape_ops_t;

/* 基类：只有一个 vptr，布局与 C++ 的「有虚函数的类」一致 */
struct shape { const shape_ops_t *vptr; };

typedef struct { shape_t base; double w, h; } rect_t;
typedef struct { shape_t base; double r; }     circle_t;

static double rect_area(const shape_t *s) { const rect_t *r = (const rect_t *)s; return r->w * r->h; }
static const char *rect_name(const shape_t *s) { (void)s; return "rect"; }
static double circle_area(const shape_t *s) { const circle_t *c = (const circle_t *)s; return 3.14159 * c->r * c->r; }
static const char *circle_name(const shape_t *s) { (void)s; return "circle"; }

static const shape_ops_t RECT_OPS   = { rect_area, rect_name };
static const shape_ops_t CIRCLE_OPS = { circle_area, circle_name };

int main(void)
{
    rect_t   r = { { &RECT_OPS }, 3.0, 4.0 };   /* base 必须是第一个成员 */
    circle_t c = { { &CIRCLE_OPS }, 1.0 };

    /* 同一个接口，两种实现：动态分派发生在 vptr->area 这一跳 */
    const shape_t *shapes[] = { (const shape_t *)&r, (const shape_t *)&c };
    for (int i = 0; i < 2; i++) {
        const shape_t *s = shapes[i];
        printf("%-6s area=%6.2f  vptr=%s\n", s->vptr->name(s), s->vptr->area(s),
               s->vptr == &RECT_OPS ? "RECT_OPS" : "CIRCLE_OPS");
    }

    printf("offsetof(shape_t,vptr)=%u  sizeof(shape_t)=%u\n",
           (unsigned)offsetof(shape_t, vptr), (unsigned)sizeof(shape_t));
    printf("sizeof(rect_t)=%u  sizeof(circle_t)=%u\n",
           (unsigned)sizeof(rect_t), (unsigned)sizeof(circle_t));
    printf("把 rect_t* 当 shape_t* 用是合法的：base 在偏移 0\n");
    return 0;
}
