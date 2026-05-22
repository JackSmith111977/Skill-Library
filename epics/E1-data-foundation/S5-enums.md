# Story E1-S5: 状态值枚举定义

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E1-S5 |
| Epic | E1 数据基础层 |
| 状态 | `done` |
| 依赖 | 无 |
| 开始时间 | 2026-05-22 |
| 完成时间 | 2026-05-22 |

## 需求

定义所有状态值枚举，作为状态机的 single source of truth

## 验收标准

1. mount-status: mounted / unmounted / error / outdated
2. quality-status: passed / failed / unchecked
3. type: atomic / workflow
4. design-pattern: tool-wrapper / generator / reviewer / inversion / pipeline
5. skill-type: discipline / technical / mindskill / reference
6. load-mode: once / turn / session
7. agent-type: generic / claude-code / hermes / openclaw

## 实现要点

```python
from enum import Enum

class MountStatus(str, Enum):
    MOUNTED = "mounted"
    UNMOUNTED = "unmounted"
    ERROR = "error"
    OUTDATED = "outdated"

class QualityStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    UNCHECKED = "unchecked"

class SkillType(str, Enum):
    ATOMIC = "atomic"
    WORKFLOW = "workflow"

class DesignPattern(str, Enum):
    TOOL_WRAPPER = "tool-wrapper"
    GENERATOR = "generator"
    REVIEWER = "reviewer"
    INVERSION = "inversion"
    PIPELINE = "pipeline"

class SkillCategory(str, Enum):
    DISCIPLINE = "discipline"
    TECHNICAL = "technical"
    MINDSET = "mindset"
    REFERENCE = "reference"

class LoadMode(str, Enum):
    ONCE = "once"
    TURN = "turn"
    SESSION = "session"

class AgentType(str, Enum):
    GENERIC = "generic"
    CLAUDE_CODE = "claude-code"
    HERMES = "hermes"
    OPENCLAW = "openclaw"
```

## 测试用例

```python
def test_mount_status_values():
    """枚举值正确"""

def test_quality_status_values():
    """枚举值正确"""

def test_design_pattern_values():
    """枚举值正确"""

def test_enum_string_conversion():
    """枚举 ↔ 字符串转换正确"""
```
