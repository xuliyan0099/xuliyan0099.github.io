/* 中介者：三个 ECU 不互相认识，所有转发走同一条总线 */
#include <stdio.h>
#include <string.h>

typedef struct mediator mediator_t;
typedef struct ecu ecu_t;

struct ecu { const char *name; mediator_t *bus; };
struct mediator { ecu_t *nodes[3]; int n; };

static void bus_publish(mediator_t *m, ecu_t *from, const char *topic)
{
    printf("[BUS] %s -> %s\n", from->name, topic);
    for (int i = 0; i < m->n; i++) {
        ecu_t *to = m->nodes[i];
        if (to == from) continue;
        int want = strcmp(topic, "BRAKE") == 0 || strcmp(to->name, "DASH") == 0;
        if (want) printf("      %s handles %s\n", to->name, topic);
    }
}

int main(void)
{
    ecu_t engine = { "ENGINE", NULL };
    ecu_t dash   = { "DASH",   NULL };
    ecu_t brake  = { "BRAKE",  NULL };
    mediator_t bus = { .nodes = { &engine, &dash, &brake }, .n = 3 };

    engine.bus = &bus; dash.bus = &bus; brake.bus = &bus;

    bus_publish(&bus, &engine, "BRAKE");
    bus_publish(&bus, &engine, "TEMP");
    bus_publish(&bus, &brake,  "WHEEL_SPEED");
    printf("发送方只认识 bus，不认识另外两个节点\n");
    return 0;
}
