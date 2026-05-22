# Story E17-S3: 更新文档（PRD/IMPLEMENTATION/CLAUDE）

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E17-S3 |
| Epic | E17 CLI 层完全移除 |
| 状态 | `done` |
| 依赖 | - |

## 需求

更新 PRD.md、IMPLEMENTATION.md、CLAUDE.md，移除所有 CLI 引用。

## 验收标准

1. PRD.md 删除 §5.3 CLI 选配层附录
2. PRD.md 架构图和描述中 CLI 引用清除
3. IMPLEMENTATION.md 所有 CLI 引用清除（配置、架构、部署）
4. CLAUDE.md "CLI 为选配层" 说明移除
5. 版本正确 bump

## 改动文件

| 文件 | 改动 |
|------|------|
| `PRD.md` | 删除 §5.3, 更新架构图, bump 版本 |
| `IMPLEMENTATION.md` | 清除全部 CLI 引用, bump 版本 |
| `CLAUDE.md` | 移除 CLI 选配说明 |
