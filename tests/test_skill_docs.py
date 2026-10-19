"""Documentation contract for the ai-trace-remover skill.

Locks the template structure (README mirrors task-organizer's section order),
the version three-way, the CRLF changelog, and the zero-CJK invariant on
README.md.
"""
from __future__ import annotations

import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_DIR / "SKILL.md"
README_MD = SKILL_DIR / "README.md"
README_ZH_MD = SKILL_DIR / "README_zh.md"
CHANGELOG_MD = SKILL_DIR / "CHANGELOG.md"


def _fm(text: str, key: str) -> str | None:
    m = re.search(rf"^\s{{0,2}}{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip().strip('"') if m else None


def _has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


# --- version & metadata ---------------------------------------------------


def test_version_consistency() -> None:
    from src import __version__

    assert _fm(SKILL_MD.read_text(encoding="utf-8"), "version") == __version__
    assert __version__ == "1.0.0"


def test_skill_frontmatter_name() -> None:
    assert _fm(SKILL_MD.read_text(encoding="utf-8"), "name") == "ai-trace-remover"


def test_skill_frontmatter_entry_point() -> None:
    assert _fm(SKILL_MD.read_text(encoding="utf-8"), "entry_point") == "python -m src.cli"


def test_skill_has_license_and_author() -> None:
    text = SKILL_MD.read_text(encoding="utf-8")
    assert _fm(text, "license") == "MIT"
    assert _fm(text, "author") == "Jiaming Shi"


# --- template structure (mirrors task-organizer) -------------------------

EN_SECTIONS = [
    "## Design principles & core features",
    "## Download and install",
    "## Quick start",
    "## Tests & coverage",
    "## Project layout",
    "## Using as an agent skill",
    "## License",
    "## Report issues",
]

ZH_SECTIONS = [
    "## 设计原则与核心特征",
    "## 下载与安装",
    "## 快速开始",
    "## 测试与覆盖率",
    "## 项目结构",
    "## 作为 Agent 技能挂载使用",
    "## 开源协议",
    "## 报告问题与反馈",
]


def test_readme_has_template_sections_in_order() -> None:
    text = README_MD.read_text(encoding="utf-8")
    positions = []
    for sec in EN_SECTIONS:
        pos = text.find(sec)
        assert pos != -1, f"README.md missing section {sec!r}"
        positions.append(pos)
    assert positions == sorted(positions), "README.md sections out of order"


def test_readme_zh_has_template_sections_in_order() -> None:
    text = README_ZH_MD.read_text(encoding="utf-8")
    positions = []
    for sec in ZH_SECTIONS:
        pos = text.find(sec)
        assert pos != -1, f"README_zh.md missing section {sec!r}"
        positions.append(pos)
    assert positions == sorted(positions), "README_zh.md sections out of order"


def test_readme_carries_bilingual_nav_link() -> None:
    text = README_MD.read_text(encoding="utf-8")
    assert "[中文说明](README_zh.md)" in text, "README must carry the bilingual nav link"


def test_readme_zh_carries_bilingual_nav_link() -> None:
    text = README_ZH_MD.read_text(encoding="utf-8")
    assert "[English](README.md)" in text, "README_zh must carry the English nav link"


# --- CJK / language invariants --------------------------------------------


def test_readme_md_is_pure_english() -> None:
    text = README_MD.read_text(encoding="utf-8")
    body = text.replace("[中文说明](README_zh.md)", "")
    cjk = [ch for ch in body if "\u4e00" <= ch <= "\u9fff"]
    assert not cjk, f"README.md contains CJK: {cjk[:5]}"


def test_readme_zh_has_chinese_content() -> None:
    assert _has_cjk(README_ZH_MD.read_text(encoding="utf-8"))


# --- changelog ------------------------------------------------------------


def test_changelog_is_crlf() -> None:
    raw = CHANGELOG_MD.read_bytes()
    assert b"\n" not in raw.replace(b"\r\n", b""), "CHANGELOG.md must be CRLF"
    assert b"\r\n" in raw


def test_changelog_has_version_entry() -> None:
    assert "## [1.0.0]" in CHANGELOG_MD.read_text(encoding="utf-8")


def test_citation_cff_matches_version() -> None:
    cff = SKILL_DIR / "CITATION.cff"
    if cff.exists():
        m = re.search(r"^\s*version:\s*(.+)$", cff.read_text(encoding="utf-8"), re.MULTILINE)
        assert m, "CITATION.cff must carry a version field"
        assert m.group(1).strip() == "1.0.0"


# --- required files --------------------------------------------------------


def test_required_files_present() -> None:
    for name in (
        "SKILL.md", "README.md", "README_zh.md", "LICENSE",
        "CHANGELOG.md", "CITATION.cff", "pyproject.toml", "requirements.txt",
    ):
        assert (SKILL_DIR / name).exists(), f"missing required file {name}"
    for name in ("engine.py", "patterns_zh.py", "patterns_en.py",
                 "hard_bans.py", "sound_rules.py"):
        assert (SKILL_DIR / "src" / "core" / name).exists(), f"missing {name}"
    assert (SKILL_DIR / "src" / "cli.py").exists()
