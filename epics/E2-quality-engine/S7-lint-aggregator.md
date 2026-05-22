# Story E2-S7: lint 结果聚合器

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E2-S7 |
| Epic | E2 质量检测引擎 |
| 状态 | `pending` |
| 依赖 | E2-S1~S6 |

## 需求

聚合 7 项规则结果，输出 LintResult

## 验收标准

1. 执行全部 7 项规则
2. 输出 LintResult（passed/errors/warnings/score）
3. ERROR 存在 → passed=False
4. score = 100 - errors*10 - warnings*2

## 测试用例

```python
def test_all_pass(): score=100, passed=True
def test_has_error(): passed=False
def test_has_warning(): passed=True, warnings>0
```
