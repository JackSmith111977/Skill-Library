"""工作流规则 2: 编排步骤完整性校验"""

import re
from ..models import LintError


# 匹配步骤编号：Step 1:, Step 2:, 步骤 1:, ## Step 1 等
STEP_PATTERN = re.compile(r"(?:Step|步骤)\s*(\d+)", re.IGNORECASE)


def check_steps_complete(body: str) -> list[LintError]:
    """校验 Pipeline 步骤序号连续性。

    要求从 1 开始，序号连续无间隔。
    """
    errors = []

    steps = [int(m.group(1)) for m in STEP_PATTERN.finditer(body)]
    if not steps:
        return errors

    steps_sorted = sorted(set(steps))

    # 检查是否从 1 开始
    if steps_sorted[0] != 1:
        errors.append(LintError(
            rule="workflow-steps",
            message=f"步骤序号应从 1 开始，实际从 {steps_sorted[0]} 开始",
        ))

    # 检查连续性
    for i in range(1, len(steps_sorted)):
        expected = steps_sorted[i - 1] + 1
        if steps_sorted[i] != expected:
            errors.append(LintError(
                rule="workflow-steps",
                message=f"步骤序号不连续: {steps_sorted[i-1]} → {steps_sorted[i]}，缺少 {expected}",
            ))

    return errors
