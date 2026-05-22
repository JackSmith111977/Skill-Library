# Story E17-S4: 更新 README + skill 文档

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E17-S4 |
| Epic | E17 CLI 层完全移除 |
| 状态 | `done` |
| 依赖 | - |

## 需求

更新 README.md 和 skill 文档，移除所有 CLI 引用。

## 验收标准

1. README.md 无 CLI 相关段落（可选路径、CLI 参考）
2. README.md 依赖列表无 click/rich
3. skill-manager SKILL.md 附录 CLI 移除
4. cli-examples.md 附录 CLI 移除
5. 版本正确 bump

## 改动文件

| 文件 | 改动 |
|------|------|
| `README.md` | 移除 CLI 路径 + 参考 + 架构表 CLI 行 |
| `skills/skill-manager/SKILL.md` | 移除附录 CLI |
| `skills/skill-manager/references/cli-examples.md` | 移除附录 CLI |
