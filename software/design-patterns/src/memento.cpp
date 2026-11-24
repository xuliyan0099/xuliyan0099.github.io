// 备忘录 · C++：Memento 只暴露给 Originator，外部拿不到内部字段
// 编译：g++ -std=c++17 -Wall -Wextra memento.cpp -o memento_cpp
#include <cstdio>

struct Calib { int gain; int offset; int mode; };

class Memento {
public:
    explicit Memento(const Calib &c) : c_(c) {}
private:
    friend class Ecu;
    Calib c_;
};

class Ecu {
public:
    void set(int g, int o, int m) { c_ = Calib{g, o, m}; }
    Memento save() const { return Memento(c_); }
    void restore(const Memento &m) { c_ = m.c_; }
    void dump(const char *tag) const
    {
        std::printf("%-9s gain=%d offset=%d mode=%d\n", tag, c_.gain, c_.offset, c_.mode);
    }
private:
    Calib c_{};
};

int main()
{
    Ecu ecu;
    ecu.set(12, 0, 1);
    ecu.dump("before");
    Memento m = ecu.save();

    ecu.set(30, -8, 3);
    ecu.dump("tuned");

    ecu.restore(m);
    ecu.dump("restored");
    std::printf("快照是值拷贝：之后改 ecu 不会污染 memento\n");
    return 0;
}
