# -*- coding: utf-8 -*-
"""第三批经典例子源码：职责链、命令、解释器、迭代器、中介者、备忘录、观察者、状态、策略、模板方法、访问者。"""
import pathlib

SRC = pathlib.Path(__file__).resolve().parent.parent / "src"
C = {}

C["chain.c"] = r'''/* 职责链 · 客服逐级升级
 * gcc -std=c11 -Wall -Wextra chain.c -o chain
 */
#include <stdio.h>

typedef struct handler handler_t;
typedef int (*handle_fn)(int level, const char *msg);

struct handler {
    const char *name;
    int max_level;
    handle_fn fn;
    handler_t *next;
};

static int faq(int level, const char *msg) {
    if (level <= 1) { printf("  FAQ：%s\n", msg); return 1; }
    return 0;
}
static int tech(int level, const char *msg) {
    if (level <= 2) { printf("  技术支持：%s\n", msg); return 1; }
    return 0;
}
static int engineer(int level, const char *msg) {
    printf("  工程师：%s\n", msg); return 1; (void)level;
}

static void dispatch(handler_t *h, int level, const char *msg)
{
    printf("工单 L%d「%s」\n", level, msg);
    for (; h; h = h->next)
        if (h->fn(level, msg)) { printf("  -> %s 接手\n", h->name); return; }
    printf("  没人处理\n");
}

int main(void)
{
    handler_t eng  = { "工程师", 9, engineer, NULL };
    handler_t techh= { "技术支持", 2, tech, &eng };
    handler_t faqh = { "FAQ", 1, faq, &techh };

    dispatch(&faqh, 1, "怎么改密码");
    dispatch(&faqh, 2, "客户端连不上");
    dispatch(&faqh, 3, "服务器 500");
    return 0;
}
'''

C["chain.cpp"] = r'''// 职责链 · 客服逐级升级
// g++ -std=c++17 -Wall -Wextra chain.cpp -o chain_cpp
#include <cstdio>
#include <memory>
#include <string>

class Handler {
public:
    explicit Handler(std::string name, int maxLevel)
        : name_(std::move(name)), maxLevel_(maxLevel) {}
    virtual ~Handler() = default;

    Handler& setNext(std::unique_ptr<Handler> next) {
        next_ = std::move(next);
        return *next_;
    }

    void dispatch(int level, const std::string& msg) {
        std::printf("工单 L%d「%s」\n", level, msg.c_str());
        Handler* h = this;
        while (h) {
            if (h->canHandle(level, msg)) {
                std::printf("  -> %s 接手\n", h->name_.c_str());
                return;
            }
            h = h->next_.get();
        }
        std::puts("  没人处理");
    }

protected:
    virtual bool canHandle(int level, const std::string& msg) = 0;
    std::string name_;

private:
    int maxLevel_;
    std::unique_ptr<Handler> next_;
};

class Faq final : public Handler {
public:
    Faq() : Handler("FAQ", 1) {}
protected:
    bool canHandle(int level, const std::string& msg) override {
        if (level <= 1) { std::printf("  FAQ：%s\n", msg.c_str()); return true; }
        return false;
    }
};

class Tech final : public Handler {
public:
    Tech() : Handler("技术支持", 2) {}
protected:
    bool canHandle(int level, const std::string& msg) override {
        if (level <= 2) { std::printf("  技术支持：%s\n", msg.c_str()); return true; }
        return false;
    }
};

class Engineer final : public Handler {
public:
    Engineer() : Handler("工程师", 9) {}
protected:
    bool canHandle(int level, const std::string& msg) override {
        (void)level;
        std::printf("  工程师：%s\n", msg.c_str());
        return true;
    }
};

int main()
{
    auto faq = std::make_unique<Faq>();
    auto tech = std::make_unique<Tech>();
    auto eng = std::make_unique<Engineer>();
    faq->setNext(std::move(tech)).setNext(std::move(eng));

    faq->dispatch(1, "怎么改密码");
    faq->dispatch(2, "客户端连不上");
    faq->dispatch(3, "服务器 500");
    return 0;
}
'''

