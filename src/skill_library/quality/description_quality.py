"""Description 质量评估"""

import re
from dataclasses import dataclass, field
from typing import Any

TRIGGER_PATTERN = re.compile(r"['\"]([^'\"]+)['\"]")
THIRD_PERSON_PATTERN = re.compile(
    r"^(This skill should be used|This skill is triggered|Use this skill when)", re.IGNORECASE
)
VERB_THIRD_PERSON = re.compile(
    r"\b(asks|creates|builds|runs|executes|manages|handles|processes|generates|"
    r"validates|checks|analyzes|extracts|transforms|loads|saves|updates|deletes|"
    r"searches|filters|sorts|merges|splits|converts|formats|parses|renders)\b",
    re.IGNORECASE,
)


@dataclass
class DescriptionReport:
    score: int = 0
    trigger_count: int = 0
    triggers: list[str] = field(default_factory=list)
    has_third_person: bool = False
    has_verb_third_person: bool = False
    length: int = 0
    suggestions: list[str] = field(default_factory=list)
    passed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "trigger_count": self.trigger_count,
            "triggers": self.triggers,
            "has_third_person": self.has_third_person,
            "has_verb_third_person": self.has_verb_third_person,
            "length": self.length,
            "suggestions": self.suggestions,
            "passed": self.passed,
        }


class TriggerExtractor:
    """E12-S1: 触发词提取器"""

    @staticmethod
    def extract(description: str) -> list[str]:
        """提取引号内的触发短语。"""
        return TRIGGER_PATTERN.findall(description)


class CoverageAssessor:
    """E12-S2: 覆盖率评估"""

    MIN_TRIGGERS = 3
    IDEAL_TRIGGERS = 6

    @staticmethod
    def assess(description: str, triggers: list[str]) -> int:
        """评估触发覆盖率，返回 0-100 分。

        评分规则：
        - 无触发词：0 分
        - < MIN_TRIGGERS: 按比例 0-60 分
        - MIN ~ IDEAL: 60-90 分
        - > IDEAL: 90-100 分
        - 空 description: 0 分
        """
        if not description or not description.strip():
            return 0

        count = len(triggers)
        if count == 0:
            return 0
        if count < CoverageAssessor.MIN_TRIGGERS:
            return int(60 * count / CoverageAssessor.MIN_TRIGGERS)
        if count <= CoverageAssessor.IDEAL_TRIGGERS:
            return 60 + int(30 * (count - CoverageAssessor.MIN_TRIGGERS) / (
                CoverageAssessor.IDEAL_TRIGGERS - CoverageAssessor.MIN_TRIGGERS
            ))
        return min(100, 90 + int(10 * (count - CoverageAssessor.IDEAL_TRIGGERS) / 3))


class ThirdPersonDetector:
    """E12-S3: 第三人称检测"""

    @staticmethod
    def check(description: str) -> tuple[bool, bool]:
        """检测 description 的第三人称使用。

        Returns:
            (has_third_person_opening, has_third_person_verb)
        """
        has_opening = bool(THIRD_PERSON_PATTERN.search(description))
        has_verb = bool(VERB_THIRD_PERSON.search(description))
        return has_opening, has_verb


class SuggestionGenerator:
    """E12-S4: Description 优化建议"""

    @staticmethod
    def generate(description: str, report: DescriptionReport) -> list[str]:
        """根据报告生成优化建议。"""
        suggestions = []

        if not description or not description.strip():
            suggestions.append("description 为空，请添加描述。")
            return suggestions

        if not report.has_third_person:
            suggestions.append(
                '建议以第三人称开头: "This skill should be used when..."'
            )
        if not report.has_verb_third_person:
            suggestions.append(
                "建议使用第三人称单数动词（如 creates、manages、handles）"
            )
        if report.trigger_count == 0:
            suggestions.append(
                "未检测到触发短语，请在引号内添加触发词（如 \"create a skill\"）。"
            )
        elif report.trigger_count < CoverageAssessor.MIN_TRIGGERS:
            suggestions.append(
                f"触发短语偏少（{report.trigger_count}个），建议至少添加至"
                f" {CoverageAssessor.MIN_TRIGGERS} 个。"
            )
        if len(description) > 1024:
            suggestions.append(
                f"description 过长（{len(description)}字符），建议控制在 1024 字符以内。"
            )
        if len(description) < 20:
            suggestions.append("description 过短，建议补充更多触发场景描述。")

        if not suggestions:
            suggestions.append("description 质量良好，无需优化。")

        return suggestions


def assess_description(description: str) -> DescriptionReport:
    """综合评估 description 质量，返回报告。"""
    report = DescriptionReport()
    report.length = len(description)

    # S1: 触发词提取
    extractor = TriggerExtractor()
    report.triggers = extractor.extract(description)
    report.trigger_count = len(report.triggers)

    # S2: 覆盖率
    assessor = CoverageAssessor()
    report.score = assessor.assess(description, report.triggers)

    # S3: 第三人称检测
    detector = ThirdPersonDetector()
    report.has_third_person, report.has_verb_third_person = detector.check(description)

    # S4: 优化建议
    gen = SuggestionGenerator()
    report.suggestions = gen.generate(description, report)

    report.passed = report.score >= 60
    return report
