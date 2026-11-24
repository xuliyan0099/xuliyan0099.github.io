# -*- coding: utf-8 -*-
"""生成创建型 4 个 + 桥接、组合的 C/C++ 样例源码。"""
import os, pathlib

SRC = pathlib.Path(__file__).resolve().parents[1] / "src"
SRC.mkdir(exist_ok=True)

FILES = {}

FILES["abstract_factory.c"] = r'''/* 抽象工厂：一次取到“同一代”的两个零件，而不是各取各的 */
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
'''

FILES["abstract_factory.cpp"] = r'''// 抽象工厂 · C++：家族返回 unique_ptr，生命周期跟着走
// 编译：g++ -std=c++17 -Wall -Wextra abstract_factory.cpp -o abstract_factory_cpp
#include <cstdio>
#include <memory>

struct Can {
    virtual ~Can() = default;
    virtual void send(const char *msg) = 0;
};
struct Nvram {
    virtual ~Nvram() = default;
    virtual void save(int value) = 0;
};

class BoschCan : public Can {
public:
    void send(const char *m) override { std::printf("[CAN/BOSCH] %s\n", m); }
};
class BoschNvram : public Nvram {
public:
    void save(int v) override { std::printf("[NVRAM/BOSCH] save %d\n", v); }
};
class ContiCan : public Can {
public:
    void send(const char *m) override { std::printf("[CAN/CONTI] %s\n", m); }
};
class ContiNvram : public Nvram {
public:
    void save(int v) override { std::printf("[NVRAM/CONTI] save %d\n", v); }
};

struct Family {
    virtual ~Family() = default;
    virtual const char *name() const = 0;
    virtual std::unique_ptr<Can> makeCan() const = 0;
    virtual std::unique_ptr<Nvram> makeNvram() const = 0;
};

class BoschFamily : public Family {
public:
    const char *name() const override { return "BOSCH"; }
    std::unique_ptr<Can> makeCan() const override { return std::make_unique<BoschCan>(); }
    std::unique_ptr<Nvram> makeNvram() const override { return std::make_unique<BoschNvram>(); }
};
class ContiFamily : public Family {
public:
    const char *name() const override { return "CONTI"; }
    std::unique_ptr<Can> makeCan() const override { return std::make_unique<ContiCan>(); }
    std::unique_ptr<Nvram> makeNvram() const override { return std::make_unique<ContiNvram>(); }
};

int main()
{
    std::unique_ptr<Family> fams[] = {
        std::make_unique<BoschFamily>(), std::make_unique<ContiFamily>()
    };
    for (auto &f : fams) {
        std::printf("-- family %s --\n", f->name());
        auto can = f->makeCan();
        auto nv = f->makeNvram();
        can->send("0x18FF50E5");
        nv->save(7);
    }
    std::printf("family 数 2，零件组合 2 种\n");
    return 0;
}
'''

FILES["builder.c"] = r'''/* 建造者：把“拼一帧”拆成可检查的步骤，最后一次性交付 */
#include <stdio.h>
#include <stddef.h>

typedef struct {
    unsigned id;
    int dlc;
    unsigned char data[8];
    unsigned crc;
} frame_t;

typedef struct { frame_t f; } builder_t;

static void b_start(builder_t *b)          { b->f.id = 0; b->f.dlc = 0; b->f.crc = 0; }
static void b_id(builder_t *b, unsigned v) { b->f.id = v; }
static void b_data(builder_t *b, const unsigned char *d, int n)
{
    if (n > 8) n = 8;
    b->f.dlc = n;
    for (int i = 0; i < n; i++) b->f.data[i] = d[i];
}
static void b_crc(builder_t *b)
{
    unsigned sum = b->f.id;
    for (int i = 0; i < b->f.dlc; i++) sum += b->f.data[i];
    b->f.crc = sum & 0xFFu;
}
static frame_t b_build(const builder_t *b) { return b->f; }

static void dump(const frame_t *f)
{
    printf("id=0x%X dlc=%d data=[", f->id, f->dlc);
    for (int i = 0; i < f->dlc; i++) printf("%s%02X", i ? " " : "", f->data[i]);
    printf("] crc=0x%02X\n", f->crc);
}

int main(void)
{
    builder_t b;
    unsigned char payload[8] = { 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80 };

    b_start(&b);
    b_id(&b, 0x18FF50E5u);
    b_data(&b, payload, 3);
    b_crc(&b);
    frame_t f1 = b_build(&b);
    printf("frame1 ");
    dump(&f1);

    b_start(&b);                 /* 复用同一个 builder，不残留上一帧 */
    b_id(&b, 0x7DFu);
    b_data(&b, payload, 8);      /* 超长被截到 8 字节 */
    b_crc(&b);
    frame_t f2 = b_build(&b);
    printf("frame2 ");
    dump(&f2);
    printf("两次建造独立：frame1 dlc=%d, frame2 dlc=%d\n", f1.dlc, f2.dlc);
    return 0;
}
'''

