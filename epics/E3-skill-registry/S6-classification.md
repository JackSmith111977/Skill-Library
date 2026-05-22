# Story E3-S6: 二维分类标记

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E3-S6 |
| Epic | E3 Skill Registry |
| 状态 | `done` |
| 依赖 | E3-S3 |

## 需求

注册时自动从 frontmatter 提取并写入二维分类字段。

## 验收标准

1. 从 frontmatter metadata 提取 design-pattern 和 skill-type
2. 缺失时使用默认值（design-pattern=tool-wrapper, skill-type=atomic）
3. 写入 state.json 时使用枚举值

## 测试用例

```python
def test_extract_classification(): 从 metadata 提取
def test_default_classification(): 缺失时用默认值
def test_write_to_state(): 写入 state.json
```
