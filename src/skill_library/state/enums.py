"""状态值枚举定义"""

from enum import Enum


class MountStatus(str, Enum):
    """skill 挂载状态"""
    MOUNTED = "mounted"
    UNMOUNTED = "unmounted"
    ERROR = "error"
    OUTDATED = "outdated"


class QualityStatus(str, Enum):
    """质量检测状态"""
    PASSED = "passed"
    FAILED = "failed"
    UNCHECKED = "unchecked"


class SkillType(str, Enum):
    """skill 类型"""
    ATOMIC = "atomic"
    WORKFLOW = "workflow"


class DesignPattern(str, Enum):
    """设计模式（Google 5 种）"""
    TOOL_WRAPPER = "tool-wrapper"
    GENERATOR = "generator"
    REVIEWER = "reviewer"
    INVERSION = "inversion"
    PIPELINE = "pipeline"


class SkillCategory(str, Enum):
    """skill 分类（Writing-Skills 4 种）"""
    DISCIPLINE = "discipline"
    TECHNICAL = "technical"
    MINDSET = "mindset"
    REFERENCE = "reference"


class LoadMode(str, Enum):
    """加载生命周期模式"""
    ONCE = "once"
    TURN = "turn"
    SESSION = "session"


class AgentType(str, Enum):
    """Agent 类型"""
    GENERIC = "generic"
    CLAUDE_CODE = "claude-code"
    HERMES = "hermes"
    OPENCLAW = "openclaw"
