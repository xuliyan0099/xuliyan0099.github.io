// 单例模式 · C++ 实现：Meyers singleton（C++11 起初始化线程安全）
// 编译：g++ -std=c++17 -Wall -Wextra singleton.cpp -o singleton_cpp
#include <cstdio>

class Config {
public:
    static Config& instance() {
        static Config c;          // 局部静态：首次调用时构造，C++11 保证线程安全
        return c;
    }

    int timeout_ms = 500;
    int log_level  = 2;

private:
    Config() = default;
    Config(const Config&) = delete;
    Config& operator=(const Config&) = delete;
};

int main() {
    Config& a = Config::instance();
    Config& b = Config::instance();
    Config& c = Config::instance();

    std::printf("三次取实例是同一个对象：%s\n", (&a == &b && &b == &c) ? "是" : "否");

    a.timeout_ms = 800;
    std::printf("通过 a 改，通过 b 读：timeout=%d\n", b.timeout_ms);
    std::printf("a 与 b 是同一块内存：%s\n", (&a == &b) ? "是" : "否");
    // 拷贝构造已 delete：写 `Config copy = a;` 会在编译期失败，而不是运行时多一个实例
    return 0;
}
