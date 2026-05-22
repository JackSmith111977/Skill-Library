# Epic 15: skill-manager 元 Skill 重写（Skill 即接口）

> **主题**：按"Skill 即接口"设计哲学重写 skill-manager SKILL.md，从 CLI 命令手册改为直接指导 AI 操作文件 + state.json。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E15 |
| 优先级 | P1 |
| Story 数 | 5 |
| 依赖 | PRD v1.5.0（设计哲学确认）, E9（现有 skill-manager） |
| 状态 | `done` |

## 影响范围

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| `skills/skill-manager/SKILL.md` | 重写 body | ~50 处 CLI 引用 → skill-based 文件操作流程 |
| `skills/skill-manager/references/cli-examples.md` | 重写 | CLI 示例 → skill-based 操作示例 |
| `skills/skill-manager/scripts/scan-and-register.sh` | 更新 | `skill-manager register` → 直接调用 Python 模块 |
| `skills/skill-creator/SKILL.md` | 轻微修改 | 自验证步骤的 CLI 引用改为 Python 直接调用 |
| `skills/workflow-creator/SKILL.md` | 轻微修改 | 同上 |
| `PROGRESS.md` | 新增 | E15 进度追踪 |
| `docs-alignment.json` | 更新 | 版本 bump |

## 不改动的

- Python 模块（quality/state/registry/loader）— 零改动
- CLI 代码（src/skill_library/cli/）— 保留作选配层，不删
- 测试 — 345 测试继续通过，不改
- skill-creator / workflow-creator 的 references 和主体逻辑 — 只改自验证引用

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E15-S1 | SKILL.md body 重写：CLI 命令 → 文件操作流程 | `done` | - |
| E15-S2 | references 重写：cli-examples.md → skill-based 示例 | `done` | E15-S1 |
| E15-S3 | scripts 适配：scan-and-register.sh 改用 Python 模块 | `done` | - |
| E15-S4 | 交叉引用修复：skill-creator + workflow-creator 自验证路径 | `done` | E15-S1 |
| E15-S5 | 自验证 + 文档对齐 | `done` | E15-S1~S4 |

## 测试门禁

```bash
cd "D:\WorkPlace\VibeCoding\Skill Library"
python -m pytest tests/ -q                     # 345 不回归
python -m skill_library.quality.lint skills/skill-manager     # score >= 90
python -m skill_library.quality.lint skills/skill-creator     # 不回归
python -m skill_library.quality.lint skills/workflow-creator  # 不回归
```
