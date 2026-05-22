# Story E4-S2: 前置检查器

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E4-S2 |
| Epic | E4 状态机引擎 |
| 状态 | `done` |
| 依赖 | E1-S5 |

## 需求

操作执行前检查前置条件是否满足。

## 验收标准

1. mount 前检查 quality-status == passed
2. unmount 前检查 mount-status == mounted
3. classify 前检查 skill 已注册
4. 前置检查失败抛出 PreconditionError

## 测试用例

```python
def test_mount_requires_passed(): 未通过质量检测不能 mount
def test_unmount_requires_mounted(): 未 mounted 不能 unmount
def test_classify_requires_registered(): 未注册不能 classify
```
