# -*- coding: utf-8 -*-
"""第一批经典例子源码：工厂方法、抽象工厂、建造者、原型、单例。"""
import pathlib

SRC = pathlib.Path(__file__).resolve().parent.parent / "src"

C = {}

C["factory.c"] = r'''/* 工厂方法 · 物流：卡车与轮船
 * gcc -std=c11 -Wall -Wextra factory.c -o factory
 */
#include <stdio.h>
#include <string.h>

typedef struct transport transport_t;
struct transport {
    const char *(*name)(transport_t *);
    void (*deliver)(transport_t *);
};

typedef transport_t *(*creator_t)(void);

typedef struct { transport_t base; } truck_t;
static const char *truck_name(transport_t *t) { (void)t; return "卡车"; }
static void truck_deliver(transport_t *t) { (void)t; puts("  卡车：陆运 200 箱"); }
static transport_t *truck_new(void) {
    static truck_t x = { { truck_name, truck_deliver } };
    return &x.base;
}

typedef struct { transport_t base; } ship_t;
static const char *ship_name(transport_t *t) { (void)t; return "轮船"; }
static void ship_deliver(transport_t *t) { (void)t; puts("  轮船：海运 800 箱"); }
static transport_t *ship_new(void) {
    static ship_t x = { { ship_name, ship_deliver } };
    return &x.base;
}

static const struct { const char *kind; creator_t create; } REG[] = {
    { "truck", truck_new },
    { "ship",  ship_new  },
};

static transport_t *create(const char *kind)
{
    for (unsigned i = 0; i < sizeof REG / sizeof REG[0]; i++)
        if (strcmp(kind, REG[i].kind) == 0)
            return REG[i].create();
    return NULL;
}

int main(void)
{
    const char *want[] = { "truck", "ship", "plane" };
    for (unsigned i = 0; i < 3; i++) {
        transport_t *t = create(want[i]);
        if (!t) { printf("create(\"%s\") -> 未知类型，返回 NULL\n", want[i]); continue; }
        printf("create(\"%s\") -> %s\n", want[i], t->name(t));
        t->deliver(t);
    }
    return 0;
}
'''

C["factory.cpp"] = r'''// 工厂方法 · 物流：卡车与轮船
// g++ -std=c++17 -Wall -Wextra factory.cpp -o factory_cpp
#include <cstdio>
#include <memory>
#include <string>

class Transport {
public:
    virtual ~Transport() = default;
    virtual const char* name() const = 0;
    virtual void deliver() const = 0;
};

class Truck final : public Transport {
public:
    const char* name() const override { return "卡车"; }
    void deliver() const override { std::puts("  卡车：陆运 200 箱"); }
};

class Ship final : public Transport {
public:
    const char* name() const override { return "轮船"; }
    void deliver() const override { std::puts("  轮船：海运 800 箱"); }
};

class Logistics {
public:
    virtual ~Logistics() = default;
    virtual std::unique_ptr<Transport> create() const = 0;

    void plan(const char* kind) const {
        auto t = create();
        std::printf("create(\"%s\") -> %s\n", kind, t->name());
        t->deliver();
    }
};

class RoadLogistics final : public Logistics {
public:
    std::unique_ptr<Transport> create() const override {
        return std::make_unique<Truck>();
    }
};

class SeaLogistics final : public Logistics {
public:
    std::unique_ptr<Transport> create() const override {
        return std::make_unique<Ship>();
    }
};

int main()
{
    RoadLogistics road;
    SeaLogistics sea;
    road.plan("truck");
    sea.plan("ship");
    std::puts("create(\"plane\") -> 没有对应工厂，返回 nullptr");
    return 0;
}
'''

C["abstract_factory.c"] = r'''/* 抽象工厂 · GUI：浅色/深色两套控件
 * gcc -std=c11 -Wall -Wextra abstract_factory.c -o abstract_factory
 */
#include <stdio.h>

typedef struct { const char *(*label)(void); } button_t;
typedef struct { const char *(*label)(void); } checkbox_t;

typedef struct {
    button_t   *(*button)(void);
    checkbox_t *(*checkbox)(void);
} gui_factory_t;

static const char *light_btn_label(void) { return "[ 浅色按钮 ]"; }
static button_t light_btn = { light_btn_label };
static button_t *light_button(void) { return &light_btn; }
static const char *light_box_label(void) { return "[ ] 浅色复选框"; }
static checkbox_t light_box = { light_box_label };
static checkbox_t *light_checkbox(void) { return &light_box; }
static gui_factory_t LIGHT = { light_button, light_checkbox };

static const char *dark_btn_label(void) { return "[ 深色按钮 ]"; }
static button_t dark_btn = { dark_btn_label };
static button_t *dark_button(void) { return &dark_btn; }
static const char *dark_box_label(void) { return "[x] 深色复选框"; }
static checkbox_t dark_box = { dark_box_label };
static checkbox_t *dark_checkbox(void) { return &dark_box; }
static gui_factory_t DARK = { dark_button, dark_checkbox };

static void render(const char *theme, gui_factory_t *f)
{
    button_t   *b = f->button();
    checkbox_t *c = f->checkbox();
    printf("%s 界面：%s  %s\n", theme, b->label(), c->label());
}

int main(void)
{
    render("浅色", &LIGHT);
    render("深色", &DARK);
    return 0;
}
'''