C["command.c"] = r'''/* 命令 · 编辑器撤销
 * gcc -std=c11 -Wall -Wextra command.c -o command
 */
#include <stdio.h>
#include <string.h>

typedef struct { char text[64]; int len; } editor_t;

typedef struct { int kind; char ch; } cmd_t;   /* 0=追加 1=删除 */

static void apply(editor_t *e, cmd_t c)
{
    if (c.kind == 0 && e->len < 63) e->text[e->len++] = c.ch, e->text[e->len] = 0;
    else if (c.kind == 1 && e->len > 0) e->text[--e->len] = 0;
}

static void undo(editor_t *e, cmd_t c)
{
    if (c.kind == 0) { if (e->len > 0) e->text[--e->len] = 0; }
    else             { if (e->len < 63) e->text[e->len++] = c.ch, e->text[e->len] = 0; }
}

int main(void)
{
    editor_t e = { "", 0 };
    cmd_t history[16];
    int n = 0;

    cmd_t a = { 0, 'H' }, b = { 0, 'i' }, c = { 0, '!' };
    apply(&e, history[n++] = a);
    apply(&e, history[n++] = b);
    apply(&e, history[n++] = c);
    printf("输入三个命令后：\"%s\"（len=%d）\n", e.text, e.len);

    for (int i = 0; i < 2; i++) {
        undo(&e, history[--n]);
        printf("撤销一步：\"%s\"\n", e.text);
    }
    return 0;
}
'''

C["command.cpp"] = r'''// 命令 · 编辑器撤销
// g++ -std=c++17 -Wall -Wextra command.cpp -o command_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

class Editor {
public:
    std::string text;
};

class Command {
public:
    virtual ~Command() = default;
    virtual void execute(Editor& e) = 0;
    virtual void undo(Editor& e) = 0;
};

class Append final : public Command {
public:
    explicit Append(char c) : c_(c) {}
    void execute(Editor& e) override { e.text.push_back(c_); }
    void undo(Editor& e) override { if (!e.text.empty()) e.text.pop_back(); }
private:
    char c_;
};

class Delete final : public Command {
public:
    void execute(Editor& e) override {
        if (!e.text.empty()) { last_ = e.text.back(); e.text.pop_back(); }
    }
    void undo(Editor& e) override { e.text.push_back(last_); }
private:
    char last_ = 0;
};

class Invoker {
public:
    void run(std::unique_ptr<Command> c, Editor& e) {
        c->execute(e);
        history_.push_back(std::move(c));
    }
    void undo(Editor& e) {
        if (history_.empty()) return;
        history_.back()->undo(e);
        history_.pop_back();
    }
private:
    std::vector<std::unique_ptr<Command>> history_;
};

int main()
{
    Editor e;
    Invoker inv;
    inv.run(std::make_unique<Append>('H'), e);
    inv.run(std::make_unique<Append>('i'), e);
    inv.run(std::make_unique<Append>('!'), e);
    std::printf("输入三个命令后：\"%s\"\n", e.text.c_str());

    inv.undo(e);
    std::printf("撤销一步：\"%s\"\n", e.text.c_str());
    inv.undo(e);
    std::printf("撤销两步：\"%s\"\n", e.text.c_str());
    return 0;
}
'''

C["interpreter.c"] = r'''/* 解释器 · 算术表达式 (2 + 3) * 4
 * gcc -std=c11 -Wall -Wextra interpreter.c -o interpreter
 */
#include <stdio.h>

typedef struct expr expr_t;
struct expr {
    int kind;          /* 0=数字 1=加法 2=乘法 */
    int value;
    expr_t *l, *r;
};

static int eval(const expr_t *e)
{
    switch (e->kind) {
    case 0: return e->value;
    case 1: return eval(e->l) + eval(e->r);
    case 2: return eval(e->l) * eval(e->r);
    }
    return 0;
}

int main(void)
{
    expr_t n2 = { 0, 2, NULL, NULL };
    expr_t n3 = { 0, 3, NULL, NULL };
    expr_t n4 = { 0, 4, NULL, NULL };
    expr_t add = { 1, 0, &n2, &n3 };
    expr_t mul = { 2, 0, &add, &n4 };

    printf("表达式： (2 + 3) * 4\n");
    printf("求值 = %d\n", eval(&mul));
    printf("换成 (2 + 3) * 5 只需换一个叶子，树结构不变\n");
    return 0;
}
'''

