// 备忘录 · 撤销快照
// g++ -std=c++17 -Wall -Wextra memento.cpp -o memento_cpp
#include <cstdio>
#include <string>

class Memento {
public:
    Memento(std::string text, int cursor) : text_(std::move(text)), cursor_(cursor) {}
private:
    friend class Editor;
    std::string text_;
    int cursor_;
};

class Editor {
public:
    void setText(std::string t, int cursor) { text_ = std::move(t); cursor_ = cursor; }
    const std::string& text() const { return text_; }
    int cursor() const { return cursor_; }

    Memento save() const { return Memento(text_, cursor_); }
    void restore(const Memento& m) { text_ = m.text_; cursor_ = m.cursor_; }

private:
    std::string text_;
    int cursor_ = 0;
};

int main()
{
    Editor e;
    e.setText("hello", 5);
    std::printf("初始：\"%s\" cursor=%d\n", e.text().c_str(), e.cursor());

    auto snap = e.save();

    e.setText("hello world", 11);
    std::printf("编辑后：\"%s\" cursor=%d\n", e.text().c_str(), e.cursor());

    e.restore(snap);
    std::printf("恢复后：\"%s\" cursor=%d\n", e.text().c_str(), e.cursor());
    std::puts("快照是值拷贝，编辑过程不会污染它");
    return 0;
}