FILES["builder.cpp"] = r'''// 建造者 · C++：链式调用，build() 只交付一次
// 编译：g++ -std=c++17 -Wall -Wextra builder.cpp -o builder_cpp
#include <cstdio>
#include <array>

struct Frame {
    unsigned id = 0;
    int dlc = 0;
    std::array<unsigned char, 8> data{};
    unsigned crc = 0;
};

class Builder {
public:
    Builder &start() { f_ = Frame{}; return *this; }
    Builder &id(unsigned v) { f_.id = v; return *this; }
    Builder &data(const unsigned char *d, int n)
    {
        if (n > 8) n = 8;
        f_.dlc = n;
        for (int i = 0; i < n; i++) f_.data[static_cast<size_t>(i)] = d[i];
        return *this;
    }
    Builder &crc()
    {
        unsigned sum = f_.id;
        for (int i = 0; i < f_.dlc; i++) sum += f_.data[static_cast<size_t>(i)];
        f_.crc = sum & 0xFFu;
        return *this;
    }
    Frame build() const { return f_; }
private:
    Frame f_;
};

static void dump(const Frame &f)
{
    std::printf("id=0x%X dlc=%d data=[", f.id, f.dlc);
    for (int i = 0; i < f.dlc; i++) std::printf("%s%02X", i ? " " : "", f.data[static_cast<size_t>(i)]);
    std::printf("] crc=0x%02X\n", f.crc);
}

int main()
{
    unsigned char payload[8] = { 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80 };
    Builder b;
    Frame f1 = b.start().id(0x18FF50E5u).data(payload, 3).crc().build();
    std::printf("frame1 ");
    dump(f1);

    Frame f2 = b.start().id(0x7DFu).data(payload, 8).crc().build();
    std::printf("frame2 ");
    dump(f2);
    std::printf("两次建造独立：frame1 dlc=%d, frame2 dlc=%d\n", f1.dlc, f2.dlc);
    return 0;
}
'''

FILES["prototype.c"] = r'''/* 原型：配置先登记，用的时候按名字复制一份，改副本不动原版 */
#include <stdio.h>
#include <string.h>
#include <stddef.h>

typedef struct {
    char name[16];
    int timeout_ms;
    int retry;
} config_t;

typedef struct {
    const char *key;
    config_t proto;
} proto_t;

static proto_t PROTOS[] = {
    { "default", { "default", 500, 3 } },
    { "fast",    { "fast",    120, 1 } },
};

static const proto_t *find_proto(const char *key)
{
    for (size_t i = 0; i < sizeof PROTOS / sizeof PROTOS[0]; i++)
        if (strcmp(PROTOS[i].key, key) == 0) return &PROTOS[i];
    return NULL;
}

static config_t clone(const proto_t *p)
{
    config_t c = p->proto;          /* 结构体整体复制 = 深拷贝（这里没有指针成员） */
    return c;
}

static void dump(const char *tag, const config_t *c)
{
    printf("%-8s name=%-8s timeout=%d retry=%d\n", tag, c->name, c->timeout_ms, c->retry);
}

int main(void)
{
    const proto_t *p = find_proto("fast");
    if (!p) { printf("no prototype\n"); return 1; }

    config_t a = clone(p);
    config_t b = clone(p);
    dump("original", &p->proto);

    b.timeout_ms = 90;              /* 只改副本 */
    strcpy(b.name, "fast-tuned");
    dump("clone-a", &a);
    dump("clone-b", &b);
    dump("original", &p->proto);

    const proto_t *miss = find_proto("slow");
    printf("lookup slow: %s\n", miss ? "found" : "miss");
    printf("克隆 2 份，原型仍 timeout=%d\n", p->proto.timeout_ms);
    return 0;
}
'''

