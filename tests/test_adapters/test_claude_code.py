"""E7-S3,S4,S5: Claude Code 适配器测试"""

import pytest

from skill_library.adapters.claude_code import ClaudeCodeAdapter


@pytest.fixture
def adapter():
    return ClaudeCodeAdapter()


# ===== E7-S3: 扩展字段 =====

class TestClaudeExtensions:
    def test_extract_argument_hint(self, adapter):
        """提取 argument-hint"""
        fm = {"argument-hint": "<name> [options]"}
        result = adapter.extract_extensions(fm)
        assert result["argument-hint"] == "<name> [options]"

    def test_extract_model(self, adapter):
        """提取 model"""
        fm = {"model": "sonnet"}
        result = adapter.extract_extensions(fm)
        assert result["model"] == "sonnet"

    def test_extract_no_extensions(self, adapter):
        """无扩展字段"""
        result = adapter.extract_extensions({"name": "test"})
        assert result["argument-hint"] is None
        assert result["model"] is None

    def test_adapt_with_arg_hint(self, adapter):
        """适配时添加 arg hint"""
        content = "Body content"
        result = adapter.adapt_content(content, {"argument-hint": "<file>"})
        assert "Argument hint" in result
        assert "<file>" in result

    def test_adapt_without_arg_hint(self, adapter):
        """无 arg hint 不改内容"""
        content = "Body content"
        result = adapter.adapt_content(content, {})
        assert result == content


# ===== E7-S4: 动态注入 =====

class TestClaudeInjection:
    def test_parse_injection_passthrough(self, adapter):
        """注入标记保留"""
        content = "Run {{command}} or $(shell cmd)"
        result = adapter.adapt_content(content, {})
        assert "{{command}}" in result
        assert "$(shell cmd)" in result

    def test_no_injection(self, adapter):
        """无注入通过"""
        content = "Plain content"
        result = adapter.adapt_content(content, {})
        assert result == content


# ===== E7-S5: 参数占位符 =====

class TestArgPlaceholder:
    def test_parse_argument_hint_placeholders(self, adapter):
        """解析 argument-hint 占位符"""
        result = adapter.parse_argument_hint("<name> --option {{value}}")
        assert "value" in result

    def test_parse_complex_hint(self, adapter):
        """解析复杂占位符"""
        result = adapter.parse_argument_hint("{{source-file}} {{target-dir}} [--force]")
        assert "source-file" in result
        assert "target-dir" in result

    def test_no_placeholders(self, adapter):
        """无占位符"""
        result = adapter.parse_argument_hint("<name>")
        assert result == []
