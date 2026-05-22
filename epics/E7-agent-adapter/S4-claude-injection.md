# Story E7-S4: Claude Code 动态注入处理

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E7-S4 |
| Epic | E7 Agent 适配框架 |
| 状态 | `done` |
| 依赖 | E7-S3 |

## 需求

处理 Claude Code 的动态注入语法。

## 验收标准

1. 解析 `{{command}}` 格式注入
2. 解析 `$(shell cmd)` 格式注入
3. 注入标记保留或转换

## 测试用例

```python
def test_parse_injection(): 解析注入语法
def test_no_injection(): 无注入通过
```
