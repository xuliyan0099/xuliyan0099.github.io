// 装饰器 · 给文本加粗、加斜体
// g++ -std=c++17 -Wall -Wextra decorator.cpp -o decorator_cpp
#include <cstdio>
#include <memory>
#include <string>

class Text {
public:
    virtual ~Text() = default;
    virtual std::string render() const = 0;
};

class Plain final : public Text {
public:
    explicit Plain(std::string s) : s_(std::move(s)) {}
    std::string render() const override { return s_; }
private:
    std::string s_;
};

class Bold final : public Text {
public:
    explicit Bold(std::unique_ptr<Text> inner) : inner_(std::move(inner)) {}
    std::string render() const override { return "<b>" + inner_->render() + "</b>"; }
private:
    std::unique_ptr<Text> inner_;
};

class Italic final : public Text {
public:
    explicit Italic(std::unique_ptr<Text> inner) : inner_(std::move(inner)) {}
    std::string render() const override { return "<i>" + inner_->render() + "</i>"; }
private:
    std::unique_ptr<Text> inner_;
};

int main()
{
    std::printf("原始：%s\n", Plain("hello").render().c_str());
    std::printf("加粗：%s\n", Bold(std::make_unique<Plain>("hello")).render().c_str());
    std::printf("加粗+斜体：%s\n",
                Italic(std::make_unique<Bold>(std::make_unique<Plain>("hello"))).render().c_str());
    std::printf("顺序反过来：%s\n",
                Bold(std::make_unique<Italic>(std::make_unique<Plain>("hello"))).render().c_str());
    return 0;
}
