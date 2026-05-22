"""Rule 6: allowed-tools 格式校验"""

from ..models import LintError


def check_allowed_tools(allowed_tools: str | list | None) -> list[LintError]:
    """校验 allowed-tools 格式"""
    errors = []

    if allowed_tools is None:
        return errors

    # 支持字符串和列表格式
    if isinstance(allowed_tools, str):
        if not allowed_tools:
            return errors
        tools = allowed_tools.split()
    elif isinstance(allowed_tools, list):
        tools = allowed_tools
    else:
        errors.append(LintError(
            rule="allowed-tools",
            message="allowed-tools 格式无效，应为空格分隔的字符串或列表",
        ))
        return errors

    # 检查每个工具名
    for tool in tools:
        if not tool:
            errors.append(LintError(
                rule="allowed-tools",
                message="allowed-tools 包含空的工具名",
            ))
        elif " " in tool:
            errors.append(LintError(
                rule="allowed-tools",
                message=f"工具名 '{tool}' 包含空格",
            ))

    # 检查连续空格（字符串格式）
    if isinstance(allowed_tools, str) and "  " in allowed_tools:
        errors.append(LintError(
            rule="allowed-tools",
            message="allowed-tools 包含连续空格",
        ))

    return errors
