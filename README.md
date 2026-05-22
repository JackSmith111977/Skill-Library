# Skill Library

跨项目的 Agent Skill 管理系统。管理 AI Agent 技能包的全生命周期：创建、分类、质量检测、安装/卸载、渐进式加载。

## 快速开始

```bash
# 安装
pip install -r requirements.txt
pip install -e .

# 创建 skill
skill-manager create my-skill --pack development --type atomic

# 质量检测
skill-manager lint my-skill

# 查看版本
skill-manager --version
```

## 核心概念

### Skill 格式

每个 skill 是一个目录，包含标准化的 `SKILL.md` 主文档：

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

两个分类维度：

**设计模式**（Google ADK 5 种）：Tool Wrapper | Generator | Reviewer | Inversion | Pipeline

**Skill 类型**（Writing-Skills 4 种）：discipline | technical | mindset | reference

### 三级加载机制

| 层级 | 加载内容 | 时机 | Token 成本 |
|------|----------|------|-----------|
| L1 元数据 | name + description | 会话启动 | ~50-100/skill |
| L2 指令 | 完整 SKILL.md body | skill 触发 | <5000 tokens |
| L3 资源 | references/scripts/assets | 按需引用 | 视文件大小 |

20 个 skill 时，初始加载仅 1000-2000 tokens，比单体提示词减少约 90%。

### 质量检测

- **原子 skill**: 7 项检测（name 格式、description 长度/触发词、body 长度、文件引用、allowed-tools、metadata）
- **工作流 skill**: 额外 4 项（引用存在性、步骤完整性、门控标记、循环依赖）
- **膨胀检测**: body > 500 行 / > 5000 词 / reference > 10 个
- **Description 质量**: 触发词覆盖率评分、第三人称检测、优化建议

## 架构

### 模块

| 模块 | 职责 |
|------|------|
| **CLI** | Click 命令行入口（create/lint/load/version） |
| **State Machine** | 状态机引擎，所有操作的 single source of truth |
| **Quality Engine** | 11 项 lint 规则 + description 质量评估 + 膨胀检测 |
| **Skill Registry** | skill 扫描、注册、索引、查询 |
| **Progressive Loader** | 三级加载 + LRU 淘汰 + 生命周期管理 |
| **Template Engine** | 原子/工作流 skill 模板，9 种设计模式 |
| **Agent Adapter** | 通用 ↔ 特定 agent 格式转换 |

### 数据流

```
用户/Agent → CLI → 读 state.json → 前置检查 → 执行操作 → 写 state.json
```

状态机驱动：每次管理操作必须经过"读状态 → 检查 → 执行 → 写回"。

## CLI 参考

```bash
skill-manager create <name>    # 创建新 skill
skill-manager lint <name>      # 质量检测
skill-manager load <name>      # 查看加载状态
skill-manager version          # 版本信息
skill-manager --version        # 版本号
```

所有命令支持 `--help` 查看详细参数。

## 项目状态

全部 **14 个 Epic**，**71 个 Story** 开发完成，**345 个测试** 通过。

| Epic | 主题 | Story 数 | 状态 |
|------|------|----------|------|
| E1 | 数据基础层 | 5 | ✅ |
| E2 | 质量检测引擎 | 8 | ✅ |
| E3 | Skill Registry | 6 | ✅ |
| E4 | 状态机引擎 | 8 | ✅ |
| E5 | 工作流 Skill 支持 | 5 | ✅ |
| E6 | Skill 模板系统 | 4 | ✅ |
| E7 | Agent 适配框架 | 7 | ✅ |
| E8 | 渐进式加载 | 6 | ✅ |
| E9 | Skill Manager 元 Skill | 4 | ✅ |
| E10 | 多 Agent 隔离 | 4 | ✅ |
| E11 | LRU 淘汰策略 | 4 | ✅ |
| E12 | Description 质量评估 | 4 | ✅ |
| E13 | 生态完善 | 4 | ✅ |
| E14 | Skill 创建元技能 | 2 | ✅ |

详细进度见 [PROGRESS.md](PROGRESS.md)。

## 文档索引

| 文档 | 用途 |
|------|------|
| [PRD.md](PRD.md) | 产品需求（What + Why） |
| [IMPLEMENTATION.md](IMPLEMENTATION.md) | 实现技术（How） |
| [CLAUDE.md](CLAUDE.md) | 开发规则（Rules） |
| [PROGRESS.md](PROGRESS.md) | 开发进度（Status） |
| [epics/](epics/) | Epic/Story 详情 |

## 开发

```bash
# 运行全部测试
python -m pytest

# 运行单个测试文件
python -m pytest tests/test_quality/test_lint.py -v

# 安装可编辑模式
pip install -e .
```

依赖：Python 3.11+, pyyaml, click, rich, jsonschema, gitpython
