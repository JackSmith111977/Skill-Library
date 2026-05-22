# Story E5-S3: 硬性门控标记校验

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E5-S3 |
| Epic | E5 工作流支持 |
| 状态 | `done` |
| 依赖 | - |

## 需求

校验 Inversion 类型工作流是否包含门控标记。

## 验收标准

1. 检测 Inversion 工作流
2. 检查是否包含 STAGE_GATE 标记
3. 无门控标记 → WARNING

## 测试用例

```python
def test_has_gate_marker(): 有门控 → 通过
def test_no_gate_marker(): 无门控 → WARNING
def test_not_inversion(): 非 Inversion → 跳过
```
