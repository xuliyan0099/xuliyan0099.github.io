/* 组合 · 文件与文件夹
 * gcc -std=c11 -Wall -Wextra composite.c -o composite
 */
#include <stdio.h>
#include <string.h>

typedef struct node node_t;
struct node {
    char name[16];
    int  is_dir;
    int  size;                 /* 文件大小；目录忽略 */
    node_t *kids[4];
    int  nkids;
};

static node_t *add(node_t *dir, node_t *kid)
{
    if (dir->nkids < 4) dir->kids[dir->nkids++] = kid;
    return dir;
}

static int total(const node_t *n)
{
    if (!n->is_dir) return n->size;
    int sum = 0;
    for (int i = 0; i < n->nkids; i++) sum += total(n->kids[i]);
    return sum;
}

static void list(const node_t *n, int depth)
{
    for (int i = 0; i < depth; i++) printf("  ");
    printf("%s%s\n", n->is_dir ? "[D] " : "    ", n->name);
    if (n->is_dir)
        for (int i = 0; i < n->nkids; i++) list(n->kids[i], depth + 1);
}

int main(void)
{
    node_t root = { "root", 1, 0, { 0 }, 0 };
    node_t src  = { "src",  1, 0, { 0 }, 0 };
    node_t a    = { "a.c",  0, 120, { 0 }, 0 };
    node_t b    = { "b.c",  0, 80,  { 0 }, 0 };
    node_t read = { "README", 0, 10, { 0 }, 0 };

    add(&src, &a); add(&src, &b);
    add(&root, &src); add(&root, &read);

    list(&root, 0);
    printf("总大小 = %d 字节\n", total(&root));
    return 0;
}
