// 桥接 · C++：Link 与 Protocol 各自抽象，组合时只传引用
// 编译：g++ -std=c++17 -Wall -Wextra bridge.cpp -o bridge_cpp
#include <cstdio>
#include <memory>
#include <string>

class Link {
public:
    virtual ~Link() = default;
    virtual const char *name() const = 0;
    virtual void send(const std::string &frame) const = 0;
};
class CanLink : public Link {
public:
    const char *name() const override { return "CAN"; }
    void send(const std::string &f) const override { std::printf("[CAN ] %s\n", f.c_str()); }
};
class LinLink : public Link {
public:
    const char *name() const override { return "LIN"; }
    void send(const std::string &f) const override { std::printf("[LIN ] %s\n", f.c_str()); }
};

class Protocol {
public:
    explicit Protocol(const Link &l) : link_(l) {}
    virtual ~Protocol() = default;
    virtual const char *name() const = 0;
    virtual void request(const std::string &svc) const = 0;
    const char *linkName() const { return link_.name(); }
protected:
    const Link &link_;
};
class Uds : public Protocol {
public:
    using Protocol::Protocol;
    const char *name() const override { return "UDS"; }
    void request(const std::string &svc) const override
    {
        link_.send("UDS " + svc + " -> " + link_.name());
    }
};
class Obd : public Protocol {
public:
    using Protocol::Protocol;
    const char *name() const override { return "OBD"; }
    void request(const std::string &svc) const override
    {
        link_.send("OBD " + svc + " -> " + link_.name());
    }
};

int main()
{
    CanLink can;
    LinLink lin;
    Uds udsCan(can), udsLin(lin);
    Obd obdCan(can), obdLin(lin);

    const Protocol *protos[] = { &udsCan, &udsLin, &obdCan, &obdLin };
    for (const Protocol *p : protos) {
        std::printf("-- %s over %s --\n", p->name(), p->linkName());
        p->request("0x22F190");
    }
    std::printf("协议 2 × 物理层 2 = 4 种组合，新增一种只改一侧\n");
    return 0;
}
