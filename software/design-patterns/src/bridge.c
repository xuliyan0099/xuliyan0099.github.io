/* 桥接：协议和物理层各管各的，四种组合靠两张表拼出来 */
#include <stdio.h>
#include <string.h>

typedef struct { const char *name; void (*send)(const char *frame); } link_t;

static void can_send(const char *f) { printf("[CAN ] %s\n", f); }
static void lin_send(const char *f) { printf("[LIN ] %s\n", f); }

static const link_t LINKS[] = {
    { "CAN", can_send },
    { "LIN", lin_send },
};

typedef struct proto proto_t;
struct proto {
    const char *name;
    const link_t *link;
    void (*request)(const proto_t *self, const char *svc);
};

static void uds_request(const proto_t *self, const char *svc)
{
    char buf[64];
    snprintf(buf, sizeof buf, "UDS %s -> %s", svc, self->link->name);
    self->link->send(buf);
}
static void obd_request(const proto_t *self, const char *svc)
{
    char buf[64];
    snprintf(buf, sizeof buf, "OBD %s -> %s", svc, self->link->name);
    self->link->send(buf);
}

int main(void)
{
    proto_t uds = { "UDS", &LINKS[0], uds_request };
    proto_t obd = { "OBD", &LINKS[1], obd_request };

    const proto_t *protos[] = { &uds, &obd };
    for (size_t i = 0; i < sizeof protos / sizeof protos[0]; i++)
        for (size_t k = 0; k < sizeof LINKS / sizeof LINKS[0]; k++) {
            proto_t p = *protos[i];
            p.link = &LINKS[k];
            printf("-- %s over %s --\n", p.name, p.link->name);
            p.request(&p, "0x22F190");
        }
    printf("协议 2 × 物理层 2 = 4 种组合，新增一种只改一侧\n");
    return 0;
}
