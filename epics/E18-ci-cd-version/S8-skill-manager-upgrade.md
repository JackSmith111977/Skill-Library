# Story E18-S8: skill-manager 升级支持

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E18-S8 |
| Epic | E18 CI/CD + 版本管理 + 升级渠道 |
| 状态 | `done` |
| 依赖 | E18-S7 |

## 需求

在 skill-manager SKILL.md 中添加 Agent 可自主执行的升级工作流。

## 验收标准

1. skill-manager SKILL.md 包含升级工作流章节
2. 工作流步骤：检查版本 → 查询最新 Release → 对比 → 执行升级
3. Agent 可自主执行，无需人工介入

## 改动

| 文件 | 改动 |
|------|------|
| `skills/skill-manager/SKILL.md` | 修改 |
