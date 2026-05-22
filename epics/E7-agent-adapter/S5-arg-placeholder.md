# Story E7-S5: Claude Code 参数占位符处理

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E7-S5 |
| Epic | E7 Agent 适配框架 |
| 状态 | `done` |
| 依赖 | E7-S3 |

## 需求

解析和处理 Claude Code 的 argument-hint 参数占位符。

## 验收标准

1. 解析 `{{argument-hint}}` 格式
2. 生成参数提示
3. 占位符格式正确

## 测试用例

```python
def test_parse_argument_hint(): 解析参数提示
def test_generate_prompt(): 生成 prompt
```
