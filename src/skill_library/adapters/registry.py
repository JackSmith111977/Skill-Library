"""适配器注册表"""

from typing import Any
from .base import AgentAdapter


class AdapterRegistry:
    """按 agent 名称管理适配器"""

    def __init__(self):
        self._adapters: dict[str, AgentAdapter] = {}
        self._default: AgentAdapter | None = None

    def register(self, adapter: AgentAdapter, default: bool = False) -> None:
        """注册适配器。同名覆盖。"""
        self._adapters[adapter.name] = adapter
        if default:
            self._default = adapter

    def get(self, agent_name: str) -> AgentAdapter:
        """按名称查找适配器。不存在时返回默认适配器。"""
        adapter = self._adapters.get(agent_name)
        if adapter is not None:
            return adapter
        if self._default is not None:
            return self._default
        raise KeyError(f"未找到适配器: {agent_name}")

    def list(self) -> list[str]:
        """列出所有已注册的适配器名称。"""
        return list(self._adapters.keys())


# 全局注册表
_default_registry = AdapterRegistry()


def get_registry() -> AdapterRegistry:
    """获取全局适配器注册表。"""
    return _default_registry
