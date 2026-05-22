# Story E10-S1: Agent 注册

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E10-S1 |
| Epic | E10 多 Agent 隔离 |
| 状态 | `done` |
| 依赖 | E1-S2 |

## 需求

实现 Agent 在 state.json 中的注册和注销功能。

## 验收标准

1. register_agent(agent_id, agent_type, path) 创建 agent 条目
2. unregister_agent(agent_id) 移除 agent 条目
3. Agent 条目包含 path、agent-type、skills 字段
4. 重复注册抛出异常
