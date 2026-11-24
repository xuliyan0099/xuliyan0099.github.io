// 适配器模式 · C++ 实现：对象适配器（包住旧驱动）与接口统一
// 编译：g++ -std=c++17 -Wall -Wextra adapter.cpp -o adapter_cpp
#include <cstdio>

// 目标接口：新代码只依赖它
struct Reading { bool ok; float temp_c; float hum_pct; };

class ISensor {
public:
    virtual ~ISensor() = default;
    virtual Reading read() = 0;
};

// 被适配者 A：厂商库，整数 + 缩放，且要求先 init
class Sht3xDriver {
public:
    bool init() { ready_ = true; return true; }
    bool readRaw(int& t_x100, int& h_x100) {
        if (!ready_) return false;
        t_x100 = 2360;
        h_x100 = 4850;
        return true;
    }
private:
    bool ready_ = false;
};

class Sht3xAdapter final : public ISensor {
public:
    Sht3xAdapter() { drv_.init(); }
    Reading read() override {
        int t = 0, h = 0;
        if (!drv_.readRaw(t, h)) return {};
        return { true, t / 100.0f, h / 100.0f };
    }
private:
    Sht3xDriver drv_;
};

// 被适配者 B：ADC 原始计数，只能测温
class NtcAdc {
public:
    int rawCount() const { return 2100; }
};

class NtcAdapter final : public ISensor {
public:
    Reading read() override {
        float t = 25.0f + (adc_.rawCount() - 2048) * 0.05f;
        return { true, t, -1.0f };     // -1 表示湿度不可用
    }
private:
    NtcAdc adc_;
};

void report(const char* tag, ISensor& s) {
    Reading r = s.read();
    std::printf("%s: ", tag);
    if (r.ok) std::printf("temp=%.1fC ", r.temp_c);
    else      std::printf("temp=<err> ");
    if (r.ok && r.hum_pct >= 0) std::printf("hum=%.1f%%\n", r.hum_pct);
    else                        std::printf("hum=<不支持>\n");
}

int main() {
    Sht3xAdapter a;
    NtcAdapter b;
    report("SHT3x", a);
    report("NTC  ", b);
    return 0;
}
