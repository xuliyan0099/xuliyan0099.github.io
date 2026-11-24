// 中介者 · 聊天室转发
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
