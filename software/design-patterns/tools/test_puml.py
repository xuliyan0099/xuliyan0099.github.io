# -*- coding: utf-8 -*-
import zlib, base64, urllib.request

def enc(s):
    c = zlib.compress(s.encode("utf-8"))[2:-4]
    return base64.b64encode(c).decode().replace("+", "-").replace("/", "_").rstrip("=")

src = "@startuml\nA -> B: hi\n@enduml"
u = "https://www.plantuml.com/plantuml/svg/" + enc(src)
req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
data = urllib.request.urlopen(req, timeout=20).read()
print(len(data), data[:60])
