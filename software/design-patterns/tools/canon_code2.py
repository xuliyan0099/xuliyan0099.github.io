# -*- coding: utf-8 -*-
"""第二批经典例子源码：适配器、桥接、组合、装饰、外观、享元、代理。"""
import pathlib

SRC = pathlib.Path(__file__).resolve().parent.parent / "src"
C = {}

C["adapter.c"] = r'''/* 适配器 · 方钉插圆孔
 * gcc -std=c11 -Wall -Wextra adapter.c -o adapter
 */
#include <stdio.h>

typedef struct { int radius; } round_hole_t;
typedef struct { int width;  } square_peg_t;

/* 旧接口：只认圆钉 */
static int round_fits(const round_hole_t *h, int peg_radius)
{
    return peg_radius <= h->radius;
}

/* 适配器：把方钉包一层，暴露“半径” */
typedef struct { square_peg_t peg; } square_adapter_t;

static int adapter_radius(const square_adapter_t *a)
{
    /* 方钉对角线一半，才能塞进圆孔 */
    return (a->peg.width * 2) / 3;
}

int main(void)
{
    round_hole_t hole = { 5 };
    square_peg_t small = { 6 };
    square_peg_t big   = { 10 };

    printf("圆孔半径 %d\n", hole.radius);

    square_adapter_t a1 = { small };
    square_adapter_t a2 = { big };
    printf("方钉 6  -> 适配半径 %d -> %s\n", adapter_radius(&a1),
           round_fits(&hole, adapter_radius(&a1)) ? "塞得进" : "塞不进");
    printf("方钉 10 -> 适配半径 %d -> %s\n", adapter_radius(&a2),
           round_fits(&hole, adapter_radius(&a2)) ? "塞得进" : "塞不进");
    return 0;
}
'''

C["adapter.cpp"] = r'''// 适配器 · 方钉插圆孔
// g++ -std=c++17 -Wall -Wextra adapter.cpp -o adapter_cpp
#include <cstdio>

class RoundHole {
public:
    explicit RoundHole(int r) : r_(r) {}
    int radius() const { return r_; }
    bool fits(int pegRadius) const { return pegRadius <= r_; }
private:
    int r_;
};

class SquarePeg {
public:
    explicit SquarePeg(int w) : w_(w) {}
    int width() const { return w_; }
private:
    int w_;
};

class SquarePegAdapter {
public:
    explicit SquarePegAdapter(const SquarePeg& p) : peg_(p) {}
    int radius() const { return (peg_.width() * 2) / 3; }
private:
    SquarePeg peg_;
};

int main()
{
    RoundHole hole(5);
    SquarePeg small(6), big(10);
    SquarePegAdapter a1(small), a2(big);

    std::printf("圆孔半径 %d\n", hole.radius());
    std::printf("方钉 6  -> 适配半径 %d -> %s\n", a1.radius(),
                hole.fits(a1.radius()) ? "塞得进" : "塞不进");
    std::printf("方钉 10 -> 适配半径 %d -> %s\n", a2.radius(),
                hole.fits(a2.radius()) ? "塞得进" : "塞不进");
    return 0;
}
'''

C["bridge.c"] = r'''/* 桥接 · 形状 × 渲染器
 * gcc -std=c11 -Wall -Wextra bridge.c -o bridge
 */
#include <stdio.h>

typedef struct renderer renderer_t;
struct renderer {
    const char *name;
    void (*circle)(renderer_t *, int);
    void (*square)(renderer_t *, int);
};

typedef struct {
    const char *name;
    int size;
    const renderer_t *r;
} shape_t;

static void shape_draw(const shape_t *s)
{
    printf("[%s] %s size=%d -> ", s->r->name, s->name, s->size);
    if (s->name[0] == 'C') s->r->circle((renderer_t *)s->r, s->size);
    else                   s->r->square((renderer_t *)s->r, s->size);
}

static void vector_circle(renderer_t *r, int s) { (void)r; printf("矢量圆 r=%d\n", s); }
static void vector_square(renderer_t *r, int s) { (void)r; printf("矢量方 w=%d\n", s); }
static renderer_t VECTOR = { "矢量", vector_circle, vector_square };

static void raster_circle(renderer_t *r, int s) { (void)r; printf("位图圆 半径 %dpx\n", s); }
static void raster_square(renderer_t *r, int s) { (void)r; printf("位图方 边长 %dpx\n", s); }
static renderer_t RASTER = { "位图", raster_circle, raster_square };

int main(void)
{
    shape_t shapes[] = {
        { "Circle", 5, &VECTOR },
        { "Square", 5, &VECTOR },
        { "Circle", 5, &RASTER },
        { "Square", 5, &RASTER },
    };
    for (unsigned i = 0; i < 4; i++) shape_draw(&shapes[i]);
    printf("2 种形状 × 2 种渲染器 = 4 种组合，没有 4 个子类\n");
    return 0;
}
'''

