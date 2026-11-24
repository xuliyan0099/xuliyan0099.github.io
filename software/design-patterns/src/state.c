/* 状态模式 · C 实现：ECU 电源/运行状态机，转移写成表
 * 编译：gcc -std=c11 -Wall -Wextra state.c -o state
 * 5 个状态 × 6 个事件 = 30 个格子，非法格子统一返回 -1。
 */
#include <stdio.h>

enum { ST_OFF, ST_ACC, ST_ON, ST_RUN, ST_FAULT, ST_N };
enum { EV_ACC, EV_ON, EV_CRANK, EV_OFF, EV_OVER, EV_CLEAR, EV_N };

static const char *const ST_NAME[] = { "OFF", "ACC", "ON", "RUN", "FAULT" };
static const char *const EV_NAME[] = { "ACC", "ON", "CRANK", "OFF", "OVERTEMP", "CLEAR" };

/* 行 = 当前状态，列 = 事件；-1 表示该状态下这个事件非法 */
static const int TRANS[ST_N][EV_N] = {
    /* OFF   */ { ST_ACC, -1,     -1,      -1,     -1,       -1     },
    /* ACC   */ { -1,     ST_ON,  -1,      ST_OFF, ST_FAULT, -1     },
    /* ON    */ { ST_ACC, -1,     ST_RUN,  ST_OFF, ST_FAULT, -1     },
    /* RUN   */ { -1,     -1,     -1,      ST_OFF, ST_FAULT, -1     },
    /* FAULT */ { -1,     -1,     -1,      ST_OFF, -1,       ST_OFF }
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
    static const int seq[] = { EV_ACC, EV_ON, EV_CRANK, EV_OVER, EV_CRANK, EV_CLEAR, EV_CRANK };
    static const char *const why[] = {
        "钥匙拧到 ACC", "再拧到 ON（点火档）", "起动机拖动，发动机运转", "冷却液超温",
        "已进故障，再打起动机", "故障清除", "已断电，再打起动机"
    };

    for (unsigned i = 0; i < sizeof seq / sizeof seq[0]; i++) {
        printf("--- %s ---\n", why[i]);
        ecu_inject(&e, seq[i]);
    }
    printf("最终状态：%s\n", ST_NAME[e.state]);

    int legal = 0;
    for (int s = 0; s < ST_N; s++)
        for (int k = 0; k < EV_N; k++)
            if (TRANS[s][k] >= 0) legal++;
    printf("转移表 %d 个格子，其中合法转移 %d 个\n", ST_N * EV_N, legal);
    return 0;
}
