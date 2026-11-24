# -*- coding: utf-8 -*-
"""生成结构型补全 5 个（装饰/外观/享元/代理）与解释器的样例源码。"""
import pathlib

SRC = pathlib.Path(__file__).resolve().parents[1] / "src"
FILES = {}

FILES["decorator.c"] = r'''/* 装饰：一条读数流水线，每层只加一件事，顺序可换 */
#include <stdio.h>

typedef struct stage stage_t;
struct stage {
    int (*apply)(stage_t *self, int raw);
    stage_t *inner;   /* 下一层；最底层为 NULL */
    int arg;
};

static int raw_apply(stage_t *self, int raw) { (void)self; return raw; }

static int offset_apply(stage_t *self, int raw)
{
    int v = self->inner->apply(self->inner, raw);
    return v + self->arg;
}
static int clamp_apply(stage_t *self, int raw)
{
    int v = self->inner->apply(self->inner, raw);
    if (v < 0) v = 0;
    if (v > self->arg) v = self->arg;
    return v;
}

int main(void)
{
    stage_t raw   = { raw_apply,   NULL, 0 };
    stage_t off   = { offset_apply, &raw, 5 };
    stage_t clamp = { clamp_apply,  &off, 40 };

    printf("raw       = %d\n", raw.apply(&raw, 42));
    printf("+offset5  = %d\n", off.apply(&off, 42));
    printf("+clamp40  = %d\n", clamp.apply(&clamp, 42));

    stage_t off2   = { offset_apply, &raw, -60 };
    stage_t clamp2 = { clamp_apply,  &off2, 40 };
    printf("负值路径  = %d\n", clamp2.apply(&clamp2, 42));
    printf("三层顺序：raw -> offset -> clamp，换顺序结果会变\n");
    return 0;
}
'''

FILES["decorator.cpp"] = r'''// 装饰 · C++：unique_ptr 串起流水线，析构自动拆链
// 编译：g++ -std=c++17 -Wall -Wextra decorator.cpp -o decorator_cpp
#include <cstdio>
#include <memory>

class Sensor {
public:
    virtual ~Sensor() = default;
    virtual int read(int raw) const = 0;
};

class Raw : public Sensor {
public:
    int read(int raw) const override { return raw; }
};

class Offset : public Sensor {
public:
    Offset(std::unique_ptr<Sensor> in, int off) : in_(std::move(in)), off_(off) {}
    int read(int raw) const override { return in_->read(raw) + off_; }
private:
    std::unique_ptr<Sensor> in_;
    int off_;
};

class Clamp : public Sensor {
public:
    Clamp(std::unique_ptr<Sensor> in, int hi) : in_(std::move(in)), hi_(hi) {}
    int read(int raw) const override
    {
        int v = in_->read(raw);
        if (v < 0) v = 0;
        if (v > hi_) v = hi_;
        return v;
    }
private:
    std::unique_ptr<Sensor> in_;
    int hi_;
};

int main()
{
    auto raw = std::make_unique<Raw>();
    auto off = std::make_unique<Offset>(std::make_unique<Raw>(), 5);
    auto clamp = std::make_unique<Clamp>(
        std::make_unique<Offset>(std::make_unique<Raw>(), 5), 40);

    std::printf("raw       = %d\n", raw->read(42));
    std::printf("+offset5  = %d\n", off->read(42));
    std::printf("+clamp40  = %d\n", clamp->read(42));

    auto neg = std::make_unique<Clamp>(
        std::make_unique<Offset>(std::make_unique<Raw>(), -60), 40);
    std::printf("负值路径  = %d\n", neg->read(42));
    std::printf("三层顺序：raw -> offset -> clamp，换顺序结果会变\n");
    return 0;
}
'''

FILES["facade.c"] = r'''/* 外观：上电这一套动作收进一个函数，调用方不再关心顺序 */
#include <stdio.h>

static int ignition_on(void)  { printf("[IGN ] relay -> ON\n"); return 1; }
static int fuel_pump_on(void) { printf("[PUMP] pressure 3.0 bar\n"); return 1; }
static int ecu_handshake(void){ printf("[ECU ] seed/key ok\n"); return 1; }

/* 外观：固定顺序、失败即回滚，调用方只看到 0/负值 */
int vehicle_start(const char *vin)
{
    printf("start %s\n", vin);
    if (!ignition_on()) return -1;
    if (!fuel_pump_on()) { printf("[ROLL] ignition off\n"); return -2; }
    if (!ecu_handshake()) { printf("[ROLL] pump off\n"); return -3; }
    printf("[READY] engine can crank\n");
    return 0;
}

int main(void)
{
    int rc = vehicle_start("VIN-0001");
    printf("vehicle_start -> %d\n", rc);
    printf("调用方只依赖一个入口，子系统仍可单独测试\n");
    return 0;
}
'''

