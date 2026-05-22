# Story E8-S5: 加载生命周期管理

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E8-S5 |
| Epic | E8 渐进式加载 |
| 状态 | `done` |
| 依赖 | E8-S1~S3 |

## 需求

管理 skill 加载生命周期和模式切换。

## 验收标准

1. L1 → L2 切换（触发）
2. L2 → L3 切换（引用资源）
3. L3 降级到 L2（释放资源）
4. 生命周期状态追踪

## 测试用例

```python
def test_initial_l1(): 初始为 L1
def test_trigger_l2(): 切换到 L2
def test_trigger_l3(): 切换到 L3
def test_downgrade(): 降级回 L2
```
