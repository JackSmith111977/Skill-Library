# Story E3-S3: skill 注册函数

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E3-S3 |
| Epic | E3 Skill Registry |
| 状态 | `done` |
| 依赖 | E3-S1, E3-S2 |

## 需求

将扫描到的 skill 注册到 state.json 的 skills 段。

## 验收标准

1. 注册 skill 时写入 state.json skills 段
2. 字段包括：name, path, version, type, design-pattern, category, mount-status, quality-status
3. 重复注册同一 skill 时更新而非新建
4. 注册后 state.json 格式符合 schema

## 测试用例

```python
def test_register_new_skill(tmp_path): 新 skill 注册成功
def test_register_update_existing(tmp_path): 重复注册更新
def test_register_writes_state(tmp_path): 写入 state.json
def test_register_schema_valid(tmp_path): 符合 schema
```
