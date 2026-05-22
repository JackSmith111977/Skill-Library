# Story E2-S1: name 格式校验规则

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E2-S1 |
| Epic | E2 质量检测引擎 |
| 状态 | `pending` |
| 依赖 | 无 |

## 需求

校验 skill name 格式：kebab-case，1-64 字符，与目录名一致

## 验收标准

1. 正则：`^[a-z][a-z0-9-]{0,62}[a-z0-9]$`
2. 不以连字符开头/结尾
3. 无连续连字符
4. 与目录名一致
5. 长度 1-64 字符

## 测试用例

```python
def test_valid_name(): "skill-name" → pass
def test_uppercase(): "Skill-Name" → fail
def test_start_hyphen(): "-skill" → fail
def test_end_hyphen(): "skill-" → fail
def test_double_hyphen(): "skill--name" → fail
def test_too_long(): 65 chars → fail
def test_mismatch_dir(): name != dir → fail
```
