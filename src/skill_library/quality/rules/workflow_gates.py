"""工作流规则 3: 硬性门控标记校验"""

import re
from ..models import LintWarning


# 检测 Inversion 设计模式的标记
INVERSION_PATTERN = re.compile(r"(?:inversion|Inversion|INVERSION|门控|STAGE_GATE|gate)", re.IGNORECASE)
GATE_PATTERN = re.compile(r"STAGE_GATE|HALT|硬性门控", re.IGNORECASE)


def check_gate_markers(body: str, design_pattern: str = "") -> list[LintWarning]:
    """校验 Inversion 工作流是否包含门控标记。

    非 Inversion 模式跳过检查。
    """
    warnings = []

    # 仅对 Inversion 模式检查
    if design_pattern and design_pattern != "inversion":
        return warnings

    # 如果 body 中提到 inversion 关键词但没有门控标记
    if INVERSION_PATTERN.search(body) and not GATE_PATTERN.search(body):
        warnings.append(LintWarning(
            rule="workflow-gates",
            message="Inversion 工作流建议包含 STAGE_GATE 门控标记",
        ))

    return warnings
