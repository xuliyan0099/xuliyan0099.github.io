# -*- coding: utf-8 -*-
"""生成行为型补全 5 个（迭代器/中介者/备忘录/模板方法/访问者）的样例源码。"""
import pathlib

SRC = pathlib.Path(__file__).resolve().parents[1] / "src"
FILES = {}

FILES["iterator.c"] = r'''/* 迭代器：调用方只拿 next()，看不到故障表是数组还是链表 */
#include <stdio.h>
#include <stddef.h>

typedef struct {
    int code;
    const char *name;
} fault_t;

static const fault_t FAULTS[] = {
    { 0,  "none" },
    { 17, "O2 heater" },
    { 0,  "none" },
    { 42, "misfire" },
    { 91, "CAN bus off" },
};

typedef struct {
    const fault_t *arr;
    int n;
    int i;
} fault_iter_t;

static void iter_init(fault_iter_t *it, const fault_t *arr, int n)
{
    it->arr = arr; it->n = n; it->i = 0;
}

/* 只返回有效故障；返回 NULL 表示遍历结束 */
static const fault_t *iter_next(fault_iter_t *it)
{
    while (it->i < it->n) {
        const fault_t *f = &it->arr[it->i++];
        if (f->code != 0) return f;
    }
    return NULL;
}

int main(void)
{
    fault_iter_t it;
    iter_init(&it, FAULTS, (int)(sizeof FAULTS / sizeof FAULTS[0]));

    const fault_t *f;
    int count = 0;
    while ((f = iter_next(&it)) != NULL) {
        printf("fault #%d code=%d %s\n", ++count, f->code, f->name);
    }
    printf("有效故障 %d 条，全部遍历完\n", count);
    return 0;
}
'''

FILES["iterator.cpp"] = r'''// 迭代器 · C++：自定义 begin/end，range-for 直接遍历有效故障
// 编译：g++ -std=c++17 -Wall -Wextra iterator.cpp -o iterator_cpp
#include <cstdio>
#include <vector>

struct Fault {
    int code;
    const char *name;
};

class FaultList {
public:
    void add(int code, const char *name) { items_.push_back(Fault{code, name}); }

    class Iter {
    public:
        Iter(const FaultList *list, std::size_t pos) : list_(list), pos_(pos) { skip(); }
        const Fault &operator*() const { return list_->items_[pos_]; }
        Iter &operator++() { ++pos_; skip(); return *this; }
        bool operator!=(const Iter &o) const { return pos_ != o.pos_; }
    private:
        void skip() { while (pos_ < list_->items_.size() && list_->items_[pos_].code == 0) ++pos_; }
        const FaultList *list_;
        std::size_t pos_;
    };

    Iter begin() const { return Iter(this, 0); }
    Iter end() const { return Iter(this, items_.size()); }
private:
    std::vector<Fault> items_;
};

int main()
{
    FaultList list;
    list.add(0, "none");
    list.add(17, "O2 heater");
    list.add(0, "none");
    list.add(42, "misfire");
    list.add(91, "CAN bus off");

    int count = 0;
    for (const Fault &f : list)
        std::printf("fault #%d code=%d %s\n", ++count, f.code, f.name);
    std::printf("有效故障 %d 条，全部遍历完\n", count);
    return 0;
}
'''

FILES["mediator.c"] = r'''/* 中介者：三个 ECU 不互相认识，所有转发走同一条总线 */
#include <stdio.h>
#include <string.h>

typedef struct mediator mediator_t;
typedef struct ecu ecu_t;

struct ecu { const char *name; mediator_t *bus; };
struct mediator { ecu_t *nodes[3]; int n; };

static void bus_publish(mediator_t *m, ecu_t *from, const char *topic)
{
    printf("[BUS] %s -> %s\n", from->name, topic);
    for (int i = 0; i < m->n; i++) {
        ecu_t *to = m->nodes[i];
        if (to == from) continue;
        int want = strcmp(topic, "BRAKE") == 0 || strcmp(to->name, "DASH") == 0;
        if (want) printf("      %s handles %s\n", to->name, topic);
    }
}

int main(void)
{
    ecu_t engine = { "ENGINE", NULL };
    ecu_t dash   = { "DASH",   NULL };
    ecu_t brake  = { "BRAKE",  NULL };
    mediator_t bus = { .nodes = { &engine, &dash, &brake }, .n = 3 };

    engine.bus = &bus; dash.bus = &bus; brake.bus = &bus;

    bus_publish(&bus, &engine, "BRAKE");
    bus_publish(&bus, &engine, "TEMP");
    bus_publish(&bus, &brake,  "WHEEL_SPEED");
    printf("发送方只认识 bus，不认识另外两个节点\n");
    return 0;
}
'''

