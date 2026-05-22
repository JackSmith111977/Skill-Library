# Story E13-S3: 社区 skill 模板库

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E13-S3 |
| Epic | E13 生态完善 |
| 状态 | `done` |
| 依赖 | E6-S1, E6-S2 |

## 需求

创建社区 skill 模板库，提供开箱即用的 skill 模板。

## 验收标准

1. templates/ 目录包含常用 skill 模板
2. 每个模板包含 SKILL.md + references/ 骨架
3. 模板可被 `skill-manager create --from-template` 使用
