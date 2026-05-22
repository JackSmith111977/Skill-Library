# Story E11-S3: last-used 时间戳更新

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E11-S3 |
| Epic | E11 LRU 淘汰策略 |
| 状态 | `done` |
| 依赖 | E1-S3 |

## 需求

在 skill 被访问（load/get）时更新 last-used 时间戳。

## 验收标准

1. load/get 操作更新 last-used 为当前时间
2. last-used 写入 state.json
3. 刚加载的 skill 不会被立即淘汰
