"""Rule 1: name 格式校验"""

import re
from ..models import LintError

# 单字符：仅小写字母；多字符：小写字母开头，中间可含数字和连字符，小写字母或数字结尾
NAME_PATTERN = re.compile(r"^[a-z]([a-z0-9-]*[a-z0-9])?$")


def check_name_format(name: str, dir_name: str) -> list[LintError]:
    """校验 skill name 格式"""
    errors = []

    if not name:
        errors.append(LintError(rule="name-format", message="name 不能为空"))
        return errors

    if len(name) > 64:
        errors.append(LintError(rule="name-format", message=f"name 长度 {len(name)} 超过 64 字符"))

    # 先检查连续连字符（正则可能匹配但规则不允许）
    if "--" in name:
        errors.append(LintError(rule="name-format", message="name 不能包含连续连字符"))
    elif not NAME_PATTERN.match(name):
        if name.startswith("-"):
            errors.append(LintError(rule="name-format", message="name 不能以连字符开头"))
        elif name.endswith("-"):
            errors.append(LintError(rule="name-format", message="name 不能以连字符结尾"))
        elif not re.match(r"^[a-z]", name):
            errors.append(LintError(rule="name-format", message="name 必须以小写字母开头"))
        else:
            errors.append(LintError(rule="name-format", message="name 格式无效，仅允许小写字母、数字和连字符"))

    if name != dir_name:
        errors.append(LintError(
            rule="name-format",
            message=f"name '{name}' 与目录名 '{dir_name}' 不一致",
        ))

    return errors
