import re,os,glob
badpats=['</span></h2>','</th></th>','</p></b>','<<','</wbr>','</it>','</strong></b>','</figcaption></button>','</p></li>','<tr><tr>','</div></h2>','</p></h2>','</summary></summary>','</summary></div>','</p></td>','</td></p>','</b></div></div>']
for f in sorted(glob.glob('imx6ull/hardware/p4/c*.html')):
    t=open(f,encoding='utf-8').read()
    bad=[p for p in badpats if p in t]
    miss=[]
    for m in re.finditer(r'src="(../../assets/img/[^"]+)"',t):
        p=os.path.normpath(os.path.join(os.path.dirname(f),m.group(1)))
        if not os.path.exists(p): miss.append(m.group(1))
    print(os.path.basename(f), len(t), 'details', t.count('<details'), '/', t.count('</details>'), 'bad=',bad,'missing=',miss)
