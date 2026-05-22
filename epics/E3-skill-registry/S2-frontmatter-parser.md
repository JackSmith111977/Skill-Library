# Story E3-S2: frontmatter 解析器

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E3-S2 |
| Epic | E3 Skill Registry |
| 状态 | `done` |
| 依赖 | - |

## 需求

解析 SKILL.md 的 YAML frontmatter，提取结构化元数据。

## 验收标准

1. 解析标准 frontmatter 字段（name, description, version, allowed-tools 等）
2. 处理缺失字段（提供默认值）
3. 处理无 frontmatter 的情况（返回空 dict）
4. 使用 pyyaml 解析（与 lint 模块的简单解析区分）

## 测试用例

```python
def test_parse_full_frontmatter(): 解析完整字段
def test_parse_minimal_frontmatter(): 仅含 name + description
def test_parse_no_frontmatter(): 无 frontmatter 返回空
def test_parse_list_field(): 解析 allowed-tools 列表
def test_parse_multiline_desc(): 解析多行 description（> 折叠）
```
