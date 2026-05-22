# Story E7-S1: AgentAdapter 抽象基类

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E7-S1 |
| Epic | E7 Agent 适配框架 |
| 状态 | `done` |
| 依赖 | - |

## 需求

定义 AgentAdapter 抽象基类和接口。

## 验收标准

1. 定义 `adapt_content()` 方法
2. 定义 `name` / `version` 属性
3. 定义 `target_patterns` 属性
4. 接口完整可扩展

## 测试用例

```python
def test_cannot_instantiate_abstract(): 不能实例化抽象类
def test_concrete_adapter(): 实现接口可实例化
```
