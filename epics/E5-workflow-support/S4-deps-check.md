# Story E5-S4: 步骤依赖关系校验

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E5-S4 |
| Epic | E5 工作流支持 |
| 状态 | `done` |
| 依赖 | - |

## 需求

校验步骤间无循环依赖。

## 验收标准

1. 解析步骤依赖关系
2. 检测循环依赖
3. 循环依赖 → ERROR

## 测试用例

```python
def test_no_cycle(): 无循环 → 通过
def test_cycle_detected(): 有循环 → ERROR
def test_no_deps(): 无依赖 → 通过
```
