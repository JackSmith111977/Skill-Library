# Story E6-S4: 模板参数填充

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E6-S4 |
| Epic | E6 模板系统 |
| 状态 | `done` |
| 依赖 | E6-S3 |

## 需求

模板变量替换和参数填充。

## 验收标准

1. {{name}} → skill 名称
2. {{description}} → 描述
3. {{version}} → 版本号
4. {{pack}} → pack 名称

## 测试用例

```python
def test_fill_name(): 填充名称
def test_fill_description(): 填充描述
def test_fill_all_vars(): 填充所有变量
def test_missing_var_keeps_placeholder(): 缺失变量保留占位符
```
