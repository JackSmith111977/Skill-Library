# Story E10-S3: 按 Agent 过滤查询

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E10-S3 |
| Epic | E10 多 Agent 隔离 |
| 状态 | `done` |
| 依赖 | E3-S5 |

## 需求

实现按 agent 过滤的 registry 查询功能。

## 验收标准

1. query_by_agent(agent_id) 返回该 agent 挂载的所有 skill
2. query_by_agent_type(agent_type) 返回该类型的所有 agent
3. list_agents() 返回所有注册 agent
