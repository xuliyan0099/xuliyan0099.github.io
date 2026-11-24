// 观察者 · 天气站订阅
// g++ -std=c++17 -Wall -Wextra observer.cpp -o observer_cpp
#include <cstdio>
#include <string>
#include <vector>

class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(int temp) = 0;
};

class WeatherStation {
public:
    void subscribe(Observer* o) { subs_.push_back(o); }
    void setTemp(int t) {
        std::printf("气温 -> %d℃\n", t);
        for (auto o : subs_) o->update(t);
    }
private:
    std::vector<Observer*> subs_;
};

class PhoneApp final : public Observer {
public:
    void update(int t) override { std::printf("  手机 App：显示 %d℃\n", t); }
};

class BigScreen final : public Observer {
public:
    void update(int t) override { std::printf("  客厅大屏：大屏刷新 %d℃\n", t); }
};

int main()
{
    WeatherStation s;
    PhoneApp a;
    BigScreen b;
    s.subscribe(&a);
    s.subscribe(&b);

    s.setTemp(21);
    s.setTemp(24);
    std::puts("发布者不认识订阅者，只遍历名单");
    return 0;
}
