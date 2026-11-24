// 观察者模式 · C++ 实现：shared_ptr 订户 + 通知时拷贝列表
// 编译：g++ -std=c++17 -Wall -Wextra observer.cpp -o observer_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

class Observer {
public:
    virtual ~Observer() = default;
    virtual void onEvent(const std::string& ev) = 0;
};

class Subject {
public:
    int attach(std::shared_ptr<Observer> o) {
        slots_.push_back(Slot{ next_id_++, std::move(o) });
        return slots_.back().id;
    }

    // 通知中退订：只清空指针，不移动元素
    void detach(int id) {
        for (auto& s : slots_) {
            if (s.id != id) continue;
            s.obs.reset();
            if (depth_ == 0) compact();
            return;
        }
    }

    void notify(const std::string& ev) {
        auto snapshot = slots_;          // 关键：拷贝，通知期间列表不被改动
        ++depth_;
        for (auto& s : snapshot)
            if (s.obs) s.obs->onEvent(ev);
        --depth_;
        if (depth_ == 0) compact();
    }

private:
    struct Slot { int id; std::shared_ptr<Observer> obs; };
    std::vector<Slot> slots_;
    int next_id_ = 1;
    int depth_ = 0;

    void compact() {
        std::vector<Slot> live;
        for (auto& s : slots_) if (s.obs) live.push_back(std::move(s));
        slots_ = std::move(live);
    }
};

class Gauge final : public Observer {
public:
    void onEvent(const std::string& ev) override { std::printf("  gauge    <- %s\n", ev.c_str()); }
};

class Diag final : public Observer {
public:
    void onEvent(const std::string& ev) override { std::printf("  diag     <- %s\n", ev.c_str()); }
};

class Recorder final : public Observer {
public:
    explicit Recorder(Subject& s) : s_(s) {}
    void bind(int id) { id_ = id; }
    void onEvent(const std::string& ev) override {
        std::printf("  recorder <- %s（收到后退订自己）\n", ev.c_str());
        if (id_ > 0) s_.detach(id_);
    }
private:
    Subject& s_;
    int id_ = 0;
};

int main() {
    Subject bus;
    auto gauge = std::make_shared<Gauge>();
    auto rec   = std::make_shared<Recorder>(bus);
    auto diag  = std::make_shared<Diag>();

    bus.attach(gauge);
    rec->bind(bus.attach(rec));
    bus.attach(diag);

    std::printf("安全版本：\n");
    bus.notify("speed=62");
    bus.notify("speed=63");
    return 0;
}
