# Story E15-S2: references 重写

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E15-S2 |
| Epic | E15 skill-manager 元 Skill 重写 |
| 状态 | `done` |
| 依赖 | E15-S1 |

## 需求

重写 `skills/skill-manager/references/cli-examples.md`，从 CLI 示例改为 skill-based 操作示例。

## 验收标准

1. cli-examples.md 改为 skill-based 操作步骤，非 CLI 命令
2. 每个操作含具体步骤（文件路径、命令、state 变更）
3. 覆盖 mount/unmount/lint/register 完整工作流
4. 含多 Agent 场景示例
5. CLI 命令仅以附录形式存在

## 内容大纲

- 完整工作流（skill-based）：
  1. lint 检查质量
  2. register 到 state.json
  3. mount 到指定 agent
  4. 验证挂载状态
  5. unmount 移除
- 多 Agent 场景：同一 skill 挂载到多个 agent
- 附录：CLI 等效命令（供参考）
