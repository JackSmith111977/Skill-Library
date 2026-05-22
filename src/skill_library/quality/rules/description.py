"""Rule 2+3: description 校验"""

import re
from ..models import LintError, LintWarning

TRIGGER_PATTERN = re.compile(r"['\"][^'\"]+['\"]")
THIRD_PERSON_PATTERN = re.compile(r"This skill should be used when", re.IGNORECASE)


def check_description(description: str) -> tuple[list[LintError], list[LintWarning]]:
    """校验 description 长度和触发词"""
    errors = []
    warnings = []

    if not description:
        errors.append(LintError(rule="description", message="description 不能为空"))
        return errors, warnings

    if len(description) > 1024:
        errors.append(LintError(
            rule="description",
            message=f"description 长度 {len(description)} 超过 1024 字符",
        ))

    # 检测触发词（WARNING）
    triggers = TRIGGER_PATTERN.findall(description)
    if not triggers:
        warnings.append(LintWarning(
            rule="description-triggers",
            message="description 中未检测到引号内的触发短语",
        ))

    # 检测第三人称（WARNING）
    if not THIRD_PERSON_PATTERN.search(description):
        warnings.append(LintWarning(
            rule="description-third-person",
            message="description 建议使用第三人称：'This skill should be used when...'",
        ))

    return errors, warnings
