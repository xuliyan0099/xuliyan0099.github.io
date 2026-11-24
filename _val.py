import re,os
base=r"D:\Workspace\MainPage\imx6ull\hardware\p3"
bad=[r"</span></h2>",r"</th></th>",r"</p></b>",r"<<",r"</wbr>",r"</it>",r"</strong></b>",r"</figcaption></button>",r"</p></li>",r"<tr><tr>",r"</div></h2>",r"</p></h2>",r"</summary></summary>",r"</summary></div>"]
for i in range(1,13):
    p=os.path.join(base,f"c{i:02d}.html")
    s=open(p,encoding="utf-8").read()
    hits=[b for b in bad if b in s]
    imgs=re.findall(r'src="([^"]+)"',s)
    missing=[]
    for im in imgs:
        ap=os.path.normpath(os.path.join(base,im))
        if not os.path.exists(ap): missing.append(im)
    d1=s.count("<details"); d2=s.count("</details>")
    print(f"c{i:02d}.html {len(s)} chars, details {d1}/{d2}, bad={hits}, missing={missing}")
