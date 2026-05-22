# Skill Library

> 版本：1.2.0 | 更新：2026-05-23

跨项目 Agent Skill 管理系统。**Skill 即接口** — 通过 meta-skill SKILL.md 管理技能全生命周期，零运行时依赖。

零运行时依赖：mount = `cp -r`，unmount = `rm -rf`，任何支持 agentskills.io 标准的 Agent 可直接使用。

---

## 快速开始

### 安装

```bash
# 复制元 skill 到 Agent 技能目录
cp -r skills/skill-manager <agent-skill-dir>/skill-manager
cp -r skills/skill-creator <agent-skill-dir>/skill-creator
cp -r skills/workflow-creator <agent-skill-dir>/workflow-creator

# 安装 Python 依赖（lint 用）
pip install -r requirements.txt
```

Agent 自动识别 SKILL.md，按指引执行管理操作。

---

## 核心概念

### 设计哲学：Skill 即接口

```
┌──────────────────────────────────────────┐
│  Skill 层（主接口）                       │
│  skill-manager SKILL.md                  │
│  指导 AI 直接操作文件和 state.json         │
├──────────────────────────────────────────┤
│  工具库层（Python 模块）                  │
│  quality/ state/ registry/ loader        │
│  被 SKILL.md 通过 Bash 调用              │
└──────────────────────────────────────────┘
```

### 管理操作映射

| 操作 | 机制 | 前置检查 | 状态变更 |
|------|------|----------|----------|
| mount | `cp -r <skill> <agent-dir>/<name>/` | quality=passed | agents.skills 写入 mounted |
| unmount | `rm -rf <agent-dir>/<name>/` | 已挂载 | agents.skills 清除 |
| lint | `python -m skill_library.quality.lint <path>` | skill 存在 | skills 写入 quality-status |
| register | 扫描目录 + 写 state.json | 目录存在 | skills 段新增条目 |
| status | 读 state.json | 无（只读） | 无 |

### Skill 格式

每个 skill 是一个目录，必须包含 `SKILL.md`：

```
skill-name/
├── SKILL.md              # 主文档（YAML frontmatter + Markdown body）
├── agents/               # Agent 适配版本（可选）
│   └── claude-code/SKILL.md
├── references/           # 参考文档（按需加载）
├── scripts/              # 可执行脚本
└── assets/               # 模板、资源文件
```

### Skill 分类

两个维度：

**设计模式**（Google ADK 5 种）：Tool Wrapper | Generator | Reviewer | Inversion | Pipeline

**Skill 类型**（Writing-Skills 4 种）：discipline | technical | mindset | reference

### 三级加载机制

| 层级 | 加载内容 | 时机 | Token 成本 |
|------|----------|------|-----------|
| L1 元数据 | name + description | 会话启动 | ~50-100/skill |
| L2 指令 | 完整 SKILL.md body | skill 触发 | <5000 tokens |
| L3 资源 | references/scripts/assets | 按需引用 | 视文件大小 |

20 个 skill 时初始加载仅 1000-2000 tokens，比单体提示词减少约 90%。

---

## For Agents

本段面向发现此项目的 AI Agent。如需安装此系统的管理功能：

### 安装

```bash
# 1. 前提：确认有 Python 3.11+（lint 用）
python --version

# 2. 安装 Python 依赖
pip install -r requirements.txt

# 3. 复制元 skill 到你的技能目录
cp -r skills/skill-manager <your-skill-dir>/skill-manager
```

### 使用

当用户要求管理技能时，加载 `skill-manager` 并遵循其 SKILL.md 指引：

1. **Lint** — `python -m skill_library.quality.lint <path>`
2. **Mount** — `cp -r <from> <to>` + 更新 state.json（mount-status: mounted）
3. **Unmount** — `rm -rf <path>` + 更新 state.json（清除条目）
4. **Register** — 扫描目录 + 解析 frontmatter + 写入 state.json

三个元 skill 的职责：

| 元技能 | 触发场景 |
|--------|----------|
| `skill-manager` | 用户要求"管理/安装/卸载 skill"时 |
| `skill-creator` | 用户要求"创建一个 skill"时 |
| `workflow-creator` | 用户要求"创建工作流 skill"时 |

---

## For Humans

### 架构

| 模块 | 职责 |
|------|------|
| **State Machine** | 状态机引擎，所有操作的 single source of truth |
| **Quality Engine** | 11 项 lint 规则 + description 质量评估 + 膨胀检测 |
| **Skill Registry** | skill 扫描、注册、索引、查询 |
| **Progressive Loader** | 三级加载 + LRU 淘汰 + 生命周期管理 |
| **Template Engine** | 原子/工作流 skill 模板，9 种设计模式 |
| **Agent Adapter** | 通用 ↔ 特定 agent 格式转换 |

Profile 驱动质量检测：`generic`（开放标准）| `skill-library`（默认，项目扩展）| `claude-code`（Claude Code 扩展）。

---

## 项目状态

**17 个 Epic，84 个 Story，333 个测试 — 全部通过。**

| Epic | 主题 | Story 数 | 状态 |
|------|------|----------|------|
| E1 | 数据基础层 | 5 | done |
| E2 | 质量检测引擎 | 8 | done |
| E3 | Skill Registry | 6 | done |
| E4 | 状态机引擎 | 8 | done |
| E5 | 工作流 Skill 支持 | 5 | done |
| E6 | Skill 模板系统 | 4 | done |
| E7 | Agent 适配框架 | 7 | done |
| E8 | 渐进式加载 | 6 | done |
| E9 | Skill Manager 元 Skill | 4 | done |
| E10 | 多 Agent 隔离 | 4 | done |
| E11 | LRU 淘汰策略 | 4 | done |
| E12 | Description 质量评估 | 4 | done |
| E13 | 生态完善 | 4 | done |
| E14 | Skill 创建元技能 | 2 | done |
| E15 | Meta-Skill "Skill 即接口" 重写 | 5 | done |
| E16 | 用户文档体系完善 | 3 | done |
| E17 | CLI 层完全移除 | 5 | done |

详细进度见 [PROGRESS.md](PROGRESS.md)。

---

## 文档索引

| 文档 | 用途 |
|------|------|
| [PRD.md](PRD.md) | 产品需求（What + Why） |
| [IMPLEMENTATION.md](IMPLEMENTATION.md) | 实现技术（How） |
| [CLAUDE.md](CLAUDE.md) | 开发规则（Rules） |
| [PROGRESS.md](PROGRESS.md) | 开发进度（Status） |
| [epics/](epics/) | Epic/Story 详情 |
| [research/](research/) | 调研文档 |

---

## 开发

```bash
# 运行全部测试
python -m pytest

# 运行单个测试文件
python -m pytest tests/test_quality/test_lint.py -v

# 安装可编辑模式
pip install -e .

# Lint 项目所有 skill
for dir in skills/*/; do python -m skill_library.quality.lint "$dir"; done
```

依赖：Python 3.11+, pyyaml, jsonschema, gitpython
