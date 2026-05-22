"""LRU 淘汰策略"""

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


class LRUEvictor:
    """LRU 淘汰器，超限时淘汰最近最少使用的 skill。"""

    def __init__(self, max_loaded: int = 10):
        if max_loaded < 1:
            raise ValueError(f"max_loaded 必须 >= 1: {max_loaded}")
        self.max_loaded = max_loaded
        self._events: list[dict[str, Any]] = []

    def record_access(self, skill_name: str, state: dict[str, Any]) -> None:
        """记录 skill 访问，更新 last-used 时间戳。"""
        now = datetime.now(timezone.utc).isoformat()
        skills = state.get("skills", {})
        if skill_name in skills:
            skills[skill_name]["last-used"] = now
        # 也更新 agent 隔离存储中的时间戳
        for agent in state.get("agents", {}).values():
            agent_skills = agent.get("skills", {})
            if skill_name in agent_skills:
                agent_skills[skill_name]["last-used"] = now

    def evict_if_needed(self, state: dict[str, Any]) -> list[dict[str, Any]]:
        """检查是否超限，超限则淘汰最久未使用的 skill。返回淘汰事件列表。"""
        evicted = []
        skills = state.get("skills", {})
        loaded = {
            name: info
            for name, info in skills.items()
            if info.get("load-level", "L1") != "L1"
        }

        while len(loaded) > self.max_loaded:
            target = self._find_lru(loaded)
            if target is None:
                break
            name = target[0]
            # 降级到 L1
            skills[name]["load-level"] = "L1"
            if "body" in skills[name]:
                del skills[name]["body"]
            if "resources" in skills[name]:
                del skills[name]["resources"]
            event = {
                "skill": name,
                "evicted-at": datetime.now(timezone.utc).isoformat(),
                "last-used": skills[name].get("last-used", ""),
            }
            self._events.append(event)
            evicted.append(event)
            logger.info("LRU evicted skill: %s", name)
            # 刷新 loaded 列表
            loaded = {
                n: i for n, i in skills.items()
                if i.get("load-level", "L1") != "L1"
            }

        return evicted

    def _find_lru(self, loaded: dict[str, dict[str, Any]]) -> tuple[str, dict[str, Any]] | None:
        """找到 last-used 最早的 skill（最近最少使用的）。"""
        if not loaded:
            return None
        return min(
            loaded.items(),
            key=lambda item: item[1].get("last-used", ""),
        )

    def get_events(self) -> list[dict[str, Any]]:
        """获取历史淘汰事件。"""
        return list(self._events)

    def clear_events(self) -> None:
        """清空淘汰事件。"""
        self._events.clear()
