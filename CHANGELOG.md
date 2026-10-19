# Changelog

All notable changes to this skill are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-10-19

First public release of ai-trace-remover: a universal de-AI-flavour skill
that makes Chinese and English prose read as if a specific person wrote it.
Pattern categories are original; before/after examples are self-authored and
built from public-domain teaching texts and classic public-domain fiction.
No upstream skill code is copied.

### Added

- A pure standard-library scanner (`src/core/engine.py`) with no network and
  no third-party dependency; it detects, quantifies, and reports - it never
  rewrites.
- An original Chinese lexical pattern library (`src/core/patterns_zh.py`,
  A1-A13 with head/tail position weighting and repeat decay) and an English
  pattern library (`src/core/patterns_en.py`, E1-E24, original category
  design with self-authored before/after examples built from public-domain
  teaching texts and classic public-domain fiction).
- A 0-100 human index for Chinese prose (higher = more human) and an
  opposite-direction AI-taste score for English prose (higher = more AI).
- Blocking "hard-ban" rules (`src/core/hard_bans.py`): em-dash, prompt-style
  colons, reversal rhetoric, marketing jargon, inflated endings, English
  chat-residue / sycophancy / cutoff disclaimers, and decorative emoji (HB14).
  Any hit blocks shipping.
- The quantifiable subset of the five "sound of a person" checks
  (`src/core/sound_rules.py`): concrete numbers, concrete nouns,
  uncertainty, speaker presence, and a reference-only rhythm ratio.
- Two voice registers as hard constraints: in chat, speak like a friend
  (calm, a little warmth); in a file deliverable, stay cool and restrained.
  The output carries no emoji at all.
- Three Chinese trace classes in the word-surface library: literature /
  cyber tells (A11), lexical collapse (A12), and social-register tics (A13).
- A CLI (`src/cli.py`): `python -m src.cli <file|-> [--json] [-o out.md]
  [--score-only]`, with exit codes 0 (shippable) / 1 (not shippable) / 2
  (read/parse failure).
- Human-readable references: `ai-patterns-zh.md`, `ai-patterns-en.md`,
  `scoring-rubric.md`, `revision.md` (seven-pass + five checks + absolute
  banned-word table), and `example-diff.md` (four cross-lingual before/after
  scenes).

### Design

- **Detection is the tool; rewriting is the agent.** The engine makes the
  tells visible and measurable; the agent rewrites by hand following
  `references/`, preserving the author's voice instead of swapping one
  template for another.
- **Clean word-surface is not "has a person".** Deleting boilerplate
  without adding specifics only turns AI-ese into a press release; the
  five checks and the cold-read four questions exist to catch that.
- **Two opposite scales, never mixed.** Chinese and English score in
  opposite directions; the 0-100 shipping gate (>=85) applies to Chinese
  prose only.

### Not claimed

- No semantic, factual, or stylistic judgement: the scanner works on
  word-surface and light structure only. Whether a detail is real, whether
  a passage has a pulse, and whether the author's voice survived are
  manual checks on purpose.
- No automatic rewrite. The skill deliberately ships a detector plus
  reference material, not a rewriter.
