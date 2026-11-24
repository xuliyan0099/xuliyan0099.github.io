// 享元 · 森林共享树型
// g++ -std=c++17 -Wall -Wextra flyweight.cpp -o flyweight_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

struct TreeType {
    std::string name;
    int leafColor;
};

class TreeFactory {
public:
    const TreeType& get(const std::string& name, int color) {
        auto it = pool_.find(name);
        if (it == pool_.end())
            it = pool_.emplace(name, TreeType{name, color}).first;
        return it->second;
    }
private:
    std::unordered_map<std::string, TreeType> pool_;
};

struct Tree {
    const TreeType* type;
    int x, y;
};

int main()
{
    TreeFactory factory;
    std::vector<Tree> forest;
    forest.reserve(1000);
    for (int i = 0; i < 1000; i++) {
        const auto& type = i % 2 ? factory.get("松树", 0x1B5E20)
                                 : factory.get("橡树", 0x2E7D32);
        forest.push_back(Tree{&type, i * 3, i * 5});
    }

    std::printf("1000 棵树，共享 2 份树型描述\n");
    std::printf("%s x=%d y=%d color=0x%06X\n",
                forest[0].type->name.c_str(), forest[0].x, forest[0].y, forest[0].type->leafColor);
    std::printf("%s x=%d y=%d color=0x%06X\n",
                forest[999].type->name.c_str(), forest[999].x, forest[999].y, forest[999].type->leafColor);
    std::puts("每棵树只多存 2 个坐标，不复制颜色和名字");
    return 0;
}
