/* 模板方法 · 生成 CSV / HTML 报告
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