FILES["facade.cpp"] = r'''// 外观 · C++：Facade 持子系统，start() 负责顺序与回滚
// 编译：g++ -std=c++17 -Wall -Wextra facade.cpp -o facade_cpp
#include <cstdio>
#include <string>

class Ignition {
public:
    bool on() { std::printf("[IGN ] relay -> ON\n"); return true; }
    void off() { std::printf("[IGN ] relay -> OFF\n"); }
};
class FuelPump {
public:
    bool on() { std::printf("[PUMP] pressure 3.0 bar\n"); return true; }
    void off() { std::printf("[PUMP] stop\n"); }
};
class Ecu {
public:
    bool handshake() { std::printf("[ECU ] seed/key ok\n"); return true; }
};

class VehicleFacade {
public:
    explicit VehicleFacade(std::string vin) : vin_(std::move(vin)) {}
    int start()
    {
        std::printf("start %s\n", vin_.c_str());
        if (!ign_.on()) return -1;
        if (!pump_.on()) { ign_.off(); return -2; }
        if (!ecu_.handshake()) { pump_.off(); return -3; }
        std::printf("[READY] engine can crank\n");
        return 0;
    }
private:
    std::string vin_;
    Ignition ign_;
    FuelPump pump_;
    Ecu ecu_;
};

int main()
{
    VehicleFacade car("VIN-0001");
    std::printf("vehicle_start -> %d\n", car.start());
    std::printf("调用方只依赖一个入口，子系统仍可单独测试\n");
    return 0;
}
'''

FILES["flyweight.c"] = r'''/* 享元：1000 个信号共用 8 份单位描述，只存指针 */
#include <stdio.h>
#include <string.h>
#include <stddef.h>

typedef struct {
    const char *unit;
    double scale;
} sig_t;

typedef struct {
    sig_t pool[8];
    int n;
} registry_t;

static const sig_t *intern(registry_t *r, const char *unit, double scale)
{
    for (int i = 0; i < r->n; i++)
        if (strcmp(r->pool[i].unit, unit) == 0) return &r->pool[i];
    if (r->n >= 8) return NULL;
    r->pool[r->n].unit = unit;
    r->pool[r->n].scale = scale;
    return &r->pool[r->n++];
}

int main(void)
{
    static const char *UNITS[] = { "C", "kPa", "rpm", "%", "V", "A", "km/h", "deg" };
    registry_t reg = { .n = 0 };
    const sig_t *signals[1000];

    size_t nu = sizeof UNITS / sizeof UNITS[0];
    for (size_t i = 0; i < 1000; i++)
        signals[i] = intern(&reg, UNITS[i % nu], 1.0 + (double)(i % nu) / 10.0);

    printf("信号 1000 个，描述池 %d 份\n", reg.n);
    printf("sig[0]   unit=%-4s scale=%.1f\n", signals[0]->unit, signals[0]->scale);
    printf("sig[7]   unit=%-4s scale=%.1f\n", signals[7]->unit, signals[7]->scale);
    printf("sig[999] unit=%-4s scale=%.1f\n", signals[999]->unit, signals[999]->scale);
    printf("指针相同：sig[0]==sig[8] -> %s\n", signals[0] == signals[8] ? "yes" : "no");
    return 0;
}
'''

FILES["flyweight.cpp"] = r'''// 享元 · C++：工厂缓存 shared_ptr，1000 个句柄只留 8 份对象
// 编译：g++ -std=c++17 -Wall -Wextra flyweight.cpp -o flyweight_cpp
#include <cstdio>
#include <map>
#include <memory>
#include <string>
#include <vector>

struct Signal {
    std::string unit;
    double scale;
};

class SignalFactory {
public:
    std::shared_ptr<const Signal> intern(const std::string &unit, double scale)
    {
        auto it = pool_.find(unit);
        if (it != pool_.end()) return it->second;
        auto s = std::make_shared<const Signal>(Signal{ unit, scale });
        pool_.emplace(unit, s);
        return s;
    }
    std::size_t size() const { return pool_.size(); }
private:
    std::map<std::string, std::shared_ptr<const Signal>> pool_;
};

int main()
{
    const std::string units[] = { "C", "kPa", "rpm", "%", "V", "A", "km/h", "deg" };
    SignalFactory f;
    std::vector<std::shared_ptr<const Signal>> signals;
    signals.reserve(1000);
    for (int i = 0; i < 1000; i++)
        signals.push_back(f.intern(units[static_cast<size_t>(i) % 8], 1.0 + (i % 8) / 10.0));

    std::printf("信号 1000 个，描述池 %zu 份\n", f.size());
    std::printf("sig[0]   unit=%-4s scale=%.1f use_count=%ld\n",
                signals[0]->unit.c_str(), signals[0]->scale, signals[0].use_count());
    std::printf("sig[999] unit=%-4s scale=%.1f\n",
                signals[999]->unit.c_str(), signals[999]->scale);
    std::printf("指针相同：sig[0]==sig[8] -> %s\n", signals[0] == signals[8] ? "yes" : "no");
    return 0;
}
'''

