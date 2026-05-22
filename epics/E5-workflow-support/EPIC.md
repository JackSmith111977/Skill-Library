# Epic 5: 工作流 Skill 支持

> **主题**：扩展质量检测支持工作流 skill，实现额外 4 项规则。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E5 |
| 优先级 | P1 |
| Story 数 | 5 |
| 依赖 | E2, E3 |
| 状态 | `pending` |

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E5-S1 | 引用原子 skill 存在性校验 | `pending` | E3-S1 |
| E5-S2 | 编排步骤完整性校验 | `pending` | - |
| E5-S3 | 硬性门控标记校验 | `pending` | - |
| E5-S4 | 步骤依赖关系校验 | `pending` | - |
| E5-S5 | 工作流 lint 入口 | `pending` | E5-S1~S4, E2-S7 |

## 测试门禁

```bash
# 单元测试
pytest tests/test_quality/test_workflow_rules.py -v

# 验收条件
- [ ] 4 项规则全部实现且有对应测试
- [ ] 引用存在的原子 skill → 通过
- [ ] 引用不存在的原子 skill → ERROR
- [ ] Pipeline 序号不连续 → ERROR
- [ ] 循环依赖 → ERROR
- [ ] Inversion 无门控标记 → WARNING
```
