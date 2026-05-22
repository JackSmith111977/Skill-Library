# Story E4-S5: classify 操作

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E4-S5 |
| Epic | E4 状态机引擎 |
| 状态 | `done` |
| 依赖 | E4-S1 |

## 需求

更新 skill 的分类标签。

## 验收标准

1. 更新 design-pattern / category / skill-type
2. 使用枚举值校验
3. state.json 更新正确

## 测试用例

```python
def test_classify_success(): 分类成功
def test_classify_invalid_enum(): 非法枚举值拒绝
```
