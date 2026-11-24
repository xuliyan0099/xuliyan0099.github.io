/* 外观 · 家庭影院一键开机
 * gcc -std=c11 -Wall -Wextra facade.c -o facade
 */
#include <stdio.h>

static void lights_dim(void)   { puts("  灯光调到 20%"); }
static void projector_on(void) { puts("  投影仪开机"); }
static void amplifier_on(void){ puts("  功放开机，切到 HDMI 1"); }
static void screen_down(void)  { puts("  幕布放下"); }

typedef struct { int started; } theater_t;

static void watch_movie(theater_t *t)
{
    puts("watch_movie():");
    lights_dim();
    projector_on();
    amplifier_on();
    screen_down();
    t->started = 1;
    puts("  可以开始播放");
}

static void end_movie(theater_t *t)
{
    puts("end_movie():");
    puts("  关投影、关功放、灯光回升、幕布收起");
    t->started = 0;
}

int main(void)
{
    theater_t t = { 0 };
    watch_movie(&t);
    end_movie(&t);
    printf("上层只调了两个方法，没有碰任何子系统\n");
    return 0;
}
