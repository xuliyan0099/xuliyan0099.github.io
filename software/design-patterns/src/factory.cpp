// 工厂方法 · 物流：卡车与轮船
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