C["interpreter.cpp"] = r'''// 解释器 · 算术表达式 (2 + 3) * 4
// g++ -std=c++17 -Wall -Wextra interpreter.cpp -o interpreter_cpp
#include <cstdio>
#include <memory>

class Expr {
public:
    virtual ~Expr() = default;
    virtual int eval() const = 0;
};

class Number final : public Expr {
public:
    explicit Number(int v) : v_(v) {}
    int eval() const override { return v_; }
private:
    int v_;
};

class Add final : public Expr {
public:
    Add(std::unique_ptr<Expr> l, std::unique_ptr<Expr> r)
        : l_(std::move(l)), r_(std::move(r)) {}
    int eval() const override { return l_->eval() + r_->eval(); }
private:
    std::unique_ptr<Expr> l_, r_;
};

class Mul final : public Expr {
public:
    Mul(std::unique_ptr<Expr> l, std::unique_ptr<Expr> r)
        : l_(std::move(l)), r_(std::move(r)) {}
    int eval() const override { return l_->eval() * r_->eval(); }
private:
    std::unique_ptr<Expr> l_, r_;
};

int main()
{
    auto tree = std::make_unique<Mul>(
        std::make_unique<Add>(std::make_unique<Number>(2), std::make_unique<Number>(3)),
        std::make_unique<Number>(4));
    std::puts("表达式： (2 + 3) * 4");
    std::printf("求值 = %d\n", tree->eval());
    std::puts("换成 (2 + 3) * 5 只需换一个叶子，树结构不变");
    return 0;
}
'''

C["iterator.c"] = r'''/* 迭代器 · 遍历数组集合
 * gcc -std=c11 -Wall -Wextra iterator.c -o iterator
 */
#include <stdio.h>

typedef struct {
    const int *data;
    int n;
    int i;
} iter_t;

static void iter_init(iter_t *it, const int *data, int n)
{
    it->data = data; it->n = n; it->i = 0;
}

static const int *iter_next(iter_t *it)
{
    if (it->i >= it->n) return NULL;
    return &it->data[it->i++];
}

int main(void)
{
    int nums[] = { 10, 20, 30, 40, 50 };
    iter_t it;
    iter_init(&it, nums, 5);

    const int *p;
    int sum = 0;
    while ((p = iter_next(&it)) != NULL) {
        printf("  取到 %d\n", *p);
        sum += *p;
    }
    printf("总和 = %d\n", sum);
    printf("调用方没有用到下标，换链表也不用改这里\n");
    return 0;
}
'''

C["iterator.cpp"] = r'''// 迭代器 · 遍历数组集合
// g++ -std=c++17 -Wall -Wextra iterator.cpp -o iterator_cpp
#include <cstdio>
#include <vector>

class Range {
public:
    explicit Range(std::vector<int> v) : v_(std::move(v)) {}

    class Iter {
    public:
        explicit Iter(const int* p) : p_(p) {}
        bool operator!=(const Iter& o) const { return p_ != o.p_; }
        void operator++() { ++p_; }
        int operator*() const { return *p_; }
    private:
        const int* p_;
    };

    Iter begin() const { return Iter(v_.data()); }
    Iter end() const { return Iter(v_.data() + v_.size()); }

private:
    std::vector<int> v_;
};

int main()
{
    Range r({ 10, 20, 30, 40, 50 });
    int sum = 0;
    for (int x : r) {
        std::printf("  取到 %d\n", x);
        sum += x;
    }
    std::printf("总和 = %d\n", sum);
    std::puts("range-for 背后就是 begin/end 迭代器");
    return 0;
}
'''

