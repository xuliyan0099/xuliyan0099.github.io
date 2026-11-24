// 桥接 · 形状 × 渲染器
// g++ -std=c++17 -Wall -Wextra bridge.cpp -o bridge_cpp
#include <cstdio>
#include <memory>
#include <string>

class Renderer {
public:
    virtual ~Renderer() = default;
    virtual std::string name() const = 0;
    virtual void circle(int size) const = 0;
    virtual void square(int size) const = 0;
};

class VectorRenderer final : public Renderer {
public:
    std::string name() const override { return "矢量"; }
    void circle(int s) const override { std::printf("矢量圆 r=%d\n", s); }
    void square(int s) const override { std::printf("矢量方 w=%d\n", s); }
};

class RasterRenderer final : public Renderer {
public:
    std::string name() const override { return "位图"; }
    void circle(int s) const override { std::printf("位图圆 半径 %dpx\n", s); }
    void square(int s) const override { std::printf("位图方 边长 %dpx\n", s); }
};

class Shape {
public:
    Shape(std::unique_ptr<Renderer> r, int size) : r_(std::move(r)), size_(size) {}
    virtual ~Shape() = default;
    virtual std::string name() const = 0;
    void draw() const {
        std::printf("[%s] %s size=%d -> ", r_->name().c_str(), name().c_str(), size_);
        if (name() == "Circle") r_->circle(size_);
        else                    r_->square(size_);
    }
protected:
    const Renderer& renderer() const { return *r_; }
    int size() const { return size_; }
private:
    std::unique_ptr<Renderer> r_;
    int size_;
};

class Circle final : public Shape {
public:
    Circle(std::unique_ptr<Renderer> r, int s) : Shape(std::move(r), s) {}
    std::string name() const override { return "Circle"; }
};

class Square final : public Shape {
public:
    Square(std::unique_ptr<Renderer> r, int s) : Shape(std::move(r), s) {}
    std::string name() const override { return "Square"; }
};

int main()
{
    Circle v1(std::make_unique<VectorRenderer>(), 5); v1.draw();
    Square v2(std::make_unique<VectorRenderer>(), 5); v2.draw();
    Circle r1(std::make_unique<RasterRenderer>(), 5); r1.draw();
    Square r2(std::make_unique<RasterRenderer>(), 5); r2.draw();
    std::puts("2 种形状 × 2 种渲染器 = 4 种组合，没有 4 个子类");
    return 0;
}
