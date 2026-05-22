# Story E4-S1: 状态机引擎核心

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E4-S1 |
| Epic | E4 状态机引擎 |
| 状态 | `done` |
| 依赖 | E1-S3 |

## 需求

实现状态机核心，定义合法状态转换和执行转换的函数。

## 验收标准

1. 定义 mount-status 状态转换表
2. 定义 quality-status 状态转换表
3. `transition()` 函数执行合法转换，拒绝非法转换
4. 非法转换抛出 ValueError

## 测试用例

```python
def test_valid_mount_transition(): mounted → unmounted 合法
def test_invalid_mount_transition(): mounted → passed 非法
def test_valid_quality_transition(): unchecked → passed 合法
def test_invalid_quality_transition(): passed → unchecked 非法
```
