"""Rule 5: 文件引用有效性校验"""

import re
from pathlib import Path
from ..models import LintError

REFERENCE_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def check_references(skill_path: Path, body: str) -> list[LintError]:
    """校验 SKILL.md 中引用的文件是否存在"""
    errors = []

    for match in REFERENCE_PATTERN.finditer(body):
        text, ref_path = match.group(1), match.group(2)

        # 跳过 URL
        if ref_path.startswith(("http://", "https://", "mailto:")):
            continue

        # 解析相对路径
        full_path = skill_path / ref_path
        if not full_path.exists():
            errors.append(LintError(
                rule="references",
                message=f"引用的文件不存在: {ref_path}",
            ))

    return errors
