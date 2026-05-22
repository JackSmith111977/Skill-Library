# Story E18-S6: GitHub Actions Release 配置

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E18-S6 |
| Epic | E18 CI/CD + 版本管理 + 升级渠道 |
| 状态 | `done` |
| 依赖 | E18-S5 |

## 需求

创建 GitHub Actions Release 工作流，当 `v*` tag 被推送时自动创建 GitHub Release。

## 验收标准

1. `.github/workflows/release.yml` 存在且语法正确
2. `v*` tag 推送时触发
3. 自动生成 Release Notes（基于 commit 历史）
4. 构建 wheel + sdist 并附加到 Release

## 改动

| 文件 | 改动 |
|------|------|
| `.github/workflows/release.yml` | 新建 |
