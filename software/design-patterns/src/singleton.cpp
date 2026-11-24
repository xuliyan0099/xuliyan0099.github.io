// 单例 · 全局配置
// g++ -std=c++17 -Wall -Wextra singleton.cpp -o singleton_cpp
#include <cstdio>
#include <string>

class Config {
public:
    static Config& instance() {
        static Config cfg;
        return cfg;
    }

    std::string theme = "light";
    int font_size = 12;

    Config(const Config&) = delete;
    Config& operator=(const Config&) = delete;

private:
    Config() { std::puts("  初始化配置（只发生一次）"); }
};

int main()
{
    Config& a = Config::instance();
    Config& b = Config::instance();
    Config& c = Config::instance();

    std::printf("取三次实例：%p %p %p（同一个地址）\n",
                static_cast<void*>(&a), static_cast<void*>(&b), static_cast<void*>(&c));

    a.theme = "dark";
    a.font_size = 16;
    std::printf("通过 a 改成 %s/%d，通过 c 读：%s/%d\n",
                a.theme.c_str(), a.font_size, c.theme.c_str(), c.font_size);
    return 0;
}
