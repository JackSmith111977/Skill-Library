# Story E5-S2: 编排步骤完整性校验

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E5-S2 |
| Epic | E5 工作流支持 |
| 状态 | `done` |
| 依赖 | - |

## 需求

校验 Pipeline 类型工作流的步骤序号连续性。

## 验收标准

1. 识别 Pipeline 工作流的步骤编号
2. 检查序号是否从 1 开始且连续
3. 序号不连续 → ERROR

## 测试用例

```python
def test_steps_continuous(): 序号连续 → 通过
def test_steps_gap(): 序号有间隔 → ERROR
def test_steps_not_start_from_1(): 不从 1 开始 → ERROR
def test_no_steps(): 无步骤 → 通过
```
