# Story E9-S1: skill-manager SKILL.md

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E9-S1 |
| Epic | E9 元 Skill |
| 状态 | `done` |
| 依赖 | E2-S8, E4-S7 |

## 需求

创建 `skills/skill-manager/SKILL.md`，将管理功能封装为标准格式的元 skill。

## 验收标准

1. 符合标准 SKILL.md 格式（frontmatter + body）
2. description 包含正确触发词（manage/create/lint skill）
3. body 覆盖 skill-manager CLI 全部命令
4. 通过 lint 检测（原子 skill 7 项）

## 内容大纲

- 项目定位和架构
- CLI 命令参考（create/lint/load）
- Skill 生命周期管理
- 分类体系说明
