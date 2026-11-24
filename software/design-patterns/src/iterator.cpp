// 迭代器 · 遍历数组集合
// g++ -std=c++17 -Wall -Wextra iterator.cpp -o iterator_cpp
#include <cstdio>
#include <vector>

class Range {
public:
    explicit Range(std::vector<int> v) : v_(std::move(v)) {}

    class Iter {
    public:
        explicit Iter(const int* p) : p_(p) {}
        bool operator!=(const Iter& o) const { return p_ != o.p_; }
        void operator++() { ++p_; }
        int operator*() const { return *p_; }
    private:
        const int* p_;
    };

    Iter begin() const { return Iter(v_.data()); }
    Iter end() const { return Iter(v_.data() + v_.size()); }

private:
    std::vector<int> v_;
};

int main()
{
    Range r({ 10, 20, 30, 40, 50 });
    int sum = 0;
    for (int x : r) {
        std::printf("  取到 %d\n", x);
        sum += x;
    }
    std::printf("总和 = %d\n", sum);
    std::puts("range-for 背后就是 begin/end 迭代器");
    return 0;
}
