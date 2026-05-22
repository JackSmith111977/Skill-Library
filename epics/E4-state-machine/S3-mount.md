# Story E4-S3: mount 操作

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E4-S3 |
| Epic | E4 状态机引擎 |
| 状态 | `done` |
| 依赖 | E4-S1, E4-S2 |

## 需求

将 skill mount 到指定 agent。

## 验收标准

1. mount 后 skill 的 mount-status 变为 mounted
2. 记录 mount 的 agent-id
3. 前置检查：quality-status 必须为 passed

## 测试用例

```python
def test_mount_success(): mount 成功
def test_mount_updates_state(): state.json 更新
def test_mount_records_agent(): 记录 agent-id
```
