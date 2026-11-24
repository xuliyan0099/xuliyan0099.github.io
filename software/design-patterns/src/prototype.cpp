// 原型 · C++：clone() 返回 unique_ptr，注册表只读，副本归调用方
// 编译：g++ -std=c++17 -Wall -Wextra prototype.cpp -o prototype_cpp
#include <cstdio>
#include <map>
#include <memory>
#include <string>

struct Config {
    std::string name;
    int timeout_ms;
    int retry;
    virtual ~Config() = default;
    virtual std::unique_ptr<Config> clone() const = 0;
};

struct FastConfig : Config {
    std::unique_ptr<Config> clone() const override
    {
        return std::make_unique<FastConfig>(*this);
    }
};

int main()
{
    std::map<std::string, std::unique_ptr<Config>> protos;
    protos["fast"] = std::make_unique<FastConfig>();
    protos["fast"]->name = "fast";
    protos["fast"]->timeout_ms = 120;
    protos["fast"]->retry = 1;

    auto a = protos["fast"]->clone();
    auto b = protos["fast"]->clone();
    b->timeout_ms = 90;
    b->name = "fast-tuned";

    std::printf("original name=%-8s timeout=%d\n", protos["fast"]->name.c_str(), protos["fast"]->timeout_ms);
    std::printf("clone-a  name=%-8s timeout=%d\n", a->name.c_str(), a->timeout_ms);
    std::printf("clone-b  name=%-8s timeout=%d\n", b->name.c_str(), b->timeout_ms);
    std::printf("原型未变：timeout=%d\n", protos["fast"]->timeout_ms);
    return 0;
}
