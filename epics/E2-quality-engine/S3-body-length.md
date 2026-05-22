# Story E2-S3: body 长度校验规则

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E2-S3 |
| Epic | E2 质量检测引擎 |
| 状态 | `pending` |
| 依赖 | 无 |

## 需求

校验 SKILL.md body 长度

## 验收标准

1. 行数 ≤ 500（WARNING）
2. Token 估算 ≤ 5000（WARNING）

## 测试用例

```python
def test_short_body(): 100 lines → pass
def test_long_body(): 501 lines → warning
def test_token_estimate(): estimate_tokens() works
```
