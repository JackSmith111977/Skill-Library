# Story E16-S2: README.md 全文重写（Skill-first）

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E16-S2 |
| Epic | E16 用户文档体系完善 |
| 状态 | `done` |
| 依赖 | E16-S1 |

## 需求

按 PRD §12 规范，将 README.md 从 CLI-centric 重写为 Skill-first 结构。

## 验收标准

1. Quick Start 分双路径：Primary（cp -r any-agent）> Optional（pip install）
2. 包含 For Agents 段落：安装步骤 + 前提 + 快速用法
3. 包含 For Humans 段落：CLI 参考（标注"可选"）+ 精简架构
4. 项目状态更新：15 Epics / 76 Stories / 345 tests，含 E15 行
5. 保留原 README 中正确的技术内容（skill 目录树、分类、三级加载、文档索引、开发命令）
6. 版本从 1.0.0 → 1.1.0

## 改动文件

| 文件 | 改动 |
|------|------|
| `README.md` | 全文重写 |
