# Story E14-S1: skill-creator 元 skill

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E14-S1 |
| Epic | E14 Skill 创建元技能 |
| 状态 | `done` |
| 依赖 | E6-S1, E6-S2 |

## 需求

创建 `skill-creator` 元 skill，指导 AI Agent 创建符合 Skill Library 标准的原子 skill。

## 验收标准

1. `skills/skill-creator/SKILL.md` 存在，lint 通过
2. Frontmatter 包含 name / description / version / allowed-tools
3. Description 包含第三人称触发短语（引号内）
4. Body 覆盖完整创建流程：需求澄清 → 脚手架 → Frontmatter → Description → Body → References → 验证
5. `skills/skill-creator/references/` 包含 3 个参考文档：
   - `frontmatter-reference.md`（所有字段详细说明）
   - `description-guide.md`（写法规范 + 示例）
   - `quality-standards.md`（lint 规则 + 膨胀阈值）
6. `skills/skill-creator/scripts/` 和 `skills/skill-creator/assets/` 目录存在
