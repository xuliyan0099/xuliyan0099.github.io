// 原型 · 克隆图形
// g++ -std=c++17 -Wall -Wextra prototype.cpp -o prototype_cpp
#include <cstdio>
#include <memory>
#include <string>

class Shape {
public:
    explicit Shape(std::string kind, int size) : kind_(std::move(kind)), size_(size) {}
    virtual ~Shape() = default;
    virtual std::unique_ptr<Shape> clone() const = 0;

    std::string kind() const { return kind_; }
    int size() const { return size_; }
    void setSize(int s) { size_ = s; }

private:
    std::string kind_;
    int size_;
};

class Circle final : public Shape {
public:
    Circle() : Shape("圆", 10) {}
    std::unique_ptr<Shape> clone() const override {
        return std::make_unique<Circle>(*this);
    }
};

class Square final : public Shape {
public:
    Square() : Shape("方", 10) {}
    std::unique_ptr<Shape> clone() const override {
        return std::make_unique<Square>(*this);
    }
};

int main()
{
    Circle proto;
    auto a = proto.clone();
    auto b = proto.clone();
    std::printf("克隆两份圆：a.size=%d  b.size=%d\n", a->size(), b->size());

    b->setSize(25);
    std::printf("改 b 之后：a.size=%d  b.size=%d（互不影响）\n", a->size(), b->size());
    std::printf("原型仍是 size=%d\n", proto.size());
    return 0;
}
