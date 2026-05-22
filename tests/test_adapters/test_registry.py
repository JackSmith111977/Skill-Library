"""E7-S7: 适配器注册表测试"""

import pytest

from skill_library.adapters.registry import AdapterRegistry, get_registry
from skill_library.adapters.generic import GenericAdapter
from skill_library.adapters.claude_code import ClaudeCodeAdapter


class TestAdapterRegistry:
    @pytest.fixture
    def registry(self):
        return AdapterRegistry()

    def test_register_and_get(self, registry):
        """注册和查找"""
        adapter = GenericAdapter()
        registry.register(adapter)
        result = registry.get("generic")
        assert result.name == "generic"

    def test_get_not_found_with_default(self, registry):
        """无匹配返回默认"""
        default = GenericAdapter()
        registry.register(default, default=True)
        result = registry.get("nonexistent")
        assert result.name == "generic"

    def test_get_not_found_no_default(self, registry):
        """无默认时报错"""
        adapter = ClaudeCodeAdapter()
        registry.register(adapter)
        with pytest.raises(KeyError):
            registry.get("nonexistent")

    def test_register_override(self, registry):
        """同名覆盖"""
        a1 = GenericAdapter()
        registry.register(a1)
        registry.register(a1)  # 无异常

    def test_list(self, registry):
        """列出名称"""
        registry.register(GenericAdapter())
        registry.register(ClaudeCodeAdapter())
        names = registry.list()
        assert "generic" in names
        assert "claude-code" in names


class TestGlobalRegistry:
    def test_get_registry_has_defaults(self):
        """全局注册表有默认适配器"""
        registry = get_registry()
        result = registry.get("generic")
        assert result.name == "generic"
        result = registry.get("claude-code")
        assert result.name == "claude-code"
