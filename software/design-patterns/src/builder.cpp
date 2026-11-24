// 建造者 · 一步步盖房子
// g++ -std=c++17 -Wall -Wextra builder.cpp -o builder_cpp
#include <cstdio>
#include <string>

class House {
public:
    std::string walls, doors, windows;
    bool roof = false;
};

class HouseBuilder {
public:
    HouseBuilder& addWalls(int n)   { h_.walls   = std::to_string(n) + " 面墙"; std::printf("  砌 %d 面墙\n", n); return *this; }
    HouseBuilder& addDoors(int n)   { h_.doors   = std::to_string(n) + " 扇门"; std::printf("  装 %d 扇门\n", n); return *this; }
    HouseBuilder& addWindows(int n) { h_.windows = std::to_string(n) + " 扇窗"; std::printf("  装 %d 扇窗\n", n); return *this; }
    HouseBuilder& addRoof()         { h_.roof = true; std::puts("  封顶"); return *this; }

    bool build() const {
        if (h_.walls.empty() || h_.doors.empty() || h_.windows.empty() || !h_.roof) {
            std::puts("  校验失败：房子还不完整");
            return false;
        }
        std::printf("  交付：%s / %s / %s / 有屋顶\n",
                    h_.walls.c_str(), h_.doors.c_str(), h_.windows.c_str());
        return true;
    }

private:
    House h_;
};

int main()
{
    std::puts("普通小屋：");
    HouseBuilder{}.addWalls(4).addDoors(1).addWindows(2).addRoof().build();

    std::puts("缺步骤的房子：");
    HouseBuilder{}.addWalls(4).addDoors(1).build();
    return 0;
}
