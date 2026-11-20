
#!/usr/bin/env python3
"""Validator for The Flavor Lab — 1,154 questions, 64 chapters."""

import json
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
bank = json.loads(
    (ROOT / "data/questions.json").read_text(encoding="utf-8")
)

questions = bank["questions"]
chapters = bank["chapters"]
errors = []

# 1. Overall counts and sequential IDs
if len(questions) != 1154:
    errors.append(f"Expected 1154 questions; got {len(questions)}")

if len(chapters) != 64:
    errors.append(f"Expected 64 chapters; got {len(chapters)}")

ids = [q.get("id") for q in questions]

if ids != list(range(476, 1630)):
    errors.append("Question IDs must be sequential from 476 to 1629.")

if len(set(ids)) != len(ids):
    errors.append("Duplicate question IDs found.")

chapter_ids = [c.get("id") for c in chapters]

if len(set(chapter_ids)) != len(chapter_ids):
    errors.append("Duplicate chapter IDs found.")

# 2. Chapter ranges and question mapping
seen = Counter(q.get("chapterId") for q in questions)

for chapter in chapters:
    ch_id = chapter["id"]
    expected_ids = set(range(chapter["from"], chapter["to"] + 1))

    actual_ids = {
        q["id"] for q in questions
        if q.get("chapterId") == ch_id
    }

    if actual_ids != expected_ids:
        errors.append(f"{ch_id}: question IDs do not match declared range.")

    if seen[ch_id] != len(expected_ids):
        errors.append(f"{ch_id}: incorrect question count.")

if sum(seen.values()) != len(questions):
    errors.append("Question-to-chapter mapping is inconsistent.")

if any(ch not in set(chapter_ids) for ch in seen):
    errors.append("Found an unrecognized chapter ID.")

# 3. Question structure and answer validation
for q in questions:
    qid = q.get("id")
    opts = q.get("options", [])
    labels = [o.get("label") for o in opts]

    if len(opts) < 2 or len(set(labels)) != len(labels):
        errors.append(f"Q{qid}: invalid option count or duplicate labels.")

    if not q.get("question", "").strip():
        errors.append(f"Q{qid}: missing question text.")

    if any(not o.get("text", "").strip() for o in opts):
        errors.append(f"Q{qid}: blank option text.")

    if q.get("correctOption") not in labels:
        errors.append(f"Q{qid}: correct option missing.")

    if "✓" in q.get("question", "") or any(
        "✓" in o.get("text", "") for o in opts
    ):
        errors.append(f"Q{qid}: visible correct-answer marker.")

    # Original questions added in previous updates
    if 286 <= qid <= 725:
        if (
            not q.get("sourceTitle")
            or not isinstance(q.get("sourceQuestionId"), int)
            or not q.get("sourcePage")
        ):
            errors.append(f"Q{qid}: existing source reference missing.")

    # New sourced questions
    if qid >= 726:
        if (
            not q.get("sourceTitle")
            or not isinstance(q.get("sourceQuestionId"), int)
            or not isinstance(q.get("sourceChapterNumber"), int)
            or not q.get("sourceChapterTitle")
        ):
            errors.append(f"Q{qid}: new source metadata incomplete.")

# 4. Final result
if errors:
    print("FAILED:")
    for error in errors:
        print(" - " + error)
    sys.exit(1)

print("PASS: 1,154 questions; 64 chapters.")
print("PASS: Sequential IDs, unique chapters and valid answer keys.")
print("PASS: Question structure and source metadata.")
