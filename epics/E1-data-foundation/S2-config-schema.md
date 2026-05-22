# Story E1-S2: config.json 结构定义

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E1-S2 |
| Epic | E1 数据基础层 |
| 状态 | `pending` |
| 依赖 | 无 |

## 需求

定义 config.json 结构，包含技能库路径和 agent 配置

## 验收标准

1. JSON Schema 定义完整
2. 包含 library-path 字段
3. 包含 agents 段（agent-id → path, description）
4. 路径字段支持绝对路径

## 实现要点

```json
{
  "library-path": "D:\\WorkPlace\\VibeCoding\\Skill Library",
  "agents": {
    "<agent-id>": {
      "path": "C:\\Users\\...\\.claude\\skills",
      "description": "主开发环境"
    }
  }
}
```

## 测试用例

```python
def test_config_schema_valid():
    """合法 config.json 通过 Schema 校验"""

def test_config_schema_missing_path():
    """缺少 library-path → 校验失败"""

def test_config_schema_relative_path():
    """相对路径 → 校验失败"""
```
