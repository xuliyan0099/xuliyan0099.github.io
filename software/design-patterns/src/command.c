/* 命令模式 · C 实现：诊断参数写入队列 + 撤销
 * 编译：gcc -std=c11 -Wall -Wextra command.c -o command
 */
#include <stdio.h>

typedef struct { int gain; int mode; } device_t;

typedef struct cmd cmd_t;
typedef struct {
    void (*exec)(cmd_t *self);
    void (*undo)(cmd_t *self);
} cmd_ops_t;

struct cmd { const cmd_ops_t *ops; };      /* 命令的「类型 + 状态」都在这里 */

/* 具体命令 1：设置增益。exec 时自己记住旧值，undo 才能还原 */
typedef struct {
    cmd_t     base;      /* 必须放第一位：才能把 cmd_t* 安全还原成 set_gain_t* */
    device_t *dev;
    int       value;
    int       old;
} set_gain_t;

static void gain_exec(cmd_t *self)
{
    set_gain_t *c = (set_gain_t *)self;
    c->old = c->dev->gain;
    c->dev->gain = c->value;
    printf("  exec  SetGain(%d)，旧值 %d\n", c->value, c->old);
}

static void gain_undo(cmd_t *self)
{
    set_gain_t *c = (set_gain_t *)self;
    c->dev->gain = c->old;
    printf("  undo  SetGain(%d)，还原成 %d\n", c->value, c->old);
}

static const cmd_ops_t GAIN_OPS = { gain_exec, gain_undo };

/* 具体命令 2：切换模式 */
typedef struct {
    cmd_t     base;
    device_t *dev;
    int       value;
    int       old;
} set_mode_t;

static void mode_exec(cmd_t *self)
{
    set_mode_t *c = (set_mode_t *)self;
    c->old = c->dev->mode;
    c->dev->mode = c->value;
    printf("  exec  SetMode(%d)，旧值 %d\n", c->value, c->old);
}

static void mode_undo(cmd_t *self)
{
    set_mode_t *c = (set_mode_t *)self;
    c->dev->mode = c->old;
    printf("  undo  SetMode(%d)，还原成 %d\n", c->value, c->old);
}

static const cmd_ops_t MODE_OPS = { mode_exec, mode_undo };

/* 调用者：只认 cmd_t*，不知道命令具体做什么 */
typedef struct {
    cmd_t *queued[8];  int qn;
    cmd_t *history[8]; int hn;
} invoker_t;

static void invoker_post(invoker_t *iv, cmd_t *c)
{
    if (iv->qn < 8) iv->queued[iv->qn++] = c;
    printf("  post  队列长度=%d\n", iv->qn);
}

static void invoker_run(invoker_t *iv)
{
    printf("--- 执行队列 ---\n");
    for (int i = 0; i < iv->qn; i++) {
        iv->queued[i]->ops->exec(iv->queued[i]);
        iv->history[iv->hn++] = iv->queued[i];
    }
    iv->qn = 0;
}

static void invoker_undo_last(invoker_t *iv)
{
    if (iv->hn == 0) { printf("  没有可撤销的命令\n"); return; }
    cmd_t *c = iv->history[--iv->hn];
    c->ops->undo(c);
}

int main(void)
{
    device_t dev = { 0, 0 };
    set_gain_t c1 = { { &GAIN_OPS }, &dev, 12, 0 };
    set_gain_t c2 = { { &GAIN_OPS }, &dev, 20, 0 };
    set_mode_t c3 = { { &MODE_OPS }, &dev, 2, 0 };
    invoker_t iv = { .qn = 0, .hn = 0 };

    printf("初始 gain=%d mode=%d\n", dev.gain, dev.mode);
    invoker_post(&iv, (cmd_t *)&c1);
    invoker_post(&iv, (cmd_t *)&c2);
    invoker_post(&iv, (cmd_t *)&c3);
    invoker_run(&iv);
    printf("执行后 gain=%d mode=%d\n", dev.gain, dev.mode);

    printf("--- 撤销两次 ---\n");
    invoker_undo_last(&iv);
    invoker_undo_last(&iv);
    printf("撤销后 gain=%d mode=%d\n", dev.gain, dev.mode);
    printf("历史剩余=%d\n", iv.hn);
    return 0;
}
