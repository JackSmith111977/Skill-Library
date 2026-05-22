"""E10-S1+S2: Agent 注册与隔离存储测试"""

import pytest
from pathlib import Path

from skill_library.state.machine import StateMachine, PreconditionError
from skill_library.state.manager import StateManager


@pytest.fixture
def sm(tmp_path):
    mgr = StateManager(tmp_path / "state.json")
    return StateMachine(mgr)


class TestAgentRegistration:
    """E10-S1: Agent 注册"""

    def test_register_agent(self, sm):
        result = sm.register_agent("claude-main", "claude-code", "C:\\agents\\claude")
        assert result["agent-type"] == "claude-code"
        assert result["path"] == "C:\\agents\\claude"
        assert result["skills"] == {}

    def test_register_duplicate(self, sm):
        sm.register_agent("agent-1", "generic", "C:\\agents\\a1")
        with pytest.raises(KeyError, match="已注册"):
            sm.register_agent("agent-1", "generic", "C:\\agents\\a1")

    def test_register_invalid_type(self, sm):
        with pytest.raises(ValueError):
            sm.register_agent("bad-agent", "invalid-type", "C:\\agents\\bad")

    def test_register_relative_path(self, sm):
        with pytest.raises(ValueError, match="绝对路径"):
            sm.register_agent("bad-agent", "generic", "relative/path")

    def test_unregister_agent(self, sm):
        sm.register_agent("agent-1", "generic", "C:\\agents\\a1")
        assert sm.unregister_agent("agent-1") is True

    def test_unregister_nonexistent(self, sm):
        with pytest.raises(KeyError, match="未注册"):
            sm.unregister_agent("nonexistent")

    def test_list_agents(self, sm):
        sm.register_agent("a1", "generic", "C:\\a1")
        sm.register_agent("a2", "claude-code", "C:\\a2")
        agents = sm.list_agents()
        assert len(agents) == 2
        assert "a1" in agents
        assert "a2" in agents

    def test_get_agent(self, sm):
        sm.register_agent("test-agent", "generic", "C:\\test")
        result = sm.get_agent("test-agent")
        assert result is not None
        assert result["agent-type"] == "generic"

    def test_get_agent_nonexistent(self, sm):
        assert sm.get_agent("nonexistent") is None


class TestAgentIsolation:
    """E10-S2: Agent 隔离存储"""

    def test_mount_to_agent(self, sm):
        sm.register_agent("agent-1", "generic", "C:\\a1")
        sm.init_library("C:\\lib")
        sm._sm.save({
            "library": {"path": "C:\\lib"},
            "agents": {"agent-1": {"path": "C:\\a1", "agent-type": "generic", "skill-packs": [], "skills": {}}},
            "skills": {
                "test-skill": {"name": "test-skill", "version": "1.0.0", "mount-status": "unmounted", "mounted-to": []}
            }
        })
        result = sm.mount_to_agent("test-skill", "agent-1")
        assert result["status"] == "mounted"
        assert result["load-mode"] == "session"

    def test_mount_to_nonexistent_agent(self, sm):
        sm.init_library("C:\\lib")
        sm._sm.save({
            "library": {"path": "C:\\lib"},
            "agents": {},
            "skills": {"s": {"name": "s", "mount-status": "unmounted"}}
        })
        with pytest.raises(KeyError, match="未注册"):
            sm.mount_to_agent("s", "no-agent")

    def test_mount_nonexistent_skill(self, sm):
        sm.register_agent("a1", "generic", "C:\\a1")
        with pytest.raises(KeyError, match="未注册"):
            sm.mount_to_agent("no-skill", "a1")

    def test_unmount_from_agent(self, sm):
        sm._sm.save({
            "library": {"path": "C:\\lib"},
            "agents": {
                "a1": {"path": "C:\\a1", "agent-type": "generic", "skill-packs": [], "skills": {
                    "s1": {"status": "mounted", "version": "1.0", "adapter": "generic", "load-mode": "session"}
                }}
            },
            "skills": {"s1": {"name": "s1", "version": "1.0", "mount-status": "mounted", "mounted-to": ["a1"]}}
        })
        assert sm.unmount_from_agent("s1", "a1") is True

    def test_unmount_not_mounted(self, sm):
        sm._sm.save({
            "library": {"path": "C:\\lib"},
            "agents": {"a1": {"path": "C:\\a1", "agent-type": "generic", "skill-packs": [], "skills": {}}},
            "skills": {"s1": {"name": "s1", "mount-status": "unmounted", "mounted-to": []}}
        })
        with pytest.raises(KeyError, match="未挂载"):
            sm.unmount_from_agent("s1", "a1")

    def test_get_agent_skills(self, sm):
        sm._sm.save({
            "library": {"path": "C:\\lib"},
            "agents": {
                "a1": {"path": "C:\\a1", "agent-type": "generic", "skill-packs": [], "skills": {
                    "s1": {"status": "mounted", "version": "1.0", "adapter": "generic", "load-mode": "session"}
                }}
            },
            "skills": {}
        })
        skills = sm.get_agent_skills("a1")
        assert "s1" in skills

    def test_get_agent_skills_nonexistent(self, sm):
        with pytest.raises(KeyError):
            sm.get_agent_skills("no-agent")

    def test_isolation_between_agents(self, sm):
        """同一 skill 在不同 agent 有独立状态"""
        sm._sm.save({
            "library": {"path": "C:\\lib"},
            "agents": {
                "a1": {"path": "C:\\a1", "agent-type": "generic", "skill-packs": [], "skills": {
                    "s1": {"status": "mounted", "version": "1.0", "adapter": "generic", "load-mode": "session"}
                }},
                "a2": {"path": "C:\\a2", "agent-type": "generic", "skill-packs": [], "skills": {
                    "s1": {"status": "mounted", "version": "2.0", "adapter": "claude-code", "load-mode": "turn"}
                }}
            },
            "skills": {}
        })
        s1 = sm.get_agent_skills("a1")
        s2 = sm.get_agent_skills("a2")
        assert s1["s1"]["version"] == "1.0"
        assert s2["s1"]["version"] == "2.0"
        assert s1["s1"]["adapter"] != s2["s1"]["adapter"]
