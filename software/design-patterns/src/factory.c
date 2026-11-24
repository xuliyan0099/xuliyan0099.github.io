/* 工厂模式 · C 实现：按名字创建驱动（注册表 + 构造函数指针）
 * 编译：gcc -std=c11 -Wall -Wextra factory.c -o factory
 */
#include <stdio.h>
#include <string.h>

typedef struct driver driver_t;
typedef struct {
    int         (*init)(driver_t *self);
    const char *(*name)(driver_t *self);
} driver_ops_t;

struct driver { const driver_ops_t *ops; };

typedef driver_t *(*create_fn)(void);

#define MAX_REG 8
typedef struct { char name[16]; create_fn create; } entry_t;

static entry_t g_reg[MAX_REG];
static int     g_reg_n = 0;

static int driver_register(const char *name, create_fn fn)
{
    if (g_reg_n >= MAX_REG) return -1;
    snprintf(g_reg[g_reg_n].name, sizeof g_reg[g_reg_n].name, "%s", name);
    g_reg[g_reg_n].create = fn;
    g_reg_n++;
    printf("  register %-6s  (注册表长度=%d)\n", name, g_reg_n);
    return 0;
}

static driver_t *driver_create(const char *name)
{
    for (int i = 0; i < g_reg_n; i++)
        if (strcmp(g_reg[i].name, name) == 0)
            return g_reg[i].create();
    return NULL;
}

/* 具体产品 1 */
typedef struct { driver_t base; int addr; } sht_drv_t;

static int sht_init(driver_t *self) {
    sht_drv_t *d = (sht_drv_t *)self;
    printf("    sht3x init @0x%02X\n", d->addr);
    return 0;
}
static const char *sht_name(driver_t *self) { (void)self; return "sht3x"; }
static const driver_ops_t SHT_OPS = { sht_init, sht_name };
static driver_t *sht_new(void) { static sht_drv_t d = { { &SHT_OPS }, 0x44 }; return &d.base; }

/* 具体产品 2 */
typedef struct { driver_t base; int pin; } ntc_drv_t;

static int ntc_init(driver_t *self) {
    ntc_drv_t *d = (ntc_drv_t *)self;
    printf("    ntc init on pin %d\n", d->pin);
    return 0;
}
static const char *ntc_name(driver_t *self) { (void)self; return "ntc"; }
static const driver_ops_t NTC_OPS = { ntc_init, ntc_name };
static driver_t *ntc_new(void) { static ntc_drv_t d = { { &NTC_OPS }, 12 }; return &d.base; }

/* 链接期自注册：启动时自动登记，不用改 main */
static void auto_reg_ntc(void) __attribute__((constructor));
static void auto_reg_ntc(void) { driver_register("ntc", ntc_new); }

int main(void)
{
    printf("启动后注册表：\n");
    for (int i = 0; i < g_reg_n; i++) printf("  [%d] %s\n", i, g_reg[i].name);
    printf("\n");

    driver_register("sht3x", sht_new);

    const char *wanted[] = { "sht3x", "ntc", "bme280" };
    for (unsigned i = 0; i < 3; i++) {
        printf("create(\"%s\"):\n", wanted[i]);
        driver_t *d = driver_create(wanted[i]);
        if (!d) { printf("    未注册，返回 NULL（由上层决定降级）\n"); continue; }
        d->ops->init(d);
        printf("    name=%s\n", d->ops->name(d));
    }
    return 0;
}
