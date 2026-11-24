// 模板方法 · C++：run() 非虚，步骤虚函数，子类只覆写细节
// 编译：g++ -std=c++17 -Wall -Wextra template_method.cpp -o template_method_cpp
#include <cstdio>
#include <string>

class SelfTest {
public:
    explicit SelfTest(std::string name) : name_(std::move(name)) {}
    virtual ~SelfTest() = default;

    // 模板：不打算被覆写
    bool run() const
    {
        std::printf("== %s ==\n", name_.c_str());
        std::printf("step1 power  ... ");
        if (!power())  { std::printf("FAIL\n"); return false; }
        std::printf("OK\n");
        std::printf("step2 comm   ... ");
        if (!comm())   { std::printf("FAIL\n"); return false; }
        std::printf("OK\n");
        std::printf("step3 sensor ... ");
        if (!sensor()) { std::printf("FAIL\n"); return false; }
        std::printf("OK\n");
        std::printf("result PASS\n");
        return true;
    }
protected:
    virtual bool power() const = 0;
    virtual bool comm() const = 0;
    virtual bool sensor() const = 0;
private:
    std::string name_;
};

class BenchTest : public SelfTest {
public:
    BenchTest() : SelfTest("bench") {}
protected:
    bool power() const override { return true; }
    bool comm() const override { return true; }
    bool sensor() const override { return true; }
};

class FieldTest : public SelfTest {
public:
    FieldTest() : SelfTest("field") {}
protected:
    bool power() const override { return true; }
    bool comm() const override { return true; }
    bool sensor() const override { return false; }
};

int main()
{
    BenchTest b;
    FieldTest f;
    b.run();
    f.run();
    std::printf("两个变体共用同一套顺序与日志\n");
    return 0;
}
