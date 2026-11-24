// 责任链模式 · C++ 实现：链式装配 + 每节点自己决定放行或终止
// 编译：g++ -std=c++17 -Wall -Wextra chain.cpp -o chain_cpp
#include <cstdio>
#include <string>

struct Frame { int id; int len; unsigned char crc; };

enum class Result { Pass, Stop };

class Handler {
public:
    explicit Handler(std::string name) : name_(std::move(name)) {}
    virtual ~Handler() = default;

    Handler& setNext(Handler& n) { next_ = &n; return n; }

    // 模板方法：先问自己，再决定要不要往后传
    Result run(const Frame& f) {
        Result r = check(f);
        if (r == Result::Stop) return Result::Stop;
        return next_ ? next_->run(f) : Result::Pass;
    }

protected:
    const std::string& name() const { return name_; }

private:
    virtual Result check(const Frame& f) = 0;
    std::string name_;
    Handler* next_ = nullptr;
};

class LenCheck final : public Handler {
public:
    LenCheck() : Handler("len") {}
protected:
    Result check(const Frame& f) override {
        if (f.len != 8) {
            std::printf("  [%s] 丢弃 0x%03X：长度 %d != 8\n", name().c_str(), f.id, f.len);
            return Result::Stop;
        }
        std::printf("  [%s] 通过\n", name().c_str());
        return Result::Pass;
    }
};

class CrcCheck final : public Handler {
public:
    CrcCheck() : Handler("crc") {}
protected:
    Result check(const Frame& f) override {
        unsigned char want = static_cast<unsigned char>(((f.id >> 8) & 0xFF) ^ (f.id & 0xFF) ^ f.len);
        if (f.crc != want) {
            std::printf("  [%s] 丢弃 0x%03X：crc=%02X，应为 %02X\n",
                        name().c_str(), f.id, f.crc, want);
            return Result::Stop;
        }
        std::printf("  [%s] 通过\n", name().c_str());
        return Result::Pass;
    }
};

class WhiteList final : public Handler {
public:
    WhiteList() : Handler("white") {}
protected:
    Result check(const Frame& f) override {
        if (!(f.id == 0x100 || f.id == 0x2A0)) {
            std::printf("  [%s] 丢弃 0x%03X：不在白名单\n", name().c_str(), f.id);
            return Result::Stop;
        }
        std::printf("  [%s] 通过\n", name().c_str());
        return Result::Pass;
    }
};

class AppSink final : public Handler {
public:
    AppSink() : Handler("app") {}
protected:
    Result check(const Frame& f) override {
        std::printf("  [%s] 已消费 0x%03X\n", name().c_str(), f.id);
        return Result::Stop;
    }
};

int main() {
    LenCheck len;
    CrcCheck crc;
    WhiteList white;
    AppSink app;

    len.setNext(crc).setNext(white).setNext(app);

    const Frame frames[] = {
        { 0x100, 7, 0x09 },
        { 0x100, 8, 0x00 },
        { 0x500, 8, 0x0D },
        { 0x100, 8, 0x09 }
    };
    for (const auto& f : frames) {
        std::printf("frame 0x%03X len=%d crc=%02X\n", f.id, f.len, f.crc);
        len.run(f);
    }
    return 0;
}
