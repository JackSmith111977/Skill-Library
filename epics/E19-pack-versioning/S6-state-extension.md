# Story E19-S6: state.json 扩展包版本字段

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E19-S6 |
| Epic | E19 技能包官方版本化 |
| 状态 | `done` |
| 依赖 | E19-S5 |

## 需求

在 state.json 的 skills 索引中增加 `pack-version` 字段，追踪每个 skill 所属包的版本。

## 验收标准

1. state.json 中每个 skill 条目有 `pack-version` 字段
2. Pack 版本变更时，所有同 pack skill 的 pack-version 同步更新
3. 向后兼容：缺少 pack-version 的旧条目不报错

## 改动

| 文件 | 改动 |
|------|------|
| `src/skill_library/state/enums.py` | 新增 pack-version 字段 |
| `src/skill_library/registry/indexer.py` | 注册时读 pack.json 填 pack-version |
| `state.json` | 更新 |
