# Story E6-S3: create 命令

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E6-S3 |
| Epic | E6 模板系统 |
| 状态 | `done` |
| 依赖 | E6-S1, E6-S2 |

## 需求

`skill-manager create` 命令创建新 skill。

## 验收标准

1. 创建 atom 类型 skill
2. 创建 workflow 类型 skill
3. 创建指定 pack 下的 skill
4. 创建成功后输出路径

## 测试用例

```python
def test_create_atomic(runner): 创建原子 skill
def test_create_workflow(runner): 创建工作流 skill
def test_create_with_pack(runner): 指定 pack
```
