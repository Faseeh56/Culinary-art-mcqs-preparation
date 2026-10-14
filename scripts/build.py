import json,pathlib
r=pathlib.Path(__file__).resolve().parent.parent
d=json.dumps(json.load(open(r/'data/questions.json',encoding='utf-8')),ensure_ascii=False).replace('</','<\\/')
(r/'index.html').write_text((r/'app.template.html').read_text(encoding='utf-8').replace('/*DATA*/null',d),encoding='utf-8')
print('built index.html')
