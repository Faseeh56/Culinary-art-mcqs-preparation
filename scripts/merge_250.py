import json
from pathlib import Path
root=Path(__file__).resolve().parent.parent
p=root/'data/questions.json'
a=json.loads(p.read_text(encoding='utf-8'))
b=json.loads((root/'data/additions_250.json').read_text(encoding='utf-8'))
assert isinstance(a,dict) and 'chapters' in a and 'questions' in a
old={q['id'] for q in a['questions']}; new={q['id'] for q in b['questions']}
assert len(b['questions'])==250 and new==set(range(476,726))
assert len(old)==len(a['questions'])
assert all(q['id'] in old for q in a['questions'] if q['id']<=475)
if new.issubset(old):
    print('Already imported: no changes');exit()
assert not (new & old), 'Partial import or ID collision: aborted without modifying data'
assert len(a['questions'])==475 and len(a['chapters'])==18, 'Expected existing 475-question/18-chapter bank; aborted'
assert not ({c['id'] for c in a['chapters']} & {c['id'] for c in b['chapters']})
a['chapters'].extend(b['chapters']); a['questions'].extend(b['questions'])
assert len(a['questions'])==725 and len(a['chapters'])==33
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Imported 250 questions: 725 total, 33 chapters, 3 courses')
