# Story E10-S4: Agent 配置验证

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E10-S4 |
| Epic | E10 多 Agent 隔离 |
| 状态 | `done` |
| 依赖 | E1-S4 |

## 需求

增强 Agent 配置校验，包括类型验证和路径存在性检查。

## 验收标准

1. Agent type 必须是有效枚举值（AgentType）
2. Agent path 必须存在（目录）
3. 校验结果以列表形式返回，不抛出异常