FILES["proxy.c"] = r'''/* 代理：在真 NVRAM 前加缓存和写穿，读两次只打一次底层 */
#include <stdio.h>

typedef struct {
    int (*read)(int addr);
    void (*write)(int addr, int value);
} nv_t;

static int REAL[16];

static int real_read(int addr)
{
    printf("[NVRAM] read  [%d] = %d\n", addr, REAL[addr]);
    return REAL[addr];
}
static void real_write(int addr, int value)
{
    REAL[addr] = value;
    printf("[NVRAM] write [%d] = %d\n", addr, value);
}

typedef struct {
    nv_t real;
    int cache[16];
    int valid[16];
} proxy_t;

static int proxy_read(nv_t *self, int addr)
{
    proxy_t *p = (proxy_t *)self;      /* nv_t 是 proxy_t 的第一个成员 */
    if (!p->valid[addr]) {
        p->cache[addr] = p->real.read(addr);
        p->valid[addr] = 1;
        printf("[PROXY] cache miss [%d]\n", addr);
    } else {
        printf("[PROXY] cache hit  [%d] = %d\n", addr, p->cache[addr]);
    }
    return p->cache[addr];
}
static void proxy_write(nv_t *self, int addr, int value)
{
    proxy_t *p = (proxy_t *)self;
    p->real.write(addr, value);        /* 写穿：底层一定更新 */
    p->cache[addr] = value;
    p->valid[addr] = 1;
    printf("[PROXY] write-through [%d]\n", addr);
}

int main(void)
{
    proxy_t p = { .real = { real_read, real_write }, .valid = { 0 } };
    REAL[3] = 11;

    printf("read1 = %d\n", proxy_read(&p.real, 3));
    printf("read2 = %d\n", proxy_read(&p.real, 3));
    proxy_write(&p.real, 3, 25);
    printf("read3 = %d\n", proxy_read(&p.real, 3));
    printf("真实存储 [3] = %d\n", REAL[3]);
    return 0;
}
'''

FILES["proxy.cpp"] = r'''// 代理 · C++：Proxy 持 RealNvram 与缓存，接口对调用方完全一致
// 编译：g++ -std=c++17 -Wall -Wextra proxy.cpp -o proxy_cpp
#include <cstdio>
#include <array>
#include <memory>

class Nvram {
public:
    virtual ~Nvram() = default;
    virtual int read(int addr) = 0;
    virtual void write(int addr, int value) = 0;
};

class RealNvram : public Nvram {
public:
    int read(int addr) override
    {
        std::printf("[NVRAM] read  [%d] = %d\n", addr, mem_[static_cast<size_t>(addr)]);
        return mem_[static_cast<size_t>(addr)];
    }
    void write(int addr, int value) override
    {
        mem_[static_cast<size_t>(addr)] = value;
        std::printf("[NVRAM] write [%d] = %d\n", addr, value);
    }
private:
    std::array<int, 16> mem_{};
};

class Proxy : public Nvram {
public:
    explicit Proxy(Nvram &real) : real_(real) {}
    int read(int addr) override
    {
        auto i = static_cast<size_t>(addr);
        if (!valid_[i]) {
            cache_[i] = real_.read(addr);
            valid_[i] = true;
            std::printf("[PROXY] cache miss [%d]\n", addr);
        } else {
            std::printf("[PROXY] cache hit  [%d] = %d\n", addr, cache_[i]);
        }
        return cache_[i];
    }
    void write(int addr, int value) override
    {
        real_.write(addr, value);
        cache_[static_cast<size_t>(addr)] = value;
        valid_[static_cast<size_t>(addr)] = true;
        std::printf("[PROXY] write-through [%d]\n", addr);
    }
private:
    Nvram &real_;
    std::array<int, 16> cache_{};
    std::array<bool, 16> valid_{};
};

int main()
{
    RealNvram real;
    Proxy proxy(real);
    real.write(3, 11);
    std::printf("read1 = %d\n", proxy.read(3));
    std::printf("read2 = %d\n", proxy.read(3));
    proxy.write(3, 25);
    std::printf("read3 = %d\n", proxy.read(3));
    std::printf("真实存储 [3] = %d\n", real.read(3));
    return 0;
}
'''

