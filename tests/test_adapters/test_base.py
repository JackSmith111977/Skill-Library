"""E7-S1,S2,S6: 适配器基类和通用适配器测试"""

import pytest
from pathlib import Path

from skill_library.adapters.base import AgentAdapter
from skill_library.adapters.generic import GenericAdapter


# ===== E7-S1: 抽象基类 =====

class TestAgentAdapter:
    def test_cannot_instantiate_abstract(self):
        """不能实例化抽象类"""
        with pytest.raises(TypeError):
            AgentAdapter()

    def test_concrete_adapter(self):
        """实现接口可实例化"""
        adapter = GenericAdapter()
        assert adapter.name == "generic"
        assert adapter.version == "1.0.0"

    def test_abstract_methods(self):
        """接口方法存在"""
        methods = ["adapt_content"]
        for m in methods:
            assert hasattr(AgentAdapter, m)


# ===== E7-S2: 通用适配器 =====

class TestGenericAdapter:
    def test_generic_adapter_passthrough(self):
        """适配后内容不变"""
        adapter = GenericAdapter()
        content = "Hello, world!"
        result = adapter.adapt_content(content, {})
        assert result == content

    def test_generic_target_patterns(self):
        """通用适配器无目标模式"""
        adapter = GenericAdapter()
        assert adapter.target_patterns == []


# ===== E7-S6: 版本降级 =====

class TestVersionFallback:
    def test_prefer_agent_version(self, tmp_path):
        """优先 agent 版"""
        adapter = GenericAdapter()
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("generic content")
        agent_dir = skill_dir / "agents" / "generic"
        agent_dir.mkdir(parents=True)
        (agent_dir / "SKILL.md").write_text("agent specific content")

        content = adapter.load_skill(skill_dir)
        assert content == "agent specific content"

    def test_fallback_generic(self, tmp_path):
        """降级到通用版"""
        adapter = GenericAdapter()
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("generic content")

        content = adapter.load_skill(skill_dir)
        assert content == "generic content"

    def test_no_skill_md(self, tmp_path):
        """无文件返回 None"""
        adapter = GenericAdapter()
        skill_dir = tmp_path / "empty-skill"
        skill_dir.mkdir()
        assert adapter.load_skill(skill_dir) is None

    def test_get_effective_content_agent(self, tmp_path):
        """get_effective_content 返回 agent 来源"""
        adapter = GenericAdapter()
        skill_dir = tmp_path / "test"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("generic")
        agent_dir = skill_dir / "agents" / "generic"
        agent_dir.mkdir(parents=True)
        (agent_dir / "SKILL.md").write_text("agent")
        content, source = adapter.get_effective_content(skill_dir)
        assert source == "agent"

    def test_get_effective_content_generic(self, tmp_path):
        """get_effective_content 返回 generic 来源"""
        adapter = GenericAdapter()
        skill_dir = tmp_path / "test"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("generic")
        content, source = adapter.get_effective_content(skill_dir)
        assert source == "generic"
