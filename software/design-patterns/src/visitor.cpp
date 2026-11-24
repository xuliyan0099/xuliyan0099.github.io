// 访问者 · C++：accept/visit 双向分派，节点与统计彻底解耦
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
