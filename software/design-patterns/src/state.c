/* 状态模式 · C 实现：ECU 电源状态机，转移写成表
 * 编译：gcc -std=c11 -Wall -Wextra state.c -o state
 */
#include <stdio.h>

enum { ST_OFF, ST_ACC, ST_ON, ST_RUN, ST_FAULT, ST_N };
enum { EV_IGN, EV_START, EV_STOP, EV_OVER, EV_CLEAR, EV_N };

static const char *const ST_NAME[] = { "OFF", "ACC", "ON", "RUN", "FAULT" };
static const char *const EV_NAME[] = { "IGN", "START", "STOP", "OVERTEMP", "CLEAR" };

/* 行 = 当前状态，列 = 事件；-1 表示该状态下这个事件非法 */
static const int TRANS[ST_N][EV_N] = {
    /* OFF   */ { ST_ACC, -1,     -1,     -1,      -1     },
    /* ACC   */ { ST_OFF, ST_ON,  -1,     ST_FAULT, -1    },
    /* ON    */ { ST_OFF, ST_RUN, ST_ACC, ST_FAULT, -1    },
    /* RUN   */ { ST_OFF, -1,     ST_ON,  ST_FAULT, -1    },
    /* FAULT */ { ST_OFF, -1,     -1,     -1,      ST_OFF }
};

typedef struct { int state; } ecu_t;

static int ecu_inject(ecu_t *e, int ev)
{
    int next = TRANS[e->state][ev];
    if (next < 0) {
        printf("[ECU] %-5s + %-8s -> 拒绝（该状态下事件非法）\n",
               ST_NAME[e->state], EV_NAME[ev]);
        return -1;
    }
    printf("[ECU] %-5s + %-8s -> %s\n", ST_NAME[e->state], EV_NAME[ev], ST_NAME[next]);
    e->state = next;
    return 0;
}

int main(void)
{
    ecu_t e = { ST_OFF };
    static const int seq[] = { EV_IGN, EV_START, EV_START, EV_OVER, EV_START, EV_CLEAR, EV_STOP };
    static const char *const why[] = {
        "上电钥匙拧到 ACC", "发动机点火", "运行中再按 START", "冷却液超温",
        "故障下点火", "故障清除", "已 OFF 再按 STOP"
    };

    for (unsigned i = 0; i < sizeof seq / sizeof seq[0]; i++) {
        printf("--- %s ---\n", why[i]);
        ecu_inject(&e, seq[i]);
    }

    printf("最终状态：%s\n", ST_NAME[e.state]);
    printf("转移表 %d 个格子，其中合法转移 %d 个\n",
           ST_N * EV_N, 8);
    return 0;
}
