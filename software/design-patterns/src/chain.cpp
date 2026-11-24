// 职责链 · 客服逐级升级
// g++ -std=c++17 -Wall -Wextra chain.cpp -o chain_cpp
#include <cstdio>
#include <memory>
#include <string>

class Handler {
public:
    explicit Handler(std::string name, int maxLevel)
        : name_(std::move(name)), maxLevel_(maxLevel) {}
    virtual ~Handler() = default;

    Handler& setNext(std::unique_ptr<Handler> next) {
        next_ = std::move(next);
        return *next_;
    }

    void dispatch(int level, const std::string& msg) {
        std::printf("工单 L%d「%s」\n", level, msg.c_str());
        Handler* h = this;
        while (h) {
            if (h->canHandle(level, msg)) {
                std::printf("  -> %s 接手\n", h->name_.c_str());
                return;
            }
            h = h->next_.get();
        }
        std::puts("  没人处理");
    }

protected:
    virtual bool canHandle(int level, const std::string& msg) = 0;
    std::string name_;

private:
    int maxLevel_;
    std::unique_ptr<Handler> next_;
};

class Faq final : public Handler {
public:
    Faq() : Handler("FAQ", 1) {}
protected:
    bool canHandle(int level, const std::string& msg) override {
        if (level <= 1) { std::printf("  FAQ：%s\n", msg.c_str()); return true; }
        return false;
    }
};

class Tech final : public Handler {
public:
    Tech() : Handler("技术支持", 2) {}
protected:
    bool canHandle(int level, const std::string& msg) override {
        if (level <= 2) { std::printf("  技术支持：%s\n", msg.c_str()); return true; }
        return false;
    }
};

class Engineer final : public Handler {
public:
    Engineer() : Handler("工程师", 9) {}
protected:
    bool canHandle(int level, const std::string& msg) override {
        (void)level;
        std::printf("  工程师：%s\n", msg.c_str());
        return true;
    }
};

int main()
{
    auto faq = std::make_unique<Faq>();
    auto tech = std::make_unique<Tech>();
    auto eng = std::make_unique<Engineer>();
    faq->setNext(std::move(tech)).setNext(std::move(eng));

    faq->dispatch(1, "怎么改密码");
    faq->dispatch(2, "客户端连不上");
    faq->dispatch(3, "服务器 500");
    return 0;
}
