# Story E7-S3: Claude Code 扩展字段处理

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E7-S3 |
| Epic | E7 Agent 适配框架 |
| 状态 | `done` |
| 依赖 | E7-S1 |

## 需求

处理 Claude Code 的 frontmatter 扩展字段。

## 验收标准

1. 处理 `argument-hint` 字段
2. 处理 `model` 字段
3. 非 Claude Code 适配器忽略扩展字段

## 测试用例

```python
def test_extract_argument_hint(): 提取 argument-hint
def test_extract_model(): 提取 model
def test_skip_if_not_claude(): 非 Claude Code 忽略
```
