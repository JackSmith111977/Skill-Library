# Skill Library 产品需求文档（PRD）

> 版本：1.1.0 | 更新：2026-05-22

## 1. 项目概述

### 1.1 定位

Agent Skill Library — 跨项目的 skill 管理系统。管理系统本身以元 skill 形式实现（标准 skill 格式），管理其他 skill 的全生命周期：创建、分类、版本控制、安装/卸载、质量检测。

### 1.2 核心价值

- Agent 按用途挂载对应技能包，不加载无关 skill
- 原子 skill 单一职责，工作流 skill 编排复杂任务
- 状态机驱动，每次操作可追溯
- 自动化质量检测，保障 skill 可靠性

---

## 2. 核心概念

### 2.1 Skill 类型

每个 skill 是一个目录，必须包含 `SKILL.md`。分两类：

- **原子 skill** — 执行单一特定任务，职责内聚
- **工作流 skill** — 编排多个原子 skill，处理长流程复杂任务

```
skill-name/
├── SKILL.md              # 必需：主文档（YAML frontmatter + Markdown body）
├── references/           # 可选：参考文档，按需加载到上下文
├── scripts/              # 可选：可执行脚本（Python/Shell/Node）
├── temp/                 # 可选：过程文件，不纳入版本管理
└── assets/               # 可选：模板、图片等输出资源
```

### 2.2 技能包

Skill 按能力域归入技能包。每个包内含原子 skill + 工作流 skill：

```
<pack-name>/
├── <atomic-skill>/       # 原子 skill
└── <workflow-skill>/     # 工作流 skill：编排同包内的原子 skill
```

Agent 声明所需技能包，管理系统按包挂载全部 skill（原子 + 工作流）。

### 2.3 Skill 二维分类

每个 skill 有两个分类维度（来源：Google ADK + Superpowers 框架）：

**设计模式**（Google 5 种）：

| 模式 | 说明 | 类型 |
|------|------|------|
| Tool Wrapper | 封装领域知识，按需加载 | 原子 |
| Generator | 模板+风格指南生成输出 | 原子 |
| Reviewer | 检查清单+自动化审查 | 原子 |
| Inversion | Agent 先采访用户再执行 | 工作流 |
| Pipeline | 带检查点的多步工作流 | 工作流 |

**Skill 类型**（Writing-Skills 4 种）：

| 类型 | 说明 |
|------|------|
| discipline | 纪律执行型：强制遵守规则 |
| technical | 技术指导型：具体方法操作指南 |
| mindset | 思维模式型：解决问题的心智模型 |
| reference | 参考资料型：API 文档、命令参考 |

### 2.4 Agent 适配

同一 skill 需要适配不同 agent 环境（Claude Code、Hermes、OpenClaw 等）。

**目录结构**：

```
skill-name/
├── SKILL.md                    # 通用版本（默认降级）
├── agents/                     # Agent 适配版本
│   ├── claude-code/SKILL.md    # Claude Code 版
│   ├── hermes/SKILL.md         # Hermes 版
│   └── openclaw/SKILL.md       # OpenClaw 版
├── references/                 # 共享资源（agent 无关）
├── scripts/                    # 共享脚本（agent 无关）
└── assets/                     # 共享资源
```

**适配规则**：
- 通用 `SKILL.md` 是默认版本，必须存在
- `agents/<agent-name>/SKILL.md` 是特定 agent 适配版本，可选
- 安装时优先使用匹配的 agent 版本，无匹配则降级到通用版本
- 共享资源（references/scripts/assets）对所有 agent 版本通用
- Agent 版本可覆盖通用版本的 frontmatter（name/description/allowed-tools 等）

**状态机字段**：

```json
{
  "skills": {
    "skill-name": {
      "agent-adapters": ["claude-code", "hermes"],
      "default-adapter": "generic"
    }
  }
}
```

**Agent 类型枚举**（待调研补充）：

| Agent | 格式规范 | 适配状态 |
|-------|----------|----------|
| generic | 通用 SKILL.md 规范 | 首要实现 |
| claude-code | Claude Code skill 规范 | 待调研 |
| hermes | Hermes Agent 格式 | 待调研 |
| openclaw | OpenClaw 格式 | 待调研 |

---

## 3. 状态机

状态机是 single source of truth。**每次管理操作必须：① 读取当前状态 → ② 执行操作 → ③ 写回新状态。**

### 3.1 三段式状态结构

