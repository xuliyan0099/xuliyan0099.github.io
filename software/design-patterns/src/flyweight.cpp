// 享元 · C++：工厂缓存 shared_ptr，1000 个句柄只留 8 份对象
// 编译：g++ -std=c++17 -Wall -Wextra flyweight.cpp -o flyweight_cpp
#include <cstdio>
#include <map>
#include <memory>
#include <string>
#include <vector>

struct Signal {
    std::string unit;
    double scale;
};

class SignalFactory {
public:
    std::shared_ptr<const Signal> intern(const std::string &unit, double scale)
    {
        auto it = pool_.find(unit);
        if (it != pool_.end()) return it->second;
        auto s = std::make_shared<const Signal>(Signal{ unit, scale });
        pool_.emplace(unit, s);
        return s;
    }
    std::size_t size() const { return pool_.size(); }
private:
    std::map<std::string, std::shared_ptr<const Signal>> pool_;
};

int main()
{
    const std::string units[] = { "C", "kPa", "rpm", "%", "V", "A", "km/h", "deg" };
    SignalFactory f;
    std::vector<std::shared_ptr<const Signal>> signals;
    signals.reserve(1000);
    for (int i = 0; i < 1000; i++)
        signals.push_back(f.intern(units[static_cast<size_t>(i) % 8], 1.0 + (i % 8) / 10.0));

    std::printf("信号 1000 个，描述池 %zu 份\n", f.size());
    std::printf("sig[0]   unit=%-4s scale=%.1f use_count=%ld\n",
                signals[0]->unit.c_str(), signals[0]->scale, signals[0].use_count());
    std::printf("sig[999] unit=%-4s scale=%.1f\n",
                signals[999]->unit.c_str(), signals[999]->scale);
    std::printf("指针相同：sig[0]==sig[8] -> %s\n", signals[0] == signals[8] ? "yes" : "no");
    return 0;
}