FILES["mediator.cpp"] = r'''// 中介者 · C++：Colleague 只持 Mediator&，路由规则集中在一处
// 编译：g++ -std=c++17 -Wall -Wextra mediator.cpp -o mediator_cpp
#include <cstdio>
#include <string>
#include <vector>

class Mediator;

class Colleague {
public:
    explicit Colleague(std::string name) : name_(std::move(name)) {}
    virtual ~Colleague() = default;
    const std::string &name() const { return name_; }
    void join(Mediator *m) { bus_ = m; }
    void publish(const std::string &topic);   /* 定义放在 Mediator 之后 */
protected:
    Mediator *bus_ = nullptr;
private:
    std::string name_;
};

class Mediator {
public:
    void add(Colleague *c) { nodes_.push_back(c); c->join(this); }
    void route(Colleague *from, const std::string &topic)
    {
        std::printf("[BUS] %s -> %s\n", from->name().c_str(), topic.c_str());
        for (auto *to : nodes_) {
            if (to == from) continue;
            bool want = topic == "BRAKE" || to->name() == "DASH";
            if (want) std::printf("      %s handles %s\n", to->name().c_str(), topic.c_str());
        }
    }
private:
    std::vector<Colleague *> nodes_;
};

inline void Colleague::publish(const std::string &topic)
{
    if (bus_) bus_->route(this, topic);
}

int main()
{
    Mediator bus;
    Colleague engine("ENGINE"), dash("DASH"), brake("BRAKE");
    bus.add(&engine); bus.add(&dash); bus.add(&brake);

    engine.publish("BRAKE");
    engine.publish("TEMP");
    brake.publish("WHEEL_SPEED");
    std::printf("发送方只认识 bus，不认识另外两个节点\n");
    return 0;
}
'''

FILES["memento.c"] = r'''/* 备忘录：改标定之前先存一份，出事能原样退回 */
#include <stdio.h>

typedef struct {
    int gain;
    int offset;
    int mode;
} calib_t;

typedef struct { calib_t snap; } memento_t;

static memento_t save(const calib_t *c)
{
    memento_t m = { *c };
    return m;
}
static void restore(calib_t *c, const memento_t *m)
{
    *c = m->snap;
}

static void dump(const char *tag, const calib_t *c)
{
    printf("%-9s gain=%d offset=%d mode=%d\n", tag, c->gain, c->offset, c->mode);
}

int main(void)
{
    calib_t ecu = { 12, 0, 1 };
    dump("before", &ecu);

    memento_t m = save(&ecu);

    ecu.gain = 30;          /* 现场调参，调坏了 */
    ecu.offset = -8;
    ecu.mode = 3;
    dump("tuned", &ecu);

    restore(&ecu, &m);
    dump("restored", &ecu);
    printf("快照是值拷贝：之后改 ecu 不会污染 memento\n");
    return 0;
}
'''