FILES["interpreter.c"] = r'''/* 解释器：把 "TEMP>90 AND RPM<800" 变成小语法树，换环境就能重算 */
#include <stdio.h>

typedef struct ctx { int temp; int rpm; } ctx_t;

typedef struct expr expr_t;
typedef enum { E_CMP, E_AND, E_OR } kind_t;

struct expr {
    kind_t kind;
    int var;        /* 0=temp 1=rpm，仅 CMP 用 */
    int op;         /* 0='>' 1='<' */
    int value;
    const expr_t *l;
    const expr_t *r;
};

static int eval(const expr_t *e, const ctx_t *c)
{
    switch (e->kind) {
        case E_CMP: {
            int v = e->var == 0 ? c->temp : c->rpm;
            return e->op == 0 ? v > e->value : v < e->value;
        }
        case E_AND: return eval(e->l, c) && eval(e->r, c);
        case E_OR:  return eval(e->l, c) || eval(e->r, c);
    }
    return 0;
}

int main(void)
{
    /* 等价于 TEMP>90 AND RPM<800 */
    const expr_t t90  = { .kind = E_CMP, .var = 0, .op = 0, .value = 90 };
    const expr_t r800 = { .kind = E_CMP, .var = 1, .op = 1, .value = 800 };
    const expr_t all  = { .kind = E_AND, .l = &t90, .r = &r800 };

    ctx_t hot  = { 105, 700 };   /* 超温且转速没上来 */
    ctx_t idle = { 88,  650 };
    ctx_t fast = { 95,  900 };

    printf("hot  temp=%d rpm=%d -> %s\n", hot.temp, hot.rpm, eval(&all, &hot) ? "报警" : "正常");
    printf("idle temp=%d rpm=%d -> %s\n", idle.temp, idle.rpm, eval(&all, &idle) ? "报警" : "正常");
    printf("fast temp=%d rpm=%d -> %s\n", fast.temp, fast.rpm, eval(&all, &fast) ? "报警" : "正常");
    printf("同一棵树，三组输入，不需要重新解析\n");
    return 0;
}
'''

FILES["interpreter.cpp"] = r'''// 解释器 · C++：表达式对象各自 eval，组合靠 unique_ptr 持有子树
// 编译：g++ -std=c++17 -Wall -Wextra interpreter.cpp -o interpreter_cpp
#include <cstdio>
#include <memory>

struct Ctx { int temp; int rpm; };

class Expr {
public:
    virtual ~Expr() = default;
    virtual bool eval(const Ctx &c) const = 0;
};

class Cmp : public Expr {
public:
    Cmp(int var, bool greater, int value) : var_(var), greater_(greater), value_(value) {}
    bool eval(const Ctx &c) const override
    {
        int v = var_ == 0 ? c.temp : c.rpm;
        return greater_ ? v > value_ : v < value_;
    }
private:
    int var_;
    bool greater_;
    int value_;
};

class And : public Expr {
public:
    And(std::unique_ptr<Expr> l, std::unique_ptr<Expr> r) : l_(std::move(l)), r_(std::move(r)) {}
    bool eval(const Ctx &c) const override { return l_->eval(c) && r_->eval(c); }
private:
    std::unique_ptr<Expr> l_, r_;
};

int main()
{
    auto tree = std::make_unique<And>(
        std::make_unique<Cmp>(0, true, 90),
        std::make_unique<Cmp>(1, false, 800));

    Ctx hot{ 105, 700 }, idle{ 88, 650 }, fast{ 95, 900 };
    std::printf("hot  temp=%d rpm=%d -> %s\n", hot.temp, hot.rpm, tree->eval(hot) ? "报警" : "正常");
    std::printf("idle temp=%d rpm=%d -> %s\n", idle.temp, idle.rpm, tree->eval(idle) ? "报警" : "正常");
    std::printf("fast temp=%d rpm=%d -> %s\n", fast.temp, fast.rpm, tree->eval(fast) ? "报警" : "正常");
    std::printf("同一棵树，三组输入，不需要重新解析\n");
    return 0;
}
'''

def main():
    for name, text in FILES.items():
        (SRC / name).write_text(text, encoding="utf-8")
    print("written", len(FILES))

if __name__ == "__main__":
    main()
