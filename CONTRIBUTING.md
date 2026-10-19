# Contributing to ai-trace-remover

Thank you for considering a contribution. This document explains how to
set up the development environment, run tests, and submit changes that fit
the project's standards.

## Development environment

```bash
# 1. Clone the repository
git clone https://github.com/JiamingShi-JsPhys/ai-trace-remover.git
cd ai-trace-remover

# 2. Create a virtual environment (optional; the skill is pure stdlib)
python -m venv .venv
# Windows:
#   .venv\Scripts\activate
# macOS/Linux:
#   source .venv/bin/activate

# Only needed to run the test suite:
pip install pytest
```

**Python 3.9+** is required. The detector (`src/core/`) and CLI
(`src/cli.py`) run on the standard library alone - there is **no runtime
dependency**. `pytest` is dev-only, for the test suite.

## Running tests

```bash
# all tests
pytest

# with coverage (target >= 80%)
pytest --cov=src --cov-report=term-missing

# a single module
pytest tests/test_engine.py -v
```

Before submitting, make sure:
- all tests pass;
- coverage stays at or above 80% (new public logic needs matching tests);
- `pytest -W error::SyntaxWarning` reports no warnings.

## Code style

- **PEP 8**: line width recommended <= 88; use `black` (optional) to keep
  the style consistent.
- **Type hints + docstrings**: every public function/method must have type
  hints and a docstring; private helpers are encouraged to have them too.
- **Pure standard library**: keep the detector dependency-free. If a feature
  genuinely needs a third-party package, gate it behind an optional flag and
  keep the core path on stdlib - do not add a hard runtime requirement.
- **Single responsibility**: each module does one thing; see the module
  docstrings at the top of each file in `src/core/` for the split
  (patterns / hard-bans / sound / engine / CLI).

## Pattern library changes

The Chinese lexical table lives in `src/core/patterns_zh.py`
(`HEAD` / `BODY` / `TAIL`, with head/tail position weighting and repeat
decay); the English table lives in `src/core/patterns_en.py`. When you add
or tune a pattern, **be sure** to update in the same commit:

1. the matching entry in `references/ai-patterns-zh.md` or
   `references/ai-patterns-en.md` (so the human-readable library and the
   executable table stay in sync);
2. the scoring / priority notes in `references/scoring-rubric.md` if the
   penalty or priority order changed;
3. test cases in `tests/test_engine.py` (and `tests/test_hard_bans.py` for
   hard-bans).

Two invariants must never be broken:

- **The engine detects and quantifies; it never rewrites.** Keep the engine
  side-effect-free - it must not modify the input text or write files.
- **The two score scales point opposite ways.** The Chinese 0-100 *human
  index* (higher = more human) and the English *AI-taste* score
  (higher = more AI) must not be mixed; the >=85 shipping gate applies to
  Chinese prose only.

`tests/test_engine.py` pins these down; if you change the model, change
those tests in the same commit.

## Documentation contract

`tests/test_skill_docs.py` locks the README template structure (section
order mirroring the reference skill), the three-way version agreement, the
CRLF changelog, and the CJK-free invariant on `README.md` (Chinese content
belongs in `README_zh.md` only). After any README change, run that file and
keep it green - do not loosen a contract test to make a content edit pass.

## Commit and PR workflow

1. Branch from `main`: `git checkout -b feat/your-feature`.
2. Small commits, imperative commit messages (`add: head-weighting for the
   opening-cliché pattern`).
3. Run `pytest --cov=src` locally and make sure everything is green.
4. Open the PR; the description states: what changed / why / how it was
   verified (paste coverage).
5. Merged after at least one maintainer review.

## Reporting issues

- Use the [Issue template]: reproduction steps, expected behavior, actual
  behavior, environment (Python version, OS).
- For "a clean piece was wrongly blocked" reports, attach the draft and the
  generated report so the pattern can be inspected for a false positive.

## Code signing

Sign the CLA (if any) before submitting a PR. We use a lightweight DCO
substitute: append `Signed-off-by: Your Name <you@example.com>` to the
final commit (`git commit -s`).
