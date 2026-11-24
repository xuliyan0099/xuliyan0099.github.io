// 抽象工厂 · GUI：浅色/深色两套控件
// g++ -std=c++17 -Wall -Wextra abstract_factory.cpp -o abstract_factory_cpp
#include <cstdio>
#include <memory>
#include <string>

class Button { public: virtual ~Button() = default; virtual std::string label() const = 0; };
class Checkbox { public: virtual ~Checkbox() = default; virtual std::string label() const = 0; };

class LightButton final : public Button {
public: std::string label() const override { return "[ 浅色按钮 ]"; }
};
class LightCheckbox final : public Checkbox {
public: std::string label() const override { return "[ ] 浅色复选框"; }
};

class DarkButton final : public Button {
public: std::string label() const override { return "[ 深色按钮 ]"; }
};
class DarkCheckbox final : public Checkbox {
public: std::string label() const override { return "[x] 深色复选框"; }
};

class GuiFactory {
public:
    virtual ~GuiFactory() = default;
    virtual std::unique_ptr<Button>   button() const = 0;
    virtual std::unique_ptr<Checkbox> checkbox() const = 0;

    void render(const char* theme) const {
        auto b = button();
        auto c = checkbox();
        std::printf("%s 界面：%s  %s\n", theme, b->label().c_str(), c->label().c_str());
    }
};

class LightFactory final : public GuiFactory {
public:
    std::unique_ptr<Button> button() const override { return std::make_unique<LightButton>(); }
    std::unique_ptr<Checkbox> checkbox() const override { return std::make_unique<LightCheckbox>(); }
};

class DarkFactory final : public GuiFactory {
public:
    std::unique_ptr<Button> button() const override { return std::make_unique<DarkButton>(); }
    std::unique_ptr<Checkbox> checkbox() const override { return std::make_unique<DarkCheckbox>(); }
};

int main()
{
    LightFactory light;
    DarkFactory dark;
    light.render("浅色");
    dark.render("深色");
    return 0;
}
