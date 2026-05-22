# Skill 分类体系与质量检测标准调研

> 版本：1.1.0 | 更新：2026-05-22 | 来源交叉验证：3+ 独立来源

## 一、Skill 分类体系

### 1.1 Google ADK 五种设计模式

来源：Google Cloud Tech 官方（🥇）

| 模式 | 核心逻辑 | 典型场景 | 对应类型 |
|------|----------|----------|----------|
| **Tool Wrapper** | 封装领域知识，Agent 按需加载 | 框架规范、编码风格指南 | 原子 |
| **Generator** | 模板+风格指南生成标准化输出 | 文档生成、脚手架 | 原子 |
| **Reviewer** | 检查清单+自动化审查 | PR 审查、安全扫描 | 原子 |
| **Inversion** | Agent 先采访用户再执行 | 需求不明确时的需求澄清 | 工作流 |
| **Pipeline** | 带检查点的多步工作流 | 多阶段内容生产、代码生成 | 工作流 |

选择指南：
- 需要特定技术栈的专家知识 → Tool Wrapper
- 需要一致的结构化输出 → Generator
- 需要自动化审查 → Reviewer
- 需求不明确 → Inversion
- 复杂多步任务 → Pipeline
- 不确定？从 Tool Wrapper 开始

### 1.2 Writing-Skills 四种 Skill 类型

来源：Superpowers 框架（🥈）

| 类型 | 定义 | 测试方法 | 成功标准 |
|------|------|----------|----------|
| **纪律执行型** | 强制遵守规则（如 TDD） | 压力场景+合理化借口反驳 | 最大压力下仍遵守规则 |
| **技术指导型** | 具体方法的操作指南 | 应用场景+边界情况 | 成功应用到新场景 |
| **思维模式型** | 解决问题的心智模型 | 识别场景+判断何时适用 | 正确判断何时/如何应用 |
| **参考资料型** | API 文档、命令参考 | 检索场景+信息完整性 | 找到并正确应用参考信息 |

### 1.3 二维分类矩阵

将 Google 5 模式（横轴：设计模式）× Writing-Skills 4 类型（纵轴：Skill 类型）组合：

| | Tool Wrapper | Generator | Reviewer | Inversion | Pipeline |
|---|---|---|---|---|---|
| **纪律执行型** | 编码规范强制 | - | 规则合规检查 | - | 审批流程 |
| **技术指导型** | 框架最佳实践 | 脚手架生成 | 代码审查 | 需求收集 | 多步骤构建 |
| **思维模式型** | 设计模式 | - | 架构评审 | 问题探索 | 系统设计 |
| **参考资料型** | API 参考 | 模板填充 | 文档检查 | - | 文档流水线 |

### 1.4 技能包分类建议

基于二维矩阵，建议技能包按能力域划分：

| 技能包 | 包含模式 | 典型 Skill |
|--------|----------|-----------|
| **meta** | Inversion + Pipeline | skill-creator, skill-manager |
| **retrieval** | Tool Wrapper + Pipeline | kb-search, research-workflow |
| **web** | Tool Wrapper + Pipeline | web-search, news-digest-workflow |
| **document** | Generator + Pipeline | docx-read, doc-export-workflow |
| **development** | Reviewer + Pipeline | code-lint, tdd-workflow |
| **devops** | Tool Wrapper + Pipeline | ssh-exec, release-workflow |
| **communication** | Generator + Inversion | lark-send, meeting-summary-workflow |
| **learning** | Inversion + Pipeline | flashcard, learning-workflow |
| **security** | Reviewer + Tool Wrapper | security-scan, vuln-check |
| **data** | Generator + Pipeline | csv-analyze, etl-workflow |

## 二、质量检测规则

### 2.1 原子 Skill 检测项（7 项）

| # | 检查项 | 规则 | 来源 | 严重级别 |
|---|--------|------|------|----------|
| 1 | name 格式 | 1-64 字符，仅小写字母+连字符，不以连字符开头/结尾，无连续连字符，必须与目录名一致 | 🥇 Anthropic 规范 | ERROR |
| 2 | description 长度 | 1-1024 字符，不能为空 | 🥇 Anthropic 规范 | ERROR |
| 3 | description 触发词 | 必须含具体触发短语（引号内），第三人称 | 🥈 最佳实践 | WARNING |
| 4 | body 长度 | ≤500 行，建议 <5000 tokens | 🥈 最佳实践 | WARNING |
| 5 | 文件引用有效性 | SKILL.md 中引用的 references/scripts/assets 文件必须存在 | 🥉 逻辑校验 | ERROR |
| 6 | allowed-tools 格式 | 空格分隔的工具名列表 | 🥇 Anthropic 规范 | ERROR |
| 7 | metadata 格式 | 键值对映射，version 为语义化版本 | 🥇 Anthropic 规范 | WARNING |

### 2.2 工作流 Skill 额外检测项（4 项）

| # | 检查项 | 规则 | 严重级别 |
|---|--------|------|----------|
| 1 | 引用原子 skill 存在性 | 工作流中引用的原子 skill 必须在同一技能包内存在 | ERROR |
| 2 | 编排步骤完整性 | Pipeline 模式的步骤不能有缺失，序号连续 | ERROR |
| 3 | 硬性门控标记 | Inversion 模式的确认点必须明确标记（如 STAGE_GATE、HALT） | WARNING |
| 4 | 步骤依赖关系 | 不能出现循环依赖 | ERROR |

### 2.3 Description 质量评估

| 维度 | 好的示例 | 差的示例 |
|------|----------|----------|
| 触发短语 | `Use when the user asks to "review my code", "check this PR"` | `Helps with code review` |
| 覆盖范围 | 覆盖用户可能的各种表述 | 只描述功能，不描述触发条件 |
| 语气 | 祈使语气，适当"强势" | 模糊、被动 |

