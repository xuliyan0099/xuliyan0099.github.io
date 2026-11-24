import re,os,glob
js=open('imx6ull/assets/parts.js',encoding='utf-8').read()
parts=re.findall(r"id: '(p\d)'.*?chapters: \[(.*?)\]\s*\}", js, re.S)
total=0;ready=0;missing=[]
for pid,body in parts:
    for m in re.finditer(r"\{ n: '(\S+)', t: '([^']*)', s: '([^']*)', f: '([^']*)', ready: (true|false) \}", body, re.S):
        total+=1
        if m.group(5)=='true':
            ready+=1
            p=os.path.join('imx6ull/hardware',pid,m.group(4))
            if not os.path.exists(p): missing.append(p)
print('total',total,'ready',ready,'missing',missing)
