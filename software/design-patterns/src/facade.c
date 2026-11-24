/* 外观：上电这一套动作收进一个函数，调用方不再关心顺序 */
#include <stdio.h>

static int ignition_on(void)  { printf("[IGN ] relay -> ON\n"); return 1; }
static int fuel_pump_on(void) { printf("[PUMP] pressure 3.0 bar\n"); return 1; }
static int ecu_handshake(void){ printf("[ECU ] seed/key ok\n"); return 1; }

/* 外观：固定顺序、失败即回滚，调用方只看到 0/负值 */
int vehicle_start(const char *vin)
{
    printf("start %s\n", vin);
    if (!ignition_on()) return -1;
    if (!fuel_pump_on()) { printf("[ROLL] ignition off\n"); return -2; }
    if (!ecu_handshake()) { printf("[ROLL] pump off\n"); return -3; }
    printf("[READY] engine can crank\n");
    return 0;
}

int main(void)
{
    int rc = vehicle_start("VIN-0001");
    printf("vehicle_start -> %d\n", rc);
    printf("调用方只依赖一个入口，子系统仍可单独测试\n");
    return 0;
}
