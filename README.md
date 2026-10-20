`English` · [中文说明](README_zh.md)
# ai-trace-remover

> A standalone de-AI-flavour skill (MIT, pure standard library). It makes
> Chinese and English prose stop reading as machine-generated: the bundled
> scanner detects and quantifies the tells - AI-pattern hits, a 0-100 human
> index, blocking hard-bans, and the five "sound of a person" checks - while
> the agent rewrites by hand, so the author's voice is kept instead of
> swapped for another template.

**Disclaimer**: This repository contains auxiliary tools developed by the author to automate research workflows. It is not a peer-reviewed academic project. Some boilerplate or utility scripts may have been generated with the assistance of AI, and have been integrated with high-level review and modifications by the author. The author assumes no responsibility for any third-party code issues, but commits to promptly addressing any valid claims.

<!-- TOC depthFrom:2 -->

- [ai-trace-remover](#ai-trace-remover)
  - [Design principles & core features](#design-principles-&-core-features)
  - [Download and install](#download-and-install)
  - [Quick start](#quick-start)
  - [Tests & coverage](#tests-&-coverage)
  - [Project layout](#project-layout)
  - [Using as an agent skill](#using-as-an-agent-skill)
  - [License](#license)
  - [Report issues](#report-issues)

<!-- END_TOC -->

ai-trace-remover is a universal de-AI-flavour skill that works for both
Chinese and English. It removes the tells that make prose read as
model-written and gives the result a measured score, so a piece only ships
when the tells are gone and a real person is still behind it. Pattern
categories and examples are original; the before/after corpus is self-authored
and built from public-domain teaching texts and classic public-domain fiction.
No code from any other de-AI-flavour skill is copied.

The skill has two legs, neither optional: **washing out machine smell** (a
lexical + structural pattern library, a 0-100 score, and blocking hard-bans)
and **putting a person back** (a creation discipline, a seven-pass revision,
and five "sound of a person" checks). Deleting boilerplate without adding
specifics only turns AI-ese into a press release - still no one behind it.

```
input text  (Chinese or English)
        |
        v
   +---------------------------+
   | scan (src/core/engine.py) |
   |  lexical hits            |--> 0-100 score (zh human index / en AI-taste)
   |  structural counts        |
   |  hard-ban rules          |--> blocking failures (must clear to ship)
   |  sound-of-a-person       |--> five manual checks
   +---------------------------+
        |
        v
   Markdown / JSON report     (the agent rewrites by hand, then re-runs)
```

**The one rule to remember: the engine only detects and quantifies - it never
rewrites.** A clean word-surface is not the same as "has a person"; the
five "sound of a person" checks and the cold-read four questions are the
agent's job. Two opposite scales are used and must not be read on one:
Chinese prose gets a 0-100 *human index* (higher = more human), English
prose gets an *AI-taste* score (higher = more AI).

---

## Design principles & core features

- **Trigger-to-act**: a request to make text sound human, de-AI-flavour it,
  or score how machine-written it reads triggers the whole loop - scan first,
  rewrite by hand, re-scan; describing the tells without running the scanner
  counts as a failure.
- **Detect, do not rewrite**: the engine in `src/core/` makes the tells
  visible and measurable; rewriting is the agent's job, driven by
  `references/`, so the author's voice survives instead of a new template
  replacing the old one.
- **Pure standard library**: no install, no network, no third-party
  dependency. `python -m src.cli` runs on Windows, macOS, and Linux as-is.
- **Two opposite scales**: a 0-100 *human index* for Chinese (higher = more
  human) and an *AI-taste* score for English (higher = more AI); they point
  opposite ways and are never mixed.
- **Blocking hard-bans**: a small set of "absolutely not in a finished piece"
  rules (em-dash, prompt-style colons, reversal rhetoric, marketing jargon,
  inflated endings, English chat-residue / sycophancy / cutoff
  disclaimers). Any hit blocks shipping, whatever the numeric score says.
- **Five "sound of a person" checks**: concrete numbers, concrete nouns,
  uncertainty, a visible speaker, and a reference-only rhythm ratio; the
  scanner quantifies the first three and the last, the agent answers all of
  them by hand before shipping.

### The three paths (brief)

This skill is an "act" instruction, not a summary document: once a trigger
matches, you must run the scanner and report what it found - answering with a
description of the patterns is a task failure. The full agent contract lives
in `SKILL.md`; the essentials:

1. **Pick the path by what the user wants.** Writing new prose with a real
   voice -> **A - create**; a finished draft reads machine-written ->
   **B - de-AI rewrite**; just score / detect -> **C - detect-only**.
2. **Path A (create)**: a materials gate first (non-fiction long-form lists
   at least five concrete, sourced items before writing), then a first
   draft written *with* a person, then the seven-pass revision, then the
   scanner.
3. **Path B (rewrite)**: scan, locate by priority
   (`A4 -> A3 -> A6 -> A1 -> A7 -> A8`), rewrite adding specifics and
   uncertainty, re-score until hard-bans are zero and the human index is
   >= 85 (Chinese).
4. **Path C (detect-only)**: one scan, one report, Top-3 suggestions - no
   rewrite unless the user asks for one afterwards.
5. **The shipping gate is not the whole test**: a score of 85 with the five
   "sound of a person" checks failing still needs work; the number never
   replaces the human read.

---

## Download and install

There are **four** standard ways to get this skill:

**Option 1 — The Windows executable (no Python needed)**

The **Releases** page publishes `ai-trace-remover-<version>-windows.exe`, a
single-file Windows binary built by `build_dist.py --exe`. Download it and
run it from a terminal - it bundles the whole scanner plus the CLI:

```bash
ai-trace-remover.exe draft.md --score-only
ai-trace-remover.exe draft.md -o report.md
```

The Windows binary is for users without Python. On macOS / Linux, use the
source archive below - it runs on the standard library alone.

**Option 2 — The source archive (recommended for all platforms)**

From the **Releases** page, download `ai-trace-remover-<version>.zip` and
unpack it - no installer required:

```bash
unzip ai-trace-remover-1.0.0.zip
cd ai-trace-remover-1.0.0            # the whole skill is this one folder
python -m src.cli draft.md
```

No build step, no dependencies. `python -m src.cli` runs on Windows, macOS,
and Linux as-is (Python 3.9+).

**Option 3 — Let an Agent fetch it**

Copy the following instruction to your Agent; it will locate this
skill, download it from the **Releases** page, and set it up for you:

> Please visit https://github.com/JiamingShi-JsPhys/ai-trace-remover, read
> the `README.md` at the repo root, and follow its instructions to download
> or install the skill.

You only need to tell the Agent the skill name; it handles the rest.

**Option 4 — Clone the repository**

```bash
git clone https://github.com/JiamingShi-JsPhys/ai-trace-remover.git
cd ai-trace-remover
```

Requirements: Python 3.9+. No third-party dependency - the detector and CLI
run on the standard library alone. (`pytest` is optional, dev-only, for the
test suite.)

---

## Quick start

```bash
cd ai-trace-remover

# 0. (optional) one-line summary for a pipeline: score / level / can-ship
python -m src.cli draft.md --score-only

# 1. a Markdown report to stdout
python -m src.cli draft.md

# 2. machine-readable JSON (the contract for downstream tooling)
python -m src.cli draft.md --json

# 3. pipe a file through without writing a temp file
cat draft.md | python -m src.cli -

# 4. write the report to a file
python -m src.cli draft.md -o report.md
```

Other commands:

```bash
python -m src.cli draft.md --json -o reports/<name>.json   # JSON to a file
python -m src.cli --version                                  # ai-trace-remover 1.0.0
```

Sample output:

```
38/100 [red] heavy AI flavour  hard_bans=2  can_ship=no
```

When `can_ship=yes`, the hard-bans are cleared and (for Chinese) the human
index is >= 85 - the piece may ship. When `can_ship=no`, clear the
hard-bans and rewrite the top-priority hits, then re-run; the engine never
rewrites for you.

### The workflow in a healthy session

```
you hand the draft to the agent (or ask for a score)
        |
        v
   +-----------+      +---------------------------------------+
   |  scan     |----->| Markdown / JSON report               |
   | (src.cli) |      |  hits + score + hard-bans + sound-5  |
   +-----------+      +---------------------------------------+
        |
        v  (the agent rewrites by hand, following references/)
   +-----------+
   |  re-scan  |  -->  hard-bans zero + human index >= 85 -> ship
   +-----------+
```

The goal is to keep the piece honest about its own tells: the scanner makes
them visible and measured, the agent fixes them with specifics and voice, and
a second scan proves the fix before the piece ships.

### Step-by-step calls (library use)

```python
from src.core import scan

text = open("draft.md", encoding="utf-8").read()
report = scan(text, "draft.md")
print(report.score, report.ai_taste_score)
print(report.hard_failures, report.can_ship())
```

---

## Tests & coverage

```bash
pytest                                            # full suite
pytest --cov=src --cov-report=term-missing        # with coverage
```

- 52 cases
- `pytest` from this directory; the suite also asserts the documentation
  contracts (version three-way, a CJK-free README, and the template
  structure).

Line coverage is around 85% (target >= 80%).

---

## Project layout

```
ai-trace-remover/
+---- SKILL.md              # skill entry (YAML metadata + execution guide)
+---- README.md
+---- README_zh.md          # Chinese mirror
+---- LICENSE               # MIT
+---- CHANGELOG.md
+---- CITATION.cff
+---- pyproject.toml        # packaging + tool configuration
+---- requirements.txt      # (empty; pure stdlib)
+---- src/
|   +---- __init__.py       # __version__
|   +---- cli.py            # CLI: scan / --json / --score-only / -o
|   `---- core/
|       +---- __init__.py
|       +---- engine.py     # scan(): layered checks + scoring + report
|       +---- patterns_zh.py # Chinese lexical library (A1-A10 + structure)
|       +---- patterns_en.py # English lexical library (E1-E24)
|       +---- hard_bans.py   # blocking "never in a finished piece" rules
|       `---- sound_rules.py # the five "sound of a person" checks
+---- references/
|   +---- ai-patterns-zh.md   # full Chinese library with before/after
|   +---- ai-patterns-en.md   # full English library with before/after
|   +---- scoring-rubric.md   # 0-100 algorithm, grades, shipping gate
|   +---- revision.md         # seven passes + five checks + banned-word table
|   `---- example-diff.md     # four cross-lingual before/after scenes
`---- tests/
    +---- conftest.py
    +---- test_engine.py      # Zh / En / mixed scanning
    +---- test_hard_bans.py   # blocking rules
    +---- test_cli.py         # exit codes and rendering
    `---- test_skill_docs.py  # documentation contract
```

---

## Using as an agent skill

This project is a self-contained agent Skill package. `SKILL.md` carries YAML
frontmatter (`name` / `description` / `version` / `author` / `license` /
`entry_point`) followed by an execution guide. Point any agent at this folder.
When a user request matches this skill's scope, the agent reads the execution
steps in `SKILL.md` and shells out to `python -m src.cli`. (Whether the skill
is loaded depends on the agent's recognition of its scope; it is not
guaranteed to trigger in every conversation.)

One important convention for the agent: the scanner only detects and
quantifies - it never rewrites. After the agent rewrites by hand following
`references/`, it must re-run the scanner to prove the hard-bans are zero and
(a Chinese piece) the human index has reached 85 before the piece ships.
Reporting a clean word-surface as "human" without running the five
"sound of a person" checks is a failure mode, not a shortcut.

You can also call the engine directly from Python:

```python
from src.core import scan
report = scan(open("draft.md", encoding="utf-8").read(), "draft.md")
print(report.score, report.hard_failures)
```

---

## License

MIT License, see [LICENSE](LICENSE).

---

## Report issues

Preferred: Open an issue on the repository's **Issues** page. For
security-vulnerability reports, use the alternative channel below.

Alternative (security-vulnerability reports only): Send an email to
`jiamingshi_git@outlook.com`.

- **Subject**: Must include the prefix `agent-skill_report`, the specific
  skill name, and a brief description.
  - Example: `agent-skill_report ai-trace-remover: the hard-ban regex
    misclassifies a domain-required term as jargon`
- **Body**: Must include reproduction steps, expected behavior, actual
  behavior, and the runtime environment (OS, Python version, relevant
  dependencies installed).
- For severe reports like "a clean piece was wrongly blocked", attach the
  draft and the generated report so the pattern can be inspected.
- Contributors who submit clear, reproducible issues or pull requests will be
  listed in the acknowledgements of the next release notes.