C["mediator.c"] = r'''/* 中介者 · 聊天室转发
 * gcc -std=c11 -Wall -Wextra mediator.c -o mediator
 */
#include <stdio.h>
#include <string.h>

typedef struct chat chat_t;
typedef struct { const char *name; chat_t *room; } user_t;

struct chat { user_t *users[4]; int n; };

static void join(chat_t *c, user_t *u) { u->room = c; c->users[c->n++] = u; }

static void send(user_t *from, const char *msg)
{
    printf("%s: %s\n", from->name, msg);
    for (int i = 0; i < from->room->n; i++) {
        user_t *u = from->room->users[i];
        if (u != from) printf("  -> %s 收到\n", u->name);
    }
}

int main(void)
{
    chat_t room = { { 0 }, 0 };
    user_t alice = { "Alice", NULL };
    user_t bob   = { "Bob", NULL };
    user_t carol = { "Carol", NULL };
    join(&room, &alice); join(&room, &bob); join(&room, &carol);

    send(&alice, "晚上好");
    send(&bob, "在的");
    printf("三个用户互不知道对方地址，只认识 room\n");
    return 0;
}
'''

C["mediator.cpp"] = r'''// 中介者 · 聊天室转发
// g++ -std=c++17 -Wall -Wextra mediator.cpp -o mediator_cpp
#include <cstdio>
#include <string>
#include <vector>

class ChatRoom;

class User {
public:
    User(std::string name) : name_(std::move(name)) {}
    void join(ChatRoom* room);
    void send(const std::string& msg);
    const std::string& name() const { return name_; }
private:
    std::string name_;
    ChatRoom* room_ = nullptr;
};

class ChatRoom {
public:
    void add(User* u) { users_.push_back(u); }
    void broadcast(User* from, const std::string& msg) {
        std::printf("%s: %s\n", from->name().c_str(), msg.c_str());
        for (auto u : users_)
            if (u != from) std::printf("  -> %s 收到\n", u->name().c_str());
    }
private:
    std::vector<User*> users_;
};

void User::join(ChatRoom* room) { room_ = room; room->add(this); }

void User::send(const std::string& msg) {
    if (room_) room_->broadcast(this, msg);
}

int main()
{
    ChatRoom room;
    User alice("Alice"), bob("Bob"), carol("Carol");
    alice.join(&room); bob.join(&room); carol.join(&room);

    alice.send("晚上好");
    bob.send("在的");
    std::puts("三个用户互不知道对方地址，只认识 room");
    return 0;
}
'''

C["memento.c"] = r'''/* 备忘录 · 撤销快照
 * gcc -std=c11 -Wall -Wextra memento.c -o memento
 */
#include <stdio.h>
#include <string.h>

typedef struct { char text[64]; int cursor; } editor_t;
typedef struct { char text[64]; int cursor; } memento_t;

static memento_t save(const editor_t *e)
{
    memento_t m;
    strcpy(m.text, e->text);
    m.cursor = e->cursor;
    return m;
}

static void restore(editor_t *e, const memento_t *m)
{
    strcpy(e->text, m->text);
    e->cursor = m->cursor;
}

int main(void)
{
    editor_t e = { "hello", 5 };
    printf("初始：\"%s\" cursor=%d\n", e.text, e.cursor);

    memento_t snap = save(&e);

    strcpy(e.text, "hello world");
    e.cursor = 11;
    printf("编辑后：\"%s\" cursor=%d\n", e.text, e.cursor);

    restore(&e, &snap);
    printf("恢复后：\"%s\" cursor=%d\n", e.text, e.cursor);
    printf("快照是值拷贝，编辑过程不会污染它\n");
    return 0;
}
'''

