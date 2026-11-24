// 迭代器 · C++：自定义 begin/end，range-for 直接遍历有效故障
// 编译：g++ -std=c++17 -Wall -Wextra iterator.cpp -o iterator_cpp
#include <cstdio>
#include <vector>

struct Fault {
    int code;
    const char *name;
};

class FaultList {
public:
    void add(int code, const char *name) { items_.push_back(Fault{code, name}); }

    class Iter {
    public:
        Iter(const FaultList *list, std::size_t pos) : list_(list), pos_(pos) { skip(); }
        const Fault &operator*() const { return list_->items_[pos_]; }
        Iter &operator++() { ++pos_; skip(); return *this; }
        bool operator!=(const Iter &o) const { return pos_ != o.pos_; }
    private:
        void skip() { while (pos_ < list_->items_.size() && list_->items_[pos_].code == 0) ++pos_; }
        const FaultList *list_;
        std::size_t pos_;
    };

    Iter begin() const { return Iter(this, 0); }
    Iter end() const { return Iter(this, items_.size()); }
private:
    std::vector<Fault> items_;
};

int main()
{
    FaultList list;
    list.add(0, "none");
    list.add(17, "O2 heater");
    list.add(0, "none");
    list.add(42, "misfire");
    list.add(91, "CAN bus off");

    int count = 0;
    for (const Fault &f : list)
        std::printf("fault #%d code=%d %s\n", ++count, f.code, f.name);
    std::printf("有效故障 %d 条，全部遍历完\n", count);
    return 0;
}
