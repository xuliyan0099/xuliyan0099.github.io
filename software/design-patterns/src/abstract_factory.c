/* 抽象工厂：一次取到“同一代”的两个零件，而不是各取各的 */
#include <stdio.h>
#include <stddef.h>

typedef struct { void (*send)(const char *msg); } can_t;
typedef struct { void (*save)(int value); } nvram_t;

typedef struct {
    const char *name;
    can_t   (*make_can)(void);
    nvram_t (*make_nvram)(void);
} family_t;

static void bosch_can_send(const char *m)   { printf("[CAN/BOSCH] %s\n", m); }
static void bosch_nv_save(int v)            { printf("[NVRAM/BOSCH] save %d\n", v); }
static void conti_can_send(const char *m)   { printf("[CAN/CONTI] %s\n", m); }
static void conti_nv_save(int v)            { printf("[NVRAM/CONTI] save %d\n", v); }

static can_t   bosch_can(void)   { can_t c = { bosch_can_send };   return c; }
static nvram_t bosch_nvram(void) { nvram_t n = { bosch_nv_save }; return n; }
static can_t   conti_can(void)   { can_t c = { conti_can_send };   return c; }
static nvram_t conti_nvram(void) { nvram_t n = { conti_nv_save }; return n; }

static const family_t FAMILIES[] = {
    { "BOSCH", bosch_can, bosch_nvram },
    { "CONTI", conti_can, conti_nvram },
};

int main(void)
{
    const size_t nfam = sizeof FAMILIES / sizeof FAMILIES[0];
    for (size_t i = 0; i < nfam; i++) {
        const family_t *f = &FAMILIES[i];
        can_t   c = f->make_can();     /* 同一家族：语言一致、时序一致 */
        nvram_t v = f->make_nvram();
        printf("-- family %s --\n", f->name);
        c.send("0x18FF50E5");
        v.save(7);
    }
    printf("family 数 %zu，零件组合 2 种\n", nfam);
    return 0;
}
