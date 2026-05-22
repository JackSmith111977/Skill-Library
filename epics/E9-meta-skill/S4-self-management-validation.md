# Story E9-S4: 元 skill 自管理验证

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E9-S4 |
| Epic | E9 元 Skill |
| 状态 | `done` |
| 依赖 | E9-S1 |

## 需求

验证元 skill 能管理自身：lint → mount → unmount 完整生命周期。

## 验收标准

1. `skill-manager lint skills/skill-manager` 通过（0 exit code）
2. 能通过 registry 注册和查询自身
3. 能完成 mount/unmount 操作
