# CI/CD 与版本管理调研

> 版本：1.0.0 | 更新：2026-05-23 | 来源：GitHub Docs + 社区实践

## 一、GitHub Actions Python CI 模式

### 1.1 标准模板

来源：GitHub Docs "Building and testing Python"（🥇）

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -q
```

### 1.2 关键点

- `actions/checkout@v4` 使用 `fetch-depth: 0` 获取完整历史（Release 需要）
- `actions/setup-python@v5` 支持工具缓存 + 版本矩阵
- 两步安装：先 pip 依赖，再运行测试
- Lint 可分离为独立 job 或 step

## 二、bump-my-version 配置

来源：pypi.org/project/bump-my-version（🥇）

`.bumpversion.toml` 是配置文件格式。关键配置项：

```toml
[tool.bumpversion]
current_version = "0.1.0"
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = ["{major}.{minor}.{patch}"]

[[tool.bumpversion.files]]
filename = "pyproject.toml"

[[tool.bumpversion.files]]
filename = "src/skill_library/__init__.py"

[[tool.bumpversion.files]]
filename = "docs-alignment.json"
```

### 2.1 正则匹配

`parse` 正则捕获版本组件，`serialize` 输出格式。支持预发布版本（a/b/rc）。

### 2.2 文件模式

每个 `[[tool.bumpversion.files]]` 声明一个需同步版本的文件。自动搜索文件中的版本字符串并替换。支持 glob 模式匹配多个文件。

## 三、GitHub Release 工作流模式

来源：GitHub Docs "Publishing packages"（🥇）

### 3.1 Tag 触发 Release

```yaml
name: Release
on:
  push:
    tags:
      - "v*"
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install build
      - run: python -m build
      - uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
          files: dist/*
```

### 3.2 Changelog 自动生成

`softprops/action-gh-release@v2` 的 `generate_release_notes: true` 基于 commit 前缀（feat/fix/chore/docs）自动分类生成 Release Notes。

## 四、Monorepo Pack 版本管理

### 4.1 独立版本策略

将每个 pack 视为独立子包，各自维护 `pack.json` 版本。版本相互独立，互不依赖。

### 4.2 版本追踪方式

| 方式 | 优点 | 缺点 |
|------|------|------|
| Git tag per pack | 细粒度 | tag 数量膨胀 |
| pack.json 内嵌版本 | 简单、Agent 直接读取 | 需额外工具对比 |
| Changeset 文件 | 标准化 | 引入复杂工具链 |

**推荐**：pack.json 内嵌版本 + GitHub Release 整体发布。

### 4.3 pack.json Schema

```json
{
  "name": "pack-name",
  "version": "semver",
  "description": "简短描述",
  "skills": ["skill-list"],
  "dependencies": ["other-packs"],
  "updated": "ISO-8601"
}
```

必填字段：name, version, description
可选字段：skills, dependencies, updated

## 五、参考来源

| 来源 | 链接 | 可信度 |
|------|------|--------|
| GitHub Actions Python CI | docs.github.com/actions/guides/building-and-testing-python | 🥇 |
| bump-my-version 文档 | pypi.org/project/bump-my-version | 🥇 |
| softprops/action-gh-release | github.com/softprops/action-gh-release | 🥇 |
| Monorepo 策略分析 | cloud.tencent.com/developer/article/2636330 | 🥈 |
