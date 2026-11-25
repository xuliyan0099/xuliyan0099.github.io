p = r"D:\Workspace\MainPage\imx6ull\rm\rm-data.js"
t = open(p, encoding="utf-8").read()
s = t.find('"n": 15')
s2 = t.find('{ "n": 15')
print("idx15", s, s2)
print(t[s2 - 20:s2 + 700])
print("....")
i = t.find('"n": 17')
print(t[i - 40:i + 500])
