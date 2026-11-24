// 命令 · 编辑器撤销
// g++ -std=c++17 -Wall -Wextra command.cpp -o command_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

class Editor {
public:
    std::string text;
};

class Command {
public:
    virtual ~Command() = default;
    virtual void execute(Editor& e) = 0;
    virtual void undo(Editor& e) = 0;
};

class Append final : public Command {
public:
    explicit Append(char c) : c_(c) {}
    void execute(Editor& e) override { e.text.push_back(c_); }
    void undo(Editor& e) override { if (!e.text.empty()) e.text.pop_back(); }
private:
    char c_;
};

class Delete final : public Command {
public:
    void execute(Editor& e) override {
        if (!e.text.empty()) { last_ = e.text.back(); e.text.pop_back(); }
    }
    void undo(Editor& e) override { e.text.push_back(last_); }
private:
    char last_ = 0;
};

class Invoker {
public:
    void run(std::unique_ptr<Command> c, Editor& e) {
        c->execute(e);
        history_.push_back(std::move(c));
    }
    void undo(Editor& e) {
        if (history_.empty()) return;
        history_.back()->undo(e);
        history_.pop_back();
    }
private:
    std::vector<std::unique_ptr<Command>> history_;
};

int main()
{
    Editor e;
    Invoker inv;
    inv.run(std::make_unique<Append>('H'), e);
    inv.run(std::make_unique<Append>('i'), e);
    inv.run(std::make_unique<Append>('!'), e);
    std::printf("输入三个命令后：\"%s\"\n", e.text.c_str());

    inv.undo(e);
    std::printf("撤销一步：\"%s\"\n", e.text.c_str());
    inv.undo(e);
    std::printf("撤销两步：\"%s\"\n", e.text.c_str());
    return 0;
}
