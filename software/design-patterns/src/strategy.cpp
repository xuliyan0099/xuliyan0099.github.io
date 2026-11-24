// 策略 · 排序策略
// g++ -std=c++17 -Wall -Wextra strategy.cpp -o strategy_cpp
#include <cstdio>
#include <memory>
#include <vector>

class SortStrategy {
public:
    virtual ~SortStrategy() = default;
    virtual const char* name() const = 0;
    virtual void sort(std::vector<int>& v) const = 0;
};

class Bubble final : public SortStrategy {
public:
    const char* name() const override { return "冒泡"; }
    void sort(std::vector<int>& v) const override {
        for (size_t i = 0; i < v.size(); i++)
            for (size_t j = 0; j + 1 < v.size() - i; j++)
                if (v[j] > v[j + 1]) std::swap(v[j], v[j + 1]);
    }
};

class Insertion final : public SortStrategy {
public:
    const char* name() const override { return "插入"; }
    void sort(std::vector<int>& v) const override {
        for (size_t i = 1; i < v.size(); i++) {
            int key = v[i], j = static_cast<int>(i) - 1;
            while (j >= 0 && v[j] > key) { v[j + 1] = v[j]; j--; }
            v[j + 1] = key;
        }
    }
};

class Sorter {
public:
    explicit Sorter(std::unique_ptr<SortStrategy> s) : s_(std::move(s)) {}
    void run(std::vector<int> v) {
        s_->sort(v);
        std::printf("%s：", s_->name());
        for (int x : v) std::printf(" %d", x);
        std::printf("\n");
    }
private:
    std::unique_ptr<SortStrategy> s_;
};

int main()
{
    std::vector<int> src = { 5, 1, 4, 2, 3 };
    Sorter(std::make_unique<Bubble>()).run(src);
    Sorter(std::make_unique<Insertion>()).run(src);
    std::puts("排序函数是参数，换策略不改调用方");
    return 0;
}