C["memento.cpp"] = r'''// 备忘录 · 撤销快照
// g++ -std=c++17 -Wall -Wextra memento.cpp -o memento_cpp
#include <cstdio>
#include <string>

class Memento {
public:
    Memento(std::string text, int cursor) : text_(std::move(text)), cursor_(cursor) {}
private:
    friend class Editor;
    std::string text_;
    int cursor_;
};

class Editor {
public:
    void setText(std::string t, int cursor) { text_ = std::move(t); cursor_ = cursor; }
    const std::string& text() const { return text_; }
    int cursor() const { return cursor_; }

    Memento save() const { return Memento(text_, cursor_); }
    void restore(const Memento& m) { text_ = m.text_; cursor_ = m.cursor_; }

private:
    std::string text_;
    int cursor_ = 0;
};

int main()
{
    Editor e;
    e.setText("hello", 5);
    std::printf("初始：\"%s\" cursor=%d\n", e.text().c_str(), e.cursor());

    auto snap = e.save();

    e.setText("hello world", 11);
    std::printf("编辑后：\"%s\" cursor=%d\n", e.text().c_str(), e.cursor());

    e.restore(snap);
    std::printf("恢复后：\"%s\" cursor=%d\n", e.text().c_str(), e.cursor());
    std::puts("快照是值拷贝，编辑过程不会污染它");
    return 0;
}
'''

C["observer.c"] = r'''/* 观察者 · 天气站订阅
 * gcc -std=c11 -Wall -Wextra observer.c -o observer
 */
#include <stdio.h>

typedef struct { const char *name; void (*update)(const char *, int); } observer_t;

typedef struct {
    observer_t *subs[4];
    int n;
} station_t;

static void subscribe(station_t *s, observer_t *o) { s->subs[s->n++] = o; }

static void set_temp(station_t *s, int t)
{
    printf("气温 -> %d℃\n", t);
    for (int i = 0; i < s->n; i++)
        s->subs[i]->update(s->subs[i]->name, t);
}

static void phone(const char *name, int t)   { printf("  %s：显示 %d℃\n", name, t); }
static void display(const char *name, int t) { printf("  %s：大屏刷新 %d℃\n", name, t); }

int main(void)
{
    station_t s = { { 0 }, 0 };
    observer_t a = { "手机 App", phone };
    observer_t b = { "客厅大屏", display };
    subscribe(&s, &a); subscribe(&s, &b);

    set_temp(&s, 21);
    set_temp(&s, 24);
    printf("发布者不认识订阅者，只遍历名单\n");
    return 0;
}
'''

C["observer.cpp"] = r'''// 观察者 · 天气站订阅
// g++ -std=c++17 -Wall -Wextra observer.cpp -o observer_cpp
#include <cstdio>
#include <string>
#include <vector>

class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(int temp) = 0;
};

class WeatherStation {
public:
    void subscribe(Observer* o) { subs_.push_back(o); }
    void setTemp(int t) {
        std::printf("气温 -> %d℃\n", t);
        for (auto o : subs_) o->update(t);
    }
private:
    std::vector<Observer*> subs_;
};

class PhoneApp final : public Observer {
public:
    void update(int t) override { std::printf("  手机 App：显示 %d℃\n", t); }
};

class BigScreen final : public Observer {
public:
    void update(int t) override { std::printf("  客厅大屏：大屏刷新 %d℃\n", t); }
};

int main()
{
    WeatherStation s;
    PhoneApp a;
    BigScreen b;
    s.subscribe(&a);
    s.subscribe(&b);

    s.setTemp(21);
    s.setTemp(24);
    std::puts("发布者不认识订阅者，只遍历名单");
    return 0;
}
'''

C["state.c"] = r'''/* 状态 · 订单状态流转
 * gcc -std=c11 -Wall -Wextra state.c -o state
 */
#include <stdio.h>

typedef enum { NEW, PAID, SHIPPED, DONE } state_t;

static const char *name(state_t s)
{
    static const char *N[] = { "新建", "已支付", "已发货", "已完成" };
    return N[s];
}

static state_t next(state_t s, const char *event, int *ok)
{
    *ok = 1;
    if (s == NEW     && event[0] == 'p') return PAID;
    if (s == PAID    && event[0] == 's') return SHIPPED;
    if (s == SHIPPED && event[0] == 'd') return DONE;
    *ok = 0;
    return s;
}

int main(void)
{
    state_t s = NEW;
    const char *events[] = { "pay", "pay", "ship", "done" };
    for (unsigned i = 0; i < 4; i++) {
        int ok;
        state_t n = next(s, events[i], &ok);
        if (!ok) printf("%s 状态下 %s 被拒绝\n", name(s), events[i]);
        else     printf("%s -> %s（%s）\n", name(s), name(n), events[i]);
        s = n;
    }
    return 0;
}
'''

