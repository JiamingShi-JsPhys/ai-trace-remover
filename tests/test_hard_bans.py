"""Hard-ban rules: blocking failures, and the human-judge warnings."""
from __future__ import annotations

from src.core import hard_bans, scan


def test_em_dash_blocks_zh() -> None:
    rep = scan("这是一个重要决定——不可更改。我们认真做了。", "dash")
    assert any("HB1" in f for f in rep.hard_failures), rep.hard_failures


def test_marketing_jargon_blocks() -> None:
    rep = scan("我们打造一站式全链路解决方案，赋能业务增长。", "jargon")
    assert any("HB5" in f for f in rep.hard_failures), rep.hard_failures


def test_reversal_rhetoric_blocks() -> None:
    rep = scan("这不是技术的问题，而是人的问题。", "reversal")
    assert any("HB6" in f for f in rep.hard_failures), rep.hard_failures


def test_inflated_ending_blocks() -> None:
    rep = scan("让我们共同谱写新篇章，未来可期。", "ending")
    assert any("HB7" in f for f in rep.hard_failures), rep.hard_failures


def test_template_coda_blocks() -> None:
    rep = scan("以上就是全部内容，希望本文对您有所帮助。", "coda")
    assert any("HB9" in f for f in rep.hard_failures), rep.hard_failures


def test_clean_zh_no_blocking_bans() -> None:
    text = "去年我们把加载从 3 秒压到 800 毫秒，客服误判率也降了不少。"
    rep = scan(text, "clean")
    assert rep.hard_failures == []


def test_prompt_colon_is_warning_not_blocking() -> None:
    # HB2 (prompt-style colon) is context-dependent -> warning, not failure
    rep = scan("一句话总结：这件事其实没那么复杂。", "colon")
    assert rep.hard_failures == []
    assert any("HB2" in w for w in rep.warnings), rep.warnings


def test_english_residue_blocks() -> None:
    text = "I hope this helps! Let me know if you'd like more detail."
    rep = scan(text, "en-residue")
    assert any("HB11" in f for f in rep.hard_failures), rep.hard_failures


def test_english_cutoff_disclaimer_blocks() -> None:
    text = "As of my last training update, this API is not available."
    rep = scan(text, "en-cutoff")
    assert any("HB12" in f for f in rep.hard_failures), rep.hard_failures


def test_english_sycophancy_blocks() -> None:
    text = "Great question! You're absolutely right that this is complex."
    rep = scan(text, "en-syc")
    assert any("HB13" in f for f in rep.hard_failures), rep.hard_failures


def test_decorative_emoji_blocks() -> None:
    text = "本周要点🚀💡✅⭐ 都整理好了。"
    rep = scan(text, "emoji")
    assert any("HB14" in f for f in rep.hard_failures), rep.hard_failures


def test_clean_prose_no_blocking_bans() -> None:
    text = "本周例会把排期定了下来，周一先出接口文档。"
    rep = scan(text, "prose")
    assert rep.hard_failures == []


def test_clean_english_no_blocking_bans() -> None:
    text = ("The 40-hour battery held through a cold morning in our logged "
            "field test, though I am not sure it will survive a week.")
    rep = scan(text, "en-clean")
    assert rep.hard_failures == []


def test_blocking_codes_are_a_subset() -> None:
    """Every blocking code referenced in the engine must exist in the table."""
    blocking = {"HB1", "HB5", "HB6", "HB7", "HB9", "HB11", "HB12", "HB13", "HB14"}
    all_codes = {hb.code for hb in hard_bans.HARD_BANS}
    assert blocking.issubset(all_codes)
