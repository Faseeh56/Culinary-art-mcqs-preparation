import re, json, sys
txt = open('q.txt', encoding='utf-8').read()
pages = txt.split('\f')
CH = [("ch1","The Professional Kitchen",1,15),("ch3","Heat Transfer & Cooking Methods",16,47),
("ch4","Knives, Tools & Equipment",48,64),("ch5","Stocks, Sauces & Soups",65,105),
("ch6","Vegetables & Legumes",106,129),("ch11","Fish & Shellfish",130,160),
("ch12","Produce, Grains, Dairy & Food Safety",161,250),("rapid","Rapid-Fire Class Notes",251,285)]
lines=[]  # (page, line)
for pi in range(1,34):  # pages 2..34
    for l in pages[pi].split('\n'):
        if re.search(r'Culinary Arts Question Bank|^\s*Page \d+|^\s*CHAPTER|^\s*PART B|^\s*Questions \d+–|^\s*(GRAINS, DAIRY|STORAGE)',l) and not re.match(r'\s*\d+\.',l): continue
        if l.strip(): lines.append((pi+1,l))
# subtopic headings
sub=None; subch=0; blocks=[]; cur=None
for i,(pg,l) in enumerate(lines):
    nxt = lines[i+1][1] if i+1<len(lines) else '1. '
    if re.match(r'^ ?[A-E]\. [^✓]*$',l) and not re.search(r'\s{3,}',l.strip()) and re.match(r'^\s*\d+\. ',nxt):
        sub=l.strip()[3:]; subch=int(re.match(r'^\s*(\d+)\.',nxt).group(1)); continue
    m=re.match(r'^\s*(\d+)\. (.*)',l)
    if m and int(m.group(1))==(cur['id']+1 if cur else 1):
        qid=int(m.group(1)); same=sub and [c for c in CH if c[2]<=qid<=c[3]][0]==[c for c in CH if c[2]<=subch<=c[3]][0]
        cur={'id':qid,'page':pg,'sub':sub if same else None,'raw':m.group(2)}; blocks.append(cur); continue
    cur['raw']+='\n'+l
qs=[]
def parse_col(text):
    pos=[];out=[]
    for m in re.finditer(r'(?:^|\s)([A-E])\. ',text): pos.append((m.group(1),m.end(),m.start()))
    for k,(lab,e,st) in enumerate(pos):
        t=text[e:pos[k+1][2] if k+1<len(pos) else len(text)]
        out.append((lab,'\u2713' in t,' '.join(t.replace('\u2713','').split())))
    return out
for b in blocks:
    ls=b['raw'].split('\n')
    ai=next((i for i,l in enumerate(ls) if i>0 and re.match(r'^\s*A\. ',l)) , None)
    if ai is None and re.match(r'^\s*A\. ',ls[0]): ai=0
    first=ls[0]
    stem_lines=ls[:ai]
    opt_lines=ls[ai:]
    rc=None
    for l in opt_lines:
        m=re.search(r'\s{2,}([BD]\. )',l)
        if m: rc=m.start(1); break
    if rc is None: rc=10**6
    left='\n'.join(l[:rc] for l in opt_lines); right='\n'.join(l[rc:] for l in opt_lines)
    parsed=sorted(parse_col(left)+parse_col(right),key=lambda x:x[0])
    stem=' '.join(' '.join(stem_lines).split())
    opts=[{'label':l,'text':t} for l,_,t in parsed]
    correct=[l for l,ok,_ in parsed if ok]
    ch=[c for c in CH if c[2]<=b['id']<=c[3]][0]
    qs.append({'id':b['id'],'chapterId':ch[0],'subtopic':b['sub'],'question':stem,'options':opts,
      'correctOption':correct[0] if len(correct)==1 else None,'_marks':correct,'sourcePage':b['page']})
# answer key
key={}
for pg in pages[34:36]:
    for n,a in re.findall(r'\b(\d{1,3})[ \t]+([A-E])\b',pg): key[int(n)]=a
issues=[]
for q in qs:
    if len(q['_marks'])!=1 or key.get(q['id'])!=q['correctOption']: issues.append((q['id'],q['_marks'],key.get(q['id'])))
print(len(qs),'questions; key size',len(key),'; mismatches:',issues)
for q in qs: q.pop('_marks')
json.dump({'chapters':[{'id':c[0],'title':c[1],'from':c[2],'to':c[3]} for c in CH],'questions':qs},open('flavor-lab/data/questions.json','w'),ensure_ascii=False,indent=1)