C["abstract_factory.cpp"] = r'''// 抽象工厂 · GUI：浅色/深色两套控件
// g++ -std=c++17 -Wall -Wextra abstract_factory.cpp -o abstract_factory_cpp
#include <cstdio>
#include <memory>
#include <string>

class Button { public: virtual ~Button() = default; virtual std::string label() const = 0; };
class Checkbox { public: virtual ~Checkbox() = default; virtual std::string label() const = 0; };

class LightButton final : public Button {
public: std::string label() const override { return "[ 浅色按钮 ]"; }
};
class LightCheckbox final : public Checkbox {
public: std::string label() const override { return "[ ] 浅色复选框"; }
};

class DarkButton final : public Button {
public: std::string label() const override { return "[ 深色按钮 ]"; }
};
class DarkCheckbox final : public Checkbox {
public: std::string label() const override { return "[x] 深色复选框"; }
};

class GuiFactory {
public:
    virtual ~GuiFactory() = default;
    virtual std::unique_ptr<Button>   button() const = 0;
    virtual std::unique_ptr<Checkbox> checkbox() const = 0;

    void render(const char* theme) const {
        auto b = button();
        auto c = checkbox();
        std::printf("%s 界面：%s  %s\n", theme, b->label().c_str(), c->label().c_str());
    }
};

class LightFactory final : public GuiFactory {
public:
    std::unique_ptr<Button> button() const override { return std::make_unique<LightButton>(); }
    std::unique_ptr<Checkbox> checkbox() const override { return std::make_unique<LightCheckbox>(); }
};

class DarkFactory final : public GuiFactory {
public:
    std::unique_ptr<Button> button() const override { return std::make_unique<DarkButton>(); }
    std::unique_ptr<Checkbox> checkbox() const override { return std::make_unique<DarkCheckbox>(); }
};

int main()
{
    LightFactory light;
    DarkFactory dark;
    light.render("浅色");
    dark.render("深色");
    return 0;
}
'''

C["builder.c"] = r'''/* 建造者 · 一步步盖房子
 * gcc -std=c11 -Wall -Wextra builder.c -o builder
 */
#include <stdio.h>

typedef struct {
    int walls, doors, windows;
    int has_roof;
} house_t;

static void add_walls(house_t *h, int n)   { h->walls = n;   printf("  砌 %d 面墙\n", n); }
static void add_doors(house_t *h, int n)   { h->doors = n;   printf("  装 %d 扇门\n", n); }
static void add_windows(house_t *h, int n) { h->windows = n; printf("  装 %d 扇窗\n", n); }
static void add_roof(house_t *h)           { h->has_roof = 1; printf("  封顶\n"); }

static int build(const house_t *h)
{
    if (h->walls < 4 || h->doors < 1 || h->windows < 1 || !h->has_roof) {
        printf("  校验失败：房子还不完整\n");
        return -1;
    }
    printf("  交付：%d 墙 / %d 门 / %d 窗 / 有屋顶\n",
           h->walls, h->doors, h->windows);
    return 0;
}

int main(void)
{
    house_t h = { 0, 0, 0, 0 };
    printf("普通小屋：\n");
    add_walls(&h, 4); add_doors(&h, 1); add_windows(&h, 2); add_roof(&h);
    build(&h);

    house_t v = { 0, 0, 0, 0 };
    printf("缺步骤的房子：\n");
    add_walls(&v, 4); add_doors(&v, 1);
    build(&v);
    return 0;
}
'''

C["builder.cpp"] = r'''// 建造者 · 一步步盖房子
// g++ -std=c++17 -Wall -Wextra builder.cpp -o builder_cpp
#include <cstdio>
#include <string>

class House {
public:
    std::string walls, doors, windows;
    bool roof = false;
};

class HouseBuilder {
public:
    HouseBuilder& addWalls(int n)   { h_.walls   = std::to_string(n) + " 面墙"; std::printf("  砌 %d 面墙\n", n); return *this; }
    HouseBuilder& addDoors(int n)   { h_.doors   = std::to_string(n) + " 扇门"; std::printf("  装 %d 扇门\n", n); return *this; }
    HouseBuilder& addWindows(int n) { h_.windows = std::to_string(n) + " 扇窗"; std::printf("  装 %d 扇窗\n", n); return *this; }
    HouseBuilder& addRoof()         { h_.roof = true; std::puts("  封顶"); return *this; }

    bool build() const {
        if (h_.walls.empty() || h_.doors.empty() || h_.windows.empty() || !h_.roof) {
            std::puts("  校验失败：房子还不完整");
            return false;
        }
        std::printf("  交付：%s / %s / %s / 有屋顶\n",
                    h_.walls.c_str(), h_.doors.c_str(), h_.windows.c_str());
        return true;
    }

private:
    House h_;
};

int main()
{
    std::puts("普通小屋：");
    HouseBuilder{}.addWalls(4).addDoors(1).addWindows(2).addRoof().build();

    std::puts("缺步骤的房子：");
    HouseBuilder{}.addWalls(4).addDoors(1).build();
    return 0;
}
'''

