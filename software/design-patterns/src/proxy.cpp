// 代理 · 图片懒加载
// g++ -std=c++17 -Wall -Wextra proxy.cpp -o proxy_cpp
#include <cstdio>
#include <string>

class Image {
public:
    virtual ~Image() = default;
    virtual const std::string& name() const { return name_; }
    virtual int pixels() {
        if (!loaded_) {
            loaded_ = true;
            std::printf("  真正读取磁盘：%s\n", name_.c_str());
        }
        return 1920 * 1080;
    }
protected:
    explicit Image(std::string name) : name_(std::move(name)) {}
    std::string name_;
    bool loaded_ = false;
};

class RealImage final : public Image {
public:
    explicit RealImage(std::string name) : Image(std::move(name)) {}
};

class ImageProxy {
public:
    explicit ImageProxy(std::string name) : real_(std::move(name)) {}
    int pixels() {
        std::printf("proxy_get(%s)：", real_.name().c_str());
        if (hasCache_) { std::puts("命中缓存，不碰磁盘"); return cached_; }
        std::puts("未命中，转给真实对象");
        cached_ = real_.pixels();
        hasCache_ = true;
        return cached_;
    }
private:
    RealImage real_;
    int cached_ = 0;
    bool hasCache_ = false;
};

int main()
{
    ImageProxy p("photo.jpg");
    p.pixels(); p.pixels(); p.pixels();
    std::puts("三次读取，只加载了一次");
    return 0;
}