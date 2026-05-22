# Story E18-S7: 升级脚本

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E18-S7 |
| Epic | E18 CI/CD + 版本管理 + 升级渠道 |
| 状态 | `done` |

## 需求

为人类开发者提供快捷升级脚本，一键检查并升级到最新版本。

## 验收标准

1. `scripts/upgrade.sh` — Linux/macOS 可用
2. `scripts/upgrade.ps1` — Windows PowerShell 可用
3. 脚本功能：检查当前版本 → 查询最新 Release → 有更新则执行升级
4. 脚本可单独运行，不依赖其他项目组件

## 改动

| 文件 | 改动 |
|------|------|
| `scripts/upgrade.sh` | 新建 |
| `scripts/upgrade.ps1` | 新建 |
