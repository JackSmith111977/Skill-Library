# Story E2-S4: 文件引用有效性校验

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E2-S4 |
| Epic | E2 质量检测引擎 |
| 状态 | `pending` |
| 依赖 | 无 |

## 需求

校验 SKILL.md 中引用的文件是否存在

## 验收标准

1. 扫描 `[text](path)` 格式
2. 检查 references/scripts/assets 下文件存在
3. 不存在 → ERROR

## 测试用例

```python
def test_valid_ref(): "[doc](references/doc.md)" exists → pass
def test_missing_ref(): "[doc](references/missing.md)" → fail
def test_external_url(): "[site](https://...)" → skip
```
