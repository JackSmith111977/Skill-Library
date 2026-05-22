"""Rule 2+3: description 校验"""

import re
from ..models import LintError, LintWarning

TRIGGER_PATTERN = re.compile(r"['\"][^'\"]+['\"]")
THIRD_PERSON_PATTERN = re.compile(r"This skill should be used when", re.IGNORECASE)
GENERIC_KEYWORD_PATTERN = re.compile(r"(when|used for|purpose|trigger)", re.IGNORECASE)


def check_description(description: str, frontmatter: dict | None = None, profile: str = "skill-library") -> tuple[list[LintError], list[LintWarning]]:
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

    if profile == "claude-code":
        # claude-code: 检查 triggers 字段，跳过第三人称
        triggers = (frontmatter or {}).get("triggers", [])
        if not triggers:
            warnings.append(LintWarning(
                rule="description-triggers",
                message="claude-code profile 下建议设置 triggers 字段",
            ))
    elif profile == "generic":
        # generic: 基础关键词检测，跳过引号和第三人称
        if not GENERIC_KEYWORD_PATTERN.search(description):
            warnings.append(LintWarning(
                rule="description-triggers",
                message="description 建议包含触发关键词（when/used for 等）",
            ))
    else:
        # skill-library（默认）: 引号内触发短语 + 第三人称
        triggers = TRIGGER_PATTERN.findall(description)
        if not triggers:
            warnings.append(LintWarning(
                rule="description-triggers",
                message="description 中未检测到引号内的触发短语",
            ))

        if not THIRD_PERSON_PATTERN.search(description):
            warnings.append(LintWarning(
                rule="description-third-person",
                message="description 建议使用第三人称：'This skill should be used when...'",
            ))

    return errors, warnings
