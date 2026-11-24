import zlib,base64
STD="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
PU ="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
def enc(t):
    c=zlib.compress(t.encode())[2:-4]
    b=base64.b64encode(c).decode().rstrip("=")
    return "".join(PU[STD.index(ch)] for ch in b)
print(enc("@startuml\nA -> B: hi\n@enduml"))