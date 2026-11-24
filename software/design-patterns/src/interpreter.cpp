// 解释器 · 算术表达式 (2 + 3) * 4
// g++ -std=c++17 -Wall -Wextra interpreter.cpp -o interpreter_cpp
#include <cstdio>
#include <memory>

class Expr {
public:
    virtual ~Expr() = default;
    virtual int eval() const = 0;
};

class Number final : public Expr {
public:
    explicit Number(int v) : v_(v) {}
    int eval() const override { return v_; }
private:
    int v_;
};

class Add final : public Expr {
public:
    Add(std::unique_ptr<Expr> l, std::unique_ptr<Expr> r)
        : l_(std::move(l)), r_(std::move(r)) {}
    int eval() const override { return l_->eval() + r_->eval(); }
private:
    std::unique_ptr<Expr> l_, r_;
};

class Mul final : public Expr {
public:
    Mul(std::unique_ptr<Expr> l, std::unique_ptr<Expr> r)
        : l_(std::move(l)), r_(std::move(r)) {}
    int eval() const override { return l_->eval() * r_->eval(); }
private:
    std::unique_ptr<Expr> l_, r_;
};

int main()
{
    auto tree = std::make_unique<Mul>(
        std::make_unique<Add>(std::make_unique<Number>(2), std::make_unique<Number>(3)),
        std::make_unique<Number>(4));
    std::puts("表达式： (2 + 3) * 4");
    std::printf("求值 = %d\n", tree->eval());
    std::puts("换成 (2 + 3) * 5 只需换一个叶子，树结构不变");
    return 0;
}
