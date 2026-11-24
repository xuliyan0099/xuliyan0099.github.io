// C++ 的对应写法：虚函数由编译器生成 vptr + vtable
// 编译：g++ -std=c++17 -Wall -Wextra coop.cpp -o coop_cpp
#include <cstdio>

class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;
    virtual const char* name() const = 0;
};

class Rect final : public Shape {
public:
    Rect(double w, double h) : w_(w), h_(h) {}
    double area() const override { return w_ * h_; }
    const char* name() const override { return "rect"; }
private:
    double w_, h_;
};

class Circle final : public Shape {
public:
    explicit Circle(double r) : r_(r) {}
    double area() const override { return 3.14159 * r_ * r_; }
    const char* name() const override { return "circle"; }
private:
    double r_;
};

int main() {
    Rect   r(3.0, 4.0);
    Circle c(1.0);

    Shape* shapes[] = { &r, &c };
    for (Shape* s : shapes)
        std::printf("%-6s area=%6.2f\n", s->name(), s->area());

    std::printf("sizeof(Rect)=%d  sizeof(Circle)=%d  sizeof(void*)=%d\n",
                static_cast<int>(sizeof(Rect)), static_cast<int>(sizeof(Circle)),
                static_cast<int>(sizeof(void*)));
    std::printf("单继承下 vptr 也在偏移 0：把 Rect* 转 Shape* 不用调整地址\n");
    return 0;
}
