# Story E3-S5: skill 查询接口

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E3-S5 |
| Epic | E3 Skill Registry |
| 状态 | `done` |
| 依赖 | E1-S3 |

## 需求

提供 skill 查询功能，支持按名称、分类、状态等条件查询。

## 验收标准

1. 按 name 查询单个 skill
2. 按 category / type / design-pattern 过滤
3. 返回 skill 信息 dict 或 None
4. 列出所有已注册 skill

## 测试用例

```python
def test_query_by_name(): 按名称查询
def test_query_not_found(): 不存在返回 None
def test_query_by_category(): 按分类过滤
def test_query_list_all(): 列出全部
```