FILES["prototype.cpp"] = r'''// 原型 · C++：clone() 返回 unique_ptr，注册表只读，副本归调用方
// 编译：g++ -std=c++17 -Wall -Wextra prototype.cpp -o prototype_cpp
#include <cstdio>
#include <map>
#include <memory>
#include <string>

struct Config {
    std::string name;
    int timeout_ms;
    int retry;
    virtual ~Config() = default;
    virtual std::unique_ptr<Config> clone() const = 0;
};

struct FastConfig : Config {
    std::unique_ptr<Config> clone() const override
    {
        return std::make_unique<FastConfig>(*this);
    }
};

int main()
{
    std::map<std::string, std::unique_ptr<Config>> protos;
    protos["fast"] = std::make_unique<FastConfig>();
    protos["fast"]->name = "fast";
    protos["fast"]->timeout_ms = 120;
    protos["fast"]->retry = 1;

    auto a = protos["fast"]->clone();
    auto b = protos["fast"]->clone();
    b->timeout_ms = 90;
    b->name = "fast-tuned";

    std::printf("original name=%-8s timeout=%d\n", protos["fast"]->name.c_str(), protos["fast"]->timeout_ms);
    std::printf("clone-a  name=%-8s timeout=%d\n", a->name.c_str(), a->timeout_ms);
    std::printf("clone-b  name=%-8s timeout=%d\n", b->name.c_str(), b->timeout_ms);
    std::printf("原型未变：timeout=%d\n", protos["fast"]->timeout_ms);
    return 0;
}
'''

FILES["bridge.c"] = r'''/* 桥接：协议和物理层各管各的，四种组合靠两张表拼出来 */
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
'''

FILES["bridge.cpp"] = r'''// 桥接 · C++：Link 与 Protocol 各自抽象，组合时只传引用
// 编译：g++ -std=c++17 -Wall -Wextra bridge.cpp -o bridge_cpp
#include <cstdio>
#include <memory>
#include <string>

class Link {
public:
    virtual ~Link() = default;
    virtual const char *name() const = 0;
    virtual void send(const std::string &frame) const = 0;
};
class CanLink : public Link {
public:
    const char *name() const override { return "CAN"; }
    void send(const std::string &f) const override { std::printf("[CAN ] %s\n", f.c_str()); }
};
class LinLink : public Link {
public:
    const char *name() const override { return "LIN"; }
    void send(const std::string &f) const override { std::printf("[LIN ] %s\n", f.c_str()); }
};

class Protocol {
public:
    explicit Protocol(const Link &l) : link_(l) {}
    virtual ~Protocol() = default;
    virtual const char *name() const = 0;
    virtual void request(const std::string &svc) const = 0;
    const char *linkName() const { return link_.name(); }
protected:
    const Link &link_;
};
class Uds : public Protocol {
public:
    using Protocol::Protocol;
    const char *name() const override { return "UDS"; }
    void request(const std::string &svc) const override
    {
        link_.send("UDS " + svc + " -> " + link_.name());
    }
};
class Obd : public Protocol {
public:
    using Protocol::Protocol;
    const char *name() const override { return "OBD"; }
    void request(const std::string &svc) const override
    {
        link_.send("OBD " + svc + " -> " + link_.name());
    }
};

int main()
{
    CanLink can;
    LinLink lin;
    Uds udsCan(can), udsLin(lin);
    Obd obdCan(can), obdLin(lin);

    const Protocol *protos[] = { &udsCan, &udsLin, &obdCan, &obdLin };
    for (const Protocol *p : protos) {
        std::printf("-- %s over %s --\n", p->name(), p->linkName());
        p->request("0x22F190");
    }
    std::printf("协议 2 × 物理层 2 = 4 种组合，新增一种只改一侧\n");
    return 0;
}
'''

