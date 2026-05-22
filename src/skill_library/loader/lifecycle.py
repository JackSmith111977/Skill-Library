"""加载生命周期管理"""

from enum import Enum
from pathlib import Path
from typing import Any


class LoadLevel(Enum):
    L1 = "L1"  # 元数据
    L2 = "L2"  # 指令
    L3 = "L3"  # 资源


class LoadManager:
    """管理 skill 的加载生命周期"""

    def __init__(self):
        self._cache: dict[str, dict[str, Any]] = {}

    def load(self, skill_name: str, skill_path: str | Path, level: str = "L1") -> dict[str, Any]:
        """按级别加载 skill。"""
        from .metadata import load_metadata
        from .instructions import load_body
        from .resources import load_all_resources

        if level == "L1":
            data = load_metadata(skill_path)
            self._cache[skill_name] = {"level": "L1", "data": data}
            return {"level": "L1", **data}

        if level == "L2":
            meta = load_metadata(skill_path)
            body = load_body(skill_path)
            data = {**meta, "body": body, "body_tokens": len(body) // 4}
            self._cache[skill_name] = {"level": "L2", "data": data}
            return {"level": "L2", **data}

        if level == "L3":
            meta = load_metadata(skill_path)
            body = load_body(skill_path)
            resources = load_all_resources(skill_path)
            data = {**meta, "body": body, "resources": resources}
            self._cache[skill_name] = {"level": "L3", "data": data}
            return {"level": "L3", **data}

        raise ValueError(f"未知加载级别: {level}")

    def upgrade(self, skill_name: str, skill_path: str | Path, target_level: str) -> dict[str, Any]:
        """将 skill 升级到更高加载级别。"""
        current = self._cache.get(skill_name, {}).get("level", "L1")
        levels = ["L1", "L2", "L3"]
        current_idx = levels.index(current)
        target_idx = levels.index(target_level)

        if target_idx <= current_idx:
            # 已经加载
            return self.get(skill_name)

        # 逐级升级
        for level in levels[current_idx:target_idx + 1]:
            if level != current:
                self.load(skill_name, skill_path, level)

        return self.get(skill_name)

    def downgrade(self, skill_name: str, target_level: str) -> dict[str, Any]:
        """降级 skill 到更低级别（释放资源）。"""
        entry = self._cache.get(skill_name)
        if not entry:
            return {"level": "L1"}

        data = entry["data"]
        # L3 -> L2: 去掉 resources
        if target_level == "L2" and "resources" in data:
            data = {k: v for k, v in data.items() if k != "resources"}
        # L3/L2 -> L1: 去掉 body 和 resources
        if target_level == "L1":
            data = {k: v for k, v in data.items() if k in ("name", "description", "version")}

        self._cache[skill_name] = {"level": target_level, "data": data}
        return {"level": target_level, **data}

    def get(self, skill_name: str) -> dict[str, Any] | None:
        """获取缓存中的 skill 数据。"""
        entry = self._cache.get(skill_name)
        if entry:
            return {"level": entry["level"], **entry["data"]}
        return None

    def loaded(self) -> list[str]:
        """列出当前已加载的 skill。"""
        return list(self._cache.keys())

    def clear(self) -> None:
        """清空所有缓存。"""
        self._cache.clear()