C["state.cpp"] = r'''// 状态 · 订单状态流转
// g++ -std=c++17 -Wall -Wextra state.cpp -o state_cpp
#include <cstdio>
#include <memory>
#include <string>

class Order;

class State {
public:
    virtual ~State() = default;
    virtual const char* name() const = 0;
    virtual State* next(const std::string& event) = 0;
};

class New final : public State {
public:
    const char* name() const override { return "新建"; }
    State* next(const std::string& e) override;
};
class Paid final : public State {
public:
    const char* name() const override { return "已支付"; }
    State* next(const std::string& e) override;
};
class Shipped final : public State {
public:
    const char* name() const override { return "已发货"; }
    State* next(const std::string& e) override;
};
class Done final : public State {
public:
    const char* name() const override { return "已完成"; }
    State* next(const std::string&) override { return this; }
};

static New S_NEW; static Paid S_PAID; static Shipped S_SHIPPED; static Done S_DONE;

State* New::next(const std::string& e) { return e == "pay" ? static_cast<State*>(&S_PAID) : this; }
State* Paid::next(const std::string& e) { return e == "ship" ? static_cast<State*>(&S_SHIPPED) : this; }
State* Shipped::next(const std::string& e) { return e == "done" ? static_cast<State*>(&S_DONE) : this; }

class Order {
public:
    explicit Order(State* s) : s_(s) {}
    void handle(const std::string& e) {
        State* n = s_->next(e);
        if (n == s_) std::printf("%s 状态下 %s 被拒绝\n", s_->name(), e.c_str());
        else { std::printf("%s -> %s（%s）\n", s_->name(), n->name(), e.c_str()); s_ = n; }
    }
private:
    State* s_;
};

int main()
{
    Order o(&S_NEW);
    o.handle("pay"); o.handle("pay"); o.handle("ship"); o.handle("done");
    return 0;
}
'''

C["strategy.c"] = r'''/* 策略 · 排序策略
 * gcc -std=c11 -Wall -Wextra strategy.c -o strategy
 */
#include <stdio.h>

typedef void (*sort_fn)(int *, int);

static void bubble(int *a, int n)
{
    for (int i = 0; i < n; i++)
        for (int j = 0; j + 1 < n - i; j++)
            if (a[j] > a[j + 1]) { int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; }
}

static void insertion(int *a, int n)
{
    for (int i = 1; i < n; i++) {
        int key = a[i], j = i - 1;
        while (j >= 0 && a[j] > key) { a[j + 1] = a[j]; j--; }
        a[j + 1] = key;
    }
}

static void run(const char *name, sort_fn fn, int *src, int n)
{
    int a[8];
    for (int i = 0; i < n; i++) a[i] = src[i];
    fn(a, n);
    printf("%s：", name);
    for (int i = 0; i < n; i++) printf(" %d", a[i]);
    printf("\n");
}

int main(void)
{
    int src[] = { 5, 1, 4, 2, 3 };
    run("冒泡", bubble, src, 5);
    run("插入", insertion, src, 5);
    printf("排序函数是参数，换策略不改调用方\n");
    return 0;
}
'''

