// 状态模式 · C++ 实现：每个状态一个类，由状态自己决定下一步去哪
// 编译：g++ -std=c++17 -Wall -Wextra state.cpp -o state_cpp
#include <cstdio>

enum class Event { Ign, Start, Stop, OverTemp, Clear };
const char* evName(Event e) {
    switch (e) {
        case Event::Ign: return "IGN";
        case Event::Start: return "START";
        case Event::Stop: return "STOP";
        case Event::OverTemp: return "OVERTEMP";
        case Event::Clear: return "CLEAR";
    }
    return "?";
}

class Ecu;
class State {
public:
    virtual ~State() = default;
    virtual const char* name() const = 0;
    virtual State* on(Event e, Ecu& ctx) = 0;   // 返回 nullptr 表示拒绝
};

class Off : public State {
public:
    const char* name() const override { return "OFF"; }
    State* on(Event e, Ecu& ctx) override;
};

class Acc : public State {
public:
    const char* name() const override { return "ACC"; }
    State* on(Event e, Ecu& ctx) override;
};

class On : public State {
public:
    const char* name() const override { return "ON"; }
    State* on(Event e, Ecu& ctx) override;
};

class Run : public State {
public:
    const char* name() const override { return "RUN"; }
    State* on(Event e, Ecu& ctx) override;
};

class Fault : public State {
public:
    const char* name() const override { return "FAULT"; }
    State* on(Event e, Ecu& ctx) override;
};

// 函数内静态对象：避免静态初始化顺序问题
static Off&   stOff()   { static Off s;   return s; }
static Acc&   stAcc()   { static Acc s;   return s; }
static On&    stOn()    { static On s;    return s; }
static Run&   stRun()   { static Run s;   return s; }
static Fault& stFault() { static Fault s; return s; }

class Ecu {
public:
    explicit Ecu(State* s) : st_(s) {}
    void inject(Event e) {
        State* next = st_->on(e, *this);
        if (!next) {
            std::printf("[ECU] %-5s + %-8s -> 拒绝（该状态下事件非法）\n", st_->name(), evName(e));
            return;
        }
        std::printf("[ECU] %-5s + %-8s -> %s\n", st_->name(), evName(e), next->name());
        st_ = next;
    }
    const char* name() const { return st_->name(); }
private:
    State* st_;
};

State* Off::on(Event e, Ecu&) {
    if (e == Event::Ign) return &stAcc();
    return nullptr;
}
State* Acc::on(Event e, Ecu&) {
    switch (e) {
        case Event::Ign: return &stOff();
        case Event::Start: return &stOn();
        case Event::OverTemp: return &stFault();
        default: return nullptr;
    }
}
State* On::on(Event e, Ecu&) {
    switch (e) {
        case Event::Ign: return &stOff();
        case Event::Start: return &stRun();
        case Event::Stop: return &stAcc();
        case Event::OverTemp: return &stFault();
        default: return nullptr;
    }
}
State* Run::on(Event e, Ecu&) {
    switch (e) {
        case Event::Ign: return &stOff();
        case Event::Stop: return &stOn();
        case Event::OverTemp: return &stFault();
        default: return nullptr;
    }
}
State* Fault::on(Event e, Ecu&) {
    switch (e) {
        case Event::Ign: return &stOff();
        case Event::Clear: return &stOff();
        default: return nullptr;
    }
}

int main() {
    Ecu e(&stOff());
    const Event seq[] = { Event::Ign, Event::Start, Event::Start, Event::OverTemp,
                          Event::Start, Event::Clear, Event::Stop };
    const char* why[] = {
        "上电钥匙拧到 ACC", "发动机点火", "运行中再按 START", "冷却液超温",
        "故障下点火", "故障清除", "已 OFF 再按 STOP"
    };
    for (int i = 0; i < 7; ++i) {
        std::printf("--- %s ---\n", why[i]);
        e.inject(seq[i]);
    }
    std::printf("最终状态：%s\n", e.name());
    return 0;
}
