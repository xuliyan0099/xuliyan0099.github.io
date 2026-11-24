// 策略模式 · C++ 实现：同一场景，改用抽象基类 + 虚函数
// 编译：g++ -std=c++17 -Wall -Wextra strategy.cpp -o strategy_cpp
#include <cstdio>
#include <memory>
#include <vector>

struct Frame { int id; int due_ms; };

class IScheduler {
public:
    virtual ~IScheduler() = default;
    virtual const char* name() const = 0;
    virtual int pick(const std::vector<Frame>& q) const = 0;
};

class Fifo final : public IScheduler {
public:
    const char* name() const override { return "FIFO"; }
    int pick(const std::vector<Frame>& q) const override { return q.empty() ? -1 : 0; }
};

class Edf final : public IScheduler {
public:
    const char* name() const override { return "EDF"; }
    int pick(const std::vector<Frame>& q) const override {
        int best = -1;
        for (int i = 0; i < static_cast<int>(q.size()); ++i)
            if (best < 0 || q[i].due_ms < q[best].due_ms) best = i;
        return best;
    }
};

class PriorityId final : public IScheduler {
public:
    const char* name() const override { return "PRIO"; }
    int pick(const std::vector<Frame>& q) const override {
        int best = -1;
        for (int i = 0; i < static_cast<int>(q.size()); ++i)
            if (best < 0 || q[i].id < q[best].id) best = i;
        return best;
    }
};

// 上下文持有策略的所有权；换策略即换对象
class TxQueue {
public:
    void set(std::unique_ptr<IScheduler> s) { sched_ = std::move(s); }

    void drain() {
        std::printf("%-5s ->", sched_->name());
        while (!q_.empty()) {
            int i = sched_->pick(q_);
            if (i < 0) break;
            std::printf(" %03X", q_[static_cast<std::size_t>(i)].id);
            q_.erase(q_.begin() + i);
        }
        std::printf("\n");
    }

    void reset(const std::vector<Frame>& seed) { q_ = seed; }

private:
    std::vector<Frame> q_;
    std::unique_ptr<IScheduler> sched_;
};

int main() {
    const std::vector<Frame> seed = {
        { 0x210, 10 }, { 0x120, 4 }, { 0x305, 2 }, { 0x180, 8 }, { 0x0A0, 6 }
    };
    TxQueue q;

    q.reset(seed);   q.set(std::make_unique<Fifo>());       q.drain();
    q.reset(seed);   q.set(std::make_unique<Edf>());        q.drain();
    q.reset(seed);   q.set(std::make_unique<PriorityId>()); q.drain();
    return 0;
}
