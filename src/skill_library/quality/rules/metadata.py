"""Rule 7: metadata 格式校验"""

import re
from ..models import LintWarning

SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def check_metadata(metadata: dict | None, profile: str = "skill-library") -> list[LintWarning]:
    """校验 metadata 格式"""
    warnings = []

    if metadata is None:
        return warnings

    if not isinstance(metadata, dict):
        warnings.append(LintWarning(
            rule="metadata",
            message="metadata 应为键值对映射",
        ))
        return warnings

    # 非 skill-library profile 跳过 metadata 字段检查
    if profile != "skill-library":
        return warnings

    # 检查 version 格式
    version = metadata.get("version")
    if version and not SEMVER_PATTERN.match(str(version)):
        warnings.append(LintWarning(
            rule="metadata-version",
            message=f"version '{version}' 不是语义化版本（应为 x.y.z）",
        ))

    return warnings
