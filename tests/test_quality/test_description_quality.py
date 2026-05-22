"""E12: Description 质量评估测试"""

import pytest

from skill_library.quality.description_quality import (
    TriggerExtractor,
    CoverageAssessor,
    ThirdPersonDetector,
    SuggestionGenerator,
    assess_description,
)


class TestTriggerExtractor:
    """E12-S1: 触发词提取器"""

    def test_extract_quoted(self):
        desc = 'Use when user asks to "create skill", "lint skill"'
        triggers = TriggerExtractor.extract(desc)
        assert "create skill" in triggers
        assert "lint skill" in triggers

    def test_extract_single_quote(self):
        desc = "Use for 'mount' and 'unmount' operations"
        triggers = TriggerExtractor.extract(desc)
        assert "mount" in triggers
        assert "unmount" in triggers

    def test_extract_empty(self):
        assert TriggerExtractor.extract("") == []

    def test_extract_no_quotes(self):
        assert TriggerExtractor.extract("just plain text") == []


class TestCoverageAssessor:
    """E12-S2: 覆盖率评估"""

    def test_empty_returns_zero(self):
        assert CoverageAssessor.assess("", []) == 0

    def test_no_triggers_zero(self):
        assert CoverageAssessor.assess("no quotes here", []) == 0

    def test_one_trigger(self):
        score = CoverageAssessor.assess("do \"this\"", ["this"])
        assert 0 < score <= 60

    def test_three_triggers_minimum(self):
        score = CoverageAssessor.assess("a b c", ["a", "b", "c"])
        assert score >= 60

    def test_six_triggers_ideal(self):
        score = CoverageAssessor.assess("a b c d e f", list("abcdef"))
        assert score >= 90

    def test_many_triggers_capped(self):
        score = CoverageAssessor.assess("a b c d e f g h i j", list("abcdefghij"))
        assert score == 100


class TestThirdPersonDetector:
    """E12-S3: 第三人称检测"""

    def test_detects_third_person(self):
        opening, verb = ThirdPersonDetector.check(
            "This skill should be used when the user creates a skill."
        )
        assert opening
        assert verb

    def test_no_third_person(self):
        opening, verb = ThirdPersonDetector.check("Use this for creating skills.")
        assert not opening
        # "creating" is not third-person singular verb
        assert not verb

    def test_alternative_opening(self):
        opening, _ = ThirdPersonDetector.check(
            "This skill is triggered when the user asks to manage skills."
        )
        assert opening

    def test_empty_string(self):
        opening, verb = ThirdPersonDetector.check("")
        assert not opening
        assert not verb


class TestSuggestionGenerator:
    """E12-S4: 优化建议"""

    def test_empty_description(self):
        report = assess_description("")
        assert any("为空" in s for s in report.suggestions)

    def test_no_triggers(self):
        report = assess_description("This skill should be used when needed.")
        assert any("触发" in s for s in report.suggestions)

    def test_good_description(self):
        report = assess_description(
            'This skill should be used when the user asks to "create a skill", '
            '"lint a skill", "mount a skill", "unmount a skill", "register" or "list" skills.'
        )
        assert any("良好" in s for s in report.suggestions)

    def test_too_short(self):
        report = assess_description("short desc")
        assert any("过短" in s for s in report.suggestions)


class TestAssessDescription:
    """综合评估"""

    def test_assess_good_description(self):
        report = assess_description(
            'This skill should be used when the user asks to "create a skill", '
            '"lint a skill", "mount a skill", "unmount a skill", '
            '"register" or "list" skills, or "manage" the library.'
        )
        assert report.score >= 60
        assert report.passed
        assert report.trigger_count >= 6
        assert report.has_third_person

    def test_assess_poor_description(self):
        report = assess_description("do stuff")
        assert report.score < 60
        assert not report.passed
        assert report.trigger_count == 0

    def test_assess_empty(self):
        report = assess_description("")
        assert report.score == 0
        assert not report.passed

    def test_to_dict(self):
        report = assess_description(
            'This skill manages "skills".'
        )
        d = report.to_dict()
        assert d["score"] == report.score
        assert d["passed"] == report.passed
        assert d["triggers"] == report.triggers
