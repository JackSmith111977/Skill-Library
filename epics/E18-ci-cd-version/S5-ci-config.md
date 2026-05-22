# Story E18-S5: GitHub Actions CI 配置

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E18-S5 |
| Epic | E18 CI/CD + 版本管理 + 升级渠道 |
| 状态 | `done` |
| 依赖 | E18-S4 |

## 需求

创建 GitHub Actions CI 工作流，在 push/PR 时自动运行测试和 lint。

## 验收标准

1. `.github/workflows/ci.yml` 存在且语法正确
2. Push 和 PR 时触发
3. 运行 `pytest tests/ -q`（所有测试）
4. 运行 `python -m skill_library.quality.lint skills/*`
5. Python 3.11 + 3.12 版本矩阵

## 改动

| 文件 | 改动 |
|------|------|
| `.github/workflows/ci.yml` | 新建 |