C["strategy.cpp"] = r'''// 策略 · 排序策略
// g++ -std=c++17 -Wall -Wextra strategy.cpp -o strategy_cpp
#include <cstdio>
#include <memory>
#include <vector>

class SortStrategy {
public:
    virtual ~SortStrategy() = default;
    virtual const char* name() const = 0;
    virtual void sort(std::vector<int>& v) const = 0;
};

class Bubble final : public SortStrategy {
public:
    const char* name() const override { return "冒泡"; }
    void sort(std::vector<int>& v) const override {
        for (size_t i = 0; i < v.size(); i++)
            for (size_t j = 0; j + 1 < v.size() - i; j++)
                if (v[j] > v[j + 1]) std::swap(v[j], v[j + 1]);
    }
};

class Insertion final : public SortStrategy {
public:
    const char* name() const override { return "插入"; }
    void sort(std::vector<int>& v) const override {
        for (size_t i = 1; i < v.size(); i++) {
            int key = v[i], j = static_cast<int>(i) - 1;
            while (j >= 0 && v[j] > key) { v[j + 1] = v[j]; j--; }
            v[j + 1] = key;
        }
    }
};

class Sorter {
public:
    explicit Sorter(std::unique_ptr<SortStrategy> s) : s_(std::move(s)) {}
    void run(std::vector<int> v) {
        s_->sort(v);
        std::printf("%s：", s_->name());
        for (int x : v) std::printf(" %d", x);
        std::printf("\n");
    }
private:
    std::unique_ptr<SortStrategy> s_;
};

int main()
{
    std::vector<int> src = { 5, 1, 4, 2, 3 };
    Sorter(std::make_unique<Bubble>()).run(src);
    Sorter(std::make_unique<Insertion>()).run(src);
    std::puts("排序函数是参数，换策略不改调用方");
    return 0;
}
'''

C["template_method.c"] = r'''/* 模板方法 · 生成 CSV / HTML 报告
 * gcc -std=c11 -Wall -Wextra template_method.c -o template_method
 */
#include <stdio.h>

typedef struct {
    const char *name;
    void (*header)(void);
    void (*row)(int);
    void (*footer)(void);
} report_t;

static void run(const report_t *r)
{
    printf("== %s ==\n", r->name);
    r->header();
    for (int i = 1; i <= 3; i++) r->row(i);
    r->footer();
}

static void csv_header(void) { puts("id,qty"); }
static void csv_row(int i)    { printf("%d,%d\n", i, i * 10); }
static void csv_footer(void)  { puts("--"); }

static void html_header(void) { puts("<table>"); }
static void html_row(int i)   { printf("<tr><td>%d</td><td>%d</td></tr>\n", i, i * 10); }
static void html_footer(void) { puts("</table>"); }

int main(void)
{
    report_t csv  = { "CSV", csv_header, csv_row, csv_footer };
    report_t html = { "HTML", html_header, html_row, html_footer };
    run(&csv);
    run(&html);
    printf("顺序、循环次数都在 run() 里，两个格式只换三步实现\n");
    return 0;
}
'''

C["template_method.cpp"] = r'''// 模板方法 · 生成 CSV / HTML 报告
// g++ -std=c++17 -Wall -Wextra template_method.cpp -o template_method_cpp
#include <cstdio>
#include <string>

class Report {
public:
    void run() {
        std::printf("== %s ==\n", name().c_str());
        header();
        for (int i = 1; i <= 3; i++) row(i);
        footer();
    }
    virtual ~Report() = default;
protected:
    virtual std::string name() const = 0;
    virtual void header() const = 0;
    virtual void row(int i) const = 0;
    virtual void footer() const = 0;
};

class CsvReport final : public Report {
protected:
    std::string name() const override { return "CSV"; }
    void header() const override { std::puts("id,qty"); }
    void row(int i) const override { std::printf("%d,%d\n", i, i * 10); }
    void footer() const override { std::puts("--"); }
};

class HtmlReport final : public Report {
protected:
    std::string name() const override { return "HTML"; }
    void header() const override { std::puts("<table>"); }
    void row(int i) const override { std::printf("<tr><td>%d</td><td>%d</td></tr>\n", i, i * 10); }
    void footer() const override { std::puts("</table>"); }
};

int main()
{
    CsvReport csv;
    HtmlReport html;
    csv.run();
    html.run();
    std::puts("顺序、循环次数都在 run() 里，两个格式只换三步实现");
    return 0;
}
'''

