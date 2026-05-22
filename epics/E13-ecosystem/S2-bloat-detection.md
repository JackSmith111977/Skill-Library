# Story E13-S2: Skill 膨胀检测

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E13-S2 |
| Epic | E13 生态完善 |
| 状态 | `done` |
| 依赖 | E2-S3 |

## 需求

检测 skill 是否违反最佳实践（body 超长、reference 过多等）。

## 验收标准

1. Body > 500 行检测
2. Body > 5000 词检测
3. Reference 文件 > 10 个检测
4. 检测结果合并到 lint 报告