C["prototype.c"] = r'''/* 原型 · 克隆图形
 * gcc -std=c11 -Wall -Wextra prototype.c -o prototype
 */
#include <stdio.h>
#include <string.h>

typedef struct shape shape_t;
struct shape {
    const char *kind;
    int size;
    void (*clone)(const shape_t *, shape_t *out);
};

static void circle_clone(const shape_t *s, shape_t *out) { *out = *s; }
static void square_clone(const shape_t *s, shape_t *out) { *out = *s; }

static shape_t CIRCLE = { "圆", 10, circle_clone };
static shape_t SQUARE = { "方", 10, square_clone };

static shape_t *registry(const char *kind)
{
    if (strcmp(kind, "circle") == 0) return &CIRCLE;
    if (strcmp(kind, "square") == 0) return &SQUARE;
    return NULL;
}

int main(void)
{
    shape_t a, b;
    registry("circle")->clone(&CIRCLE, &a);
    registry("circle")->clone(&CIRCLE, &b);
    printf("克隆两份圆：a.size=%d  b.size=%d\n", a.size, b.size);

    b.size = 25;
    printf("改 b 之后：a.size=%d  b.size=%d（互不影响）\n", a.size, b.size);
    printf("原型仍是 size=%d\n", CIRCLE.size);
    return 0;
}
'''

C["prototype.cpp"] = r'''// 原型 · 克隆图形
// g++ -std=c++17 -Wall -Wextra prototype.cpp -o prototype_cpp
#include <cstdio>
#include <memory>
#include <string>

class Shape {
public:
    explicit Shape(std::string kind, int size) : kind_(std::move(kind)), size_(size) {}
    virtual ~Shape() = default;
    virtual std::unique_ptr<Shape> clone() const = 0;

    std::string kind() const { return kind_; }
    int size() const { return size_; }
    void setSize(int s) { size_ = s; }

private:
    std::string kind_;
    int size_;
};

class Circle final : public Shape {
public:
    Circle() : Shape("圆", 10) {}
    std::unique_ptr<Shape> clone() const override {
        return std::make_unique<Circle>(*this);
    }
};

class Square final : public Shape {
public:
    Square() : Shape("方", 10) {}
    std::unique_ptr<Shape> clone() const override {
        return std::make_unique<Square>(*this);
    }
};

int main()
{
    Circle proto;
    auto a = proto.clone();
    auto b = proto.clone();
    std::printf("克隆两份圆：a.size=%d  b.size=%d\n", a->size(), b->size());

    b->setSize(25);
    std::printf("改 b 之后：a.size=%d  b.size=%d（互不影响）\n", a->size(), b->size());
    std::printf("原型仍是 size=%d\n", proto.size());
    return 0;
}
'''

C["singleton.c"] = r'''/* 单例 · 全局配置
 * gcc -std=c11 -Wall -Wextra singleton.c -o singleton
 */
#include <stdio.h>
#include <string.h>

typedef struct {
    char theme[16];
    int  font_size;
} config_t;

static config_t *instance(void)
{
    static config_t cfg = { "light", 12 };
    static int inited = 0;
    if (!inited) {
        inited = 1;
        printf("  初始化配置（只发生一次）\n");
    }
    return &cfg;
}

int main(void)
{
    config_t *a = instance();
    config_t *b = instance();
    config_t *c = instance();

    printf("取三次实例：%p %p %p（同一个地址）\n", (void *)a, (void *)b, (void *)c);

    strcpy(a->theme, "dark");
    a->font_size = 16;
    printf("通过 a 改成 %s/%d，通过 c 读：%s/%d\n",
           a->theme, a->font_size, c->theme, c->font_size);
    return 0;
}
'''

C["singleton.cpp"] = r'''// 单例 · 全局配置
// g++ -std=c++17 -Wall -Wextra singleton.cpp -o singleton_cpp
#include <cstdio>
#include <string>

class Config {
public:
    static Config& instance() {
        static Config cfg;
        return cfg;
    }

    std::string theme = "light";
    int font_size = 12;

    Config(const Config&) = delete;
    Config& operator=(const Config&) = delete;

private:
    Config() { std::puts("  初始化配置（只发生一次）"); }
};

int main()
{
    Config& a = Config::instance();
    Config& b = Config::instance();
    Config& c = Config::instance();

    std::printf("取三次实例：%p %p %p（同一个地址）\n",
                static_cast<void*>(&a), static_cast<void*>(&b), static_cast<void*>(&c));

    a.theme = "dark";
    a.font_size = 16;
    std::printf("通过 a 改成 %s/%d，通过 c 读：%s/%d\n",
                a.theme.c_str(), a.font_size, c.theme.c_str(), c.font_size);
    return 0;
}
'''

for name, code in C.items():
    (SRC / name).write_text(code, encoding="utf-8")
print("wrote", len(C))

