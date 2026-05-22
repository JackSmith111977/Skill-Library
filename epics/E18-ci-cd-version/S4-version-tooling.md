# Story E18-S4: 版本管理工具配置

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E18-S4 |
| Epic | E18 CI/CD + 版本管理 + 升级渠道 |
| 状态 | `done` |

## 需求

配置 bump-my-version，使版本号在 pyproject.toml、__init__.py、docs-alignment.json 中同步更新。

## 验收标准

1. `.bumpversion.toml` 配置完成，包含三个文件
2. `bump-my-version bump minor` 可以正常执行
3. 执行后三个文件的版本号一致更新
4. 生成对应的 git commit + tag

## 改动

| 文件 | 改动 |
|------|------|
| `.bumpversion.toml` | 新建 |
| `src/skill_library/__init__.py` | 确保版本号与 pyproject.toml 一致 |
| `pyproject.toml` | 添加 bump-my-version 到 dev 依赖 |