C["bridge.cpp"] = r'''// 桥接 · 形状 × 渲染器
// g++ -std=c++17 -Wall -Wextra bridge.cpp -o bridge_cpp
#include <cstdio>
#include <memory>
#include <string>

class Renderer {
public:
    virtual ~Renderer() = default;
    virtual std::string name() const = 0;
    virtual void circle(int size) const = 0;
    virtual void square(int size) const = 0;
};

class VectorRenderer final : public Renderer {
public:
    std::string name() const override { return "矢量"; }
    void circle(int s) const override { std::printf("矢量圆 r=%d\n", s); }
    void square(int s) const override { std::printf("矢量方 w=%d\n", s); }
};

class RasterRenderer final : public Renderer {
public:
    std::string name() const override { return "位图"; }
    void circle(int s) const override { std::printf("位图圆 半径 %dpx\n", s); }
    void square(int s) const override { std::printf("位图方 边长 %dpx\n", s); }
};

class Shape {
public:
    Shape(std::unique_ptr<Renderer> r, int size) : r_(std::move(r)), size_(size) {}
    virtual ~Shape() = default;
    virtual std::string name() const = 0;
    void draw() const {
        std::printf("[%s] %s size=%d -> ", r_->name().c_str(), name().c_str(), size_);
        if (name() == "Circle") r_->circle(size_);
        else                    r_->square(size_);
    }
protected:
    const Renderer& renderer() const { return *r_; }
    int size() const { return size_; }
private:
    std::unique_ptr<Renderer> r_;
    int size_;
};

class Circle final : public Shape {
public:
    Circle(std::unique_ptr<Renderer> r, int s) : Shape(std::move(r), s) {}
    std::string name() const override { return "Circle"; }
};

class Square final : public Shape {
public:
    Square(std::unique_ptr<Renderer> r, int s) : Shape(std::move(r), s) {}
    std::string name() const override { return "Square"; }
};

int main()
{
    Circle v1(std::make_unique<VectorRenderer>(), 5); v1.draw();
    Square v2(std::make_unique<VectorRenderer>(), 5); v2.draw();
    Circle r1(std::make_unique<RasterRenderer>(), 5); r1.draw();
    Square r2(std::make_unique<RasterRenderer>(), 5); r2.draw();
    std::puts("2 种形状 × 2 种渲染器 = 4 种组合，没有 4 个子类");
    return 0;
}
'''

C["composite.c"] = r'''/* 组合 · 文件与文件夹
 * gcc -std=c11 -Wall -Wextra composite.c -o composite
 */
#include <stdio.h>
#include <string.h>

typedef struct node node_t;
struct node {
    char name[16];
    int  is_dir;
    int  size;                 /* 文件大小；目录忽略 */
    node_t *kids[4];
    int  nkids;
};

static node_t *add(node_t *dir, node_t *kid)
{
    if (dir->nkids < 4) dir->kids[dir->nkids++] = kid;
    return dir;
}

static int total(const node_t *n)
{
    if (!n->is_dir) return n->size;
    int sum = 0;
    for (int i = 0; i < n->nkids; i++) sum += total(n->kids[i]);
    return sum;
}

static void list(const node_t *n, int depth)
{
    for (int i = 0; i < depth; i++) printf("  ");
    printf("%s%s\n", n->is_dir ? "[D] " : "    ", n->name);
    if (n->is_dir)
        for (int i = 0; i < n->nkids; i++) list(n->kids[i], depth + 1);
}

int main(void)
{
    node_t root = { "root", 1, 0, { 0 }, 0 };
    node_t src  = { "src",  1, 0, { 0 }, 0 };
    node_t a    = { "a.c",  0, 120, { 0 }, 0 };
    node_t b    = { "b.c",  0, 80,  { 0 }, 0 };
    node_t read = { "README", 0, 10, { 0 }, 0 };

    add(&src, &a); add(&src, &b);
    add(&root, &src); add(&root, &read);

    list(&root, 0);
    printf("总大小 = %d 字节\n", total(&root));
    return 0;
}
'''

