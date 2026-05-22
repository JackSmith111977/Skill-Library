# Story E4-S4: unmount 操作

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E4-S4 |
| Epic | E4 状态机引擎 |
| 状态 | `done` |
| 依赖 | E4-S1 |

## 需求

将 skill 从 agent unmount。

## 验收标准

1. unmount 后 mount-status 变为 unmounted
2. 前置检查：必须已 mounted
3. state.json 更新正确

## 测试用例

```python
def test_unmount_success(): unmount 成功
def test_unmount_updates_state(): state.json 更新
```
