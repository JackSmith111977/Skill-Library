# Story E8-S1: L1 元数据加载器

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E8-S1 |
| Epic | E8 渐进式加载 |
| 状态 | `done` |
| 依赖 | E3-S1, E3-S2 |

## 需求

从 SKILL.md frontmatter 提取 name + description。

## 验收标准

1. 仅返回 name 和 description
2. body 不加载
3. 约 100 词以内

## 测试用例

```python
def test_load_metadata(tmp_path): 加载元数据
def test_load_metadata_no_skill(tmp_path): 无 skill 返回空
```
