/* 访问者 · 文件统计
 * gcc -std=c11 -Wall -Wextra visitor.c -o visitor
 */
#include <stdio.h>

typedef struct visitor visitor_t;
typedef struct node node_t;

struct node {
    char name[16];
    int is_dir;
    int size;
    node_t *kids[3];
    int nkids;
    void (*accept)(node_t *, visitor_t *);
};

struct visitor {
    int files;
    int total;
    void (*visit_file)(visitor_t *, const node_t *);
    void (*visit_dir)(visitor_t *, const node_t *);
};

static void file_accept(node_t *n, visitor_t *v) { v->visit_file(v, n); }
static void dir_accept(node_t *n, visitor_t *v)  { v->visit_dir(v, n); }

static void count_file(visitor_t *v, const node_t *n)
{
    v->files++; v->total += n->size;
    printf("  文件 %s (%d 字节)\n", n->name, n->size);
}
static void enter_dir(visitor_t *v, const node_t *n)
{
    printf("  进入目录 %s\n", n->name);
    (void)v;
}

int main(void)
{
    node_t a = { "a.c", 0, 120, { 0 }, 0, file_accept };
    node_t b = { "b.c", 0, 80,  { 0 }, 0, file_accept };
    node_t d = { "src", 1, 0, { &a, &b, NULL }, 2, dir_accept };
    node_t r = { "root", 1, 0, { &d, NULL, NULL }, 1, dir_accept };

    visitor_t v = { 0, 0, count_file, enter_dir };

    r.accept(&r, &v);
    d.accept(&d, &v);
    a.accept(&a, &v);
    b.accept(&b, &v);

    printf("统计：%d 个文件，%d 字节\n", v.files, v.total);
    printf("节点只负责 accept，统计逻辑在 visitor 里\n");
    return 0;
}
