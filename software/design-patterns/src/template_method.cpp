// 模板方法 · 生成 CSV / HTML 报告
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