FILES["memento.cpp"] = r'''// 备忘录 · C++：Memento 只暴露给 Originator，外部拿不到内部字段
// 编译：g++ -std=c++17 -Wall -Wextra memento.cpp -o memento_cpp
#include <cstdio>

struct Calib { int gain; int offset; int mode; };

class Memento {
public:
    explicit Memento(const Calib &c) : c_(c) {}
private:
    friend class Ecu;
    Calib c_;
};

class Ecu {
public:
    void set(int g, int o, int m) { c_ = Calib{g, o, m}; }
    Memento save() const { return Memento(c_); }
    void restore(const Memento &m) { c_ = m.c_; }
    void dump(const char *tag) const
    {
        std::printf("%-9s gain=%d offset=%d mode=%d\n", tag, c_.gain, c_.offset, c_.mode);
    }
private:
    Calib c_{};
};

int main()
{
    Ecu ecu;
    ecu.set(12, 0, 1);
    ecu.dump("before");
    Memento m = ecu.save();

    ecu.set(30, -8, 3);
    ecu.dump("tuned");

    ecu.restore(m);
    ecu.dump("restored");
    std::printf("快照是值拷贝：之后改 ecu 不会污染 memento\n");
    return 0;
}
'''

FILES["template_method.c"] = r'''/* 模板方法：自检顺序固定，每一步换成具体实现 */
#include <stdio.h>

typedef struct {
    const char *name;
    int (*power)(void);
    int (*comm)(void);
    int (*sensor)(void);
} selftest_t;

/* 骨架：顺序不可改，任何一步失败立即中止 */
static int run(const selftest_t *t)
{
    printf("== %s ==\n", t->name);
    printf("step1 power  ... ");
    if (!t->power())  { printf("FAIL\n"); return 0; }
    printf("OK\n");

    printf("step2 comm   ... ");
    if (!t->comm())   { printf("FAIL\n"); return 0; }
    printf("OK\n");

    printf("step3 sensor ... ");
    if (!t->sensor()) { printf("FAIL\n"); return 0; }
    printf("OK\n");

    printf("result PASS\n");
    return 1;
}

static int p_ok(void)  { return 1; }
static int c_ok(void)  { return 1; }
static int s_ok(void)  { return 1; }
static int s_bad(void) { return 0; }

int main(void)
{
    const selftest_t bench = { "bench",  p_ok, c_ok, s_ok };
    const selftest_t field = { "field",  p_ok, c_ok, s_bad };

    run(&bench);
    run(&field);
    printf("两个变体共用同一套顺序与日志\n");
    return 0;
}
'''

FILES["template_method.cpp"] = r'''// 模板方法 · C++：run() 非虚，步骤虚函数，子类只覆写细节
// 编译：g++ -std=c++17 -Wall -Wextra template_method.cpp -o template_method_cpp
#include <cstdio>
#include <string>

class SelfTest {
public:
    explicit SelfTest(std::string name) : name_(std::move(name)) {}
    virtual ~SelfTest() = default;

    // 模板：不打算被覆写
    bool run() const
    {
        std::printf("== %s ==\n", name_.c_str());
        std::printf("step1 power  ... ");
        if (!power())  { std::printf("FAIL\n"); return false; }
        std::printf("OK\n");
        std::printf("step2 comm   ... ");
        if (!comm())   { std::printf("FAIL\n"); return false; }
        std::printf("OK\n");
        std::printf("step3 sensor ... ");
        if (!sensor()) { std::printf("FAIL\n"); return false; }
        std::printf("OK\n");
        std::printf("result PASS\n");
        return true;
    }
protected:
    virtual bool power() const = 0;
    virtual bool comm() const = 0;
    virtual bool sensor() const = 0;
private:
    std::string name_;
};

class BenchTest : public SelfTest {
public:
    BenchTest() : SelfTest("bench") {}
protected:
    bool power() const override { return true; }
    bool comm() const override { return true; }
    bool sensor() const override { return true; }
};

class FieldTest : public SelfTest {
public:
    FieldTest() : SelfTest("field") {}
protected:
    bool power() const override { return true; }
    bool comm() const override { return true; }
    bool sensor() const override { return false; }
};

int main()
{
    BenchTest b;
    FieldTest f;
    b.run();
    f.run();
    std::printf("两个变体共用同一套顺序与日志\n");
    return 0;
}
'''

