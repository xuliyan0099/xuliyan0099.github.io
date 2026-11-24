// 解释器 · C++：表达式对象各自 eval，组合靠 unique_ptr 持有子树
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
