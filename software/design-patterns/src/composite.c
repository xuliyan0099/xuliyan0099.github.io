/* 组合：一棵诊断树，叶子是零件，枝是分组，遍历代码只写一遍 */
#include <stdio.h>
#include <stddef.h>

typedef struct node node_t;
struct node {
    const char *name;
    int is_leaf;
    int pass;
    node_t *kids[4];
    int nkids;
};

static int run_node(const node_t *nd, int depth)
{
    for (int i = 0; i < depth; i++) printf("  ");
    if (nd->is_leaf) {
        printf("- %-10s %s\n", nd->name, nd->pass ? "PASS" : "FAIL");
        return nd->pass;
    }
    printf("+ %s\n", nd->name);
    int ok = 1;
    for (int i = 0; i < nd->nkids; i++)
        if (!run_node(nd->kids[i], depth + 1)) ok = 0;
    return ok;
}

int main(void)
{
    node_t eng  = { .name = "engine",  .is_leaf = 1, .pass = 1, .kids = {0}, .nkids = 0 };
    node_t gear = { .name = "gearbox", .is_leaf = 1, .pass = 0, .kids = {0}, .nkids = 0 };
    node_t abs  = { .name = "abs",     .is_leaf = 1, .pass = 1, .kids = {0}, .nkids = 0 };
    node_t power = { .name = "powertrain", .is_leaf = 0, .pass = 0, .kids = { &eng, &gear }, .nkids = 2 };
    node_t chassis = { .name = "chassis", .is_leaf = 0, .pass = 0, .kids = { &abs }, .nkids = 1 };
    node_t root = { .name = "vehicle", .is_leaf = 0, .pass = 0, .kids = { &power, &chassis }, .nkids = 2 };

    int ok = run_node(&root, 0);
    printf("整车自检：%s\n", ok ? "PASS" : "FAIL");
    return 0;
}
