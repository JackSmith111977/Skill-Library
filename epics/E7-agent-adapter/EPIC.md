# Epic 7: Agent 适配框架

> **主题**：实现通用适配器接口和 Claude Code 适配器，支持多 agent 环境。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E7 |
| 优先级 | P1 |
| Story 数 | 7 |
| 依赖 | 无 |
| 状态 | `pending` |

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E7-S1 | AgentAdapter 抽象基类 | `pending` | - |
| E7-S2 | 通用 SKILL.md 适配器 | `pending` | E7-S1 |
| E7-S3 | Claude Code 扩展字段处理 | `pending` | E7-S1 |
| E7-S4 | Claude Code 动态注入处理 | `pending` | E7-S3 |
| E7-S5 | Claude Code 参数占位符处理 | `pending` | E7-S3 |
| E7-S6 | Agent 版本降级逻辑 | `pending` | E7-S1 |
| E7-S7 | 适配器注册表 | `pending` | E7-S1 |

## 测试门禁

```bash
# 单元测试
pytest tests/test_adapters/test_base.py -v
pytest tests/test_adapters/test_claude_code.py -v

# 验收条件
- [ ] 抽象基类接口定义完整
- [ ] Claude Code 扩展字段处理正确
- [ ] 动态注入语法解析正确
- [ ] 参数占位符替换正确
- [ ] 降级逻辑正确
- [ ] 适配器查找正确
```
