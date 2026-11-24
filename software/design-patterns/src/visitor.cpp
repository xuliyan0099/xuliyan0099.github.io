// 访问者 · 文件统计
// g++ -std=c++17 -Wall -Wextra visitor.cpp -o visitor_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

class Visitor;

class Node {
public:
    Node(std::string name, bool dir, int size = 0)
        : name_(std::move(name)), dir_(dir), size_(size) {}
    virtual ~Node() = default;
    virtual void accept(Visitor& v) = 0;
    const std::string& name() const { return name_; }
    int size() const { return size_; }
    bool isDir() const { return dir_; }
private:
    std::string name_;
    bool dir_;
    int size_;
};

class File final : public Node {
public:
    File(std::string n, int s) : Node(std::move(n), false, s) {}
    void accept(Visitor& v) override;
};

class Dir final : public Node {
public:
    Dir(std::string n) : Node(std::move(n), true) {}
    void add(std::unique_ptr<Node> k) { kids_.push_back(std::move(k)); }
    const std::vector<std::unique_ptr<Node>>& kids() const { return kids_; }
    void accept(Visitor& v) override;
private:
    std::vector<std::unique_ptr<Node>> kids_;
};

class Visitor {
public:
    virtual ~Visitor() = default;
    virtual void visitFile(const File& f) = 0;
    virtual void visitDir(const Dir& d) = 0;
};

class Counter final : public Visitor {
public:
    void visitFile(const File& f) override {
        ++files_; total_ += f.size();
        std::printf("  文件 %s (%d 字节)\n", f.name().c_str(), f.size());
    }
    void visitDir(const Dir& d) override {
        std::printf("  进入目录 %s\n", d.name().c_str());
    }
    int files() const { return files_; }
    int total() const { return total_; }
private:
    int files_ = 0;
    int total_ = 0;
};

void File::accept(Visitor& v) { v.visitFile(*this); }
void Dir::accept(Visitor& v) { v.visitDir(*this); }

int main()
{
    auto a = std::make_unique<File>("a.c", 120);
    auto b = std::make_unique<File>("b.c", 80);
    auto src = std::make_unique<Dir>("src");
    src->add(std::move(a));
    src->add(std::move(b));

    Counter c;
    src->kids()[0]->accept(c);
    src->kids()[1]->accept(c);
    src->accept(c);

    std::printf("统计：%d 个文件，%d 字节\n", c.files(), c.total());
    std::puts("节点只负责 accept，统计逻辑在 visitor 里");
    return 0;
}
