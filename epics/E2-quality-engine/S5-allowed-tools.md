# Story E2-S5: allowed-tools 格式校验

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E2-S5 |
| Epic | E2 质量检测引擎 |
| 状态 | `pending` |
| 依赖 | 无 |

## 需求

校验 allowed-tools 格式

## 验收标准

1. 空格分隔的工具名列表
2. 每个工具名非空

## 测试用例

```python
def test_valid(): "Read Bash Write" → pass
def test_empty_string(): "" → pass (optional field)
def test_double_space(): "Read  Bash" → fail
```
