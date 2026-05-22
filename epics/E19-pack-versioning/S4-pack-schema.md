# Story E19-S4: pack.json Schema 定义

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E19-S4 |
| Epic | E19 技能包官方版本化 |
| 状态 | `done` |

## 需求

定义 pack.json 的 JSON Schema，并提供 Python 校验器。

## 验收标准

1. pack.json Schema 定义：name/version/description/skills/dependencies/updated
2. name: kebab-case, 1-64 字符
3. version: semver
4. 提供 Python 校验函数 `validate_pack_json()`

## 改动

| 文件 | 改动 |
|------|------|
| `src/skill_library/state/schemas.py` | 新增或修改，添加 PackSchema |
