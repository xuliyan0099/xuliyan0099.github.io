/* 适配器模式 · C 实现：两种温湿度传感器，上层只认一套接口
 * 编译：gcc -std=c11 -Wall -Wextra adapter.c -o adapter
 */
#include <stdio.h>

/* ---------- 目标接口：上层代码只认这三个成员 ---------- */
typedef struct sensor sensor_t;
typedef struct {
    int (*read_temp)(sensor_t *self, float *out);
    int (*read_hum)(sensor_t *self, float *out);
} sensor_ops_t;

struct sensor { const sensor_ops_t *ops; void *impl; };

/* ---------- 被适配者 A：SHT3x 厂商库，返回 ×100 的整数 ---------- */
typedef struct { int t_x100; int h_x100; } sht3x_t;

static int sht3x_legacy_read(sht3x_t *d, int *t_x100, int *h_x100)
{
    if (!d) return -1;
    *t_x100 = d->t_x100;
    *h_x100 = d->h_x100;
    return 0;
}

typedef struct { sensor_t base; sht3x_t hw; } sht_adapter_t;

static int sht_read_temp(sensor_t *self, float *out)
{
    sht_adapter_t *a = (sht_adapter_t *)self;     /* 适配器知道两边 */
    int t, h;
    if (sht3x_legacy_read(&a->hw, &t, &h) != 0) return -1;
    *out = t / 100.0f;
    return 0;
}

static int sht_read_hum(sensor_t *self, float *out)
{
    sht_adapter_t *a = (sht_adapter_t *)self;
    int t, h;
    if (sht3x_legacy_read(&a->hw, &t, &h) != 0) return -1;
    *out = h / 100.0f;
    return 0;
}

static const sensor_ops_t SHT_OPS = { sht_read_temp, sht_read_hum };

/* ---------- 被适配者 B：NTC + ADC，只能测温，湿度不支持 ---------- */
typedef struct { int adc; } ntc_hw_t;

static int ntc_read_adc(ntc_hw_t *d) { return d->adc; }

typedef struct { sensor_t base; ntc_hw_t hw; } ntc_adapter_t;

static int ntc_read_temp(sensor_t *self, float *out)
{
    ntc_adapter_t *a = (ntc_adapter_t *)self;
    int adc = ntc_read_adc(&a->hw);
    *out = 25.0f + (adc - 2048) * 0.05f;          /* 分压表的线性近似 */
    return 0;
}

static int ntc_read_hum(sensor_t *self, float *out)
{
    (void)self; (void)out;
    return -2;                                   /* 能力缺失要如实报错 */
}

static const sensor_ops_t NTC_OPS = { ntc_read_temp, ntc_read_hum };

/* ---------- 上层：同一段代码，两个实现 ---------- */
static void report(const char *tag, sensor_t *s)
{
    float t = 0, h = 0;
    printf("%s: ", tag);
    if (s->ops->read_temp(s, &t) == 0) printf("temp=%.1fC ", t);
    else                               printf("temp=<err> ");
    int rc = s->ops->read_hum(s, &h);
    if (rc == 0)      printf("hum=%.1f%%\n", h);
    else if (rc == -2) printf("hum=<不支持>\n");
    else               printf("hum=<err>\n");
}

int main(void)
{
    sht_adapter_t a = { { &SHT_OPS, NULL }, { 2360, 4850 } };
    ntc_adapter_t b = { { &NTC_OPS, NULL }, { 2100 } };
    a.base.impl = &a.hw;
    b.base.impl = &b.hw;

    report("SHT3x", &a.base);
    report("NTC  ", &b.base);
    return 0;
}
