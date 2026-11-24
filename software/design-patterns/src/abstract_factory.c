/* 抽象工厂 · GUI：浅色/深色两套控件
 * gcc -std=c11 -Wall -Wextra abstract_factory.c -o abstract_factory
 */
#include <stdio.h>

typedef struct { const char *(*label)(void); } button_t;
typedef struct { const char *(*label)(void); } checkbox_t;

typedef struct {
    button_t   *(*button)(void);
    checkbox_t *(*checkbox)(void);
} gui_factory_t;

static const char *light_btn_label(void) { return "[ 浅色按钮 ]"; }
static button_t light_btn = { light_btn_label };
static button_t *light_button(void) { return &light_btn; }
static const char *light_box_label(void) { return "[ ] 浅色复选框"; }
static checkbox_t light_box = { light_box_label };
static checkbox_t *light_checkbox(void) { return &light_box; }
static gui_factory_t LIGHT = { light_button, light_checkbox };

static const char *dark_btn_label(void) { return "[ 深色按钮 ]"; }
static button_t dark_btn = { dark_btn_label };
static button_t *dark_button(void) { return &dark_btn; }
static const char *dark_box_label(void) { return "[x] 深色复选框"; }
static checkbox_t dark_box = { dark_box_label };
static checkbox_t *dark_checkbox(void) { return &dark_box; }
static gui_factory_t DARK = { dark_button, dark_checkbox };

static void render(const char *theme, gui_factory_t *f)
{
    button_t   *b = f->button();
    checkbox_t *c = f->checkbox();
    printf("%s 界面：%s  %s\n", theme, b->label(), c->label());
}

int main(void)
{
    render("浅色", &LIGHT);
    render("深色", &DARK);
    return 0;
}
