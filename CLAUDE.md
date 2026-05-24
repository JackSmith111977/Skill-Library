# CLAUDE.md

> 版本：1.7.0 | 更新：2026-05-24

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
| `LESSONS.md` | 项目教训记录 | 新问题发现时 |

## 需求新增流程

新增需求必须按以下顺序执行，不可跳步：

```
Step 1: PRD 更新
    ↓
Step 2: 网络调研（确认技术选型与架构）
    ↓
Step 3: IMPLEMENTATION.md 更新（架构设计）
    ↓
Step 4: 分解为 Epic → 原子 Story
    ↓
Step 5: 按 Story 开发实现
```

**各步骤产出**：

| 步骤 | 产出 | 说明 |
|------|------|------|
| Step 1 | `PRD.md` 更新 | 新增需求写入 PRD，明确 What + Why |
| Step 2 | 调研摘要写入 `research/` | 网络搜索确认最佳实现方案，引用来源 |
| Step 3 | `IMPLEMENTATION.md` 更新 | 架构设计、模块划分、接口定义 |
| Step 4 | `epics/<Epic>/` 目录 | EPIC.md + 原子 Story 文件 |
| Step 5 | 代码 + 测试 | 按 Epic → Story 开发流程实现 |

**调研规则**：
- 必须使用网络搜索确认技术选型，不自作假设
- 调研结果写入 `research/<topic>.md`
- 引用来源需标注可信度（🥇官方/🥈权威/🥉参考）

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
提交前自检（见 § 提交前检查清单）
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

### 提交前检查清单

每次提交前必须执行以下检查，全部通过后方可提交：

```
□ 测试通过：python -m pytest tests/ -q
□ 文档对齐：docs-alignment.json 版本号与 PRD/README/IMPLEMENTATION 实际版本一致
□ 日期同步：docs-alignment.json 中所有文档 updated 日期 >= last-alignment
□ 文档变更同步：改了什么文档，就在 docs-alignment.json 中同步更新其版本信息
□ IMPLEMENTATION.md 同步：IMPLEMENTATION.md 与当前代码架构一致（如架构变更）
□ Skill lint：改动了 skill 文件时运行 lint（python -m skill_library.quality.lint）
□ pack.json 验证：所有 pack name/description 非模板字面量
□ git status 确认：只包含预期文件，无遗漏
□ LESSONS.md 检查：本次踩坑是否需记入教训？
```

**核心原则**：`docs-alignment.json` 是提交门禁。任何文档变更必须同步更新其中的版本字段。如果提交前发现版本不同步，必须先对齐再提交。

## Skill 格式规范

项目对齐 [Agent Skills 开放标准](https://agentskills.io/specification)（Anthropic 2025-12 发布，33+ 平台采纳）。每个 skill 是一个目录，必须包含 `SKILL.md`。

```
skill-name/
├── SKILL.md                    # 必需：YAML frontmatter + Markdown body
├── agents/                     # 可选：Agent 适配版本
│   ├── claude-code/SKILL.md    # Claude Code 版
│   └── ...
├── references/                 # 可选：按需加载的参考文档
├── scripts/                    # 可选：可执行脚本
├── temp/                       # 可选：过程文件
└── assets/                     # 可选：模板、资源文件
```

**Agent 适配规则**：
- 通用 `SKILL.md` 是默认版本，必须存在
- `agents/<agent-name>/SKILL.md` 是特定 agent 适配版本，可选
- 安装时优先使用匹配的 agent 版本，无匹配则降级到通用版本
- 共享资源（references/scripts/assets）对所有 agent 版本通用

### Frontmatter（开放标准）

```yaml
---
name: skill-name              # 必需，kebab-case，1-64 字符
description: >                # 必需，触发条件，1-1024 字符
  This skill should be used when the user asks to "xxx", "yyy".
version: 0.1.0                # 可选，semver
license: MIT                  # 可选
compatibility: Python 3.11+   # 可选，环境要求
allowed-tools: [Read, Bash]   # 可选，实验性
metadata:                     # 可选，自定义扩展
  pack: development           # 项目扩展：技能包
  design-pattern: generator   # 项目扩展：设计模式
  skill-type: technical       # 项目扩展：技能类型
  author: Kei                 # 任意自定义字段
---
```

### Description 写法（按 profile）

| Profile | 要求 |
|---------|------|
| `skill-library`（默认） | 第三人称 + 引号触发短语："This skill should be used when..." |
| `generic` | 可理解、非空即可 |
| `claude-code` | 允许使用 `triggers` 字段替代 description 内嵌触发短语 |

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
├── LESSONS.md                  # 项目教训记录
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
- 分类：项目自有 skill 声明 pack + type + design-pattern + skill-type（可选 metadata）
- Agent 适配：通用 SKILL.md 必须存在，agent 版本可选，降级到通用版本
- 状态机驱动：所有管理操作必须读状态 → 前置检查 → 执行 → 写状态
- 元 skill 自管理：管理功能本身也是标准 skill，通过文件操作和 Bash 调用 Python 模块实现
- **Profile 选择**：项目自有 skill 用 `skill-library`；第三方/社区 skill 用相应 profile
- 格式对齐 [agentskills.io](https://agentskills.io/specification) 开放标准
