# Story E2-S6: metadata 格式校验

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E2-S6 |
| Epic | E2 质量检测引擎 |
| 状态 | `pending` |
| 依赖 | 无 |

## 需求

校验 metadata 格式

## 验收标准

1. 键值对映射
2. version 为语义化版本（如有）

## 测试用例

```python
def test_valid(): {"version": "1.0.0"} → pass
def test_invalid_version(): {"version": "1.0"} → warning
def test_non_mapping(): "string" → fail
```
