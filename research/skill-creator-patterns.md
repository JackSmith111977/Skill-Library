# Skill Creator 元技能模式调研

> 版本：1.0.0 | 更新：2026-05-22

## 调研背景

为 Skill Library 项目设计 `skill-creator` 和 `workflow-creator` 两个元技能，调研 Anthropic 官方及其他社区的 skill creator 实现模式。

## 来源

| 来源 | 链接 | 可信度 |
|------|------|--------|
| Anthropic 官方 skill-creator | github.com/anthropics/claude-code/tree/main/skills/skill-creator | 🥇 |
| Anthropic 官方博客 | docs.anthropic.com/en/docs/agents-and-tools/agent-skills | 🥇 |
| claude-skills-guide (社区) | github.com/sanshao85/claude-skills-guide | 🥈 |
| 官方 template-skill | github.com/anthropics/claude-code/tree/main/skills/template-skill | 🥇 |

## 核心发现

### 1. Anthropic 官方 skill-creator 流程

Anthropic 官方 skill-creator 是一个完整的"元技能"(485 行 SKILL.md)，遵循工程化研发流程：

```
捕获意图 → 面试调研 → 撰写 SKILL.md → 创建测试用例
    → 运行(with/without skill) → 评估与评分
    → 人工审核 → 反馈 → 改进技能 → [迭代]
    → 描述优化 → 打包发布
```

关键设计理念：
- **草稿→测试→评估→改进** 循环（类似 TDD）
- 两类 Skill 区分：能力提升型(Capability Uplift) vs 偏好编码型(Encoded Preference)
- 测试用例驱动：创建 with-skill / without-skill 对比测试
- 基准报告：自动生成评估报告

### 2. 官方 template-skill

最简单的 skill 模板，仅包含最小 frontmatter：

```yaml
---
name: my-skill
description: 描述这个 Skill 做什么以及何时使用
---
```

### 3. 社区实践

社区 skill-creator 更轻量，聚焦于：
- 目录结构生成（SKILL.md + scripts/ + references/ + assets/）
- Frontmatter 字段填写指南
- Description 触发词优化
- Body 编写规范

## 对 Skill Library 项目的启示

### skill-creator 定位

**不要照搬 Anthropic 官方 skill-creator 的全套测试-评估-迭代流程**。原因：

| 维度 | Anthropic 官方 | Skill Library 版 |
|------|---------------|-----------------|
| 目标 | 通用 skill 工程化 | 创建符合项目标准的 skill |
| 流程 | 草稿→测试→评估→改进 | 需求→脚手架→编写→验证 |
| 测试 | with/without 对比测试 | skill-manager lint 自验证 |
| 复杂度 | 高（485 行） | 中（~300 行） |
| 迭代 | 多轮评估循环 | 一次创建 + lint 验证 |

### workflow-creator 定位

Anthropic 官方没有单独的 workflow-creator。Workflow skill 本质上是编排多个原子 skill 的"元 skill"。Skill Library 项目有独特需求：
- Pipeline 模式：线性多步，每一步引用同包原子 skill
- Inversion 模式：先采访用户收集需求，再执行
- 必须通过工作流 4 项额外 lint 规则

### 实现建议

1. **skill-creator** 聚焦：需求澄清 → 目录脚手架 → Frontmatter → Description → Body → References → Lint 验证
2. **workflow-creator** 聚焦：模式选择(pipeline/inversion) → 同包原子 skill 检查 → 步骤编排 → 门控标记 → Lint 验证
3. 两个 skill 都属于 `meta` pack，`generator` design pattern
4. References 存放详细规范，SKILL.md body 保持核心流程
