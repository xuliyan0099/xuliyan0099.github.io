/* 桥接 · 形状 × 渲染器
 * gcc -std=c11 -Wall -Wextra bridge.c -o bridge
 */
#include <stdio.h>

typedef struct renderer renderer_t;
struct renderer {
    const char *name;
    void (*circle)(renderer_t *, int);
    void (*square)(renderer_t *, int);
};

typedef struct {
    const char *name;
    int size;
    const renderer_t *r;
} shape_t;

static void shape_draw(const shape_t *s)
{
    printf("[%s] %s size=%d -> ", s->r->name, s->name, s->size);
    if (s->name[0] == 'C') s->r->circle((renderer_t *)s->r, s->size);
    else                   s->r->square((renderer_t *)s->r, s->size);
}

static void vector_circle(renderer_t *r, int s) { (void)r; printf("矢量圆 r=%d\n", s); }
static void vector_square(renderer_t *r, int s) { (void)r; printf("矢量方 w=%d\n", s); }
static renderer_t VECTOR = { "矢量", vector_circle, vector_square };

static void raster_circle(renderer_t *r, int s) { (void)r; printf("位图圆 半径 %dpx\n", s); }
static void raster_square(renderer_t *r, int s) { (void)r; printf("位图方 边长 %dpx\n", s); }
static renderer_t RASTER = { "位图", raster_circle, raster_square };

int main(void)
{
    shape_t shapes[] = {
        { "Circle", 5, &VECTOR },
        { "Square", 5, &VECTOR },
        { "Circle", 5, &RASTER },
        { "Square", 5, &RASTER },
    };
    for (unsigned i = 0; i < 4; i++) shape_draw(&shapes[i]);
    printf("2 种形状 × 2 种渲染器 = 4 种组合，没有 4 个子类\n");
    return 0;
}
