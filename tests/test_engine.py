"""Engine tests: Chinese / English / mixed scanning, scoring, hard-bans, sound."""
from __future__ import annotations

from src.core import scan, grade_zh, grade_en

ZH_BAD = (
    "在当今社会，人工智能技术日益发展，众所周知已经渗透到各行各业。"
    "我们高度重视用户体验，深入推进产品优化，全方位提升服务质量。"
    "专家指出，AI 在医疗领域具有广阔的应用前景。"
    "这一举措不仅提升了效率，也彰显了行业创新的活力，更展示了企业的深厚底蕴。"
    "让我们共同期待，在数字化转型的道路上不断前行，谱写新篇章。"
    "希望本文能够对您有所帮助，以上就是全部内容。"
)

ZH_GOOD = (
    "去年我们给客服系统接了个大模型，第一周误判率高得离谱。"
    "问题出在 prompt 里没给例子，模型靠猜。补上 20 条真实对话样本后，"
    "误判率从 40% 降到 9%。我不确定能不能压到 5%，但打算试把纠错数据"
    "回灌进微调。"
)

EN_BAD = (
    "Our flagship device stands as a testament to our commitment to innovation. "
    "It boasts a vibrant display, showcasing how technology can truly transform "
    "the way we live. It marks a pivotal moment in the evolving landscape. "
    "I hope this helps! Let me know if you'd like me to expand on any section. "
    "As of my last training update, the future looks bright."
)

EN_GOOD = (
    "The 40-hour battery was the spec we pushed hardest on. After the first "
    "prototype drained in six hours, the firmware team rewrote the power "
    "model. I'm not sure it will hold on a cold morning, but we verified it "
    "with a week of logged usage before shipping."
)


# --- language detection ---------------------------------------------------


def test_detect_chinese() -> None:
    assert scan(ZH_BAD, "zh").language in ("zh", "mixed")


def test_detect_english() -> None:
    assert scan(EN_GOOD, "en").language == "en"


# --- Chinese scoring ------------------------------------------------------


def test_zh_bad_scores_low() -> None:
    rep = scan(ZH_BAD, "zh-bad")
    assert rep.language in ("zh", "mixed")
    assert rep.score is not None
    assert rep.score < 50, f"expected low score, got {rep.score}"


def test_zh_good_scores_high() -> None:
    rep = scan(ZH_GOOD, "zh-good")
    assert rep.score is not None
    assert rep.score >= 70, f"expected >=70, got {rep.score}"


def test_zh_good_has_no_hard_bans() -> None:
    rep = scan(ZH_GOOD, "zh-good")
    assert rep.hard_failures == []


def test_zh_bad_has_hard_bans() -> None:
    rep = scan(ZH_BAD, "zh-bad")
    assert len(rep.hard_failures) >= 1


def test_zh_good_can_ship() -> None:
    rep = scan(ZH_GOOD, "zh-good")
    assert rep.can_ship() is True, f"hard_bans={rep.hard_failures} score={rep.score}"


def test_zh_bad_cannot_ship() -> None:
    rep = scan(ZH_BAD, "zh-bad")
    assert rep.can_ship() is False


def test_zh_hits_carry_line_and_code() -> None:
    rep = scan(ZH_BAD, "zh-bad")
    assert rep.hits, "expected lexical hits on a bad draft"
    for h in rep.hits:
        assert h.line >= 1
        assert h.code.startswith("A")
        assert h.penalty > 0


def test_zh_suggestions_present() -> None:
    rep = scan(ZH_BAD, "zh-bad")
    assert rep.suggestions, "a bad draft must yield at least one suggestion"


# --- English scoring ------------------------------------------------------


def test_en_bad_high_ai_taste() -> None:
    rep = scan(EN_BAD, "en-bad")
    assert rep.language == "en"
    assert rep.ai_taste_score is not None
    assert rep.ai_taste_score > 40, f"expected high AI-taste, got {rep.ai_taste_score}"
    # English has no human-index gate
    assert rep.score is None


def test_en_good_low_ai_taste() -> None:
    rep = scan(EN_GOOD, "en-good")
    assert rep.ai_taste_score is not None
    assert rep.ai_taste_score < 40, f"expected low AI-taste, got {rep.ai_taste_score}"


def test_en_bad_has_hard_bans() -> None:
    rep = scan(EN_BAD, "en-bad")
    # "I hope this helps" / "Let me know" / cutoff disclaimer are blocking
    assert len(rep.hard_failures) >= 1


def test_en_good_can_ship() -> None:
    rep = scan(EN_GOOD, "en-good")
    assert rep.can_ship() is True, f"hard_bans={rep.hard_failures}"


# --- sound rules ----------------------------------------------------------


def test_zh_sound_checks_present() -> None:
    rep = scan(ZH_GOOD, "zh-good")
    assert set(rep.sound.keys()) >= {"S1", "S2", "S3", "S4", "S5"}
    # ZH_GOOD has numbers -> S1 should pass
    assert rep.sound["S1"]["pass"] is True
    # ZH_GOOD has "我不确定" -> S3 should pass
    assert rep.sound["S3"]["pass"] is True


def test_zh_bad_lacks_sound() -> None:
    rep = scan(ZH_BAD, "zh-bad")
    # The bad draft has no digits -> S1 fails
    assert rep.sound["S1"]["pass"] is False


def test_en_sound_empty() -> None:
    rep = scan(EN_GOOD, "en-good")
    assert rep.sound == {}


# --- grades ----------------------------------------------------------------


def test_grade_zh_boundaries() -> None:
    assert grade_zh(100) == ("人话", "")
    assert grade_zh(85) == ("人话", "")
    assert grade_zh(70) == ("微 AI 味", "")
    assert grade_zh(50) == ("中度 AI 味", "")
    assert grade_zh(30) == ("重度 AI 味", "")
    assert grade_zh(0) == ("完全 AI 体", "")


def test_grade_en_boundaries() -> None:
    assert grade_en(0)[0] == "接近人话"
    assert grade_en(19)[0] == "接近人话"
    assert grade_en(44)[0] == "微 AI 味"
    assert grade_en(69)[0] == "中度 AI 味"
    assert grade_en(100)[0] == "重度 AI 味"


# --- empty / edge ---------------------------------------------------------


def test_empty_text() -> None:
    rep = scan("", "empty")
    assert rep.language == "en"
    assert rep.hits == []
    assert rep.hard_failures == []


def test_single_ascii_char() -> None:
    rep = scan("x", "one")
    assert rep.language == "en"
    assert rep.score is None
