# Story E5-S1: 引用原子 skill 存在性校验

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E5-S1 |
| Epic | E5 工作流支持 |
| 状态 | `done` |
| 依赖 | E3-S1 |

## 需求

校验工作流 skill 引用的原子 skill 是否存在。

## 验收标准

1. 解析 body 中引用的 skill 名称
2. 检查引用的 skill 目录是否存在
3. 引用不存在 → ERROR

## 测试用例

```python
def test_ref_exists(tmp_path): 引用存在 → 通过
def test_ref_missing(tmp_path): 引用不存在 → ERROR
def test_no_refs(tmp_path): 无引用 → 通过
```
