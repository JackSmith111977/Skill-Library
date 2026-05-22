"""frontmatter 解析器：提取 SKILL.md 的结构化元数据"""

from pathlib import Path
from typing import Any

import yaml


def parse_skill_md(skill_path: str | Path) -> dict[str, Any]:
    """解析 SKILL.md，返回 frontmatter dict。

    缺失字段提供默认值：
    - name: ""
    - description: ""
    - version: "0.0.0"
    - allowed-tools: []
    - metadata: {}
    """
    skill_md = Path(skill_path) / "SKILL.md"
    if not skill_md.is_file():
        return _defaults()

    content = skill_md.read_text(encoding="utf-8")
    frontmatter, _ = _split_frontmatter(content)

    if not frontmatter:
        return _defaults()

    # 合并默认值
    result = _defaults()
    result.update(frontmatter)

    # 确保 allowed-tools 是列表
    at = result.get("allowed-tools")
    if isinstance(at, str):
        result["allowed-tools"] = [t.strip() for t in at.split() if t.strip()]
    elif not isinstance(at, list):
        result["allowed-tools"] = []

    # 确保 metadata 是 dict
    if not isinstance(result.get("metadata"), dict):
        result["metadata"] = {}

    return result


def _split_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """分离 YAML frontmatter 和 body"""
    if not content.startswith("---"):
        return {}, content

    try:
        end = content.index("---", 3)
        yaml_str = content[3:end].strip()
        body = content[end + 3:].strip()
        data = yaml.safe_load(yaml_str)
        if not isinstance(data, dict):
            return {}, body
        return data, body
    except (ValueError, yaml.YAMLError):
        return {}, content


def _defaults() -> dict[str, Any]:
    """默认字段值"""
    return {
        "name": "",
        "description": "",
        "version": "0.0.0",
        "allowed-tools": [],
        "metadata": {},
    }
