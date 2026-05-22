"""L1 元数据加载器"""

from pathlib import Path
from typing import Any

from ..registry.parser import parse_skill_md


def load_metadata(skill_path: str | Path) -> dict[str, Any]:
    """加载 skill 元数据（name + description），body 不加载。

    返回格式：
    {
        "name": "skill-name",
        "description": "...",
        "version": "0.1.0",
    }
    """
    meta = parse_skill_md(skill_path)
    return {
        "name": meta.get("name", ""),
        "description": meta.get("description", ""),
        "version": meta.get("version", "0.0.0"),
    }