FILES["visitor.c"] = r'''/* 访问者：节点只负责 accept，统计逻辑放在 visitor 里 */
#include <stdio.h>

typedef struct visitor visitor_t;
typedef struct node node_t;

struct node {
    const char *name;
    int kind;              /* 0=ECU 1=SENSOR 2=ACTUATOR */
    void (*accept)(node_t *self, visitor_t *v);
};

struct visitor {
    int ecus, sensors, actuators;
    void (*visit)(visitor_t *self, node_t *n);
};

static void visit_node(visitor_t *self, node_t *n)
{
    static const char *KIND[] = { "ECU", "SENSOR", "ACTUATOR" };
    printf("visit %-8s %s\n", KIND[n->kind], n->name);
    if (n->kind == 0) self->ecus++;
    else if (n->kind == 1) self->sensors++;
    else self->actuators++;
}

static void accept_node(node_t *self, visitor_t *v) { v->visit(v, self); }

int main(void)
{
    node_t nodes[] = {
        { "engine_ecu", 0, accept_node },
        { "o2_sensor",  1, accept_node },
        { "injector",   2, accept_node },
        { "abs_ecu",    0, accept_node },
    };
    visitor_t v = { 0, 0, 0, visit_node };

    for (size_t i = 0; i < sizeof nodes / sizeof nodes[0]; i++)
        nodes[i].accept(&nodes[i], &v);

    printf("合计 ECU=%d SENSOR=%d ACTUATOR=%d\n", v.ecus, v.sensors, v.actuators);
    printf("新增一种统计，只写新的 visitor，不改节点\n");
    return 0;
}
'''

FILES["visitor.cpp"] = r'''// 访问者 · C++：accept/visit 双向分派，节点与统计彻底解耦
// 编译：g++ -std=c++17 -Wall -Wextra visitor.cpp -o visitor_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

class Visitor;

class Element {
public:
    explicit Element(std::string name) : name_(std::move(name)) {}
    virtual ~Element() = default;
    const std::string &name() const { return name_; }
    virtual void accept(Visitor &v) const = 0;
protected:
    std::string name_;
};

class Visitor {
public:
    virtual ~Visitor() = default;
    virtual void visit(const class Ecu &e) = 0;
    virtual void visit(const class Sensor &s) = 0;
    virtual void visit(const class Actuator &a) = 0;
};

class Ecu : public Element {
public:
    using Element::Element;
    void accept(Visitor &v) const override { v.visit(*this); }
};
class Sensor : public Element {
public:
    using Element::Element;
    void accept(Visitor &v) const override { v.visit(*this); }
};
class Actuator : public Element {
public:
    using Element::Element;
    void accept(Visitor &v) const override { v.visit(*this); }
};

class Counter : public Visitor {
public:
    void visit(const Ecu &e) override      { std::printf("visit ECU      %s\n", e.name().c_str()); ecus_++; }
    void visit(const Sensor &s) override   { std::printf("visit SENSOR   %s\n", s.name().c_str()); sensors_++; }
    void visit(const Actuator &a) override { std::printf("visit ACTUATOR %s\n", a.name().c_str()); actuators_++; }
    void report() const
    {
        std::printf("合计 ECU=%d SENSOR=%d ACTUATOR=%d\n", ecus_, sensors_, actuators_);
        std::printf("新增一种统计，只写新的 visitor，不改节点\n");
    }
private:
    int ecus_ = 0, sensors_ = 0, actuators_ = 0;
};

int main()
{
    std::vector<std::unique_ptr<Element>> nodes;
    nodes.push_back(std::make_unique<Ecu>("engine_ecu"));
    nodes.push_back(std::make_unique<Sensor>("o2_sensor"));
    nodes.push_back(std::make_unique<Actuator>("injector"));
    nodes.push_back(std::make_unique<Ecu>("abs_ecu"));

    Counter c;
    for (const auto &n : nodes) n->accept(c);
    c.report();
    return 0;
}
'''

def main():
    for name, text in FILES.items():
        (SRC / name).write_text(text, encoding="utf-8")
    print("written", len(FILES))

if __name__ == "__main__":
    main()

