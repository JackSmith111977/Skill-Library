# Story E2-S2: description 校验规则

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E2-S2 |
| Epic | E2 质量检测引擎 |
| 状态 | `pending` |
| 依赖 | 无 |

## 需求

校验 description 长度和触发词

## 验收标准

1. 长度 1-1024 字符
2. 检测引号内触发短语（WARNING）
3. 检测第三人称（WARNING）

## 测试用例

```python
def test_valid(): "Use when user asks to 'xxx'" → pass
def test_empty(): "" → fail
def test_too_long(): 1025 chars → fail
def test_no_triggers(): "Helps with tasks" → warning
def test_third_person(): "This skill should be used when..." → pass
```
