# Story E15-S4: 交叉引用修复

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E15-S4 |
| Epic | E15 skill-manager 元 Skill 重写 |
| 状态 | `done` |
| 依赖 | E15-S1 |

## 需求

更新 skill-creator 和 workflow-creator 中对 CLI 的引用，对齐"Skill 即接口"设计哲学。

## 受影响文件

| 文件 | 行 | 当前内容 | 改为 |
|------|-----|----------|------|
| `skills/skill-creator/SKILL.md` | ~143 | `skill-manager lint skills/<pack>/<name>` | `python -m skill_library.quality.lint skills/<pack>/<name>` |
| `skills/workflow-creator/SKILL.md` | ~145 | `skill-manager lint skills/<pack>/<workflow-name>` | `python -m skill_library.quality.lint skills/<pack>/<workflow-name>` |

## 验收标准

1. skill-creator 自验证步骤不再强制要求 CLI
2. workflow-creator 自验证步骤不再强制要求 CLI
3. 其他内容不变
4. 两个 skill lint 通过

## 注意

仅改自验证路径。skill-creator/workflow-creator 的 references 和主体逻辑不动。
