#!/usr/bin/env python3
"""Minimal, guarded UI compatibility patch for existing app.template.html.
Refuses unknown/changed source patterns rather than doing potentially unsafe edits.
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
path = ROOT / 'app.template.html'
branch = subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
if branch in ('main','master',''):
    raise SystemExit('STOP: Run this only on your feature branch.')
src = path.read_text(encoding='utf-8')
new_meta = (
    ",'part2-veg':['#36C9AE','🥬']"
    ",'part2-potatoes':['#FFAD36','🥔']"
    ",'part2-dairy':['#B68DF2','🧈']"
    ",'part2-rice':['#35B5EE','🍚']"
    ",'special-thermo':['#FF6578','🌡️']"
    ",'special-immersion':['#7282FF','🥣']"
    ",'special-chinois':['#36C9AE','🫗']"
    ",'special-gelatin':['#B68DF2','🍮']"
    ",'special-extraction':['#FFAD36','🍲']"
    ",'special-reduction':['#FF6578','🥄']"
)
changes = [
    ("rapid:['#7282FF','⚡']};", "rapid:['#7282FF','⚡']"+new_meta+"};"),
    ("c.id==='rapid'?c.title:'Ch. '+c.id.replace('ch','')+' — '+c.title", "c.id.startsWith('ch')?'Ch. '+c.id.slice(2)+' — '+c.title:c.title"),
    ("Source: question bank p.${q.sourcePage}", "Source: ${esc(q.sourceTitle || 'Culinary Arts Question Bank')} p.${q.sourcePage}"),
    ('max="285"', 'max="${QS.length}"'),
]
for before, after in changes:
    count = src.count(before)
    if count == 1:
        src = src.replace(before, after)
    elif count == 0 and after in src:
        print('Already updated:', before[:60])
    else:
        raise SystemExit(f'STOP: Unexpected source pattern, no file written: {before[:80]!r} (found {count}). Review current app.template.html manually.')
# avoid leaving the generated HTML without its data injection marker
if '/*DATA*/null' not in src:
    raise SystemExit('STOP: Embedded-data placeholder missing; no changes saved.')
path.write_text(src,encoding='utf-8')
print('Updated chapter colors/icons, display names, source attribution and custom exam maximum.')
