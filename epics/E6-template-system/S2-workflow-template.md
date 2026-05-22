# Story E6-S2: 工作流 skill 模板

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E6-S2 |
| Epic | E6 模板系统 |
| 状态 | `done` |
| 依赖 | - |

## 需求

工作流 skill 标准模板。

## 验收标准

1. 包含 Pipeline 类型工作流结构
2. 包含 Inversion 类型门控结构
3. 符合工作流 lint 规则

## 测试用例

```python
def test_pipeline_template_passes_lint(tmp_path): Pipeline 模板通过 lint
def test_inversion_template_passes_lint(tmp_path): Inversion 模板通过 lint
```
