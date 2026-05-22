# Story E8-S4: Token 估算器

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E8-S4 |
| Epic | E8 渐进式加载 |
| 状态 | `done` |
| 依赖 | - |

## 需求

估算文本的 token 数，用于加载决策。

## 验收标准

1. 按字符数估算（character / 4）
2. 误差 ≤ 20%

## 测试用例

```python
def test_estimate_tokens(): 估算 token
def test_estimate_empty(): 空文本
```
