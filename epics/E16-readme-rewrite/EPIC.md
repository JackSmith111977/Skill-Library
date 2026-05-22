# Epic 16: 用户文档体系完善（README 重写）

> **主题**：按"Skill 即接口"设计哲学重写 README.md，从 CLI-first 改为 meta-skill-first。同步更新 PRD 用户文档规范。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E16 |
| 优先级 | P2 |
| Story 数 | 3 |
| 依赖 | E15（Skill 即接口设计哲学已确定）, PRD v1.5.0 |
| 状态 | `done` |

## 影响范围

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| `PRD.md` | 新增 §12 | 用户文档规范（README 要求、安装路径规范、AGENTS.md 概念）|
| `README.md` | 全文重写 | CLI-centric → Skill-first，双路径 Quick Start，For Agents 段落 |
| `docs-alignment.json` | 版本 bump | PRD/README 版本 + 日期同步 |

## 不改动的

- IMPLEMENTATION.md — 已对齐（v1.5.0）
- CLAUDE.md — 已对齐（v1.6.1）
- PROGRESS.md — 仅追加 E16 进度记录
- 任何 Python 代码 / skill 文件 / 测试

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E16-S1 | PRD.md 新增 §12 用户文档规范 | `done` | - |
| E16-S2 | README.md 全文重写（Skill-first） | `done` | E16-S1 |
| E16-S3 | 文档对齐 + 最终验证 | `done` | E16-S1, E16-S2 |

## 测试门禁

```bash
cd "D:\WorkPlace\VibeCoding\Skill Library"
grep -n "cp -r" README.md                            # >=2
grep -c "E15" README.md                               # >=1
grep -c "345" README.md                               # >=1
python -m pytest tests/ -q                            # 345 不回归
python -m skill_library.quality.lint skills/skill-manager  # >=90
```