C["composite.cpp"] = r'''// 组合 · 文件与文件夹
// g++ -std=c++17 -Wall -Wextra composite.cpp -o composite_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

class Node {
public:
    Node(std::string name, bool dir, int size = 0)
        : name_(std::move(name)), dir_(dir), size_(size) {}
    virtual ~Node() = default;

    void add(std::unique_ptr<Node> kid) { kids_.push_back(std::move(kid)); }
    int total() const {
        if (!dir_) return size_;
        int sum = 0;
        for (const auto& k : kids_) sum += k->total();
        return sum;
    }
    void list(int depth = 0) const {
        for (int i = 0; i < depth; i++) std::printf("  ");
        std::printf("%s%s\n", dir_ ? "[D] " : "    ", name_.c_str());
        for (const auto& k : kids_) k->list(depth + 1);
    }
private:
    std::string name_;
    bool dir_;
    int size_;
    std::vector<std::unique_ptr<Node>> kids_;
};

int main()
{
    auto root = std::make_unique<Node>("root", true);
    auto src = std::make_unique<Node>("src", true);
    src->add(std::make_unique<Node>("a.c", false, 120));
    src->add(std::make_unique<Node>("b.c", false, 80));
    root->add(std::move(src));
    root->add(std::make_unique<Node>("README", false, 10));

    root->list();
    std::printf("总大小 = %d 字节\n", root->total());
    return 0;
}
'''

C["decorator.c"] = r'''/* 装饰器 · 给文本加粗、加斜体
 * gcc -std=c11 -Wall -Wextra decorator.c -o decorator
 */
#include <stdio.h>
#include <string.h>

typedef struct { char text[96]; } text_t;

static text_t bold(text_t t)
{
    text_t out;
    snprintf(out.text, sizeof out.text, "<b>%.*s</b>", (int)(sizeof out.text - 9), t.text);
    return out;
}

static text_t italic(text_t t)
{
    text_t out;
    snprintf(out.text, sizeof out.text, "<i>%.*s</i>", (int)(sizeof out.text - 9), t.text);
    return out;
}

int main(void)
{
    text_t t = { "hello" };
    printf("原始：%s\n", t.text);

    text_t b = bold(t);
    printf("加粗：%s\n", b.text);

    text_t bi = italic(b);
    printf("加粗+斜体：%s\n", bi.text);

    text_t ib = bold(italic(t));
    printf("顺序反过来：%s\n", ib.text);
    return 0;
}
'''

C["decorator.cpp"] = r'''// 装饰器 · 给文本加粗、加斜体
// g++ -std=c++17 -Wall -Wextra decorator.cpp -o decorator_cpp
#include <cstdio>
#include <memory>
#include <string>

class Text {
public:
    virtual ~Text() = default;
    virtual std::string render() const = 0;
};

class Plain final : public Text {
public:
    explicit Plain(std::string s) : s_(std::move(s)) {}
    std::string render() const override { return s_; }
private:
    std::string s_;
};

class Bold final : public Text {
public:
    explicit Bold(std::unique_ptr<Text> inner) : inner_(std::move(inner)) {}
    std::string render() const override { return "<b>" + inner_->render() + "</b>"; }
private:
    std::unique_ptr<Text> inner_;
};

class Italic final : public Text {
public:
    explicit Italic(std::unique_ptr<Text> inner) : inner_(std::move(inner)) {}
    std::string render() const override { return "<i>" + inner_->render() + "</i>"; }
private:
    std::unique_ptr<Text> inner_;
};

int main()
{
    std::printf("原始：%s\n", Plain("hello").render().c_str());
    std::printf("加粗：%s\n", Bold(std::make_unique<Plain>("hello")).render().c_str());
    std::printf("加粗+斜体：%s\n",
                Italic(std::make_unique<Bold>(std::make_unique<Plain>("hello"))).render().c_str());
    std::printf("顺序反过来：%s\n",
                Bold(std::make_unique<Italic>(std::make_unique<Plain>("hello"))).render().c_str());
    return 0;
}
'''

C["facade.c"] = r'''/* 外观 · 家庭影院一键开机
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
'''

C["facade.cpp"] = r'''// 外观 · 家庭影院一键开机
// g++ -std=c++17 -Wall -Wextra facade.cpp -o facade_cpp
#include <cstdio>

class HomeTheater {
public:
    void watchMovie() {
        std::puts("watchMovie():");
        std::puts("  灯光调到 20%");
        std::puts("  投影仪开机");
        std::puts("  功放开机，切到 HDMI 1");
        std::puts("  幕布放下");
        std::puts("  可以开始播放");
        started_ = true;
    }
    void endMovie() {
        std::puts("endMovie():");
        std::puts("  关投影、关功放、灯光回升、幕布收起");
        started_ = false;
    }
private:
    bool started_ = false;
};

int main()
{
    HomeTheater t;
    t.watchMovie();
    t.endMovie();
    std::puts("上层只调了两个方法，没有碰任何子系统");
    return 0;
}
'''