FILES["composite.c"] = r'''/* 组合：一棵诊断树，叶子是零件，枝是分组，遍历代码只写一遍 */
#include <stdio.h>
#include <stddef.h>

typedef struct node node_t;
struct node {
    const char *name;
    int is_leaf;
    int pass;
    node_t *kids[4];
    int nkids;
};

static int run_node(const node_t *nd, int depth)
{
    for (int i = 0; i < depth; i++) printf("  ");
    if (nd->is_leaf) {
        printf("- %-10s %s\n", nd->name, nd->pass ? "PASS" : "FAIL");
        return nd->pass;
    }
    printf("+ %s\n", nd->name);
    int ok = 1;
    for (int i = 0; i < nd->nkids; i++)
        if (!run_node(nd->kids[i], depth + 1)) ok = 0;
    return ok;
}

int main(void)
{
    node_t eng  = { .name = "engine",  .is_leaf = 1, .pass = 1, .kids = {0}, .nkids = 0 };
    node_t gear = { .name = "gearbox", .is_leaf = 1, .pass = 0, .kids = {0}, .nkids = 0 };
    node_t abs  = { .name = "abs",     .is_leaf = 1, .pass = 1, .kids = {0}, .nkids = 0 };
    node_t power = { .name = "powertrain", .is_leaf = 0, .pass = 0, .kids = { &eng, &gear }, .nkids = 2 };
    node_t chassis = { .name = "chassis", .is_leaf = 0, .pass = 0, .kids = { &abs }, .nkids = 1 };
    node_t root = { .name = "vehicle", .is_leaf = 0, .pass = 0, .kids = { &power, &chassis }, .nkids = 2 };

    int ok = run_node(&root, 0);
    printf("整车自检：%s\n", ok ? "PASS" : "FAIL");
    return 0;
}
'''

FILES["composite.cpp"] = r'''// 组合 · C++：Group 持有 unique_ptr，析构自动递归
// 编译：g++ -std=c++17 -Wall -Wextra composite.cpp -o composite_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

class Component {
public:
    explicit Component(std::string name) : name_(std::move(name)) {}
    virtual ~Component() = default;
    virtual bool run(int depth) const = 0;
protected:
    std::string name_;
};

class Leaf : public Component {
public:
    Leaf(std::string n, bool pass) : Component(std::move(n)), pass_(pass) {}
    bool run(int depth) const override
    {
        for (int i = 0; i < depth; i++) std::printf("  ");
        std::printf("- %-10s %s\n", name_.c_str(), pass_ ? "PASS" : "FAIL");
        return pass_;
    }
private:
    bool pass_;
};

class Group : public Component {
public:
    explicit Group(std::string n) : Component(std::move(n)) {}
    Group &add(std::unique_ptr<Component> c) { kids_.push_back(std::move(c)); return *this; }
    bool run(int depth) const override
    {
        for (int i = 0; i < depth; i++) std::printf("  ");
        std::printf("+ %s\n", name_.c_str());
        bool ok = true;
        for (const auto &c : kids_)
            if (!c->run(depth + 1)) ok = false;
        return ok;
    }
private:
    std::vector<std::unique_ptr<Component>> kids_;
};

int main()
{
    auto root = std::make_unique<Group>("vehicle");
    auto power = std::make_unique<Group>("powertrain");
    power->add(std::make_unique<Leaf>("engine", true));
    power->add(std::make_unique<Leaf>("gearbox", false));
    root->add(std::move(power));
    auto chassis = std::make_unique<Group>("chassis");
    chassis->add(std::make_unique<Leaf>("abs", true));
    root->add(std::move(chassis));

    bool ok = root->run(0);
    std::printf("整车自检：%s\n", ok ? "PASS" : "FAIL");
    return 0;
}
'''

def main():
    for name, text in FILES.items():
        (SRC / name).write_text(text, encoding="utf-8")
    print("written", len(FILES))

if __name__ == "__main__":
    main()


