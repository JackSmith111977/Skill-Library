# Story E1-S1: state.json 三段式结构定义

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E1-S1 |
| Epic | E1 数据基础层 |
| 状态 | `pending` |
| 依赖 | 无 |

## 需求

定义 state.json 的三段式结构：library / agents / skills

## 验收标准

1. JSON Schema 定义完整
2. 包含 library 段（path, created-at, last-sync）
3. 包含 agents 段（agent-id → path, agent-type, skill-packs, skills）
4. 包含 skills 段（skill-name → pack, type, design-pattern, skill-type, version, quality-status, agent-adapters, default-adapter, mounted-to）
5. 所有字段类型定义正确

## 实现要点

```json
{
  "library": {
    "path": "string",
    "created-at": "date",
    "last-sync": "datetime"
  },
  "agents": {
    "<agent-id>": {
      "path": "string",
      "agent-type": "enum",
      "skill-packs": ["string"],
      "skills": {
        "<skill-name>": {
          "status": "enum",
          "version": "semver",
          "adapter": "string",
          "load-mode": "enum",
          "loaded-at": "date",
          "last-used": "date"
        }
      }
    }
  },
  "skills": {
    "<skill-name>": {
      "pack": "string",
      "type": "enum",
      "design-pattern": "enum",
      "skill-type": "enum",
      "version": "semver",
      "quality-status": "enum",
      "agent-adapters": ["string"],
      "default-adapter": "string",
      "mounted-to": ["string"]
    }
  }
}
```

## 测试用例

```python
def test_state_schema_valid():
    """合法 state.json 通过 Schema 校验"""

def test_state_schema_missing_library():
    """缺少 library 段 → 校验失败"""

def test_state_schema_invalid_status():
    """非法 status 值 → 校验失败"""
```
