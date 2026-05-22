# CLAUDE.md

> 版本：1.4.0 | 更新：2026-05-22

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目定位

Agent Skill Library — 跨项目的 skill 管理系统。元 skill 管理其他 skill 的全生命周期。详细需求见 `PRD.md`。

## 文档体系

| 文档 | 用途 | 更新时机 |
|------|------|----------|
| `PRD.md` | 产品需求（What + Why） | 需求变更时 |
| `IMPLEMENTATION.md` | 实现技术（How） | 架构/模块设计变更时 |
| `PROGRESS.md` | 开发进度索引（Status） | Story 状态变更时 |
| `epics/<Epic>/EPIC.md` | Epic 概述 | Epic 变更时 |
| `epics/<Epic>/S*-*.md` | Story 详情 | Story 变更时 |
| `CLAUDE.md` | 开发规则（Rules） | 规则变更时 |
| `docs-alignment.json` | 文档对齐状态 | 版本变更时 |

## 开发流程

### Epic / Story 结构

实现按 Epic → Story 两级拆分：
- **Epic**：一个实现主题，包含多个原子化 Story
- **Story**：最小可交付单元，有明确验收标准

### Story 状态机

```
pending → in_progress → testing → done
                ↓
            blocked（依赖未满足）
```

**状态变更规则**：
- `pending → in_progress`：开始开发
- `in_progress → testing`：开发完成，提交测试
- `testing → done`：测试通过，验收完成
- `in_progress → blocked`：依赖未满足或有问题
- `blocked → pending`：问题解决，重新排队

### 开发原则（强制）

**每次开发必须遵循以下流程**：

#### 1. 开始前

```
读取 Story 文件（epics/<Epic>/S*-*.md）
    ↓
理解需求和验收标准
    ↓
更新 Story 状态：pending → in_progress
    ↓
更新 PROGRESS.md 进度日志
```

#### 2. 开发中

```
按 Story 验收标准实现
    ↓
编写测试用例
    ↓
执行测试门禁（Epic EPIC.md 中定义）
```

#### 3. 开发后

```
测试通过
    ↓
更新 Story 状态：in_progress → testing → done
    ↓
更新 PROGRESS.md 进度日志
    ↓
对齐文档（docs-alignment.json）
    ↓
提交代码
```

#### 4. 状态更新位置

| 文件 | 更新内容 |
|------|----------|
| `epics/<Epic>/S*-*.md` | Story 状态字段 |
| `epics/<Epic>/EPIC.md` | Epic 状态（所有 Story 完成后） |
| `PROGRESS.md` | 进度日志 |
| `docs-alignment.json` | 文档版本对齐 |

### 进度跟踪

- 每个 Story 状态变更时，更新对应 Story 文件和 `PROGRESS.md`
- 测试门禁写在各 Epic 的 EPIC.md 中，作为验收条件
- 阻塞问题记录在进度日志中

## Skill 格式规范

每个 skill 是一个目录，必须包含 `SKILL.md`。分两类：原子 skill（单一任务）和工作流 skill（编排多个原子 skill）。

```
skill-name/
├── SKILL.md                    # 必需：通用版本（YAML frontmatter + Markdown body）
├── agents/                     # 可选：Agent 适配版本
│   ├── claude-code/SKILL.md    # Claude Code 版
│   ├── hermes/SKILL.md         # Hermes 版
│   └── ...
├── references/                 # 可选：按需加载的参考文档（共享）
├── scripts/                    # 可选：可执行脚本（共享）
├── temp/                       # 可选：过程文件
└── assets/                     # 可选：模板、资源文件（共享）
```

**Agent 适配规则**：
- 通用 `SKILL.md` 是默认版本，必须存在
- `agents/<agent-name>/SKILL.md` 是特定 agent 适配版本，可选
- 安装时优先使用匹配的 agent 版本，无匹配则降级到通用版本
- 共享资源（references/scripts/assets）对所有 agent 版本通用

### Frontmatter

```yaml
---
name: skill-name              # 必需，kebab-case，1-64 字符
description: >                # 必需，触发条件，1-1024 字符
  This skill should be used when the user asks to "xxx", "yyy".
version: 0.1.0                # 可选
allowed-tools: [Read, Bash]   # 可选
---
```

### Description 写法

- 第三人称："This skill should be used when..."
- 含具体触发短语（引号内），宁可偏激进
- **只描述触发条件，不要总结工作流程**

### Body 写法

- 祈使句/不定式（动词开头）
- 推荐 1500-2000 词，上限 5000 词、500 行
- 详细内容放 `references/`，保持精简

### 三级加载

1. **元数据**（name + description）— 始终在上下文
2. **SKILL.md body** — 触发时加载
3. **Bundled resources** — 按需加载

## 目录结构

```
Skill Library/
├── CLAUDE.md                   # 本文件（开发规则）
├── PRD.md                      # 产品需求文档
├── IMPLEMENTATION.md           # 实现技术文档
├── PROGRESS.md                 # 开发进度索引
├── docs-alignment.json         # 文档对齐状态机
├── epics/                      # Epic/Story 独立文件
│   ├── E1-data-foundation/
│   │   ├── EPIC.md             # Epic 概述
│   │   ├── S1-state-schema.md  # Story 独立文件
│   │   └── ...
│   ├── E2-quality-engine/
│   └── ...
├── config.json                 # 技能库配置
├── state.json                  # 状态机（single source of truth）
├── skills/                     # Skill 仓库（按技能包组织）
│   └── <pack-name>/
│       ├── <skill-name>/      # 原子 skill
│       └── <workflow-name>/   # 工作流 skill
├── quality/                    # 质量检测
│   ├── lint-atomic.py          # 原子 skill 7 项检测
│   ├── lint-workflow.py        # 工作流 4 项额外检测
│   └── rules/
├── research/                   # 调研文档
└── templates/                  # Skill 模板
```

## 开发约定

- Skill 命名：kebab-case，动词或名词短语
- 版本管理：语义化版本（MAJOR.MINOR.PATCH）
- 质量检测：每个 skill 提交前运行 lint（原子 7 项 + 工作流 4 项）
- 分类：每个 skill 必须声明 pack + type + design-pattern + skill-type
- Agent 适配：通用 SKILL.md 必须存在，agent 版本可选，降级到通用版本
- 状态机驱动：所有管理操作必须读状态 → 前置检查 → 执行 → 写状态
- 元 skill 自管理：管理功能本身也是标准 skill