C["flyweight.c"] = r'''/* 享元 · 森林共享树型
 * gcc -std=c11 -Wall -Wextra flyweight.c -o flyweight
 */
#include <stdio.h>
#include <string.h>

typedef struct {
    char name[16];
    int  leaf_color;
} tree_type_t;

typedef struct {
    const tree_type_t *type;   /* 共享内部状态 */
    int x, y;                  /* 外部状态 */
} tree_t;

static tree_type_t TYPES[2] = {
    { "橡树", 0x2E7D32 },
    { "松树", 0x1B5E20 },
};

static const tree_type_t *get_type(const char *name)
{
    for (unsigned i = 0; i < 2; i++)
        if (strcmp(TYPES[i].name, name) == 0) return &TYPES[i];
    return NULL;
}

int main(void)
{
    tree_t forest[1000];
    int n = 0;
    for (int i = 0; i < 1000; i++) {
        forest[n].type = get_type(i % 2 ? "松树" : "橡树");
        forest[n].x = i * 3;
        forest[n].y = i * 5;
        n++;
    }

    printf("1000 棵树，共享 %d 份树型描述\n", 2);
    printf("%s x=%d y=%d color=0x%06X\n",
           forest[0].type->name, forest[0].x, forest[0].y, forest[0].type->leaf_color);
    printf("%s x=%d y=%d color=0x%06X\n",
           forest[999].type->name, forest[999].x, forest[999].y, forest[999].type->leaf_color);
    printf("每棵树只多存 2 个坐标，不复制颜色和名字\n");
    return 0;
}
'''

C["flyweight.cpp"] = r'''// 享元 · 森林共享树型
// g++ -std=c++17 -Wall -Wextra flyweight.cpp -o flyweight_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

struct TreeType {
    std::string name;
    int leafColor;
};

class TreeFactory {
public:
    const TreeType& get(const std::string& name, int color) {
        auto it = pool_.find(name);
        if (it == pool_.end())
            it = pool_.emplace(name, TreeType{name, color}).first;
        return it->second;
    }
private:
    std::unordered_map<std::string, TreeType> pool_;
};

struct Tree {
    const TreeType* type;
    int x, y;
};

int main()
{
    TreeFactory factory;
    std::vector<Tree> forest;
    forest.reserve(1000);
    for (int i = 0; i < 1000; i++) {
        const auto& type = i % 2 ? factory.get("松树", 0x1B5E20)
                                 : factory.get("橡树", 0x2E7D32);
        forest.push_back(Tree{&type, i * 3, i * 5});
    }

    std::printf("1000 棵树，共享 2 份树型描述\n");
    std::printf("%s x=%d y=%d color=0x%06X\n",
                forest[0].type->name.c_str(), forest[0].x, forest[0].y, forest[0].type->leafColor);
    std::printf("%s x=%d y=%d color=0x%06X\n",
                forest[999].type->name.c_str(), forest[999].x, forest[999].y, forest[999].type->leafColor);
    std::puts("每棵树只多存 2 个坐标，不复制颜色和名字");
    return 0;
}
'''

C["proxy.c"] = r'''/* 代理 · 图片懒加载
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
'''

C["proxy.cpp"] = r'''// 代理 · 图片懒加载
// g++ -std=c++17 -Wall -Wextra proxy.cpp -o proxy_cpp
#include <cstdio>
#include <string>

class Image {
public:
    virtual ~Image() = default;
    virtual const std::string& name() const { return name_; }
    virtual int pixels() {
        if (!loaded_) {
            loaded_ = true;
            std::printf("  真正读取磁盘：%s\n", name_.c_str());
        }
        return 1920 * 1080;
    }
protected:
    explicit Image(std::string name) : name_(std::move(name)) {}
    std::string name_;
    bool loaded_ = false;
};

class RealImage final : public Image {
public:
    explicit RealImage(std::string name) : Image(std::move(name)) {}
};

class ImageProxy {
public:
    explicit ImageProxy(std::string name) : real_(std::move(name)) {}
    int pixels() {
        std::printf("proxy_get(%s)：", real_.name().c_str());
        if (hasCache_) { std::puts("命中缓存，不碰磁盘"); return cached_; }
        std::puts("未命中，转给真实对象");
        cached_ = real_.pixels();
        hasCache_ = true;
        return cached_;
    }
private:
    RealImage real_;
    int cached_ = 0;
    bool hasCache_ = false;
};

int main()
{
    ImageProxy p("photo.jpg");
    p.pixels(); p.pixels(); p.pixels();
    std::puts("三次读取，只加载了一次");
    return 0;
}'''

for name, code in C.items():
    (SRC / name).write_text(code, encoding="utf-8")
print("wrote", len(C))



