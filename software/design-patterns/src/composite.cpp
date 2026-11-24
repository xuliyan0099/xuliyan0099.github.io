// 组合 · 文件与文件夹
// g++ -std=c++17 -Wall -Wextra composite.cpp -o composite_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

class Node {
public:
    Node(std::string name, bool dir, int size = 0)
        : name_(std::move(name)), dir_(dir), size_(size) {}
    virtual ~Node() = default;

    void add(std::unique_ptr<Node> kid) { kids_.push_back(std::move(kid)); }
    int total() const {
        if (!dir_) return size_;
        int sum = 0;
        for (const auto& k : kids_) sum += k->total();
        return sum;
    }
    void list(int depth = 0) const {
        for (int i = 0; i < depth; i++) std::printf("  ");
        std::printf("%s%s\n", dir_ ? "[D] " : "    ", name_.c_str());
        for (const auto& k : kids_) k->list(depth + 1);
    }
private:
    std::string name_;
    bool dir_;
    int size_;
    std::vector<std::unique_ptr<Node>> kids_;
};

int main()
{
    auto root = std::make_unique<Node>("root", true);
    auto src = std::make_unique<Node>("src", true);
    src->add(std::make_unique<Node>("a.c", false, 120));
    src->add(std::make_unique<Node>("b.c", false, 80));
    root->add(std::move(src));
    root->add(std::make_unique<Node>("README", false, 10));

    root->list();
    std::printf("总大小 = %d 字节\n", root->total());
    return 0;
}
