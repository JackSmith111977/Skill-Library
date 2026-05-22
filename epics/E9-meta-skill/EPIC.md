# Epic 9: Skill Manager 元 Skill

> **主题**：将管理功能本身封装为标准格式的元 skill。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E9 |
| 优先级 | P1 |
| Story 数 | 4 |
| 依赖 | E2, E4, E5, E6 |
| 状态 | `done` |

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E9-S1 | skill-manager SKILL.md | `done` | E2-S8, E4-S7 |
| E9-S2 | skill-manager references | `done` | - |
| E9-S3 | skill-manager scripts | `done` | - |
| E9-S4 | 元 skill 自管理验证 | `done` | E9-S1 |

## 测试门禁

```bash
# 验收条件
- [ ] SKILL.md 通过 lint 检测
- [ ] description 包含正确触发词
- [ ] 所有命令可执行
- [ ] 元 skill 能管理自身（mount/unmount/lint）
```
