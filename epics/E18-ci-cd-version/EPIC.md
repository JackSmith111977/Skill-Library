# Epic 18: CI/CD + 版本管理 + 升级渠道

> **主题**：建立 GitHub Actions CI、统一版本管理、Epic 完成时自动 Release、Agent 快捷升级渠道。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E18 |
| 优先级 | P1 |
| Story 数 | 9 |
| 依赖 | E17（CLI 移除已完毕，项目进入稳定期） |
| 状态 | `done` |

## 影响范围

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| `PRD.md` | 修改 | 新增 §13 CI/CD 与版本管理、§14 技能包版本化 |
| `IMPLEMENTATION.md` | 修改 | 新增 §9 CI/CD 与版本管理 |
| `research/ci-cd-and-version-management.md` | 新建 | 调研文档 |
| `.bumpversion.toml` | 新建 | bump-my-version 配置 |
| `src/skill_library/__init__.py` | 修改 | 版本号更新 |
| `.github/workflows/ci.yml` | 新建 | CI 工作流 |
| `.github/workflows/release.yml` | 新建 | Release 工作流 |
| `scripts/upgrade.sh` | 新建 | Linux/macOS 升级脚本 |
| `scripts/upgrade.ps1` | 新建 | Windows 升级脚本 |
| `skills/skill-manager/SKILL.md` | 修改 | 添加升级工作流 |
| `docs-alignment.json` | 修改 | 版本同步 |
| `PROGRESS.md` | 修改 | 进度日志 |

## 不改动的

- 核心 Python 模块（state/quality/registry/loader/adapters/templates）— 零改动
- 现有测试 — 零改动
- 现有 skill 的 body — 仅 skill-manager 添加升级章节

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E18-S1 | PRD 更新 | `done` | - |
| E18-S2 | 网络调研 | `done` | - |
| E18-S3 | IMPLEMENTATION.md 更新 | `done` | E18-S1, S2 |
| E18-S4 | 版本管理工具配置 | `done` | - |
| E18-S5 | GitHub Actions CI 配置 | `done` | E18-S4 |
| E18-S6 | GitHub Actions Release 配置 | `done` | E18-S5 |
| E18-S7 | 升级脚本 | `done` | - |
| E18-S8 | skill-manager 升级支持 | `done` | E18-S7 |
| E18-S9 | Epic 文档 + 验证 | `done` | E18-S4~S8 |

## 测试门禁

```bash
pytest tests/ -q                              # all tests pass
python -m skill_library.quality.lint skills/*  # lint >=90
git tag --list | grep -q "v"                   # at least 1 version tag exists
```
