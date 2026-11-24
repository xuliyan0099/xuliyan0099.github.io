/* 适配器 · 方钉插圆孔
 * gcc -std=c11 -Wall -Wextra adapter.c -o adapter
 */
#include <stdio.h>

typedef struct { int radius; } round_hole_t;
typedef struct { int width;  } square_peg_t;

/* 旧接口：只认圆钉 */
static int round_fits(const round_hole_t *h, int peg_radius)
{
    return peg_radius <= h->radius;
}

/* 适配器：把方钉包一层，暴露“半径” */
typedef struct { square_peg_t peg; } square_adapter_t;

static int adapter_radius(const square_adapter_t *a)
{
    /* 方钉对角线一半，才能塞进圆孔 */
    return (a->peg.width * 2) / 3;
}

int main(void)
{
    round_hole_t hole = { 5 };
    square_peg_t small = { 6 };
    square_peg_t big   = { 10 };

    printf("圆孔半径 %d\n", hole.radius);

    square_adapter_t a1 = { small };
    square_adapter_t a2 = { big };
    printf("方钉 6  -> 适配半径 %d -> %s\n", adapter_radius(&a1),
           round_fits(&hole, adapter_radius(&a1)) ? "塞得进" : "塞不进");
    printf("方钉 10 -> 适配半径 %d -> %s\n", adapter_radius(&a2),
           round_fits(&hole, adapter_radius(&a2)) ? "塞得进" : "塞不进");
    return 0;
}
