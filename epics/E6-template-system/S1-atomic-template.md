# Story E6-S1: 原子 skill 模板

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E6-S1 |
| Epic | E6 模板系统 |
| 状态 | `done` |
| 依赖 | - |

## 需求

原子 skill 标准模板。

## 验收标准

1. 包含完整 frontmatter
2. 包含 body 占位符
3. references/ assets/ 目录

## 测试用例

```python
def test_atomic_template_passes_lint(tmp_path): 模板生成的 skill 通过 lint
def test_template_directory_structure(tmp_path): 目录结构正确
```
