// 外观 · 家庭影院一键开机
// g++ -std=c++17 -Wall -Wextra facade.cpp -o facade_cpp
#include <cstdio>

class HomeTheater {
public:
    void watchMovie() {
        std::puts("watchMovie():");
        std::puts("  灯光调到 20%");
        std::puts("  投影仪开机");
        std::puts("  功放开机，切到 HDMI 1");
        std::puts("  幕布放下");
        std::puts("  可以开始播放");
        started_ = true;
    }
    void endMovie() {
        std::puts("endMovie():");
        std::puts("  关投影、关功放、灯光回升、幕布收起");
        started_ = false;
    }
private:
    bool started_ = false;
};

int main()
{
    HomeTheater t;
    t.watchMovie();
    t.endMovie();
    std::puts("上层只调了两个方法，没有碰任何子系统");
    return 0;
}
