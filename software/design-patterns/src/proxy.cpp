// 代理 · C++：Proxy 持 RealNvram 与缓存，接口对调用方完全一致
// 编译：g++ -std=c++17 -Wall -Wextra proxy.cpp -o proxy_cpp
#include <cstdio>
#include <array>
#include <memory>

class Nvram {
public:
    virtual ~Nvram() = default;
    virtual int read(int addr) = 0;
    virtual void write(int addr, int value) = 0;
};

class RealNvram : public Nvram {
public:
    int read(int addr) override
    {
        std::printf("[NVRAM] read  [%d] = %d\n", addr, mem_[static_cast<size_t>(addr)]);
        return mem_[static_cast<size_t>(addr)];
    }
    void write(int addr, int value) override
    {
        mem_[static_cast<size_t>(addr)] = value;
        std::printf("[NVRAM] write [%d] = %d\n", addr, value);
    }
private:
    std::array<int, 16> mem_{};
};

class Proxy : public Nvram {
public:
    explicit Proxy(Nvram &real) : real_(real) {}
    int read(int addr) override
    {
        auto i = static_cast<size_t>(addr);
        if (!valid_[i]) {
            cache_[i] = real_.read(addr);
            valid_[i] = true;
            std::printf("[PROXY] cache miss [%d]\n", addr);
        } else {
            std::printf("[PROXY] cache hit  [%d] = %d\n", addr, cache_[i]);
        }
        return cache_[i];
    }
    void write(int addr, int value) override
    {
        real_.write(addr, value);
        cache_[static_cast<size_t>(addr)] = value;
        valid_[static_cast<size_t>(addr)] = true;
        std::printf("[PROXY] write-through [%d]\n", addr);
    }
private:
    Nvram &real_;
    std::array<int, 16> cache_{};
    std::array<bool, 16> valid_{};
};

int main()
{
    RealNvram real;
    Proxy proxy(real);
    real.write(3, 11);
    std::printf("read1 = %d\n", proxy.read(3));
    std::printf("read2 = %d\n", proxy.read(3));
    proxy.write(3, 25);
    std::printf("read3 = %d\n", proxy.read(3));
    std::printf("真实存储 [3] = %d\n", real.read(3));
    return 0;
}
