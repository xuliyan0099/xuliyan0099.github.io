# -*- coding: utf-8 -*-
import base64, pathlib, sys, time, urllib.request, zlib
from prod_a import P as A
from prod_b import P as B
from prod_c import P as C

P = {}
P.update(A); P.update(B); P.update(C)
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "puml"
OUT.mkdir(parents=True, exist_ok=True)

STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
PU = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def enc(t):
    c = zlib.compress(t.encode("utf-8"))[2:-4]
    b = base64.b64encode(c).decode().rstrip("=")
    return "".join(PU[STD.index(ch)] for ch in b)

def slug(k):
    return "dp-" + k.replace(".", "-")

force = "--force" in sys.argv
bad = []
for k, v in P.items():
    name = slug(k)
    src = v["puml"].strip() + "\n"
    (OUT / (name + ".puml")).write_text(src, encoding="utf-8", newline="\n")
    svg = OUT / (name + ".svg")
    if svg.exists() and svg.stat().st_size > 800 and not force:
        continue
    url = "https://www.plantuml.com/plantuml/svg/" + enc(src)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        data = urllib.request.urlopen(req, timeout=30).read()
    except Exception as e:
        bad.append((k, str(e))); continue
    if b"<svg" not in data[:200] or b"Syntax Error" in data:
        bad.append((k, "render error")); continue
    svg.write_bytes(data)
    print("ok", k, len(data))
    time.sleep(0.4)
print("BAD", bad, "TOTAL", len(P))