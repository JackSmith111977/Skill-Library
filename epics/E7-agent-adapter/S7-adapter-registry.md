# Story E7-S7: 适配器注册表

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E7-S7 |
| Epic | E7 Agent 适配框架 |
| 状态 | `done` |
| 依赖 | E7-S1 |

## 需求

实现适配器注册表，按 agent 名称查找适配器。

## 验收标准

1. `register()` 注册适配器
2. `get()` 按名称查找
3. 不存在时返回通用适配器
4. 同名适配器覆盖

## 测试用例

```python
def test_register_and_get(): 注册和查找
def test_get_not_found(): 不存在返回通用
def test_register_override(): 同名覆盖
```
