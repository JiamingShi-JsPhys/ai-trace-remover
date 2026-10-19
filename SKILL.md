---
name: ai-trace-remover
description: "De-AI-flavour (去 AI 味) skill for Chinese and English prose. Use when the user wants to make text sound like a real person wrote it, score how AI-flavoured a text reads (0-100 human index), or detect-only. Triggers on \"去AI味\", \"改得像人写的\", \"humanize\", \"score\". A pure-stdlib scanner reports AI-pattern hits, scores, and blocking hard-bans. Three paths: create-with-voice (A), de-AI-rewrite (B), detect-only (C)."
metadata:
  author: Jiaming Shi
  license: MIT
  version: 1.0.0
  entry_point: python -m src.cli
  python_requires: '>=3.9'
---

# ai-trace-remover

This skill **makes text sound like a specific person wrote it** by removing machine-generated tells. 

**Core Loop:** The engine detects and quantifies; the agent rewrites by hand. *Never present a scanner result as a rewrite.*

## When to use
- User asks to remove AI flavor (去 AI 味 / humanize) or score it.
- A draft must not read as model-generated before shipping.

## When NOT to use (Out of Scope)
- Poetry, scripts, experimental writing (judge by form, not score).
- Legal, academic, or standards-constrained prose (take detection only, do not restyle).
- Pure translation where source structure must be preserved.

## Core Workflow
Trigger this exact loop whenever the skill is activated:

1. **Scan:** Run the scanner first. Do not rewrite based on intuition.
   `python -m src.cli <file|-> --json`
2. **Locate:** Read the report and prioritize fixes based on `references/scoring-rubric.md`.
3. **Rewrite & Re-scan:** Rewrite the draft by hand following `references/revision.md`. Then run the scanner again. 
   - Iterate until hard-bans are zero and (for Chinese) human index is ≥ 85.
   - *If the score falls after rewriting, you only deleted words without adding specifics. Go back to the top-priority category.*

## Hard Constraints (Red Lines)
- **Never invent facts.** If the source lacks numbers/nouns, ask the user; do not fabricate.
- **Path A (Create) Materials Gate:** For non-fiction (≥1200 words), list at least 5 concrete facts *before* writing. Cannot list 5? Shrink to a ~600-word short answer. Never pad with boilerplate.
- **Hard-bans block shipping.** Clear them before anything else.
- **Only Chinese gets the ≥85 gate.** English prose only needs hard-bans cleared.
- **Strict tone separation.** Chat = warm/friendly. File = cool/restrained.
- **No decorative emojis.** (Blocking hard-ban HB14).

## Resources
- `references/revision.md`: Seven-pass revision + Sound-5 rules.
- `references/scoring-rubric.md`: 0-100 scoring algorithm + shipping gate.
- `references/example-diff.md`: Before/after examples.