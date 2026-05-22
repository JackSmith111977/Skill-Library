# Story E13-S1: CLI 入口封装

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E13-S1 |
| Epic | E13 生态完善 |
| 状态 | `done` |
| 依赖 | E2-S8, E4-S7, E6-S3 |

## 需求

整合所有 CLI 命令为统一的入口，确保 create/lint/load 全部可用。

## 验收标准

1. `skill-manager --help` 显示全部命令
2. create/lint/load 子命令 help 正确
3. 所有命令 exit code 正确
