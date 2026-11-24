/* 代理 · 图片懒加载
 * gcc -std=c11 -Wall -Wextra proxy.c -o proxy
 */
#include <stdio.h>
#include <string.h>

typedef struct {
    char name[32];
    int  loaded;
    int  pixels;
} image_t;

static int real_load(image_t *img)
{
    if (!img->loaded) {
        img->pixels = 1920 * 1080;
        img->loaded = 1;
        printf("  真正读取磁盘：%s\n", img->name);
    }
    return img->pixels;
}

typedef struct {
    image_t real;
    int     cached_pixels;
    int     has_cache;
} proxy_t;

static int proxy_get(proxy_t *p)
{
    printf("proxy_get(%s)：", p->real.name);
    if (p->has_cache) {
        printf("命中缓存，不碰磁盘\n");
        return p->cached_pixels;
    }
    printf("未命中，转给真实对象\n");
    p->cached_pixels = real_load(&p->real);
    p->has_cache = 1;
    return p->cached_pixels;
}

int main(void)
{
    proxy_t p = { { "photo.jpg", 0, 0 }, 0, 0 };
    proxy_get(&p);
    proxy_get(&p);
    proxy_get(&p);
    printf("三次读取，只加载了一次\n");
    return 0;
}
