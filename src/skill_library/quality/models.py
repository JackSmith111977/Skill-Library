"""质量检测数据模型"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LintError:
    """ERROR 级别问题"""
    rule: str
    message: str
    line: int | None = None
    file: str | None = None


@dataclass
class LintWarning:
    """WARNING 级别问题"""
    rule: str
    message: str
    line: int | None = None
    file: str | None = None


@dataclass
class LintResult:
    """lint 检测结果"""
    passed: bool
    errors: list[LintError] = field(default_factory=list)
    warnings: list[LintWarning] = field(default_factory=list)
    score: int = 100

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "score": self.score,
            "errors": [{"rule": e.rule, "message": e.message} for e in self.errors],
            "warnings": [{"rule": w.rule, "message": w.message} for w in self.warnings],
        }
