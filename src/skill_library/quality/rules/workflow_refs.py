"""工作流规则 1: 引用原子 skill 存在性校验"""

import re
from pathlib import Path
from ..models import LintError


# 匹配引用的 skill 名称模式：Step N: @skill-name 或 引用 skill-name
REF_PATTERN = re.compile(r"(?:@|引用\s*)([a-z][a-z0-9-]*[a-z0-9]|[a-z])")


def check_workflow_refs(skill_path: Path, body: str, skills_root: Path | None = None) -> list[LintError]:
    """校验工作流引用的 skill 是否存在。

    skill_path: 工作流 skill 目录
    body: SKILL.md body
    skills_root: skill 仓库根目录（默认为 skill_path 的父目录的父目录）
    """
    errors = []

    if skills_root is None:
        # 尝试推断：workflow-skill 在 skills/<pack>/<workflow>/ 下
        skills_root = skill_path.parent.parent

    refs = REF_PATTERN.findall(body)
    for ref_name in set(refs):
        ref_path = skills_root / ref_name
        if not ref_path.is_dir():
            errors.append(LintError(
                rule="workflow-ref-exists",
                message=f"引用的 skill 不存在: {ref_name}",
            ))

    return errors
