// 适配器 · 方钉插圆孔
// g++ -std=c++17 -Wall -Wextra adapter.cpp -o adapter_cpp
#include <cstdio>

class RoundHole {
public:
    explicit RoundHole(int r) : r_(r) {}
    int radius() const { return r_; }
    bool fits(int pegRadius) const { return pegRadius <= r_; }
private:
    int r_;
};

class SquarePeg {
public:
    explicit SquarePeg(int w) : w_(w) {}
    int width() const { return w_; }
private:
    int w_;
};

class SquarePegAdapter {
public:
    explicit SquarePegAdapter(const SquarePeg& p) : peg_(p) {}
    int radius() const { return (peg_.width() * 2) / 3; }
private:
    SquarePeg peg_;
};

int main()
{
    RoundHole hole(5);
    SquarePeg small(6), big(10);
    SquarePegAdapter a1(small), a2(big);

    std::printf("圆孔半径 %d\n", hole.radius());
    std::printf("方钉 6  -> 适配半径 %d -> %s\n", a1.radius(),
                hole.fits(a1.radius()) ? "塞得进" : "塞不进");
    std::printf("方钉 10 -> 适配半径 %d -> %s\n", a2.radius(),
                hole.fits(a2.radius()) ? "塞得进" : "塞不进");
    return 0;
}