C["visitor.c"] = r'''/* 访问者 · 文件统计
 * gcc -std=c11 -Wall -Wextra visitor.c -o visitor
 */
#include <stdio.h>

typedef struct visitor visitor_t;
typedef struct node node_t;

struct node {
    char name[16];
    int is_dir;
    int size;
    node_t *kids[3];
    int nkids;
    void (*accept)(node_t *, visitor_t *);
};

struct visitor {
    int files;
    int total;
    void (*visit_file)(visitor_t *, const node_t *);
    void (*visit_dir)(visitor_t *, const node_t *);
};

static void file_accept(node_t *n, visitor_t *v) { v->visit_file(v, n); }
static void dir_accept(node_t *n, visitor_t *v)  { v->visit_dir(v, n); }

static void count_file(visitor_t *v, const node_t *n)
{
    v->files++; v->total += n->size;
    printf("  文件 %s (%d 字节)\n", n->name, n->size);
}
static void enter_dir(visitor_t *v, const node_t *n)
{
    printf("  进入目录 %s\n", n->name);
    (void)v;
}

int main(void)
{
    node_t a = { "a.c", 0, 120, { 0 }, 0, file_accept };
    node_t b = { "b.c", 0, 80,  { 0 }, 0, file_accept };
    node_t d = { "src", 1, 0, { &a, &b, NULL }, 2, dir_accept };
    node_t r = { "root", 1, 0, { &d, NULL, NULL }, 1, dir_accept };

    visitor_t v = { 0, 0, count_file, enter_dir };

    r.accept(&r, &v);
    d.accept(&d, &v);
    a.accept(&a, &v);
    b.accept(&b, &v);

    printf("统计：%d 个文件，%d 字节\n", v.files, v.total);
    printf("节点只负责 accept，统计逻辑在 visitor 里\n");
    return 0;
}
'''

C["visitor.cpp"] = r'''// 访问者 · 文件统计
// g++ -std=c++17 -Wall -Wextra visitor.cpp -o visitor_cpp
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

class Visitor;

class Node {
public:
    Node(std::string name, bool dir, int size = 0)
        : name_(std::move(name)), dir_(dir), size_(size) {}
    virtual ~Node() = default;
    virtual void accept(Visitor& v) = 0;
    const std::string& name() const { return name_; }
    int size() const { return size_; }
    bool isDir() const { return dir_; }
private:
    std::string name_;
    bool dir_;
    int size_;
};

class File final : public Node {
public:
    File(std::string n, int s) : Node(std::move(n), false, s) {}
    void accept(Visitor& v) override;
};

class Dir final : public Node {
public:
    Dir(std::string n) : Node(std::move(n), true) {}
    void add(std::unique_ptr<Node> k) { kids_.push_back(std::move(k)); }
    const std::vector<std::unique_ptr<Node>>& kids() const { return kids_; }
    void accept(Visitor& v) override;
private:
    std::vector<std::unique_ptr<Node>> kids_;
};

class Visitor {
public:
    virtual ~Visitor() = default;
    virtual void visitFile(const File& f) = 0;
    virtual void visitDir(const Dir& d) = 0;
};

class Counter final : public Visitor {
public:
    void visitFile(const File& f) override {
        ++files_; total_ += f.size();
        std::printf("  文件 %s (%d 字节)\n", f.name().c_str(), f.size());
    }
    void visitDir(const Dir& d) override {
        std::printf("  进入目录 %s\n", d.name().c_str());
    }
    int files() const { return files_; }
    int total() const { return total_; }
private:
    int files_ = 0;
    int total_ = 0;
};

void File::accept(Visitor& v) { v.visitFile(*this); }
void Dir::accept(Visitor& v) { v.visitDir(*this); }

int main()
{
    auto a = std::make_unique<File>("a.c", 120);
    auto b = std::make_unique<File>("b.c", 80);
    auto src = std::make_unique<Dir>("src");
    src->add(std::move(a));
    src->add(std::move(b));

    Counter c;
    src->kids()[0]->accept(c);
    src->kids()[1]->accept(c);
    src->accept(c);

    std::printf("统计：%d 个文件，%d 字节\n", c.files(), c.total());
    std::puts("节点只负责 accept，统计逻辑在 visitor 里");
    return 0;
}
'''

for name, code in C.items():
    (SRC / name).write_text(code, encoding="utf-8")
print("wrote", len(C))


