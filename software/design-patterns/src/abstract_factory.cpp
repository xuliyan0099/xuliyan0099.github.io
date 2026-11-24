// 抽象工厂 · C++：家族返回 unique_ptr，生命周期跟着走
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
