/* 享元 · 森林共享树型
 * gcc -std=c11 -Wall -Wextra flyweight.c -o flyweight
 */
#include <stdio.h>
#include <string.h>

typedef struct {
    char name[16];
    int  leaf_color;
} tree_type_t;

typedef struct {
    const tree_type_t *type;   /* 共享内部状态 */
    int x, y;                  /* 外部状态 */
} tree_t;

static tree_type_t TYPES[2] = {
    { "橡树", 0x2E7D32 },
    { "松树", 0x1B5E20 },
};

static const tree_type_t *get_type(const char *name)
{
    for (unsigned i = 0; i < 2; i++)
        if (strcmp(TYPES[i].name, name) == 0) return &TYPES[i];
    return NULL;
}

int main(void)
{
    tree_t forest[1000];
    int n = 0;
    for (int i = 0; i < 1000; i++) {
        forest[n].type = get_type(i % 2 ? "松树" : "橡树");
        forest[n].x = i * 3;
        forest[n].y = i * 5;
        n++;
    }

    printf("1000 棵树，共享 %d 份树型描述\n", 2);
    printf("%s x=%d y=%d color=0x%06X\n",
           forest[0].type->name, forest[0].x, forest[0].y, forest[0].type->leaf_color);
    printf("%s x=%d y=%d color=0x%06X\n",
           forest[999].type->name, forest[999].x, forest[999].y, forest[999].type->leaf_color);
    printf("每棵树只多存 2 个坐标，不复制颜色和名字\n");
    return 0;
}
