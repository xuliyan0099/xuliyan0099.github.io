// 命令模式 · C++ 实现：命令对象自带接收者引用，历史栈持有所有权
// 编译：g++ -std=c++17 -Wall -Wextra command.cpp -o command_cpp
#include <cstdio>
#include <deque>
#include <memory>

class Device {
public:
    int gain() const { return gain_; }
    int mode() const { return mode_; }
    void setGain(int v) { gain_ = v; }
    void setMode(int v) { mode_ = v; }
private:
    int gain_ = 0;
    int mode_ = 0;
};

class ICommand {
public:
    virtual ~ICommand() = default;
    virtual void exec() = 0;
    virtual void undo() = 0;
};

class SetGain final : public ICommand {
public:
    SetGain(Device& d, int v) : d_(d), v_(v) {}
    void exec() override { old_ = d_.gain(); d_.setGain(v_); std::printf("  exec  SetGain(%d)，旧值 %d\n", v_, old_); }
    void undo() override { d_.setGain(old_); std::printf("  undo  SetGain(%d)，还原成 %d\n", v_, old_); }
private:
    Device& d_;
    int v_;
    int old_ = 0;
};

class SetMode final : public ICommand {
public:
    SetMode(Device& d, int v) : d_(d), v_(v) {}
    void exec() override { old_ = d_.mode(); d_.setMode(v_); std::printf("  exec  SetMode(%d)，旧值 %d\n", v_, old_); }
    void undo() override { d_.setMode(old_); std::printf("  undo  SetMode(%d)，还原成 %d\n", v_, old_); }
private:
    Device& d_;
    int v_;
    int old_ = 0;
};

// 调用者：只看到 ICommand
class Invoker {
public:
    void post(std::unique_ptr<ICommand> cmd) {
        queue_.push_back(std::move(cmd));
        std::printf("  post  队列长度=%d\n", static_cast<int>(queue_.size()));
    }
    void run() {
        std::printf("--- 执行队列 ---\n");
        for (auto& c : queue_) { c->exec(); history_.push_back(std::move(c)); }
        queue_.clear();
    }
    void undoLast() {
        if (history_.empty()) { std::printf("  没有可撤销的命令\n"); return; }
        history_.back()->undo();
        history_.pop_back();
    }
private:
    std::deque<std::unique_ptr<ICommand>> queue_;
    std::deque<std::unique_ptr<ICommand>> history_;
};

int main() {
    Device dev;
    Invoker iv;
    std::printf("初始 gain=%d mode=%d\n", dev.gain(), dev.mode());

    iv.post(std::make_unique<SetGain>(dev, 12));
    iv.post(std::make_unique<SetGain>(dev, 20));
    iv.post(std::make_unique<SetMode>(dev, 2));
    iv.run();
    std::printf("执行后 gain=%d mode=%d\n", dev.gain(), dev.mode());

    std::printf("--- 撤销两次 ---\n");
    iv.undoLast();
    iv.undoLast();
    std::printf("撤销后 gain=%d mode=%d\n", dev.gain(), dev.mode());
    return 0;
}
