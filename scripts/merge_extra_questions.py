#!/usr/bin/env python3
"""Safe, additive merger for Flavor Lab's two new PDF question banks.
Run from a *feature branch* in the existing repository after copying additions_190.json.
Never reassigns existing IDs 1-285 and never modifies app state.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST = ROOT / 'data/questions.json'
ADD = ROOT / 'data/additions_190.json'

def fail(msg):
    raise SystemExit('STOP: ' + msg)

try:
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
except (subprocess.CalledProcessError, FileNotFoundError):
    fail('Run inside a local Git repository, on a separate feature branch.')
if not branch or branch in ('main', 'master'):
    fail('Switch to a feature branch before importing data. Main has not been modified.')

bank = json.loads(DEST.read_text(encoding='utf-8'))
extra = json.loads(ADD.read_text(encoding='utf-8'))
if [q['id'] for q in extra['questions']] != list(range(286, 476)):
    fail('Addition IDs must be exactly 286-475.')
if len(extra['chapters']) != 10 or len({c['id'] for c in extra['chapters']}) != 10:
    fail('Expected exactly 10 distinct new sections.')

ids = [q['id'] for q in bank['questions']]
if ids == list(range(1, 476)):
    if bank['questions'][285:] == extra['questions'] and bank['chapters'][-10:] == extra['chapters']:
        print('Already imported and identical; no changes needed.')
        sys.exit(0)
    fail('475 questions already exist but differ; do not overwrite.')
if ids != list(range(1, 286)):
    fail('Original bank does not contain expected questions 1-285 in order.')
if len(bank['chapters']) != 8:
    fail('Expected 8 original sections; examine the current repository before merging.')
orig_ch_ids = {c['id'] for c in bank['chapters']}
if orig_ch_ids & {c['id'] for c in extra['chapters']}:
    fail('One or more new section IDs collide with original sections.')
merged = {'chapters': bank['chapters'] + extra['chapters'], 'questions': bank['questions'] + extra['questions']}
if len(merged['questions']) != 475:
    fail('Incorrect merged total.')
# Use the existing repository's one-space JSON indentation to reduce unrelated diff churn.
text = json.dumps(merged, ensure_ascii=False, indent=1) + '\n'
DEST.write_text(text, encoding='utf-8')
print('Merged 190 questions into data/questions.json. Total: 475. Original questions preserved.')
