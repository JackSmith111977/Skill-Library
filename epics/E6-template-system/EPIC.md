# Epic 6: Skill 模板系统

> **主题**：提供原子 skill 和工作流 skill 的标准化模板，支持快速创建。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E6 |
| 优先级 | P1 |
| Story 数 | 4 |
| 依赖 | 无 |
| 状态 | `pending` |

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E6-S1 | 原子 skill 模板 | `pending` | - |
| E6-S2 | 工作流 skill 模板 | `pending` | - |
| E6-S3 | create 命令 | `pending` | E6-S1, E6-S2 |
| E6-S4 | 模板参数填充 | `pending` | E6-S3 |

## 测试门禁

```bash
# 验收条件
- [ ] 模板生成的 skill 通过 lint 检测
- [ ] create 命令可执行
- [ ] 参数填充正确
- [ ] 目录结构符合规范
```
