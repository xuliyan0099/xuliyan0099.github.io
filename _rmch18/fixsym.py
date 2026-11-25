import re, sys, io

LABELS = {
    'i-play': '播放', 'i-pause': '暂停', 'i-reset': '重置', 'i-prev': '上一步',
    'i-next': '下一步', 'i-fullscreen': '全屏', 'i-speak': '朗读', 'i-drag': '拖动',
    'i-correct': '正确', 'i-wrong': '错误', 'i-alert': '注意', 'i-explain': '讲解',
    'i-close': '关闭'
}

def fix(path):
    t = open(path, encoding='utf-8').read()
    n = 0
    for sid, label in LABELS.items():
        pat = re.compile(r'(<symbol id="' + sid + r'"[^>]*><title>)[^<]*(</title>)')
        def rep(m):
            return m.group(1) + label + m.group(2)
        t, c = pat.subn(rep, t)
        n += c
    open(path, 'w', encoding='utf-8', newline='').write(t)
    print(path, 'symbols fixed:', n)

for p in sys.argv[1:]:
    fix(p)
