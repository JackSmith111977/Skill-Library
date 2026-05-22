# Story E19-S7: skill-manager 包级操作

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E19-S7 |
| Epic | E19 技能包官方版本化 |
| 状态 | `done` |
| 依赖 | E19-S6 |

## 需求

在 skill-manager SKILL.md 中添加包级操作工作流：列出所有包、查看包信息。

## 验收标准

1. skill-manager 可列出所有已知包及其版本
2. skill-manager 可查询单个包的详细信息
3. 操作通过 Bash + Python 模块调用实现，不依赖 CLI

## 改动

| 文件 | 改动 |
|------|------|
| `skills/skill-manager/SKILL.md` | 新增包操作章节 |
| `src/skill_library/` | 可选：新增 pack 查询工具函数 |
