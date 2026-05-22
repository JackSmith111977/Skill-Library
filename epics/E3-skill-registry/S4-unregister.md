# Story E3-S4: skill 注销函数

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E3-S4 |
| Epic | E3 Skill Registry |
| 状态 | `done` |
| 依赖 | E1-S3 |

## 需求

从 state.json 中移除 skill 注册信息。

## 验收标准

1. 注销指定 skill，从 skills 段删除
2. 不存在的 skill 注销时抛出 KeyError 或返回 False
3. 注销后 state.json 格式正确

## 测试用例

```python
def test_unregister_existing(tmp_path): 注销成功
def test_unregister_not_found(): 不存在时抛出异常
def test_unregister_writes_state(tmp_path): state.json 更新
```
