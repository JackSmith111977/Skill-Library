"""E4: 状态机引擎测试"""

import pytest
from pathlib import Path

from skill_library.state.manager import StateManager
from skill_library.state.machine import (
    StateMachine,
    PreconditionError,
    InvalidTransitionError,
)


@pytest.fixture
def state_path(tmp_path):
    return tmp_path / "state.json"


@pytest.fixture
def sm(state_path):
    return StateManager(state_path)


@pytest.fixture
def machine(sm):
    return StateMachine(sm)


def _register_skill(sm, name, quality="unchecked", mount="unmounted"):
    """辅助：注册一个 skill"""
    state = sm.load()
    state.setdefault("skills", {})[name] = {
        "name": name,
        "path": f"/skills/{name}",
        "version": "1.0.0",
        "type": "atomic",
        "design-pattern": "tool-wrapper",
        "category": "technical",
        "mount-status": mount,
        "quality-status": quality,
    }
    sm.save(state)


# ===== E4-S1: 状态转换 =====

class TestTransitions:
    def test_valid_mount_transition(self, machine, sm):
        """unmounted → mounted 合法"""
        _register_skill(sm, "test-skill")
        result = machine.transition_mount("test-skill", "mounted")
        assert result["mount-status"] == "mounted"

    def test_invalid_mount_transition(self, machine, sm):
        """unmounted → outdated 非法"""
        _register_skill(sm, "test-skill")
        with pytest.raises(InvalidTransitionError):
            machine.transition_mount("test-skill", "outdated")

    def test_mounted_to_unmounted(self, machine, sm):
        """mounted → unmounted 合法"""
        _register_skill(sm, "test-skill", mount="mounted")
        result = machine.transition_mount("test-skill", "unmounted")
        assert result["mount-status"] == "unmounted"

    def test_mounted_to_outdated(self, machine, sm):
        """mounted → outdated 合法"""
        _register_skill(sm, "test-skill", mount="mounted")
        result = machine.transition_mount("test-skill", "outdated")
        assert result["mount-status"] == "outdated"

    def test_outdated_to_mounted(self, machine, sm):
        """outdated → mounted 合法"""
        _register_skill(sm, "test-skill", mount="outdated")
        result = machine.transition_mount("test-skill", "mounted")
        assert result["mount-status"] == "mounted"

    def test_valid_quality_transition(self, machine, sm):
        """unchecked → passed 合法"""
        _register_skill(sm, "test-skill")
        result = machine.transition_quality("test-skill", "passed")
        assert result["quality-status"] == "passed"

    def test_invalid_quality_transition(self, machine, sm):
        """passed → unchecked 非法"""
        _register_skill(sm, "test-skill", quality="passed")
        with pytest.raises(InvalidTransitionError):
            machine.transition_quality("test-skill", "unchecked")

    def test_failed_to_passed(self, machine, sm):
        """failed → passed 合法"""
        _register_skill(sm, "test-skill", quality="failed")
        result = machine.transition_quality("test-skill", "passed")
        assert result["quality-status"] == "passed"

    def test_passed_to_failed(self, machine, sm):
        """passed → failed 合法"""
        _register_skill(sm, "test-skill", quality="passed")
        result = machine.transition_quality("test-skill", "failed")
        assert result["quality-status"] == "failed"


# ===== E4-S2: 前置检查 =====

class TestPreconditions:
    def test_mount_requires_passed(self, machine, sm):
        """未通过质量检测不能 mount"""
        _register_skill(sm, "test-skill", quality="unchecked")
        with pytest.raises(PreconditionError, match="quality-status"):
            machine.mount("test-skill", "agent-1")

    def test_mount_requires_passed_failed(self, machine, sm):
        """quality failed 不能 mount"""
        _register_skill(sm, "test-skill", quality="failed")
        with pytest.raises(PreconditionError):
            machine.mount("test-skill", "agent-1")

    def test_unmount_requires_mounted(self, machine, sm):
        """未 mounted 不能 unmount"""
        _register_skill(sm, "test-skill", mount="unmounted")
        with pytest.raises(PreconditionError):
            machine.unmount("test-skill")

    def test_classify_requires_registered(self, machine, sm):
        """未注册不能 classify"""
        with pytest.raises(KeyError, match="未注册"):
            machine.classify("nonexistent", category="discipline")


# ===== E4-S3: mount =====

