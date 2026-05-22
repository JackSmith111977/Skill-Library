# Story E2-S8: lint CLI 命令

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E2-S8 |
| Epic | E2 质量检测引擎 |
| 状态 | `done` |
| 依赖 | E2-S7 |

## 需求

实现 lint CLI 命令

## 验收标准

1. `skill-manager lint <skill-name>` 可执行
2. 输出可读的检测报告
3. 返回码：0=通过，1=失败

## 测试用例

```python
def test_lint_pass(): exit code 0
def test_lint_fail(): exit code 1
def test_output_format(): contains errors/warnings
```
