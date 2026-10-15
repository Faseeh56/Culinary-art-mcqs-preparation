#!/usr/bin/env python3
"""Expanded strict 475-question validator for The Flavor Lab."""
import json
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
bank = json.loads((ROOT / 'data/questions.json').read_text(encoding='utf-8'))
questions, chapters = bank['questions'], bank['chapters']
errors = []

ids = [q['id'] for q in questions]
if len(questions) != 725:
    errors.append(f'Expected 725 questions; got {len(questions)}')
if ids != list(range(1, 726)):
    errors.append('Question IDs must be sequential 1..725, with existing 1..285 unchanged.')
if len(chapters) != 33 or len(set(c['id'] for c in chapters)) != 33:
    errors.append('Expected exactly 33 unique sections')
seen = Counter(q.get('chapterId') for q in questions)
for chapter in chapters:
    ch_id = chapter['id']
    expected_ids = set(range(chapter['from'], chapter['to'] + 1))
    actual_ids = {q['id'] for q in questions if q.get('chapterId') == ch_id}
    if actual_ids != expected_ids:
        errors.append(f'{ch_id}: question IDs do not match the declared range')
    if seen[ch_id] != len(expected_ids):
        errors.append(f'{ch_id}: incorrect chapter question count')
if sum(seen.values()) != len(questions):
    errors.append('Question-to-section mapping is inconsistent')
if any(c not in {x['id'] for x in chapters} for c in seen):
    errors.append('Found unrecognized chapter ID')
for q in questions:
    opts = q.get('options', [])
    labs = [o.get('label') for o in opts]
    if len(opts) < 2 or len(set(labs)) != len(labs):
        errors.append(f'Q{q["id"]}: invalid number of options or duplicate labels')
    if not q.get('question', '').strip() or any(not o.get('text','').strip() for o in opts):
        errors.append(f'Q{q["id"]}: blank question or option text')
    if q.get('correctOption') not in labs:
        errors.append(f'Q{q["id"]}: correct option missing')
    if '✓' in q.get('question', '') or any('✓' in o.get('text','') for o in opts):
        errors.append(f'Q{q["id"]}: correct-answer marker visible to student')
    if q['id'] > 285 and (not q.get('sourceTitle') or not isinstance(q.get('sourceQuestionId'), int) or not q.get('sourcePage')):
        errors.append(f'Q{q["id"]}: new question source reference missing')
if errors:
    print('FAILED:')
    for error in errors: print(' - ' + error)
    sys.exit(1)
print('OK: 725 questions; 33 sections; IDs 1-725; valid answer keys, options and source fields.')