// 装饰 · C++：unique_ptr 串起流水线，析构自动拆链
// 编译：g++ -std=c++17 -Wall -Wextra decorator.cpp -o decorator_cpp
#include <cstdio>
#include <memory>

class Sensor {
public:
    virtual ~Sensor() = default;
    virtual int read(int raw) const = 0;
};

class Raw : public Sensor {
public:
    int read(int raw) const override { return raw; }
};

class Offset : public Sensor {
public:
    Offset(std::unique_ptr<Sensor> in, int off) : in_(std::move(in)), off_(off) {}
    int read(int raw) const override { return in_->read(raw) + off_; }
private:
    std::unique_ptr<Sensor> in_;
    int off_;
};

class Clamp : public Sensor {
public:
    Clamp(std::unique_ptr<Sensor> in, int hi) : in_(std::move(in)), hi_(hi) {}
    int read(int raw) const override
    {
        int v = in_->read(raw);
        if (v < 0) v = 0;
        if (v > hi_) v = hi_;
        return v;
    }
private:
    std::unique_ptr<Sensor> in_;
    int hi_;
};

int main()
{
    auto raw = std::make_unique<Raw>();
    auto off = std::make_unique<Offset>(std::make_unique<Raw>(), 5);
    auto clamp = std::make_unique<Clamp>(
        std::make_unique<Offset>(std::make_unique<Raw>(), 5), 40);

    std::printf("raw       = %d\n", raw->read(42));
    std::printf("+offset5  = %d\n", off->read(42));
    std::printf("+clamp40  = %d\n", clamp->read(42));

    auto neg = std::make_unique<Clamp>(
        std::make_unique<Offset>(std::make_unique<Raw>(), -60), 40);
    std::printf("负值路径  = %d\n", neg->read(42));
    std::printf("三层顺序：raw -> offset -> clamp，换顺序结果会变\n");
    return 0;
}
