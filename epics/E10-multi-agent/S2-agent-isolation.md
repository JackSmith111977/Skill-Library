# Story E10-S2: Agent 隔离存储

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E10-S2 |
| Epic | E10 多 Agent 隔离 |
| 状态 | `done` |
| 依赖 | E1-S3 |

## 需求

实现不同 agent 的 skill 状态互不干扰的隔离存储。

## 验收标准

1. 每个 agent 在 state["agents"][id]["skills"] 中有独立存储
2. mount_to_agent 将 skill 挂载到指定 agent
3. unmount_from_agent 从 agent 移除 skill
4. get_agent_skills 返回指定 agent 的 skill 列表
5. 同一 skill 可在不同 agent 有不同状态
