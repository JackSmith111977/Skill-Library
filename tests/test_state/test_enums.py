"""E1-S5: 状态值枚举定义测试"""

import pytest

from skill_library.state.enums import (
    MountStatus,
    QualityStatus,
    SkillType,
    DesignPattern,
    SkillCategory,
    LoadMode,
    AgentType,
)


# ===== MountStatus 测试 =====

def test_mount_status_values():
    """MountStatus 枚举值正确"""
    assert MountStatus.MOUNTED == "mounted"
    assert MountStatus.UNMOUNTED == "unmounted"
    assert MountStatus.ERROR == "error"
    assert MountStatus.OUTDATED == "outdated"


def test_mount_status_count():
    """MountStatus 有 4 个值"""
    assert len(MountStatus) == 4


def test_mount_status_from_string():
    """从字符串创建 MountStatus"""
    assert MountStatus("mounted") == MountStatus.MOUNTED


# ===== QualityStatus 测试 =====

def test_quality_status_values():
    """QualityStatus 枚举值正确"""
    assert QualityStatus.PASSED == "passed"
    assert QualityStatus.FAILED == "failed"
    assert QualityStatus.UNCHECKED == "unchecked"


def test_quality_status_count():
    """QualityStatus 有 3 个值"""
    assert len(QualityStatus) == 3


# ===== SkillType 测试 =====

def test_skill_type_values():
    """SkillType 枚举值正确"""
    assert SkillType.ATOMIC == "atomic"
    assert SkillType.WORKFLOW == "workflow"


def test_skill_type_count():
    """SkillType 有 2 个值"""
    assert len(SkillType) == 2


# ===== DesignPattern 测试 =====

def test_design_pattern_values():
    """DesignPattern 枚举值正确"""
    assert DesignPattern.TOOL_WRAPPER == "tool-wrapper"
    assert DesignPattern.GENERATOR == "generator"
    assert DesignPattern.REVIEWER == "reviewer"
    assert DesignPattern.INVERSION == "inversion"
    assert DesignPattern.PIPELINE == "pipeline"


def test_design_pattern_count():
    """DesignPattern 有 5 个值"""
    assert len(DesignPattern) == 5


# ===== SkillCategory 测试 =====

def test_skill_category_values():
    """SkillCategory 枚举值正确"""
    assert SkillCategory.DISCIPLINE == "discipline"
    assert SkillCategory.TECHNICAL == "technical"
    assert SkillCategory.MINDSET == "mindset"
    assert SkillCategory.REFERENCE == "reference"


def test_skill_category_count():
    """SkillCategory 有 4 个值"""
    assert len(SkillCategory) == 4


# ===== LoadMode 测试 =====

def test_load_mode_values():
    """LoadMode 枚举值正确"""
    assert LoadMode.ONCE == "once"
    assert LoadMode.TURN == "turn"
    assert LoadMode.SESSION == "session"


def test_load_mode_count():
    """LoadMode 有 3 个值"""
    assert len(LoadMode) == 3


# ===== AgentType 测试 =====

def test_agent_type_values():
    """AgentType 枚举值正确"""
    assert AgentType.GENERIC == "generic"
    assert AgentType.CLAUDE_CODE == "claude-code"
    assert AgentType.HERMES == "hermes"
    assert AgentType.OPENCLAW == "openclaw"


def test_agent_type_count():
    """AgentType 有 4 个值"""
    assert len(AgentType) == 4


# ===== 通用测试 =====

def test_enum_string_conversion():
    """枚举 ↔ 字符串转换正确"""
    for enum_class in [MountStatus, QualityStatus, SkillType, DesignPattern, SkillCategory, LoadMode, AgentType]:
        for member in enum_class:
            # 枚举值是字符串
            assert isinstance(member.value, str)
            # 可以从字符串创建
            assert enum_class(member.value) == member


def test_enum_in_list():
    """枚举值可用于列表比较"""
    statuses = [MountStatus.MOUNTED, MountStatus.UNMOUNTED]
    assert MountStatus.MOUNTED in statuses
    assert MountStatus.ERROR not in statuses


def test_enum_as_dict_key():
    """枚举值可用作字典键"""
    data = {MountStatus.MOUNTED: "active"}
    assert data[MountStatus.MOUNTED] == "active"
    assert data["mounted"] == "active"  # str 枚举支持字符串键
