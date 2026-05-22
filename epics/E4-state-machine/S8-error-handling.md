# Story E4-S8: 异常处理

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E4-S8 |
| Epic | E4 状态机引擎 |
| 状态 | `done` |
| 依赖 | E4-S1 |

## 需求

定义和处理状态机异常。

## 验收标准

1. 定义 PreconditionError（前置条件不满足）
2. 定义 InvalidTransitionError（非法状态转换）
3. 所有操作统一异常处理

## 测试用例

```python
def test_precondition_error(): 前置条件异常
def test_invalid_transition_error(): 非法转换异常
```
