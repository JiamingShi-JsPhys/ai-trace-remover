"""CLI tests: exit codes, rendering, JSON, --score-only, stdin."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_ROOT = Path(__file__).resolve().parents[1]

ZH_GOOD = (
    "去年我们给客服系统接了个大模型，第一周误判率从 40% 降到 9%。"
    "我不确定能不能压到 5%，但打算把纠错数据回灌进微调。"
)
ZH_BAD = (
    "在当今社会，AI 技术日益发展。我们高度重视并深入推进，赋能全链路闭环。"
    "让我们共同谱写新篇章，以上就是全部内容。"
)


def _run_cli(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "src.cli", *args],
        cwd=str(SKILL_ROOT),
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


@pytest.fixture
def good_file(tmp_path: Path) -> Path:
    p = tmp_path / "good.md"
    p.write_text(ZH_GOOD, encoding="utf-8")
    return p


@pytest.fixture
def bad_file(tmp_path: Path) -> Path:
    p = tmp_path / "bad.md"
    p.write_text(ZH_BAD, encoding="utf-8")
    return p


def test_version_flag() -> None:
    proc = _run_cli("--version")
    assert proc.returncode == 0
    assert "1.0.0" in proc.stdout


def test_good_exits_zero(good_file: Path) -> None:
    proc = _run_cli(str(good_file))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_bad_exits_one(bad_file: Path) -> None:
    proc = _run_cli(str(bad_file))
    assert proc.returncode == 1, proc.stdout + proc.stderr


def test_missing_file_exits_two(tmp_path: Path) -> None:
    proc = _run_cli(str(tmp_path / "nope.md"))
    assert proc.returncode == 2


def test_stdin_score_only() -> None:
    proc = _run_cli("-", "--score-only", stdin=ZH_GOOD)
    assert proc.returncode in (0, 1)
    out = proc.stdout.strip()
    assert "/100" in out, out


def test_score_only_shows_human_index() -> None:
    proc = _run_cli("-", "--score-only", stdin=ZH_BAD)
    # bad draft: cannot ship
    assert "can_ship=no" in proc.stdout, proc.stdout


def test_markdown_render_contains_sections(good_file: Path) -> None:
    proc = _run_cli(str(good_file))
    body = proc.stdout
    assert "AI 痕迹检测报告" in body
    assert "人话指数" in body
    assert "硬禁项" in body


def test_json_render_is_valid(good_file: Path) -> None:
    proc = _run_cli(str(good_file), "--json")
    data = json.loads(proc.stdout)
    assert data["source"] == str(good_file)
    assert data["language"] in ("zh", "mixed")
    assert isinstance(data["hits"], list)
    assert "hard_failures" in data
    assert "can_ship" in data


def test_output_flag_writes_file(good_file: Path, tmp_path: Path) -> None:
    out = tmp_path / "report.md"
    proc = _run_cli(str(good_file), "-o", str(out))
    assert proc.returncode == 0
    assert out.exists()
    assert "AI 痕迹检测报告" in out.read_text(encoding="utf-8")


def test_json_hits_have_contract_keys(good_file: Path) -> None:
    proc = _run_cli(str(good_file), "--json")
    data = json.loads(proc.stdout)
    if data["hits"]:
        h = data["hits"][0]
        for key in ("code", "name", "line", "column", "severity", "penalty", "text"):
            assert key in h, f"hit missing {key}"
