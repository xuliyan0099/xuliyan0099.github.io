/* 访问者：节点只负责 accept，统计逻辑放在 visitor 里 */
#include <stdio.h>

typedef struct visitor visitor_t;
typedef struct node node_t;

struct node {
    const char *name;
    int kind;              /* 0=ECU 1=SENSOR 2=ACTUATOR */
    void (*accept)(node_t *self, visitor_t *v);
};

struct visitor {
    int ecus, sensors, actuators;
    void (*visit)(visitor_t *self, node_t *n);
};

static void visit_node(visitor_t *self, node_t *n)
{
    static const char *KIND[] = { "ECU", "SENSOR", "ACTUATOR" };
    printf("visit %-8s %s\n", KIND[n->kind], n->name);
    if (n->kind == 0) self->ecus++;
    else if (n->kind == 1) self->sensors++;
    else self->actuators++;
}

static void accept_node(node_t *self, visitor_t *v) { v->visit(v, self); }

int main(void)
{
    node_t nodes[] = {
        { "engine_ecu", 0, accept_node },
        { "o2_sensor",  1, accept_node },
        { "injector",   2, accept_node },
        { "abs_ecu",    0, accept_node },
    };
    visitor_t v = { 0, 0, 0, visit_node };

    for (size_t i = 0; i < sizeof nodes / sizeof nodes[0]; i++)
        nodes[i].accept(&nodes[i], &v);

    printf("合计 ECU=%d SENSOR=%d ACTUATOR=%d\n", v.ecus, v.sensors, v.actuators);
    printf("新增一种统计，只写新的 visitor，不改节点\n");
    return 0;
}