```json
{
  "library": {
    "path": "D:\\WorkPlace\\VibeCoding\\Skill Library",
    "created-at": "2026-05-22",
    "last-sync": "2026-05-22T10:00:00Z"
  },
  "agents": {
    "<agent-id>": {
      "path": "C:\\Users\\...\\.claude\\skills",
      "agent-type": "claude-code",
      "skill-packs": ["development", "retrieval"],
      "skills": {
        "<skill-name>": {
          "status": "mounted",
          "version": "1.0.0",
          "adapter": "claude-code",
          "load-mode": "session",
          "loaded-at": "2026-05-22",
          "last-used": "2026-05-22"
        }
      }
    }
  },
  "skills": {
    "skill-name": {
      "pack": "development",
      "type": "atomic",
      "design-pattern": "tool-wrapper",
      "skill-type": "technical",
      "version": "1.0.0",
      "quality-status": "passed",
      "agent-adapters": ["claude-code"],
      "default-adapter": "generic",
      "mounted-to": ["agent-id-1", "agent-id-2"]
    }
  }
}
```

### 3.2 状态值

| 维度 | 取值 | 说明 |
|------|------|------|
| 挂载状态 | `mounted` / `unmounted` / `error` / `outdated` | skill 在 agent 上的状态 |
| 质量状态 | `passed` / `failed` / `unchecked` | lint 检测结果 |
| 类型 | `atomic` / `workflow` | skill 类型 |
| 设计模式 | `tool-wrapper` / `generator` / `reviewer` / `inversion` / `pipeline` | Google 5 种模式 |
| skill 类型 | `discipline` / `technical` / `mindset` / `reference` | Writing-Skills 4 种类型 |
| 加载模式 | `once` / `turn` / `session` | 生命周期（once=一次、turn=单轮、session=会话） |

---

## 4. 配置文件

### 4.1 config.json

```json
{
  "library-path": "D:\\WorkPlace\\VibeCoding\\Skill Library",
  "agents": {
    "<agent-id>": {
      "path": "C:\\Users\\...\\.claude\\skills",
      "description": "主开发环境"
    }
  }
}
```

### 4.2 state.json

见第 3 章。state.json 包含 library 元数据、agents 挂载详情、skills 注册信息。不再单独维护 registry.json——所有注册信息统一在 state.json 的 `skills` 段。

---

## 5. 管理元技能（skill-manager）

管理功能本身是标准格式的元 skill，所有操作以状态机驱动。

### 5.1 初始化（init）

```
skill-manager init
├── 询问技能库绝对路径 → 写入 config.json
├── 扫描并确认各 Agent 的 skill 挂载地址 → 写入 config.json
├── 扫描 skills/ 目录 → 建立 state.json 的 skills 索引
└── 输出初始化摘要
```

### 5.2 管理操作

每个操作遵循：**读状态 → 前置检查 → 执行 → 写状态**

| 操作 | 前置检查 | 状态变更 |
|------|----------|----------|
| `init` | 无 | 初始化 config.json + state.json |
| `mount` | skill 存在且 quality=passed，agent 存在 | agents.skills 写入 mounted，skills.mounted-to 更新 |
| `unmount` | skill 已 mounted | agents.skills 写入 unmounted，skills.mounted-to 清除 |
| `status` | 无（只读） | 无 |
| `classify` | skill 存在且未分类 | skills 写入 pack + type + design-pattern + skill-type |
| `lint` | skill 存在 | skills 写入 quality-status |
| `lint-workflow` | workflow skill 存在 | skills 写入 quality-status（含引用原子 skill 存在性校验） |

**异常处理**：操作失败时写入 `error` 状态 + 错误原因，不中断后续操作。

---

## 6. 质量检测规则

### 6.1 原子 skill 7 项

| # | 检查项 | 规则 | 级别 |
|---|--------|------|------|
| 1 | name 格式 | 1-64 字符，小写字母+连字符，不以连字符开头/结尾，无连续连字符，与目录名一致 | ERROR |
| 2 | description 长度 | 1-1024 字符，不能为空 | ERROR |
| 3 | description 触发词 | 必须含具体触发短语（引号内），第三人称 | WARNING |
| 4 | body 长度 | ≤500 行，建议 <5000 tokens | WARNING |
| 5 | 文件引用有效性 | SKILL.md 中引用的 references/scripts/assets 文件必须存在 | ERROR |
| 6 | allowed-tools 格式 | 空格分隔的工具名列表 | ERROR |
| 7 | metadata 格式 | 键值对映射，version 为语义化版本 | WARNING |

### 6.2 工作流 skill 额外 4 项

