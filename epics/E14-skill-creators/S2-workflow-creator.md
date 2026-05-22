# Story E14-S2: workflow-creator 元 skill

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E14-S2 |
| Epic | E14 Skill 创建元技能 |
| 状态 | `done` |
| 依赖 | E6-S1, E6-S2, E14-S1 |

## 需求

创建 `workflow-creator` 元 skill，指导 AI Agent 创建符合 Skill Library 标准的工作流 skill（pipeline / inversion）。

## 验收标准

1. `skills/workflow-creator/SKILL.md` 存在，lint 通过
2. Frontmatter 包含 name / description / version / allowed-tools
3. Description 包含第三人称触发短语（引号内）
4. Body 覆盖：模式选择 → 同包原子 skill 检查 → 脚手架 → 步骤编排 → 门控标记 → 循环依赖检测 → 验证
5. Body 分别覆盖 pipeline（线性多步）和 inversion（先采访后执行）两种模式
6. `skills/workflow-creator/references/` 包含 2 个参考文档：
   - `pipeline-pattern.md`（Pipeline 模式结构 + 示例）
   - `inversion-pattern.md`（Inversion 模式 + STAGE_GATE 用法）
7. `skills/workflow-creator/scripts/` 和 `skills/workflow-creator/assets/` 目录存在
