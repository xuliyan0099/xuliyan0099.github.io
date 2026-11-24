// 建造者 · C++：链式调用，build() 只交付一次
// 编译：g++ -std=c++17 -Wall -Wextra builder.cpp -o builder_cpp
#include <cstdio>
#include <array>

struct Frame {
    unsigned id = 0;
    int dlc = 0;
    std::array<unsigned char, 8> data{};
    unsigned crc = 0;
};

class Builder {
public:
    Builder &start() { f_ = Frame{}; return *this; }
    Builder &id(unsigned v) { f_.id = v; return *this; }
    Builder &data(const unsigned char *d, int n)
    {
        if (n > 8) n = 8;
        f_.dlc = n;
        for (int i = 0; i < n; i++) f_.data[static_cast<size_t>(i)] = d[i];
        return *this;
    }
    Builder &crc()
    {
        unsigned sum = f_.id;
        for (int i = 0; i < f_.dlc; i++) sum += f_.data[static_cast<size_t>(i)];
        f_.crc = sum & 0xFFu;
        return *this;
    }
    Frame build() const { return f_; }
private:
    Frame f_;
};

static void dump(const Frame &f)
{
    std::printf("id=0x%X dlc=%d data=[", f.id, f.dlc);
    for (int i = 0; i < f.dlc; i++) std::printf("%s%02X", i ? " " : "", f.data[static_cast<size_t>(i)]);
    std::printf("] crc=0x%02X\n", f.crc);
}

int main()
{
    unsigned char payload[8] = { 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80 };
    Builder b;
    Frame f1 = b.start().id(0x18FF50E5u).data(payload, 3).crc().build();
    std::printf("frame1 ");
    dump(f1);

    Frame f2 = b.start().id(0x7DFu).data(payload, 8).crc().build();
    std::printf("frame2 ");
    dump(f2);
    std::printf("两次建造独立：frame1 dlc=%d, frame2 dlc=%d\n", f1.dlc, f2.dlc);
    return 0;
}