class TestMount:
    def test_mount_success(self, machine, sm):
        """mount 成功"""
        _register_skill(sm, "test-skill", quality="passed")
        result = machine.mount("test-skill", "agent-1")
        assert result["mount-status"] == "mounted"

    def test_mount_updates_state(self, machine, sm, state_path):
        """state.json 更新"""
        _register_skill(sm, "test-skill", quality="passed")
        machine.mount("test-skill", "agent-1")
        sm2 = StateManager(state_path)
        state = sm2.load()
        assert state["skills"]["test-skill"]["mount-status"] == "mounted"

    def test_mount_records_agent(self, machine, sm):
        """记录 agent-id"""
        _register_skill(sm, "test-skill", quality="passed")
        result = machine.mount("test-skill", "agent-1")
        assert "agent-1" in result["mounted-to"]


# ===== E4-S4: unmount =====

class TestUnmount:
    def test_unmount_success(self, machine, sm):
        """unmount 成功"""
        _register_skill(sm, "test-skill", mount="mounted")
        result = machine.unmount("test-skill")
        assert result["mount-status"] == "unmounted"

    def test_unmount_updates_state(self, machine, sm, state_path):
        """state.json 更新"""
        _register_skill(sm, "test-skill", mount="mounted")
        machine.unmount("test-skill")
        sm2 = StateManager(state_path)
        state = sm2.load()
        assert state["skills"]["test-skill"]["mount-status"] == "unmounted"

    def test_unmount_removes_agent(self, machine, sm):
        """移除 agent-id"""
        _register_skill(sm, "test-skill", mount="mounted")
        # 先设置 mounted-to
        state = sm.load()
        state["skills"]["test-skill"]["mounted-to"] = ["agent-1"]
        sm.save(state)
        result = machine.unmount("test-skill", "agent-1")
        assert "agent-1" not in result.get("mounted-to", [])


# ===== E4-S5: classify =====

class TestClassify:
    def test_classify_success(self, machine, sm):
        """分类成功"""
        _register_skill(sm, "test-skill")
        result = machine.classify("test-skill", **{"design-pattern": "pipeline"})
        assert result["design-pattern"] == "pipeline"

    def test_classify_multiple(self, machine, sm):
        """多字段分类"""
        _register_skill(sm, "test-skill")
        result = machine.classify(
            "test-skill",
            **{"design-pattern": "inversion", "category": "discipline"}
        )
        assert result["design-pattern"] == "inversion"
        assert result["category"] == "discipline"

    def test_classify_invalid_enum(self, machine, sm):
        """非法枚举值拒绝"""
        _register_skill(sm, "test-skill")
        from enum import Enum
        with pytest.raises(ValueError):
            machine.classify("test-skill", **{"design-pattern": "invalid-pattern"})


# ===== E4-S6: status =====

class TestStatus:
    def test_status_query(self, machine, sm):
        """查询成功"""
        _register_skill(sm, "test-skill")
        result = machine.status("test-skill")
        assert result is not None
        assert result["name"] == "test-skill"

    def test_status_not_found(self, machine):
        """不存在返回 None"""
        assert machine.status("nonexistent") is None


# ===== E4-S7: init =====

class TestInit:
    def test_init_creates_state(self, machine, tmp_path):
        """创建 state.json"""
        library_path = tmp_path / "library"
        machine.init_library(library_path)
        assert (library_path / "skills").is_dir()

    def test_init_creates_dirs(self, machine, tmp_path):
        """创建目录"""
        library_path = tmp_path / "library"
        machine.init_library(library_path)
        assert library_path.is_dir()
        assert (library_path / "skills").is_dir()

    def test_init_no_overwrite(self, machine, tmp_path):
        """已存在不覆盖"""
        library_path = tmp_path / "library"
        library_path.mkdir()
        (library_path / "skills").mkdir()
        (library_path / "skills" / "existing.md").write_text("data")
        machine.init_library(library_path)
        assert (library_path / "skills" / "existing.md").read_text() == "data"

    def test_init_with_config(self, machine, tmp_path):
        """创建 config.json"""
        library_path = tmp_path / "library"
        config_path = tmp_path / "config.json"
        machine.init_library(library_path, config_path)
        assert config_path.exists()


# ===== E4-S8: 异常处理 =====

class TestErrorHandling:
    def test_precondition_error(self, machine, sm):
        """前置条件异常"""
        _register_skill(sm, "test-skill", quality="unchecked")
        with pytest.raises(PreconditionError):
            machine.mount("test-skill", "agent-1")

    def test_invalid_transition_error(self, machine, sm):
        """非法转换异常"""
        _register_skill(sm, "test-skill")
        with pytest.raises(InvalidTransitionError):
            machine.transition_mount("test-skill", "outdated")

    def test_not_registered_error(self, machine, sm):
        """未注册异常"""
        with pytest.raises(KeyError):
            machine.transition_mount("nonexistent", "mounted")
