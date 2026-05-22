# Story E5-S5: 工作流 lint 入口

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E5-S5 |
| Epic | E5 工作流支持 |
| 状态 | `done` |
| 依赖 | E5-S1~S4, E2-S7 |

## 需求

整合工作流 lint 到 QualityEngine。

## 验收标准

1. `lint_workflow()` 执行 4 项工作流规则
2. 与 `lint_atomic()` 共享基础规则
3. 返回 LintResult

## 测试用例

```python
def test_workflow_lint_valid(): 合法工作流 → 通过
def test_workflow_lint_invalid(): 非法工作流 → 失败
```
