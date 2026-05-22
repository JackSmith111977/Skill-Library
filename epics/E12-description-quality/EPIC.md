# Epic 12: Description 质量评估

> **主题**：实现 description 触发率评估，提升 skill 被正确激活的概率。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E12 |
| 优先级 | P2 |
| Story 数 | 4 |
| 依赖 | E2 |
| 状态 | `pending` |

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E12-S1 | 触发词提取器 | `pending` | E2-S2 |
| E12-S2 | 覆盖率评估 | `pending` | E12-S1 |
| E12-S3 | 第三人称检测 | `pending` | E2-S2 |
| E12-S4 | Description 优化建议 | `pending` | E12-S2 |

## 测试门禁

```bash
# 验收条件
- [ ] 触发词提取正确
- [ ] 覆盖率评估合理
- [ ] 第三人称检测准确
- [ ] 优化建议可操作
```
