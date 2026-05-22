"""工作流规则 4: 步骤依赖关系校验"""

import re
from ..models import LintError


# 匹配步骤依赖：Step N depends on Step M, 步骤 N 依赖步骤 M
DEP_PATTERN = re.compile(
    r"(?:Step|步骤)\s*(\d+)\s*(?:depends?\s*on|依赖|需要)\s*(?:Step|步骤)?\s*(\d+)",
    re.IGNORECASE,
)


def check_step_deps(body: str) -> list[LintError]:
    """校验步骤间无循环依赖。"""
    errors = []

    # 构建依赖图
    deps: dict[int, set[int]] = {}
    for m in DEP_PATTERN.finditer(body):
        step, dep = int(m.group(1)), int(m.group(2))
        deps.setdefault(step, set()).add(dep)

    if not deps:
        return errors

    # DFS 检测循环
    visited: set[int] = set()
    in_stack: set[int] = set()

    def has_cycle(node: int) -> bool:
        if node in in_stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        in_stack.add(node)
        for dep in deps.get(node, []):
            if has_cycle(dep):
                return True
        in_stack.discard(node)
        return False

    for step in deps:
        if step not in visited:
            if has_cycle(step):
                errors.append(LintError(
                    rule="workflow-deps",
                    message=f"检测到步骤循环依赖（涉及步骤 {step}）",
                ))
                break

    return errors
