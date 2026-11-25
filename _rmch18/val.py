import json
p = r"D:\Workspace\MainPage\imx6ull\rm\rm-data.js"
t = open(p, encoding="utf-8").read()
i = t.find("["); j = t.rfind("]")
d = json.loads(t[i:j+1])
print("entries", len(d), "ready", sum(1 for x in d if x.get("ready")))
for x in d:
    if x["n"] in (15, 16, 17, 18):
        print(x["n"], x.get("ready"), len(x.get("pts", [])))
