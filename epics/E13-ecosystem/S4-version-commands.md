# Story E13-S4: 版本管理命令

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E13-S4 |
| Epic | E13 生态完善 |
| 状态 | `done` |
| 依赖 | E1-S3 |

## 需求

实现版本查看和更新管理命令。

## 验收标准

1. `skill-manager --version` 显示版本号
2. 版本号从 pyproject.toml 读取
3. `skill-manager version` 子命令显示详细版本信息
