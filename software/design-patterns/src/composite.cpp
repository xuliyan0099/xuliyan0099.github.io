// 组合 · C++：Group 持有 unique_ptr，析构自动递归
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
