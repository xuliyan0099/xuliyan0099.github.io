// 状态 · 订单状态流转
// g++ -std=c++17 -Wall -Wextra state.cpp -o state_cpp
#include <cstdio>
#include <memory>
#include <string>

class Order;

class State {
public:
    virtual ~State() = default;
    virtual const char* name() const = 0;
    virtual State* next(const std::string& event) = 0;
};

class New final : public State {
public:
    const char* name() const override { return "新建"; }
    State* next(const std::string& e) override;
};
class Paid final : public State {
public:
    const char* name() const override { return "已支付"; }
    State* next(const std::string& e) override;
};
class Shipped final : public State {
public:
    const char* name() const override { return "已发货"; }
    State* next(const std::string& e) override;
};
class Done final : public State {
public:
    const char* name() const override { return "已完成"; }
    State* next(const std::string&) override { return this; }
};

static New S_NEW; static Paid S_PAID; static Shipped S_SHIPPED; static Done S_DONE;

State* New::next(const std::string& e) { return e == "pay" ? static_cast<State*>(&S_PAID) : this; }
State* Paid::next(const std::string& e) { return e == "ship" ? static_cast<State*>(&S_SHIPPED) : this; }
State* Shipped::next(const std::string& e) { return e == "done" ? static_cast<State*>(&S_DONE) : this; }

class Order {
public:
    explicit Order(State* s) : s_(s) {}
    void handle(const std::string& e) {
        State* n = s_->next(e);
        if (n == s_) std::printf("%s 状态下 %s 被拒绝\n", s_->name(), e.c_str());
        else { std::printf("%s -> %s（%s）\n", s_->name(), n->name(), e.c_str()); s_ = n; }
    }
private:
    State* s_;
};

int main()
{
    Order o(&S_NEW);
    o.handle("pay"); o.handle("pay"); o.handle("ship"); o.handle("done");
    return 0;
}
