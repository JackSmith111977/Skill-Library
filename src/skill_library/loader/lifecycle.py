"""加载生命周期管理"""

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class LoadLevel(Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


class LoadManager:
    """管理 skill 的加载生命周期"""

    def __init__(self):
        self._cache: dict[str, dict[str, Any]] = {}
        self._evictor = None

    def set_evictor(self, evictor) -> None:
        self._evictor = evictor

    def _record_access(self, skill_name: str) -> None:
        entry = self._cache.get(skill_name)
        if entry:
            entry["data"]["last-used"] = datetime.now(timezone.utc).isoformat()

    def load(self, skill_name: str, skill_path: str | Path, level: str = "L1") -> dict[str, Any]:
        from .metadata import load_metadata
        from .instructions import load_body
        from .resources import load_all_resources

        if level == "L1":
            data = load_metadata(skill_path)
            self._cache[skill_name] = {"level": "L1", "data": data}
            self._record_access(skill_name)
            return {"level": "L1", **data}

        if level == "L2":
            meta = load_metadata(skill_path)
            body = load_body(skill_path)
            data = {**meta, "body": body, "body_tokens": len(body) // 4}
            self._cache[skill_name] = {"level": "L2", "data": data}
            self._record_access(skill_name)
            self._maybe_evict()
            return {"level": "L2", **data}

        if level == "L3":
            meta = load_metadata(skill_path)
            body = load_body(skill_path)
            resources = load_all_resources(skill_path)
            data = {**meta, "body": body, "resources": resources}
            self._cache[skill_name] = {"level": "L3", "data": data}
            self._record_access(skill_name)
            self._maybe_evict()
            return {"level": "L3", **data}

        raise ValueError(f"未知加载级别: {level}")

    def upgrade(self, skill_name: str, skill_path: str | Path, target_level: str) -> dict[str, Any]:
        current = self._cache.get(skill_name, {}).get("level", "L1")
        levels = ["L1", "L2", "L3"]
        current_idx = levels.index(current)
        target_idx = levels.index(target_level)

        if target_idx <= current_idx:
            return self.get(skill_name)

        for level in levels[current_idx:target_idx + 1]:
            if level != current:
                self.load(skill_name, skill_path, level)

        return self.get(skill_name)

    def downgrade(self, skill_name: str, target_level: str) -> dict[str, Any]:
        entry = self._cache.get(skill_name)
        if not entry:
            return {"level": "L1"}

        data = entry["data"]
        if target_level == "L2" and "resources" in data:
            data = {k: v for k, v in data.items() if k != "resources"}
        if target_level == "L1":
            data = {k: v for k, v in data.items() if k in ("name", "description", "version")}

        self._cache[skill_name] = {"level": target_level, "data": data}
        return {"level": target_level, **data}

    def get(self, skill_name: str) -> dict[str, Any] | None:
        entry = self._cache.get(skill_name)
        if entry:
            self._record_access(skill_name)
            return {"level": entry["level"], **entry["data"]}
        return None

    def loaded(self) -> list[str]:
        return list(self._cache.keys())

    def clear(self) -> None:
        self._cache.clear()

    def _maybe_evict(self) -> None:
        if self._evictor is None:
            return
        state = {"skills": {}}
        for name, entry in self._cache.items():
            state["skills"][name] = dict(entry["data"])
            state["skills"][name]["load-level"] = entry["level"]
        self._evictor.evict_if_needed(state)
        for name, info in state["skills"].items():
            level = info.get("load-level", "L1")
            if level == "L1" and name in self._cache and self._cache[name]["level"] != "L1":
                self.downgrade(name, "L1")
