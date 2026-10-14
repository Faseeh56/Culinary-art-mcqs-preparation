import json,sys,pathlib,re
r=pathlib.Path(__file__).resolve().parent.parent
d=json.load(open(r/'data/questions.json',encoding='utf-8'));q=d['questions'];e=[]
if len(q)!=285:e.append('count')
if sorted(x['id'] for x in q)!=list(range(1,286)):e.append('ids')
for x in q:
    L=[o['label'] for o in x['options']]
    if len(L)<2 or len(set(L))!=len(L) or any(not o['text'] for o in x['options']):e.append(f"opts {x['id']}")
    if x['correctOption'] not in L:e.append(f"key {x['id']}")
    if any('✓' in o['text'] for o in x['options']) or '✓' in x['question']:e.append(f"leak {x['id']}")
for c in d['chapters']:
    n=sum(1 for x in q if x['chapterId']==c['id'])
    if n!=c['to']-c['from']+1:e.append('chapter '+c['id'])
print('FAIL' if e else 'OK: 285 questions, ids 1-285, keys valid, no leaks, chapter counts match',e)
sys.exit(1 if e else 0)
