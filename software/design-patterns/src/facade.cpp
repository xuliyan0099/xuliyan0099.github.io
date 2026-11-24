// 外观 · C++：Facade 持子系统，start() 负责顺序与回滚
// 编译：g++ -std=c++17 -Wall -Wextra facade.cpp -o facade_cpp
#include <cstdio>
#include <string>

class Ignition {
public:
    bool on() { std::printf("[IGN ] relay -> ON\n"); return true; }
    void off() { std::printf("[IGN ] relay -> OFF\n"); }
};
class FuelPump {
public:
    bool on() { std::printf("[PUMP] pressure 3.0 bar\n"); return true; }
    void off() { std::printf("[PUMP] stop\n"); }
};
class Ecu {
public:
    bool handshake() { std::printf("[ECU ] seed/key ok\n"); return true; }
};

class VehicleFacade {
public:
    explicit VehicleFacade(std::string vin) : vin_(std::move(vin)) {}
    int start()
    {
        std::printf("start %s\n", vin_.c_str());
        if (!ign_.on()) return -1;
        if (!pump_.on()) { ign_.off(); return -2; }
        if (!ecu_.handshake()) { pump_.off(); return -3; }
        std::printf("[READY] engine can crank\n");
        return 0;
    }
private:
    std::string vin_;
    Ignition ign_;
    FuelPump pump_;
    Ecu ecu_;
};

int main()
{
    VehicleFacade car("VIN-0001");
    std::printf("vehicle_start -> %d\n", car.start());
    std::printf("调用方只依赖一个入口，子系统仍可单独测试\n");
    return 0;
}
