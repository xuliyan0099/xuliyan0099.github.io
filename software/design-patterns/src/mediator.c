/* 中介者 · 聊天室转发
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
