# Epic 14: Skill 创建元技能

> **主题**：skill-creator 和 workflow-creator 两个元 skill，指导 AI Agent 创建符合项目标准的新 skill。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E14 |
| 优先级 | P3 |
| Story 数 | 2 |
| 依赖 | E6（模板系统）, E13（生态完善） |
| 状态 | `done` |

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E14-S1 | skill-creator 元 skill | `done` | E6-S1, E6-S2 |
| E14-S2 | workflow-creator 元 skill | `done` | E6-S1, E6-S2, E14-S1 |

## 测试门禁

```bash
cd "D:\WorkPlace\VibeCoding\Skill Library"
python -m pytest tests/ -q                          # 全部测试不回归
skill-manager lint skills/skill-creator               # 原子 lint 通过
skill-manager lint skills/workflow-creator            # 工作流 lint 通过
```
