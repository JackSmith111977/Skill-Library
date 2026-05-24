"""E10-S4: Agent 配置验证测试"""

import pytest
from pathlib import Path

from skill_library.state.config import ConfigManager


@pytest.fixture
def manager(tmp_path):
    return ConfigManager(tmp_path / "config.json")


class TestAgentConfigValidation:
    """E10-S4: Agent 配置验证"""

    def test_validate_agent_type_valid(self, manager, tmp_path):
        """有效 agent-type 通过验证"""
        config = {
            "library-path": str(tmp_path / "lib"),
            "agents": {
                "agent-1": {"path": str(tmp_path / "agents" / "a1"), "agent-type": "claude-code"}
            }
        }
        errors = manager.validate_paths(config)
        assert errors == []

    def test_validate_agent_type_invalid(self, manager, tmp_path):
        """无效 agent-type 报错"""
        config = {
            "library-path": str(tmp_path / "lib"),
            "agents": {
                "agent-1": {"path": str(tmp_path / "agents" / "a1"), "agent-type": "not-a-real-type"}
            }
        }
        errors = manager.validate_paths(config)
        assert any("type" in e for e in errors)

    def test_validate_agent_skill_packs_valid(self, manager, tmp_path):
        config = {
            "library-path": str(tmp_path / "lib"),
            "agents": {
                "agent-1": {"path": str(tmp_path / "agents" / "a1"), "skill-packs": ["dev", "ai"]}
            }
        }
        errors = manager.validate_paths(config)
        assert errors == []

    def test_validate_agent_skill_packs_not_list(self, manager, tmp_path):
        config = {
            "library-path": str(tmp_path / "lib"),
            "agents": {
                "agent-1": {"path": str(tmp_path / "agents" / "a1"), "skill-packs": "not-a-list"}
            }
        }
        errors = manager.validate_paths(config)
        assert any("必须是数组" in e for e in errors)

    def test_validate_agent_skill_packs_bad_element(self, manager, tmp_path):
        config = {
            "library-path": str(tmp_path / "lib"),
            "agents": {
                "agent-1": {"path": str(tmp_path / "agents" / "a1"), "skill-packs": [1, 2, 3]}
            }
        }
        errors = manager.validate_paths(config)
        assert any("必须是字符串" in e for e in errors)

    def test_validate_strict_path_exists(self, manager, tmp_path):
        """严格模式校验路径存在性"""
        existing_dir = tmp_path / "existing-agent"
        existing_dir.mkdir()
        config = {
            "library-path": str(tmp_path),
            "agents": {
                "good-agent": {"path": str(existing_dir)},
                "bad-agent": {"path": str(tmp_path / "nonexistent")}
            }
        }
        errors = manager.validate_agent_strict(config)
        assert len(errors) == 1
        assert "不存在" in errors[0]

    def test_validate_strict_no_extra_errors(self, manager):
        """严格模式对不存在但路径格式错误的 agent 只报告格式错误"""
        config = {
            "library-path": "relative",
            "agents": {
                "a1": {"path": "also-relative"}
            }
        }
        errors = manager.validate_agent_strict(config)
        # relative path errors take precedence — each reports once
        assert len(errors) == 2