| # | 检查项 | 规则 | 级别 |
|---|--------|------|------|
| 1 | 引用原子 skill 存在性 | 工作流中引用的原子 skill 必须在同一技能包内存在 | ERROR |
| 2 | 编排步骤完整性 | Pipeline 模式的步骤不能有缺失，序号连续 | ERROR |
| 3 | 硬性门控标记 | Inversion 模式的确认点必须明确标记 | WARNING |
| 4 | 步骤依赖关系 | 不能出现循环依赖 | ERROR |

### 6.3 Description 质量要点

- **只描述触发条件，不要总结工作流程**（否则 Agent 可能跳过 Skill 正文直接执行）
- 第三人称："This skill should be used when..."
- 含具体触发短语（引号内），宁可偏激进——Claude 倾向于不触发 skill

### 6.4 Skill 膨胀防护

- body 严格控制在 500 行以内
- 详细内容拆分到 references/
- 迭代改进时审查是否引入冗余
- 定期 lint 检查 body 大小

---

## 7. 渐进式加载机制

### 7.1 三级加载

| 层级 | 加载内容 | 加载时机 | Token 成本 |
|------|----------|----------|-----------|
| L1 目录层 | name + description | 会话启动时 | ~50-100 tokens/skill |
| L2 指令层 | 完整 SKILL.md body | Skill 被激活时 | <5000 tokens |
| L3 资源层 | references/scripts/assets | 指令引用时按需 | 视文件大小 |

关键价值：即使安装 20 个 Skill，初始加载也仅 1000-2000 tokens。相比单体式提示词，上下文使用量减少约 90%。

### 7.2 三级生命周期

| 模式 | 有效期 | 适用场景 |
|------|--------|----------|
| `once` | 注入一次后立即清除 | 一次性查询 |
| `turn`（默认） | 当前调用内有效 | 多轮工具调用 |
| `session` | 跨调用持续有效 | 长期任务 |

### 7.3 淘汰策略

- 配置最大同时加载 Skill 数（如 3 个）
- 超限时按 LRU（最近使用优先）淘汰
- 前缀扫描高效查询某 Agent 的所有已加载 Skill

---

## 8. 已知技能包

| 技能包 | 说明 | 示例原子 skill | 示例工作流 skill |
|--------|------|---------------|-----------------|
| meta | 管理其他 skill | skill-creator | skill-manager-workflow |
| retrieval | 知识库、文件搜索 | kb-search, file-grep | research-workflow |
| web | 联网搜索、抓取 | web-search, fetch-page | news-digest-workflow |
| document | 文档读写、转换 | docx-read, md-convert | doc-export-workflow |
| development | 编码、调试、测试 | code-lint, test-run | tdd-workflow |
| devops | 部署、CI/CD | ssh-exec, deploy-cmd | release-workflow |
| communication | 消息、邮件 | lark-send, mail-compose | meeting-summary-workflow |
| learning | 教学、知识沉淀 | flashcard, quiz-gen | learning-workflow |
| security | 安全扫描、漏洞检测 | vuln-scan, secret-check | security-audit-workflow |
| data | 数据处理、ETL | csv-analyze, json-transform | etl-workflow |

---

## 9. 实现优先级

| 阶段 | 任务 | 优先级 |
|------|------|--------|
| P0 | state.json 结构设计（含二维分类字段） | HIGH |
| P0 | 原子 skill 7 项 lint 规则实现 | HIGH |
| P1 | 工作流 skill 4 项 lint 规则实现 | HIGH |
| P1 | 渐进式加载机制（三级） | MEDIUM |
| P2 | 多 Agent 隔离 + LRU 淘汰 | MEDIUM |
| P2 | Description 质量评估（触发率测试） | LOW |
| P3 | Skill 膨胀检测 | LOW |

---

## 10. 参考来源

| 来源 | 链接 | 可信度 |
|------|------|--------|
| Anthropic Skill 规范 | agentskills.io/specification | 🥇 |
| Agent Skill 规范、构建与设计模式 | uml.org.cn/ai/202605181.asp | 🥇🥈 |
| Agent Skill 按需加载架构 | cloud.tencent.com/developer/article/2651831 | 🥇 |
| Agent Harness 系统分类 | zhuanlan.zhihu.com | 🥇 |
| Google ADK Skill 设计模式 | Google Cloud Tech | 🥇 |
| Superpowers 框架 | GitHub obra/superpowers | 🥈 |

详细调研见 `research/skill-classification-and-quality.md`。
