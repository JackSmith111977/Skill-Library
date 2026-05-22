# Story E4-S6: status 查询

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E4-S6 |
| Epic | E4 状态机引擎 |
| 状态 | `done` |
| 依赖 | E1-S3 |

## 需求

查询 skill 当前状态。

## 验收标准

1. 返回 skill 的完整状态信息
2. 不存在的 skill 返回 None

## 测试用例

```python
def test_status_query(): 查询成功
def test_status_not_found(): 不存在返回 None
```
