// 中介者 · C++：Colleague 只持 Mediator&，路由规则集中在一处
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