关键发现（来源：Writing-Skills）：
> **Description 只应描述触发条件，绝不要总结 Skill 的工作流程。** 当 description 总结了工作流程时，Agent 可能直接按 description 执行，而跳过阅读完整的 Skill 内容。

### 2.4 Skill 膨胀风险

来源：Medium 社区（🥉）

> "A 5KB skill balloons to 50KB. Response times slow to a crawl. Maintenance becomes a nightmare."

应对策略：
- body 严格控制在 500 行以内
- 详细内容拆分到 references/
- 迭代改进时审查是否引入冗余
- 定期 lint 检查 body 大小

## 三、渐进式加载架构

### 3.1 三级加载机制

来源：腾讯云技术文章 + Anthropic 规范（🥇）

| 层级 | 加载内容 | 加载时机 | Token 成本 |
|------|----------|----------|-----------|
| L1 目录层 | name + description | 会话启动时 | ~50-100 tokens/skill |
| L2 指令层 | 完整 SKILL.md body | Skill 被激活时 | <5000 tokens |
| L3 资源层 | references/scripts/assets | 指令引用时按需 | 视文件大小 |

关键价值：即使安装 20 个 Skill，初始加载也仅 1000-2000 tokens。相比单体式提示词，上下文使用量减少约 90%。

### 3.2 三级生命周期模式

| 模式 | 有效期 | 适用场景 | 实现 |
|------|--------|----------|------|
| **once** | 注入一次后立即清除 | 一次性查询 | State 写入后立即标记过期 |
| **turn**（默认） | 当前调用内有效 | 多轮工具调用 | 下次调用前清除 |
| **session** | 跨调用持续有效 | 长期任务 | Session 结束时清除 |

### 3.3 两种注入策略

| 策略 | 优点 | 缺点 |
|------|------|------|
| System Message 注入 | 实现简单，调试友好 | 每次加载新 Skill 失效 Prompt Caching |
| Tool Result 注入 | 保持 System Message 稳定，利于缓存 | 实现复杂，需回退机制 |

建议：默认 System Message 注入，可选 Tool Result 注入。

### 3.4 最大加载数与淘汰策略

- 配置最大同时加载 Skill 数（如 3 个）
- 超限时按 LRU（最近使用优先）淘汰
- 前缀扫描高效查询某 Agent 的所有已加载 Skill

## 四、状态管理设计

### 4.1 State Key 设计

来源：腾讯云架构文章（🥇）

两类核心 Key：

| Key | 说明 | 值 |
|-----|------|-----|
| `skill:loaded:{agent}/{skill}` | 标记某 Skill 已被某 Agent 加载 | "1" |
| `skill:docs:{agent}/{skill}` | 记录 Agent 对某 Skill 选择的文档 | "*" 或 JSON 数组 |

多 Agent 隔离：Key 中嵌入 Agent 名称，前缀扫描高效查询。

### 4.2 StateDelta 机制

Tool 执行函数（Call）和 State 写入（StateDelta）分离：
- **可测试性**：StateDelta 是纯函数，易于单元测试
- **事务性**：框架统一提交，可原子操作
- **可审计性**：结构化数据，可记录到事件日志

### 4.3 对我们的 state.json 设计启示

```json
{
  "library": { "path": "...", "created-at": "...", "last-sync": "..." },
  "agents": {
    "<agent-id>": {
      "path": "...",
      "skill-packs": [...],
      "skills": {
        "<skill-name>": {
          "status": "mounted",
          "version": "...",
          "load-mode": "session",
          "loaded-at": "...",
          "last-used": "..."
        }
      }
    }
  },
  "skills": {
    "<skill-name>": {
      "pack": "...",
      "type": "atomic|workflow",
      "design-pattern": "tool-wrapper|generator|reviewer|inversion|pipeline",
      "skill-type": "discipline|technical|mindset|reference",
      "version": "...",
      "quality-status": "passed|failed|unchecked",
      "mounted-to": [...]
    }
  }
}
```

新增字段：
- `design-pattern`：Google 5 种设计模式
- `skill-type`：Writing-Skills 4 种类型
- `load-mode`：once/turn/session

## 五、实现路径与优先级

| 阶段 | 任务 | 优先级 | 依赖 |
|------|------|--------|------|
| P0 | state.json 结构设计（含二维分类字段） | HIGH | - |
| P0 | 原子 skill 7 项 lint 规则实现 | HIGH | - |
| P1 | 工作流 skill 4 项 lint 规则实现 | HIGH | P0 原子 lint |
| P1 | 渐进式加载机制（三级） | MEDIUM | P0 state.json |
| P2 | 多 Agent 隔离 + LRU 淘汰 | MEDIUM | P1 加载机制 |
| P2 | Description 质量评估（触发率测试） | LOW | P0 lint |
| P3 | Skill 膨胀检测 | LOW | P0 lint |

## 六、参考来源

| 来源 | 链接 | 可信度 |
|------|------|--------|
| Anthropic Skill 规范 | agentskills.io/specification | 🥇 |
| Agent Skill 规范、构建与设计模式 | uml.org.cn/ai/202605181.asp | 🥇🥈 |
| Agent Skill 按需加载架构 | cloud.tencent.com/developer/article/2651831 | 🥇 |
| agent-skills-lint | CSDN (多篇) | 🥈 |
| Agent Harness 系统分类 | zhuanlan.zhihu.com | 🥇 |
| Google ADK Skill 设计模式 | 百家号/Google Cloud Tech | 🥇 |
| Superpowers 框架 | GitHub obra/superpowers | 🥈 |
| Hermes Agent Skills 闭环 | cloud.tencent.com/developer/article/2654253 | 🥈 |
