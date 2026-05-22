# Story E11-S1: 最大加载数配置

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E11-S1 |
| Epic | E11 LRU 淘汰策略 |
| 状态 | `done` |
| 依赖 | - |

## 需求

在 config.json 中添加 max-loaded-skills 配置项。

## 验收标准

1. config.json schema 支持 max-loaded-skills
2. 默认值 10
3. ConfigManager 能读取和校验该字段
