/* 观察者 · 天气站订阅
 * gcc -std=c11 -Wall -Wextra observer.c -o observer
 */
#include <stdio.h>

typedef struct { const char *name; void (*update)(const char *, int); } observer_t;

typedef struct {
    observer_t *subs[4];
    int n;
} station_t;

static void subscribe(station_t *s, observer_t *o) { s->subs[s->n++] = o; }

static void set_temp(station_t *s, int t)
{
    printf("气温 -> %d℃\n", t);
    for (int i = 0; i < s->n; i++)
        s->subs[i]->update(s->subs[i]->name, t);
}

static void phone(const char *name, int t)   { printf("  %s：显示 %d℃\n", name, t); }
static void display(const char *name, int t) { printf("  %s：大屏刷新 %d℃\n", name, t); }

int main(void)
{
    station_t s = { { 0 }, 0 };
    observer_t a = { "手机 App", phone };
    observer_t b = { "客厅大屏", display };
    subscribe(&s, &a); subscribe(&s, &b);

    set_temp(&s, 21);
    set_temp(&s, 24);
    printf("发布者不认识订阅者，只遍历名单\n");
    return 0;
}
