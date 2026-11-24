// 工厂模式 · C++ 实现：注册表 + std::function + 自注册模板
// 编译：g++ -std=c++17 -Wall -Wextra factory.cpp -o factory_cpp
#include <cstdio>
#include <functional>
#include <map>
#include <memory>
#include <string>
#include <vector>

class Driver {
public:
    virtual ~Driver() = default;
    virtual const char* name() const = 0;
    virtual bool init() = 0;
};

class Sht3x final : public Driver {
public:
    const char* name() const override { return "sht3x"; }
    bool init() override { std::printf("    sht3x init @0x44\n"); return true; }
};

class Ntc final : public Driver {
public:
    const char* name() const override { return "ntc"; }
    bool init() override { std::printf("    ntc init on pin 12\n"); return true; }
};

class DriverFactory {
public:
    using Creator = std::function<std::unique_ptr<Driver>()>;

    static DriverFactory& instance() {      // 函数内静态：规避初始化顺序问题
        static DriverFactory f;
        return f;
    }

    void reg(const std::string& name, Creator c) {
        map_[name] = std::move(c);
        std::printf("  register %-6s  (注册表长度=%d)\n", name.c_str(), static_cast<int>(map_.size()));
    }

    std::unique_ptr<Driver> create(const std::string& name) const {
        auto it = map_.find(name);
        if (it == map_.end()) return nullptr;
        return it->second();
    }

    std::vector<std::string> names() const {
        std::vector<std::string> v;
        for (const auto& kv : map_) v.push_back(kv.first);
        return v;
    }

private:
    std::map<std::string, Creator> map_;
};

// 自注册：定义一个静态对象，构造即登记
template <class T>
struct AutoReg {
    explicit AutoReg(const char* name) {
        DriverFactory::instance().reg(name, [] { return std::make_unique<T>(); });
    }
};

static AutoReg<Ntc>   g_reg_ntc("ntc");
static AutoReg<Sht3x> g_reg_sht("sht3x");

int main() {
    std::printf("启动后注册表：\n");
    for (const auto& n : DriverFactory::instance().names()) std::printf("  %s\n", n.c_str());
    std::printf("\n");

    const char* wanted[] = { "sht3x", "ntc", "bme280" };
    for (const char* w : wanted) {
        std::printf("create(\"%s\"):\n", w);
        auto d = DriverFactory::instance().create(w);
        if (!d) { std::printf("    未注册，返回 nullptr（由上层决定降级）\n"); continue; }
        d->init();
        std::printf("    name=%s\n", d->name());
    }
    return 0;
}
