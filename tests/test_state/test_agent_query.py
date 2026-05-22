"""E10-S3: 按 Agent 过滤查询测试"""

import pytest
from pathlib import Path

from skill_library.state.manager import StateManager
from skill_library.registry.indexer import SkillIndexer
from skill_library.state.machine import StateMachine


@pytest.fixture
def indexer(tmp_path):
    sm = StateManager(tmp_path / "state.json")
    return SkillIndexer(sm)


@pytest.fixture
def state_with_agents(tmp_path):
    """预填充 agent 和 skill 的 state"""
    mgr = StateManager(tmp_path / "state.json")
    mgr.save({
        "library": {"path": str(tmp_path)},
        "agents": {
            "a1": {"path": "C:\\a1", "agent-type": "generic", "skill-packs": [], "skills": {
                "s1": {"status": "mounted", "version": "1.0", "adapter": "generic", "load-mode": "session"},
                "s2": {"status": "mounted", "version": "1.0", "adapter": "generic", "load-mode": "session"},
            }},
            "a2": {"path": "C:\\a2", "agent-type": "claude-code", "skill-packs": [], "skills": {
                "s1": {"status": "mounted", "version": "2.0", "adapter": "claude-code", "load-mode": "turn"},
            }},
        },
        "skills": {
            "s1": {"name": "s1", "version": "1.0", "type": "atomic"},
            "s2": {"name": "s2", "version": "1.0", "type": "atomic"},
        }
    })
    return SkillIndexer(mgr)


class TestAgentQuery:
    """E10-S3: 按 Agent 过滤查询"""

    def test_query_by_agent(self, state_with_agents):
        """查询 agent 挂载的所有 skill"""
        result = state_with_agents.query_by_agent("a1")
        assert "s1" in result
        assert "s2" in result
        assert len(result) == 2

    def test_query_by_agent_partial(self, state_with_agents):
        """a2 只有 s1"""
        result = state_with_agents.query_by_agent("a2")
        assert "s1" in result
        assert "s2" not in result

    def test_query_by_agent_nonexistent(self, state_with_agents):
        """不存在的 agent 返回空"""
        result = state_with_agents.query_by_agent("no-agent")
        assert result == {}

    def test_query_by_agent_type(self, state_with_agents):
        """按 agent 类型过滤"""
        result = state_with_agents.query_by_agent_type("claude-code")
        assert "a2" in result
        assert "a1" not in result

    def test_query_by_agent_type_empty(self, state_with_agents):
        result = state_with_agents.query_by_agent_type("hermes")
        assert result == {}
