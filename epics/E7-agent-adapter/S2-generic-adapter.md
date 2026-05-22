# Story E7-S2: 通用 SKILL.md 适配器

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E7-S2 |
| Epic | E7 Agent 适配框架 |
| 状态 | `done` |
| 依赖 | E7-S1 |

## 需求

实现通用适配器，原样输出 SKILL.md。

## 验收标准

1. 适配后内容不变
2. 适用于所有 agent 类型

## 测试用例

```python
def test_generic_adapter_passthrough(): 适配后内容不变
```
